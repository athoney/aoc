import time
from collections import Counter


def check_if_valid(value):
    """
    an ID is invalid if it is made only of some
    sequence of digits repeated at least twice.
    """
    freq = Counter(value).values()
    smallest_freq = sorted(freq)[0]

    if smallest_freq < 2:
        return False
    
    n = len(value) // smallest_freq
    chunks = [value[i:i + n] for i in range(0, len(value), n)]

    return len(set(chunks)) == 1

def day_two(filename):
    p1 = 0
    p2 = 0
    ids = open(filename).read().split(",")
    for id_range in ids:
        start, stop = id_range.split('-')
        # print(start, stop)
        for value in range(int(start), int(stop)+1):
            value = str(value)
            id_len = len(value)
            if id_len % 2 == 0:
                midpoint = id_len // 2
                if value[0:midpoint] == value[midpoint:]:
                    p1 += int(value)

            if check_if_valid(value):
                p2 += int(value)

    return p1, p2

        



def main():
    p1, p2 = day_two("input.txt")
    print(p1, p2)
    # p1-13919717792
    # p2-14582313461
    
main()
# start_time = time.time()
# p1, p2 = day_one("input.txt")
# print("--- %s seconds ---" % (time.time() - start_time))
# print(f"Part 1: {p1}")
# print(f"Part 2: {p2}")
