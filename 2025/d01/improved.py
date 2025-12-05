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
            start = click_i


            if direction == "R":
                # increase
                end = (start + clicks) % 100
                # Count click_i on zero
                p2 += (start + clicks) // 100

            else:
                # decrease
                end = (start - clicks) % 100
                # Count click_i on zero
                if start == 0:
                    p2 += clicks // 100
                else:
                    if clicks >= start:
                        p2 += 1 + (clicks - start) // 100
                

            click_i = end


            # print(f"{direction}{clicks} --> {click_i} p2={p2}")

            if click_i == 0:
                p1 += 1


    return p1, p2



def main():
    day_one("input.txt")
    # p1 = 1195
    # p2 = 6770
    

start_time = time.time()
p1, p2 = day_one("input.txt")
print("--- %s seconds ---" % (time.time() - start_time))
print(f"Part 1: {p1}")
print(f"Part 2: {p2}")
