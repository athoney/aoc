import sys
import numpy as np
import logging

def setup_logger(debug):
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)
    logger = logging.getLogger(__name__)
    return logger


def part_one(filename):
    p1 = 0
    with open(filename) as f:
        valids = []
        for line in f:
            if "-" in line:
                # range
                valid = line.strip().split("-")
                # print(valid)
                valids.append([int(valid[0]), int(valid[1])])
            elif line == "\n":
                pass
                # print(f"switching to checking. len = {len(valids)}")
            else:
                # id to check
                avail_id = int(line.strip())
                for valid in valids:
                    if avail_id >= valid[0] and avail_id <= valid[1]:
                        # print(f"found {avail_id} in range {valid}")
                        p1 += 1
                        break
    return p1

def part_two(filename, logger):
    p2 = 0
    valids = []
    with open(filename) as f:
        for line in f:
            if "-" in line:
                # range
                new_range = list(map(int, line.strip().split("-")))
                logger.debug(f"testing range: {new_range}")
                i = 0
                merge = False
                while i < len(valids):
                    test_sort = sorted(valids[i] + new_range)
                    # 1212 or 2121
                    test_sort_1 = [valids[i][0], new_range[0], valids[i][1], new_range[1]]
                    test_sort_2 = [new_range[0], valids[i][0], new_range[1],  valids[i][1]]
                    # 1221 or 2112
                    test_sort_3 = [valids[i][0], new_range[0], new_range[1], valids[i][1]]
                    test_sort_4 = [new_range[0], valids[i][0], valids[i][1],  new_range[1]]
                    # logger.debug(f"test_sort: {test_sort}")
                    if test_sort == test_sort_1 or test_sort == test_sort_2 or test_sort == test_sort_3 or test_sort == test_sort_4:
                        logger.debug(f"\tmerging old range: {valids[i]} with new range: {new_range} to get: {test_sort}")
                        del valids[i]
                        new_range = [test_sort[0], test_sort[-1]]
                        i = 0
                    else:
                        i += 1
                    
                    
                    
                logger.debug(f"\tadding new range {new_range}")
                valids.append(new_range)

                logger.debug(f"valids: {valids}")
                        
            elif line == "\n":
                break

    for valid in valids:
        p2 += valid[1] - valid[0] + 1
    return p2


def main():
    if len(sys.argv) < 2:
        print("usage: python3 code.py <filename>")
    else:
        logger = setup_logger(False)
        p1 = part_one(sys.argv[1])
        print(f"Part one: {p1}")
        p2 = part_two(sys.argv[1], logger)
        print(f"Part two: {p2}")


main()
