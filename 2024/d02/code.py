import time

def main(filename="/home/athoney/Userdata/aoc/2024/d02/input.txt"):
    def safe(levels):
        inc = levels[0] < levels[1]
        for i in range(0, len(levels)-1):
            new_inc = levels[i] < levels[i+1]
            diff = abs(levels[i+1] - levels[i])
            if (not inc == new_inc) or diff == 0 or diff > 3:
                return 0
        return 1
    

    p1_safe_levels = 0
    p2_safe_levels = 0
    with open (filename, "r") as file:
        for line in file:
            levels = list(map(int, line.split()))
            if safe(levels):
                p1_safe_levels += 1
            else:
                for i in range(0, len(levels)):
                    if safe(levels[0:i] + levels[i+1:]):
                        p2_safe_levels += 1
                        break

    print(f"Part 1: {p1_safe_levels}")
    print(f"Part 2: {p1_safe_levels+p2_safe_levels}")

    
start_time = time.time()
main()
print("--- %s seconds ---" % (time.time() - start_time))