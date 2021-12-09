"""
Resources:

Lectures by Kaj-Mikael Björk, Arcada 2021
https://arcada.itslearning.com/

PuLP & PuLP case studies
https://coin-or.github.io/pulp/index.html
by Dr Stuart Mitchell et al.
"""

import numpy as np
from pulp import *

VALS = ROWS = COLS = range(1, 10) # 9 rader, 9 columner med värderna 1 - 9

# Gör 9 3x3 rutnät och ge dem unika index för solvern
Boxes = [
    [(3 * i + k + 1, 3 * j + l + 1) for k in range(3) for l in range(3)]
    for i in range(3)
    for j in range(3)
]


prob = LpProblem("sudoku") # LP problem från PuLP

choices = LpVariable.dicts("Choice", (VALS, ROWS, COLS), cat="Binary")

for r in ROWS:
    for c in COLS:
        prob += lpSum([choices[v][r][c] for v in VALS]) == 1
        # The row, column and box constraints are added for each value
for v in VALS:
    for r in ROWS:
        prob += lpSum([choices[v][r][c] for c in COLS]) == 1

    for c in COLS:
        prob += lpSum([choices[v][r][c] for r in ROWS]) == 1

    for b in Boxes:
        prob += lpSum([choices[v][r][c] for (r, c) in b]) == 1

"""  
Vi har därmed binära variabler från
Choice_1_1_1 till Choice_9_9_9, alltså 9x9x9 = 729 binära 

Vi har constraints för alla 81 val
dvs att det endast får vara 1 siffra per position
Alternativt några absoluta constraints, t.ex: 
    Choice_5_2_4 == 1
dvs att det måste vara en 5:a på rad 2, column 4

Vi har även constraints för varje låda t.ex:
    Choice_1_1_1 + Choice_1_1_2 + Choice_1_1_3 + Choice_1_2_1 + Choice_1_2_2 + Choice_1_2_3 + Choice_1_3_1 + Choice_1_3_2 + Choice_1_3_3 = 1

dvs att i första 3x3 lådan får det bara finnas EN instans av siffran 1

samma princip används sedan för varje rad och column, t.ex: 
    Choice_1_1_1 + Choice_2_1_1 + Choice_3_1_1 .... + Choice_9_1_1 == 1

totalt får vi alltså 1 constraint per siffra per låda, 81 st
sedan samma för rader och columner, med andra ord 81 x 3 = 243 constraints
                               (+ varierande absoluta constraints per sudoku)

Massor med binära constraints, varje rad, låda och columns får endast ha unika nummer
Om vi nu kör skulle vi få väldigt fina sudoku:n som ser ut t.ex:
   [1,2,3,4,5,6,7,8,9]
   [9,1,2,3,4,5,6,7,8]
   [8,9,1,2,3,4,5,6,7]
   [7,8,9,1,2,3,4,5,6]
   [6,7,8,9,1,2,3,4,5]
   [5,6,7,8,9,1,2,3,4]
   [4,5,6,7,8,9,1,2,3]
   [3,4,5,6,7,8,9,1,2]
   [2,3,4,5,6,7,8,9,1]
Diagonalt och fint!
Men nu har ju sudokun constraints färdiga så riktigt så enkelt blev det inte
"""


# PuLP vill ha våra sudokuns färdiga värden som tuples
# t.ex. En 5:a på rad 2 i column 4 blir (5,2,4)
# Därför loopar vi igenom våra exmpel sudokun (list of lists) och sparar deras contraints i en ny variable

from sudokus.samples import samples
sudokus = samples.sudokus()


sudokus_constraints = []

level = 'expert'  # expert    / easy
sample = 4      # 0-4       / 0-2

for s in sudokus[level]:
    sc = []
    for row, r in enumerate(s):
        for column, i in enumerate(r):
            if i != 0:
                sc.append(tuple((i, row+1, column+1)))
    sudokus_constraints.append(sc)

input_data = sudokus_constraints[sample]

# Sen lägger vi till dessa nya constraints i vårt problem
# t.ex. att en 5:a på rad 2, column 4 måste vara true
for (v, r, c) in input_data:
    prob += choices[v][r][c] == 1

# Vi skriver nu vårt problem till en lp fil, som PuLP sedan kan läsa lösa
prob.writeLP("Sudoku.lp")

# Ta tiden det tar att lösa!
# stop tiden - start tiden, printar tiden det tog
from time import time_ns
def timeTaken(msStart):
    msStop = time_ns() // 1000000 
    msTaken = msStop - msStart
    print('Time: ',msTaken,' ms')

msStart = time_ns() // 1000000 

# Fin data som tid, memory, osv, precis som lpSolve
print("Status:", LpStatus[prob.status])


while True:
    # Så länge solvern körs
    prob.solve()
    # Om det finns (vilket vi vet med våra 5 exempel) en optimal lösning så
    # läser vi lösningen i PuLP och spara den i en list of lists
    if LpStatus[prob.status] == "Optimal":
        solution = []
        row = []
        for r in ROWS:
            if r in [1, 4, 7]: # formattering
                pass
            for c in COLS:
                for v in VALS:
                    if value(choices[v][r][c]) == 1: # Om en binär är True, printa värdet/siffran
                        row.append(v)
                        if c in [1, 4, 7]: # mer formattering
                                pass
                        if c == 9:
                            solution.append(row)
                            row = []
        # Spara den optimala lösningen och leta efter fler, ifall det finns
        prob += (
            lpSum(
                [
                    choices[v][r][c]
                    for v in VALS
                    for r in ROWS
                    for c in COLS
                    if value(choices[v][r][c]) == 1
                ]
            )
            <= 80
        )
    # Om vi inte hittar fler lösningar så slutar vi PuLP
    else:
        break

# skriv ut lösningen
# finare print med numpy array
print(np.array(solution))
timeTaken(msStart)