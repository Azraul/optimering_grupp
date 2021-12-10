import random
import numpy as np
from typing import List, Tuple
from pmx import pmx
from sudokus.samples.samples import sudokus

# Just a custom type def for the puzzle
Puzzle = np.ndarray  # List[List[int]]

# List of sudokus from our samples
sudokus = sudokus()

## Generate random solutions based on a given starting-set puzzle
def generate_solutions(puzzle: Puzzle, n: int) -> List[Puzzle]:
    solutions = []
    size = puzzle.shape[0] + 1
    for i in range(n):
        temp_puzzle = puzzle.copy()
        for row in temp_puzzle:
            if 0 in row:
                # Generate all numbers that don't exist
                nums = [v for v in range(1, size) if v not in row]
                random.shuffle(nums)
                # Place them into the places that dont contain the fixed numbers
                row[row[:] == 0] = nums

        solutions.append(temp_puzzle)

    return solutions


# Instantiate evaluator based off a puzzle, then you can repetively call a function that evalutes
class Fitness:
    def __init__(self, puzzle) -> None:
        self.puzzle = puzzle

    def consistent(self, solution) -> int:
        """Check how many different elements there are in each row.
        Returns the sum of the number of duplicates"""
        return sum([len(solution) - len(set(row)) for row in solution])

    def check(self, solutions: List[Puzzle]):
        """
        Counts the number of conflicts in a puzzle.
        Returns puzzles sorted by their score
        """
        scored = []
        for solution in solutions:
            s = 0
            # Checks along columns. Rows don't get checked because how solutions are generated
            s += self.consistent(np.rot90(solution, 1))
            # Checks how many duplicates in each cell
            s += self.consistent(
                [
                    solution[i : i + 3, j : j + 3].flatten()
                    for i in range(0, 9, 3)
                    for j in range(0, 9, 3)
                ]
            )
            scored.append([solution, s])
        scored = np.array(sorted(scored, key=lambda pair: pair[1]), dtype=object)
        return list(scored[:, 0]), list(scored[:, 1])


def breed_pmx(p1: Puzzle, p2: Puzzle, mask):
    """
    Combines two puzzles using partially mapped crossover method
    """
    parent1 = p1.copy()
    parent2 = p2.copy()
    crossed_parts_1, crossed_parts_2 = [], []
    first_cross_point, second_cross_point = 0, 0

    # Loops through puzzle row-wise. m = one row of the mask
    for i, m in enumerate(mask):
        # Selects only the elements that are not given by the puzzle.
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
    # Swaps just a row between two parents
    # This function isn't used unless replaced with pmx down in the main function
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
    print(puzzle)
    print(
        f"Running ga with: {n_parents=} {n_generations=} {divisor=} {mutation_rate=} {selection_ratio=}"
    )
    # Generate random candidates based on the given sudoku
    solutions = generate_solutions(puzzle, n_parents)
    mask = puzzle == 0  # A numpy mask. Used for selecting elements like in pandas dataframes
    prev_best_fitness = 99999

    # Fitness evaluator instance
    fitness = Fitness(puzzle)
    # Evaluates and ranks the solutions
    solutions, fitnesses = fitness.check(solutions)
    print("Start, best fitness:", fitnesses[0])

    for generation in range(n_generations):

        # Termination condition if the puzzle is solved
        if fitnesses[0] == 0:
            print("Sudoku solved in generation:", generation)
            break

        # Generate a new population if no improvement has been made in 800 generations
        if generation % 500 == 0:
            current_best_fitness = fitnesses[0]
            if (prev_best_fitness - current_best_fitness) == 0:
                print("No improvement in last 500 generations, restarting population")
                solutions = generate_solutions(puzzle, n_parents)
                solutions, fitnesses = fitness.check(solutions)
                current_best_fitness = fitnesses[0]
            prev_best_fitness = current_best_fitness

        # Select only the best n solutions to evolve with
        solutions = solutions[0 : int(selection_ratio * len(solutions))]
        next_gen = []
        weights = []
        total = 0
        # Generate weights based on the new selected population.
        # The best one gets 1/2, 2nd 1/3, 3rd 1/4th weight etc.
        for i in range(divisor, len(solutions) + divisor):
            total += 1 / i
            weights.append((1 / i))

        # Create n_parents new children
        for i in range(0, n_parents, 2):
            parent1_idx = random.choice(range(len(solutions)))
            #parent1_idx = random.choices(range(len(solutions)), weights=weights)[0] # weighted version
            parent1 = solutions[parent1_idx]
            parent2_idx = random.choice(range(len(solutions)))
            #parent2_idx = random.choices(range(len(solutions)), weights=weights)[0] # weighted version
            parent2 = solutions[parent2_idx]

            child1, child2 = breed_pmx(parent1, parent2, mask)
            #child1, child2 = breed_swap_rows(parent1, parent2, mask)

            # Chance for the children to mutate.
            # Swaps two elements in a row
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

    print("Finished, best fitnesses:", fitnesses[:10])
    print("Best solution:\n", solutions[0])


""" Run GA """
import time

puzzle = np.array(sudokus["easy"][0])
t0 = time.time()
ga(
    puzzle=puzzle,
    n_parents=6000,
    n_generations=10000,
    divisor=2,
    mutation_rate=0.1,
    selection_ratio=0.25,
)
t1 = time.time()
print("Finished in ", round(t1 - t0, 2))
