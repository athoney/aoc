from collections import defaultdict


def read_input(filename):
    list1 = []
    list2 = []
    with open(filename) as f:
        for line in f:
            list1.append(line.split()[0])
            list2.append(line.split()[1])
    return list1, list2


def main():
    list1, list2 = read_input('input.txt')

    answer1 = sum([abs(int(x) - int(y)) for x, y in zip(sorted(list1), sorted(list2))])
    print(f"part 1: {answer1}")

    answer2 = sum([int(x) * list2.count(x) for x in list1])
    print(f"part 2: {answer2}")

main()