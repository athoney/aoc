import time
from collections import Counter


def read_input(filename):
    list1 = []
    list2 = []
    with open(filename) as f:
        for line in f:
            list1.append(int(line.split()[0]))
            list2.append(int(line.split()[1]))
    return list1, list2


def main():
    list1, list2 = read_input('input.txt')

    answer1 = sum(abs(x - y) for x, y in zip(sorted(list1), sorted(list2)))
    print(f"part 1: {answer1}")

    list2_counts = Counter(list2)
    answer2 = sum(x * list2_counts[x] for x in list1)
    print(f"part 2: {answer2}")

start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))
