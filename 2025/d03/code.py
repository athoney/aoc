def part_one(filename):
    total = 0
    with open(filename) as f:
        for bank in f:
            bank = bank.strip()
            n1 = max(bank[:-1])
            i = bank.index(n1)
            n2 = max(bank[i+1:])
            total += int(n1+n2)
    return total

def part_two(filename):
    total = 0
    with open(filename) as f:
        for bank in f:
            bank = bank.strip()
            joltage = ""
            i = -1
            for buffer in range(11, -1, -1):
                bank_slice = bank[i+1:(len(bank)-buffer)] # cut off previously used numbers and save room for remaining
                n1 = max(bank_slice) # find the max in the bank
                i = bank_slice.index(n1) + len(bank[:i+1]) # get the index of the new max and add an offset for the previously chopped bank
                joltage += n1 # append max number to joltage
            
            total += int(joltage) # add joltage to total
    return total


print(f"Part one: {part_one("input.txt")}") #16854
print(f"Part two: {part_two("input.txt")}") #167526011932478