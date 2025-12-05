import sys
import numpy as np

def part_one(filename):
    papers = (open(filename, "r").readlines())
    for r in range(len(papers)):
        papers[r] = list(papers[r].strip())
    papers = np.array(papers)
    p1 = 0
    # print(papers)
    for r,c in np.ndindex(papers.shape):
        if papers[r,c] == "@":
            rows = [r-1, r, r+1]
            cols = [c-1, c, c+1]
            if r == 0:
                rows = [r, r+1]
            elif r == len(papers)-1:
                rows = [r-1, r]
            if c == 0:
                cols = [c, c+1]
            elif c == len(papers[r])-1:
                cols = [c-1, c]
            
            frame = papers[np.ix_(rows, cols)].flatten()
            neighbors = len(frame[frame == "@"])-1
            p1 += 1 if neighbors < 4 else 0
    return p1


def part_two(filename):
    papers = (open(filename, "r").readlines())
    for r in range(len(papers)):
        papers[r] = list(papers[r].strip())
    papers = np.array(papers)
    p2 = 0
    prev_p2 = -1
    # print(papers)
    while prev_p2 != p2:
        prev_p2 = p2
        for r,c in np.ndindex(papers.shape):
            if papers[r,c] == "@":
                rows = [r-1, r, r+1]
                cols = [c-1, c, c+1]
                if r == 0:
                    rows = [r, r+1]
                elif r == len(papers)-1:
                    rows = [r-1, r]
                if c == 0:
                    cols = [c, c+1]
                elif c == len(papers[r])-1:
                    cols = [c-1, c]
                
                frame = papers[np.ix_(rows, cols)].flatten()
                neighbors = len(frame[frame == "@"])-1
                if neighbors < 4:
                    p2 += 1
                    papers[r,c] = '.'
    return p2




def main():
    if len(sys.argv) < 2:
        print('usage: python3 d4.py <filename>')
    else:
        filename = sys.argv[1]
        p1 = part_one(filename)
        print(f"Part one: {p1}")
        p2 = part_two(filename)
        print(f"Part two: {p2}")

main()