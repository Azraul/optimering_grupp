"""
Resources:

University of Notthingham - Computerphile Youtube channel
https://www.youtube.com/watch?v=G_UYXzGuqvM

Löser alla sudokus vi provat hittils!
"""
import numpy as np
from time import time_ns
# import sample sudokus
from sudokus.samples import samples
sudokus = samples.sudokus()

# iterations, bör vara global pga. recursive & resets
### Kan bygga en funktion som kallas men blir mindre tydligt då
iterations = 0

# startar iden i nano sekunder (undviker float32 oprecision)
msStart = time_ns() // 1000000 

# stop tiden - start tiden, printar tiden det tog
def timeTaken(msStart):
    msStop = time_ns() // 1000000 
    msTaken = msStop - msStart
    print('Time: ',msTaken,' ms')

# Kollar om en siffra är giltig
# Finns siffran redan i y eller x axeln
# Finns siffran redan i 3x3 rutnät
def possible(y,x,n,grid):
    global iterations
    iterations = iterations + 1
    for i in range(0,9):
        if grid[y][i] == n:
            return False
    for i in range(0,9):
        if grid[i][x] == n:
            return False
    x0 = (x//3)*3
    y0 = (y//3)*3
    for i in range(0,3):
        for j in range(0,3):
            if grid[y0+i][x0+j] == n:
                return False
    return True

# Kollar alla celler genom att kalla på funktionen ovan om det är en 0:a (tom ruta) i sudokun
# Om funktionen ovan ger false går den tillbaka och provar något annat
# t.ex provar den sätta en 1 i första tomma rutan och sedan lösa sudokun.
## eftersom vi så fint definerat att det bara finns en 1:a i varje rad/kolumn
## och därmed kommer den snabbt till att det kanske inte går
# Om det inte lyckas provar den sätta en 2:a i den första rutan och lösa sudokun osv osv.
# Om inget nummer 1-9 funka i den första tomma rutan går den till nästa ruta och provar samma där
# När vi inte har några tomma rutor kvar är alltså 
def solve(grid):
    i = 1
    for y in range(9):
        for x in range(9):
            if grid[y][x] == 0:
                for n in range(1,10):
                    if possible(y,x,n,grid):
                        grid[y][x] = n
                        solve(grid)
                        grid[y][x] = 0
                return
    global iterations, msStart
    print("solution ", i,":")
    print('iterations:' , iterations)
    timeTaken(msStart)
    print(np.matrix(grid))
    i = i + 1

# sample grid
grid = [
    [5,3,0,0,7,0,0,0,0],
    [6,0,0,1,9,5,0,0,0],
    [0,9,8,0,0,0,0,6,0],
    [8,0,0,0,6,0,0,0,3],
    [4,0,0,8,0,3,0,0,1],
    [7,0,0,0,2,0,0,0,6],
    [0,6,0,0,0,0,2,8,0],
    [0,0,0,4,1,9,0,0,5],
    [0,0,0,0,8,0,0,7,9]
]


# sen grid/sudoku of choice into function
solve(sudokus[4])