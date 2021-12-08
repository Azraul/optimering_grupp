

# I ett sudoku på 9st 3x3 (standard sudoku alltså), har vi 9 rader, 9 columner och siffror 1-9
VALS = ROWS = COLS = range(1, 10)

# Vi har en binär för varje val, dvs. 9 siffror och 81 val (9rader * 9 columner)
# Alltså 729 st olika binära alterantiv
BINARIES = []

for V in VALS:
    for R in ROWS:
        for C in COLS:
            BINARIES.append(f'x{V}{R}{C}')


# För att få våran sudoku att fungera måste vi ha 4 olika typer av constraints.
# Varje värde får endast hamna 1 gånger per:
# Rad, 9 rader * 9 siffror = 81 constraints
# Kolumn, 9 kolumner * 9 siffror = 81 constraints
# 3x3 låda/rutnät, 9 lådor * 9 siffror = 81 constraints
# Val/cell, 81 celler = 81 constraints
# Totalt får vi då 324 constraints och 729 binära tal för lpsolve
# Vi har även ett antal till constraints som direct kommer överskrida våra cell
# konstraints i form av sudokuns färdiga rutor.

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

from sudokus.samples import samples
sudokus = samples.sudokus()



# list alla sudokus constraints
sudoku_constraints = []

for s in sudokus:
    sc = []
    for row, r in enumerate(s):
        for column, i in enumerate(r):
            if i != 0:
                sc.append(f'x{i}{row+1}{column+1} = 1')
    sudoku_constraints.append(sc)

sample = 5 # Välj vilket sample du vill prova 

# Vi skriver allt till en text fil som man enkelt kan copy pasta över till en lp
# Vi kunde såklart bara ändrat filen till en .lp och lagt till följande:

# file.write('/* No objective for sudoku */')
# file.write('\n')
# file.write('max: ;')
# file.write('\n')

file = open('sudoku_solve.txt', 'w')

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
            file.write(row + ';')
            file.write('\n')
    else:
        pass


file.write('\n')
file.write('/* Binaries */')
file.write('\n')
file.write('bin')
file.write('\n')
for i, binary in enumerate(BINARIES):
    file.write(binary)
    if(i+1 == len(BINARIES)):
        file.write(';')
    else:
        file.write(', ')
    file.write('\n')
        

file.write('\n')

file.close()

# Trots att problemt är fullt funktionelt tycks lpsolve inte riktigt kunna lösa sudokun.
# Efter ca 5h väntande och 500 miljoner iterationer gav vi upp på lpsolve.

# P.S ser ut som vi måste ta bort binary definition på variabler som är sudoku defined, t.ex.
# sudoku constraint: 311 = 1
# ta då bort binary setting av 311, annars tycks den bli om definerad