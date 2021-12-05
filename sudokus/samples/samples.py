
# sudoku pussles, taken from:
# https://sudoku.com/expert/
# expert level used for all 5 samples


def sudokus():
    sudoku00 = [
    [0,0,0,0,0,5,4,0,6],
    [0,0,0,0,0,0,0,0,0],
    [0,0,0,2,0,8,0,5,0],
    [0,1,3,0,9,0,8,0,7],
    [0,0,4,0,0,0,0,0,1],
    [0,0,0,8,0,0,0,0,9],
    [0,0,8,0,0,1,9,0,0],
    [0,2,0,7,3,0,0,0,0],
    [5,0,0,0,0,0,0,7,0]
    ]

    sudoku01 = [
        [4,0,0,8,0,0,1,0,0],
        [0,1,0,0,0,0,3,0,0],
        [7,0,0,0,9,6,0,0,0],
        [8,0,0,6,0,0,0,4,0],
        [0,0,0,0,5,0,0,0,0],
        [0,3,1,0,0,0,0,7,2],
        [3,0,0,0,0,0,9,0,0],
        [0,6,2,0,0,0,4,0,0],
        [0,0,0,4,0,0,0,6,0]
    ]

    sudoku02 = [
        [0,2,0,0,0,0,9,1,3],
        [0,0,5,0,0,0,0,8,7],
        [0,0,0,1,9,0,0,0,0],
        [1,0,0,6,8,0,0,7,0],
        [0,9,0,0,0,0,0,0,2],
        [0,0,4,0,0,0,0,0,0],
        [0,0,0,0,0,1,0,2,0],
        [8,0,0,0,0,0,0,4,0],
        [0,0,6,4,0,3,0,0,0]
    ]

    # Hardest one
    sudoku03 = [
        [0,0,7,5,0,0,0,0,3],
        [0,0,8,0,0,0,0,0,0],
        [0,4,0,0,0,0,8,0,7],
        [0,0,0,2,0,0,4,0,0],
        [9,2,0,0,0,0,0,1,0],
        [0,0,0,0,3,0,0,5,0],
        [0,0,0,3,8,7,0,0,0],
        [4,0,1,0,0,5,0,0,0],
        [6,0,0,0,0,4,0,0,0]
    ]

    sudoku04 = [
        [0,0,1,0,8,0,0,0,0],
        [0,3,0,7,0,0,0,0,0],
        [0,9,0,0,0,0,8,0,5],
        [0,0,0,0,0,1,0,0,4],
        [0,0,0,0,0,3,0,9,1],
        [0,0,0,6,7,2,0,0,0],
        [7,0,0,0,3,0,0,2,0],
        [2,0,6,0,0,0,1,0,0],
        [0,0,0,0,0,0,0,6,0]
    ]

    list = []
    list.append(sudoku00)
    list.append(sudoku01)
    list.append(sudoku02)
    list.append(sudoku03)
    list.append(sudoku04)

    return list