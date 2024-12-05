import cocotb
from cocotb.triggers import Timer, RisingEdge, FallingEdge
from cocotb.clock import Clock
import random
from coverpoints import sample_cp, report_coverage

# Constants for message and key sizes
MSG_SIZE = 64  # Message size in bits
KEY_SIZE = 8   # Key size in bits

# Helper class for serialization
class Serializer:
    def __init__(self, dut):
        self.dut = dut

    async def send_serial_data(self, data, num_bits, flag_index):
        """
        Serially send data into ui_in[0] with ui_in[flag_index] indicating data valid.
        :param data: The data to send
        :param num_bits: Number of bits to send
        :param flag_index: Index of the flag signal in ui_in
        """
        for bit_index in reversed(range(num_bits)):
            bit = (data >> bit_index) & 0x1
            self.dut.ui_in[0].value = bit               # Send bit
            self.dut.ui_in[flag_index].value = 1        # Set flag to indicate valid data
            await RisingEdge(self.dut.clk)
            self.dut.ui_in[flag_index].value = 0        # Clear flag
            await RisingEdge(self.dut.clk)

# Helper class for checking DUT outputs
class Checker:
    @staticmethod
    def check_ciphertext(received, expected):
        assert received == expected, f"Ciphertext does not match expected value.\nReceived: {hex(received)}\nExpected: {hex(expected)}"

    @staticmethod
    def check_encryption_status(dut):
        encryption_status = int(dut.uo_out[2].value)
        assert encryption_status == 0, "Encryption status should be low after encryption is complete"

    @staticmethod
    def check_ciphertext_counter(dut, expected_counter):
        """
        Checks that oCiphertext_counter in the xor_message module reached the expected value.
        :param dut: The top-level DUT.
        :param expected_counter: The expected value of oCiphertext_counter.
        """
        # Access the internal signal oCiphertext_counter inside the xor_message instance
        oCiphertext_counter = int(dut.xor_message.oCiphertext_counter.value)
        assert oCiphertext_counter == expected_counter, (
            f"oCiphertext_counter did not reach expected value {expected_counter}, "
            f"got {oCiphertext_counter}"
        )

