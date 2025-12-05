import re
import numpy as np

def look_x(puzzle, r, c, word):
    found = 0
    # bound check for xmas right
    if c <= len(puzzle[c])-len(word):
        if ''.join([puzzle[r][c+i] for i in range(len(word))]).lower() == word.lower():
            found += 1
    # bound check for xmas left
    if c >= len(word)-1:
        if ''.join([puzzle[r][c-i] for i in range(len(word))]).lower() == word.lower():
            found += 1
    return found
    

def look_y(puzzle, r, c, word):
    found = 0
    # bound check for xmas down
    if r <= len(puzzle)-len(word):
        if ''.join([puzzle[r+i][c] for i in range(len(word))]).lower() == word.lower():
            found += 1
    # bound check for xmas up
    if r >= len(word)-1:
        if ''.join([puzzle[r-i][c] for i in range(len(word))]).lower() == word.lower():
            found += 1
    return found

def look_dig(puzzle, r, c, word):
    found = 0
    # bound check for xmas down right
    if r <= len(puzzle)-len(word) and c <= len(puzzle[c])-len(word):
        if ''.join([puzzle[r+i][c+i] for i in range(len(word))]).lower() == word.lower():
            found += 1
    # bound check for xmas up left
    if r >= len(word)-1 and c >= len(word)-1:
        if ''.join([puzzle[r-i][c-i] for i in range(len(word))]).lower() == word.lower():
            found += 1
    # bound check for xmas up right
    if r >= len(word)-1 and c <= len(puzzle[c])-len(word):
        if ''.join([puzzle[r-i][c+i] for i in range(len(word))]).lower() == word.lower():
            found += 1
    # bound check for xmas down left
    if r <= len(puzzle)-len(word) and c >= len(word)-1:
        if ''.join([puzzle[r+i][c-i] for i in range(len(word))]).lower() == word.lower():
            found += 1
    return found

           

def word_search(puzzle, word):
    r = 0
    c = 0
    found = 0
    while r < len(puzzle):
        while c < len(puzzle[r]):
            if puzzle[r][c].lower() == word[0]:
                # print(puzzle[r][c])
                found += look_x(puzzle, r, c, word)
                found += look_y(puzzle, r, c, word)
                found += look_dig(puzzle, r, c, word)
            c += 1
        r += 1
        c = 0
    return found


def x_search(puzzle):
    r = 0
    c = 0
    found = 0
    while r < len(puzzle):
        while c < len(puzzle[r]):
            if puzzle[r][c].lower() == "a":
                # print(puzzle[r][c])
                if r >= 1 and c >= 1 and r < len(puzzle)-1 and c < len(puzzle[c])-1:
                    top_bottom = ''.join([puzzle[r+i][c+i] for i in range(-1,2)]).lower()
                    bottom_top = ''.join([puzzle[r-i][c+i] for i in range(-1,2)]).lower()
                    # print(top_bottom, bottom_top)
                    if (top_bottom == "mas" or top_bottom == "sam") and (bottom_top == "mas" or bottom_top == "sam"):
                        found += 1
            c += 1
        r += 1
        c = 0
    return found



def main():

    with open ('input.txt', 'r') as f:
        puzzle = [list(line.strip()) for line in f]
        print(puzzle)
    print(f"found {word_search(puzzle, 'xmas')}")
    print(f"found {x_search(puzzle)}")



main()