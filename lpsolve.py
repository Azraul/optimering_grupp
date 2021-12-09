"""
Resources:

Lectures by Kaj-Mikael Björk, Arcada 2021
https://arcada.itslearning.com/

Vi bygger upp object funktionen, binära variabler och
alla våra behövliga constraints.

Vi kommer att söka efter minsta möjliga lösning (alltså 81 binära svar)

Vi bygger varje cell med xVärdeRadKolumn
    t.ex. första rutan, högst upp till vänster är en 3:a
    x311    -     x   3       1       1
                    Värde    Rad    Kolumn

Sen skriver vi ut allt till en lp fil

Vi har en binär för varje val, dvs. 9 siffror och 81 val (9rader * 9 columner)
Alltså 729 st olika binära alterantiv
    -   Några av dessa kommer sedan inte skrivas ut som binära eftersom varje sudoku
        startar med en hel del färdiga positioner/celler.
    -   Ta x311 från ovan, om den första rutan högst upp till vänster ska vara True
        x311 = 1; kommer vi inte ha den med i listan över binära tal
        p.g.a. lpsolve då omdefinerar vårt constraint till x311 kan vara 0 eller 1.

För att få våran sudoku att fungera måste vi ha 4 olika typer av constraints.
Varje värde får endast hamna 1 gånger per:
Rad, 9 rader * 9 siffror = 81 constraints
Kolumn, 9 kolumner * 9 siffror = 81 constraints
3x3 låda/rutnät, 9 lådor * 9 siffror = 81 constraints
Val/cell, 81 celler = 81 constraints
Totalt får vi då 324 constraints och 729 binära tal för lpsolve
Vi har även ett antal till constraints som direct kommer överskrida våra cell
konstraints i form av sudokuns färdiga rutor.

"""

# I ett sudoku på 9st 3x3 (standard sudoku), har vi 9 rader, 9 columner och siffror 1-9
VALS = ROWS = COLS = range(1, 10)

# våra 729 binära tal som strings i en lista
BINARIES = []

for V in VALS:
    for R in ROWS:
        for C in COLS:
            BINARIES.append(f'x{V}{R}{C}')

# alla våra 324 constraints, färdiga som strings i listor
CONSTRAINTS = []

# max 1 siffra per rad
for V in VALS:
    for R in ROWS:
        s = ""
        for i, C in enumerate(COLS):
            s = s + f'x{V}{R}{C}'
            if i == 8:
                s = s + ' = 1'
            else:
                s = s + ' + '
        CONSTRAINTS.append(s)

# max 1 siffra per kolumn
for V in VALS:
    for C in COLS:
        s = ""
        for i, R in enumerate(ROWS):
            s = s + f'x{V}{R}{C}'
            if i == 8:
                s = s + ' = 1'
            else:
                s = s + ' + '
        CONSTRAINTS.append(s)

# max 1 siffra per cell
for C in COLS:
    for R in ROWS:
        s = ""
        for i, V in enumerate(VALS):
            s = s + f'x{V}{R}{C}'
            if i == 8:
                s = s + ' = 1'
            else:
                s = s + ' + '
        CONSTRAINTS.append(s)


# 3x3 max 1 per value
for V in VALS:
    for i in range(3):
        for j in range(3):   
            row = 3*i
            col = 3*j
            s = ""
            for k, R in enumerate(range(1+row,4+row)):
                for n, C in enumerate(range(1+col,4+col)):
                    s = s + f'x{V}{R}{C}'
                    if k+n == 4:
                        s = s + ' = 1'
                    else:
                        s = s + ' + '
            CONSTRAINTS.append(s)
            

print(len(CONSTRAINTS))
print('Choice_VALUE_ROW_COLUMN')
print('ROW:', CONSTRAINTS[0])
print('COLUMN:', CONSTRAINTS[81])
print('CELL:', CONSTRAINTS[162])
print('BOX:', CONSTRAINTS[243])

# importera våra sudoku samples
from sudokus.samples import samples
sudokus = samples.sudokus()



# lista alla sudokus celler med constraints i listor som stringar
## Vi måste lägga till själva constrainet senare när vi skriver till en fil
## Det för att enkelt kunna jämnaföra våra sudoku celler med de binära
sudoku_constraints = []

for s in sudokus['easy']: # easy, lp and expert don't work!
    sc = []
    for row, r in enumerate(s):
        for column, i in enumerate(r):
            if i != 0:
                sc.append(f'x{i}{row+1}{column+1}')
    sudoku_constraints.append(sc)

sample = 2 # Välj 2, det är enkelt nog till lpsolve

# Vi skriver allt till en lp fil
# Sen är det bara att köra med lpsolve

file = open('sudoku_solve.lp', 'w')

file.write('/* Objective for sudoku */')
file.write('\n')
file.write('min:')
file.write('\n')

for i, bin in enumerate(BINARIES):
    file.write(bin)
    if(i+1 ==len(BINARIES)):
        file.write(';')
    else:
        file.write(' + ')

file.write('\n')
file.write('/* Variable Constraints */')
file.write('\n')
for constraint in CONSTRAINTS:
    file.write(constraint + ';')
    file.write('\n')
file.write('\n')
file.write('/* Sudoku Constraints */')
file.write('\n')
for i, sudoku in enumerate(sudoku_constraints):
    if(i==sample): 
        file.write('\n')
        file.write(f'/* Sudoku0{i} constraints*/')
        file.write('\n')
        for row in sudoku:
            file.write(row + ' = 1;')
            file.write('\n')
    else:
        pass


file.write('\n')
file.write('/* Binaries */')
file.write('\n')
file.write('bin')
file.write('\n')

# Vi skriver bara de binaries som inte är definerade från vårt sudoku redan

for i, binary in enumerate(BINARIES):
    if(binary not in sudoku_constraints[sample]):
        file.write(binary)
        if(i+1 == len(BINARIES)):
            file.write(';')
        else:
            file.write(', ')
        file.write('\n')
    else:
        pass
        

file.write('\n')

file.close()

# Trots att problemt är fullt funktionelt tycks lpsolve inte riktigt kunna lösa svårare sudokun inom rimlig tid.
# Därför satta vi in ett 5:e sample, sudoku05, som är av graden easy vilket den lyckas lösa snabbt och effektivt