@cocotb.test()
async def test_xor_encrypt_design(dut):
    """Testbench for the XOR Encrypt Design."""

    # Initialize clock with a period of 10 ns
    cocotb.start_soon(Clock(dut.clk, 10, units="ns").start())

    # Reset the DUT (active low)
    dut.rst_n.value = 0
    dut.ena.value = 0
    dut.ui_in.value = 0
    await Timer(20, units="ns")  # Wait for 20 ns
    dut.rst_n.value = 1          # Release reset

    # Wait for a few clock cycles to ensure the reset is processed
    for _ in range(5):
        await RisingEdge(dut.clk)

    # Enable the DUT
    dut.ena.value = 1

    # Instantiate helper classes
    serializer = Serializer(dut)
    checker = Checker()

    # Initialize coverage trackers
    covered_keys = set()
    covered_messages = set()
    transitions = {'0_to_1': 0, '1_to_0': 0}
    ciphertext_counters = []
    ciphertext_lengths = []

    # Randomly generate a message and a key for testing
    message = random.getrandbits(MSG_SIZE)
    key = random.getrandbits(KEY_SIZE)

    # Track covered keys and messages
    covered_keys.add(key)
    covered_messages.add(message)

    dut._log.info(f"Testing with message: {hex(message)} and key: {hex(key)}")
    dut._log.info(f"Covered keys: {covered_keys}")
    dut._log.info(f"Covered messages: {covered_messages}")

    # Send the key first using ui_in[1] as the key flag
    await serializer.send_serial_data(key, KEY_SIZE, flag_index=1)

    # Wait for a few clock cycles before sending the message
    for _ in range(5):
        await RisingEdge(dut.clk)

    # Send the message using ui_in[2] as the message flag
    await serializer.send_serial_data(message, MSG_SIZE, flag_index=2)

    # Initialize previous encryption status
    previous_encryption_status = int(dut.uo_out[2].value)

    # Wait for the encryption to start by monitoring uo_out[2] (encryption_status)
    while int(dut.uo_out[2].value) == 0:
        await RisingEdge(dut.clk)
        current_encryption_status = int(dut.uo_out[2].value)
        if previous_encryption_status == 0 and current_encryption_status == 1:
            transitions['0_to_1'] += 1
            dut._log.info("Encryption status transitioned from 0 to 1 (Started)")
        elif previous_encryption_status == 1 and current_encryption_status == 0:
            transitions['1_to_0'] += 1
            dut._log.info("Encryption status transitioned from 1 to 0 (Stopped)")
        previous_encryption_status = current_encryption_status

    dut._log.info("Encryption started")
    dut._log.info(f"Encryption Status Transitions: {transitions}")

    # Wait for encryption to complete
    while int(dut.uo_out[2].value) == 1:
        await RisingEdge(dut.clk)
        current_encryption_status = int(dut.uo_out[2].value)
        if previous_encryption_status == 0 and current_encryption_status == 1:
            transitions['0_to_1'] += 1
            dut._log.info("Encryption status transitioned from 0 to 1 (Started)")
        elif previous_encryption_status == 1 and current_encryption_status == 0:
            transitions['1_to_0'] += 1
            dut._log.info("Encryption status transitioned from 1 to 0 (Stopped)")
        previous_encryption_status = current_encryption_status
        # Record oCiphertext_counter value
        oCiphertext_counter_value = int(dut.xor_message.oCiphertext_counter.value)
        ciphertext_counters.append(oCiphertext_counter_value)
        dut._log.info(f"oCiphertext_counter value: {oCiphertext_counter_value}")

    dut._log.info("Encryption completed")
    dut._log.info(f"Encryption Status Transitions: {transitions}")
    dut._log.info(f"All oCiphertext_counter values: {ciphertext_counters}")

    # Collect the ciphertext bits from uo_out[0] while uo_out[1] (oData_flag) is high
    ciphertext_bits = []

    # Wait for the serializer to set oData_flag
    while int(dut.uo_out[1].value) == 0:
        await RisingEdge(dut.clk)

    dut._log.info("Serialization started")

    # Collect bits while oData_flag is high
    while int(dut.uo_out[1].value) == 1:
        bit = int(dut.uo_out[0].value)
        ciphertext_bits.append(bit)
        await RisingEdge(dut.clk)

    ciphertext_lengths.append(len(ciphertext_bits))
    dut._log.info(f"Received {len(ciphertext_bits)} bits of ciphertext")
    dut._log.info(f"Ciphertext lengths recorded: {ciphertext_lengths}")

    # Reconstruct the ciphertext from the collected bits
    ciphertext = 0
    for bit in ciphertext_bits:
        ciphertext = (ciphertext << 1) | bit

    dut._log.info(f"Received ciphertext: {hex(ciphertext)}")

    # Calculate the expected ciphertext by XORing message chunks with the key
    expected_ciphertext = 0
    for i in range(0, MSG_SIZE, KEY_SIZE):
        # Extract a chunk of the message
        shift_amount = MSG_SIZE - KEY_SIZE - i
        chunk = (message >> shift_amount) & ((1 << KEY_SIZE) - 1)
        # XOR the chunk with the key
        encrypted_chunk = chunk ^ key
        expected_ciphertext = (expected_ciphertext << KEY_SIZE) | encrypted_chunk

    dut._log.info(f"Expected ciphertext: {hex(expected_ciphertext)}")

    # Assertion to check if the received ciphertext matches the expected ciphertext
    checker.check_ciphertext(ciphertext, expected_ciphertext)

    # Check that encryption_status is low after encryption is complete
    checker.check_encryption_status(dut)

    # Check that oCiphertext_counter reached the expected value
    expected_counter = MSG_SIZE  # Since oCiphertext_counter counts bits from 0 to 63
    checker.check_ciphertext_counter(dut, expected_counter)

    dut._log.info("Test completed successfully")
    
    
    dut._log.info("Trying covergroup")

    
    # Simulate some values for testing
    for _ in range(10):
        message = random.getrandbits(MSG_SIZE)
        key = random.getrandbits(KEY_SIZE)
        print(f"Generated message: {hex(message)} and key {hex(key)}")
        sample_cp(message,key)

    # Generate and print the coverage report
    report_coverage()

    # Final assertion: Check that uio_oe value is 0
    assert dut.uio_oe.value == 0, "Enable path is not 0!"