import re
import numpy as np

def look_x(puzzle, r, c, word):
    # bound check for xmas -->
    found = 0
    if c <= len(puzzle[c])-len(word):
        if ''.join(puzzle[r][c:c+len(word)]).lower() == word.lower():
            print(''.join(puzzle[r][c:c+len(word)]).lower())
            print(f"row {r}")
            found += 1
    # bound check for samx <--
    if c >= len(word):
        if ''.join(puzzle[r][c-len(word)+1:c+1]).lower() == word.lower()[::-1]:
            print(''.join(puzzle[r][c-len(word)+1:c+1]).lower())
            print(f"row {r}")

            found += 1
    return found

def look_y(puzzle, r, c, word):
    

           

def word_search(puzzle, word):
    r = 0
    c = 0
    found = 0
    while r < len(puzzle):
        while c < len(puzzle[r]):
            if puzzle[r][c].lower() == word[0]:
                # print(puzzle[r][c])
                found += look_x(puzzle, r, c, word)
            c += 1
        r += 1
        c = 0
    return found



def main():

    with open ('sm.txt', 'r') as f:
        puzzle = [list(line.strip()) for line in f]
        print(puzzle)
    print(word_search(puzzle, 'xmas'))



main()