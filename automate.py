#/*=====Start Change Task 2=====*/

import csv
from eightpuzzle import (EightPuzzleState)

def load_csv(filename):

    puzzle_data = []
    with open(filename, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) == 9:
                puzzle = [int(cell) for cell in row]
                puzzle_data.append(puzzle)
    return puzzle_data


def create_puzzles_from_csv(puzzle_data):

    puzzles = []
    for puzzle_config in puzzle_data:
        puzzle = EightPuzzleState(puzzle_config)
        puzzles.append(puzzle)
    return puzzles

#*=====End Change Task 2=====*/
