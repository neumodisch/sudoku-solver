import numpy as np
import time

class SudokuSolver:

    def __init__(self):
        self.puzzle = None

    def set_puzzle(self, puzzle):
        self.puzzle = puzzle.copy()
    
    def get_puzzle(self):
        return self.puzzle

    def _chk_line(self, line):
        numbers, counts = np.unique(line, return_counts=True)
        for i, number in enumerate(numbers):
            if number < 0 or number > 9:
                return False
            elif number != 0 and counts[i] != 1:
                return False
        if np.sum(line) > np.sum(np.arange(1, 10)):
            return False
        return True

    def _chk_sudoku(self, sudoku, a, b):
        # check the current row and column first
        if self._chk_line(sudoku[a, :]) == False or self._chk_line(sudoku[:, b]) == False:
            return False
        for i in range(9):
            if i == a:
                # Skip this value, since it was already checked
                continue
            if self._chk_line(sudoku[i, :]) == False:
                return False
        for i in range(9):
            if i == b:
                # Skip this value, since it was already checked
                continue
            if self._chk_line(sudoku[:, i]) == False:
                return False
        for box in np.hsplit(sudoku, 3):
            for smallbox in np.vsplit(box, 3):
                if self._chk_line(smallbox.ravel()) == False:
                    return False
        return True
        
    def _try_number(self):
        for i in range(9):
            for j in range(9):
                if (self.puzzle[i, j] == 0):
                    # Found an empty spot
                    success = False
                    for k in range(1, 10):
                        # Try a number in the next empty spot
                        self.puzzle[i, j] = k
                        if self._chk_sudoku(self.puzzle, i, j) == True:
                            if np.unique(self.puzzle)[0] != 0:
                                # There are no 0s left, we found a solution
                                success = True
                                break
                            elif self._try_number() == True:
                                success = True
                                break
                    if success == False:
                        # None of the numbers is correct, reset to zero and go back
                        self.puzzle[i, j] = 0
                    return success

    def solve(self):
        if self.puzzle is not None:
            return self._try_number()
        else:
            raise Exception("No puzzle set!")

sudoku = np.array([[5,3,0,0,7,0,0,0,0],
                   [6,0,0,1,9,5,0,0,0],
                   [0,9,8,0,0,0,0,6,0],
                   [8,0,0,0,6,0,0,0,3],
                   [4,0,0,8,0,3,0,0,1],
                   [7,0,0,0,2,0,0,0,6],
                   [0,6,0,0,0,0,2,8,0],
                   [0,0,0,4,1,9,0,0,5],
                   [0,0,0,0,8,0,0,7,9]])

solver = SudokuSolver()
solver.set_puzzle(sudoku)
start = time.time()

if solver.solve():
    print("Found a solution for this sudoku in {}s:".format(time.time() - start))
    print(solver.get_puzzle())
else:
    print("This sudoku has no solution!")