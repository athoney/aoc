import re

def multiply(s):
    s = s.removeprefix("mul(").removesuffix(")").split(",")
    return int(s[0]) * int(s[1])

def main():
    pattern1 = r"mul\(\d{1,3},\d{1,3}\)"
    instructions = 0
    with open("input.txt") as f:
        for line in f.readlines():
            groups = re.findall(pattern1, line)
            instructions += sum(map(multiply,groups))
    print(instructions)

def p2():
    pattern1 = r"do\(\).*"
    pattern2 = r"mul\(\d{1,3},\d{1,3}\)"
    instructions = 0
    int1 = 0
    with open("input.txt") as f:
        groups = f.read().replace("\n", '').split("don't()")

    do = list(map(lambda x: re.findall(pattern1, x), groups))
    for d in do:
        muls = list(map(lambda x: re.findall(pattern2, x), d))
        for mul in muls:
            instructions += sum(map(multiply,mul))
    print(instructions)


main()
p2()