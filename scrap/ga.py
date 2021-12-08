import random
import numpy as np
from typing import List, Tuple
from pmx import pmx


puz = np.array(
[[0,8,3,0,2,1,0,0,7],
[9,6,0,3,0,5,8,2,1],
[2,5,1,0,0,6,0,9,3],
[0,4,8,1,0,2,0,7,0],
[0,2,9,0,0,4,0,3,0],
[0,3,0,7,0,8,0,4,0],
[3,7,0,0,0,9,0,1,4],
[8,1,0,2,5,3,0,6,9],
[6,9,0,4,0,7,0,8,2],]

)
Puzzle = np.ndarray  # List[List[int]]

## Generate random solutions based on a given starting-set puzzle
def generate_solutions(puzzle: Puzzle, n: int) -> List[Puzzle]:
    solutions = []
    size = puzzle.shape[0] + 1
    for i in range(n):
        temp_puzzle = puzzle.copy()
        for row in temp_puzzle:
            if 0 in row:
                l = [v for v in range(1, size) if v not in row]
                random.shuffle(l)
                row[row[:] == 0] = l

        solutions.append(temp_puzzle)

    return solutions


# Instantiate evaluator based off a puzzle, then you can repetively call a function that evalutes
class Fitness:
    def __init__(self, puzzle) -> None:
        self.puzzle = puzzle

    def consistent(self, solution) -> int:
        """Check how many different elements there are in each row.
        Ideally there should be DIM different elements, if there are no duplicates."""
        return sum([len(solution) - len(set(row)) for row in solution])

    def check(self, solutions: List[Puzzle]):
        scored = []
        for solution in solutions:
            s = 0
            s += self.consistent(np.rot90(solution, 1))
            s += self.consistent(
                [
                    solution[i : i + 3, j : j + 3].flatten()
                    for i in range(0, 9, 3)
                    for j in range(0, 9, 3)
                ]
            )
            scored.append([solution, s])
        scored = np.array(sorted(scored, key=lambda pair: pair[1]))
        return list(scored[:, 0]), list(scored[:, 1])


def breed_pmx(p1: Puzzle, p2: Puzzle, mask):
    parent1 = p1.copy()
    parent2 = p2.copy()
    crossed_parts_1, crossed_parts_2 = [], []
    first_cross_point, second_cross_point = 0, 0
    for i, m in enumerate(mask):
        p1_crossable_genes = parent1[i, m]
        p2_crossable_genes = parent2[i, m]
        gene_len = len(p1_crossable_genes)
        # Choosing good crossover places depending how long the array is
        if gene_len == 0:
            continue
        if gene_len == 1 or gene_len == 2:
            crossed_parts_1.extend(p2_crossable_genes)
            crossed_parts_2.extend(p1_crossable_genes)
            continue
        if gene_len == 3:
            first_cross_point = 1
            second_cross_point = 2
        elif gene_len == 4:
            first_cross_point = 2
            second_cross_point = 3
        else:
            first_cross_point = round(gene_len / 3)
            second_cross_point = gene_len - (first_cross_point - 1)

        # a, b = pmx(p1_mutable_genes, p2_mutable_genes, first_cross_point, second_cross_point)
        cross1, cross2 = pmx(
            list(p1_crossable_genes),
            list(p2_crossable_genes),
            first_cross_point,
            second_cross_point,
        )

        crossed_parts_1.extend(cross1)
        crossed_parts_2.extend(cross2)

    # These are actually the new children, but by not re-assigning them we should improve performance
    parent1[mask] = crossed_parts_1
    parent2[mask] = crossed_parts_2
    return parent1, parent2


def breed_swap_rows(p1: Puzzle, p2: Puzzle, mask):
    parent1 = p1.copy()
    parent2 = p2.copy()
    randy = random.randint(0, 7)
    temp_par1_row = parent1[randy]
    parent1[randy] = parent2[randy + 1]
    parent2[randy + 1] = temp_par1_row
    return parent1, parent2


def mutate(genes: Puzzle, mask):
    """
    Swaps 2 places on a random row. Happens only on the changeable places
    """
    # mask == like selecting pandas dataframe rows on a condition
    # Select a random row of the sudoku
    random_row = np.random.choice(len(mask))
    mutable_genes = genes[random_row, mask[random_row]]
    # Generate 2 random numbers(duplicates wont be chosen with replace=False) to do the swap on
    gene_1_idx, gene_2_idx = np.random.choice(len(mutable_genes), size=2, replace=False)

    # Swap two elements with eachother
    temp = mutable_genes[gene_1_idx]
    mutable_genes[gene_1_idx] = mutable_genes[gene_2_idx]
    mutable_genes[gene_2_idx] = temp
    # Place back the new changed row into the puzzle
    genes[random_row, mask[random_row]] = mutable_genes
    return genes


def ga(
    puzzle: Puzzle,
    n_parents=200,
    n_generations=100,
    divisor=2,
    mutation_rate=0.01,
    selection_ratio=0.25,
):
    print(f"Running ga with: {n_parents=} {n_generations=} {divisor=} {mutation_rate=}")
    solutions = generate_solutions(puzzle, n_parents)
    mask = puzzle == 0
    prev_best_fitness = 99999

    fitness = Fitness(puzzle)
    solutions, fitnesses = fitness.check(solutions)
    print("Start, best fitness:", fitnesses[0])

    for generation in range(
        n_generations
    ):  # This should be termination condition ie. when puzzle is solved
        if fitnesses[0] == 0:
            print("Sudoku solved in generation:", generation)
            break

        if generation % 800 == 0:
            current_best_fitness = fitnesses[0]
            if (prev_best_fitness - current_best_fitness) == 0:
                print("No improvement in last 800 generations, restarting population")
                solutions = generate_solutions(puzzle, n_parents)
                solutions, fitnesses = fitness.check(solutions)
                current_best_fitness = fitnesses[0]
            prev_best_fitness = current_best_fitness

        # Select only the best solutions to evolve with ### Holy crap this was a winner move!
        solutions = solutions[0 : int(selection_ratio * len(solutions))]
        next_gen = []
        weights = []
        total = 0
        for i in range(divisor, len(solutions) + divisor):
            total += 1 / i
            weights.append((1 / i))

        for i in range(0, n_parents, 2):
            parent1_idx = random.choices(range(len(solutions)), weights=weights)[0]
            parent1 = solutions[parent1_idx]
            parent2_idx = random.choices(range(len(solutions)), weights=weights)[0]
            parent2 = solutions[parent2_idx]

            child1, child2 = breed_pmx(parent1, parent2, mask)

            if np.random.rand() < mutation_rate:
                child1 = mutate(child1, mask)

            if np.random.rand() < mutation_rate:
                child2 = mutate(child2, mask)

            next_gen.append(child1)
            next_gen.append(child2)
        next_gen, next_gen_fitnesses = fitness.check(next_gen)
        solutions = next_gen
        fitnesses = next_gen_fitnesses
        if generation % 100 == 0:
            print("Gen", generation, "Best fitness=", fitnesses[0])

    print("Finished, best fitnesses:", fitnesses[:50])


import time

t0 = time.time()
ga(
    puzzle=puz,
    n_parents=3000,
    n_generations=10000,
    divisor=2,
    mutation_rate=0.1,
    selection_ratio=0.25,
)
t1 = time.time()
print("Finished in ", round(t1 - t0, 2))
