# sudoku pussles, taken from:
# https://sudoku.com/expert/
# expert level used for all 5 samples
## added 6th easy sudoku sample


def sudokus():
    sudoku00 = [
        [0, 0, 0, 0, 0, 5, 4, 0, 6],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 2, 0, 8, 0, 5, 0],
        [0, 1, 3, 0, 9, 0, 8, 0, 7],
        [0, 0, 4, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 8, 0, 0, 0, 0, 9],
        [0, 0, 8, 0, 0, 1, 9, 0, 0],
        [0, 2, 0, 7, 3, 0, 0, 0, 0],
        [5, 0, 0, 0, 0, 0, 0, 7, 0],
    ]

    sudoku01 = [
        [4, 0, 0, 8, 0, 0, 1, 0, 0],
        [0, 1, 0, 0, 0, 0, 3, 0, 0],
        [7, 0, 0, 0, 9, 6, 0, 0, 0],
        [8, 0, 0, 6, 0, 0, 0, 4, 0],
        [0, 0, 0, 0, 5, 0, 0, 0, 0],
        [0, 3, 1, 0, 0, 0, 0, 7, 2],
        [3, 0, 0, 0, 0, 0, 9, 0, 0],
        [0, 6, 2, 0, 0, 0, 4, 0, 0],
        [0, 0, 0, 4, 0, 0, 0, 6, 0],
    ]

    sudoku02 = [
        [0, 2, 0, 0, 0, 0, 9, 1, 3],
        [0, 0, 5, 0, 0, 0, 0, 8, 7],
        [0, 0, 0, 1, 9, 0, 0, 0, 0],
        [1, 0, 0, 6, 8, 0, 0, 7, 0],
        [0, 9, 0, 0, 0, 0, 0, 0, 2],
        [0, 0, 4, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 2, 0],
        [8, 0, 0, 0, 0, 0, 0, 4, 0],
        [0, 0, 6, 4, 0, 3, 0, 0, 0],
    ]

    # Hardest one
    sudoku03 = [
        [0, 0, 7, 5, 0, 0, 0, 0, 3],
        [0, 0, 8, 0, 0, 0, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 8, 0, 7],
        [0, 0, 0, 2, 0, 0, 4, 0, 0],
        [9, 2, 0, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 0, 3, 0, 0, 5, 0],
        [0, 0, 0, 3, 8, 7, 0, 0, 0],
        [4, 0, 1, 0, 0, 5, 0, 0, 0],
        [6, 0, 0, 0, 0, 4, 0, 0, 0],
    ]

    sudoku04 = [
        [0, 0, 1, 0, 8, 0, 0, 0, 0],
        [0, 3, 0, 7, 0, 0, 0, 0, 0],
        [0, 9, 0, 0, 0, 0, 8, 0, 5],
        [0, 0, 0, 0, 0, 1, 0, 0, 4],
        [0, 0, 0, 0, 0, 3, 0, 9, 1],
        [0, 0, 0, 6, 7, 2, 0, 0, 0],
        [7, 0, 0, 0, 3, 0, 0, 2, 0],
        [2, 0, 6, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 6, 0],
    ]

    expert = []
    expert.append(sudoku00)
    expert.append(sudoku01)
    expert.append(sudoku02)
    expert.append(sudoku03)
    expert.append(sudoku04)

    easy = []
    easy.append(
        [
            [3, 4, 0, 2, 6, 0, 8, 0, 1],
            [0, 2, 0, 5, 0, 8, 3, 0, 0],
            [0, 0, 1, 0, 3, 0, 0, 0, 0],
            [0, 6, 2, 0, 4, 7, 0, 9, 8],
            [4, 0, 0, 0, 5, 0, 0, 0, 2],
            [5, 0, 8, 1, 9, 0, 7, 6, 0],
            [0, 1, 0, 0, 8, 5, 0, 2, 0],
            [0, 8, 7, 0, 0, 0, 9, 1, 0],
            [0, 0, 0, 9, 7, 0, 0, 8, 0],
        ]
    )
    easy.append(
        [
            [2, 1, 9, 0, 4, 6, 0, 3, 0],
            [0, 0, 5, 1, 0, 0, 0, 0, 0],
            [7, 1, 0, 0, 8, 0, 0, 5, 4],
            [6, 0, 0, 1, 0, 0, 3, 0, 5],
            [1, 8, 5, 0, 0, 0, 7, 2, 0],
            [0, 4, 0, 6, 0, 2, 8, 0, 0],
            [0, 6, 8, 0, 0, 0, 4, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 6, 2],
            [0, 0, 0, 4, 0, 7, 5, 3, 0],
        ]
    )

    sudokus = {
        "easy": [],
        "expert": [],
    }
    sudokus["expert"].extend(expert)
    sudokus["easy"].extend(easy)
    return sudokus
