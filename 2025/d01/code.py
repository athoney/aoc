import time
from collections import Counter


def day_one(filename):
    click_i = 50
    p1 = 0
    p2 = 0
    with open(filename) as f:
        for line in f:
            direction = line[0]
            clicks = int(line.strip()[1:])

            if direction.lower() == "r":
                # increase
                for i in range(clicks):
                    if click_i == 99:
                        click_i = 0
                    else:
                        if click_i == 0:
                            p2 += 1
                        click_i += 1
            else:
                # decrease
                for i in range(clicks):
                    if click_i == 0:
                        click_i = 99
                        p2 += 1
                    else:
                        click_i -= 1

            # print(f"{direction}{clicks} --> {click_i} p2={p2}")

            if click_i == 0:
                p1 += 1


    return p1, p2



def main():
    day_one("input.txt")
    # p1 = 1195
    

start_time = time.time()
p1, p2 = day_one("input.txt")
print("--- %s seconds ---" % (time.time() - start_time))
print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
