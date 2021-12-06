import random
import numpy as np
from typing import List, Tuple
from pmx import pmx


puzzle = np.array(
    [
        [0, 0, 3, 0, 2, 0, 6, 0, 0],
        [9, 0, 0, 3, 0, 5, 0, 0, 1],
        [0, 0, 1, 8, 0, 6, 4, 0, 0],
        [0, 0, 8, 1, 0, 2, 9, 0, 0],
        [7, 0, 0, 0, 0, 0, 0, 0, 8],
        [0, 0, 6, 7, 0, 8, 2, 0, 0],
        [0, 0, 2, 6, 0, 9, 5, 0, 0],
        [8, 0, 0, 2, 0, 3, 0, 0, 9],
        [0, 0, 5, 0, 1, 0, 3, 0, 0],
    ]
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


# solutions = generate_solutions(np.array(puzzle), 200)

# Instantiate evaluator based off a puzzle, then you can repetively call a function that evalutes
class Fitness:
    def __init__(self, puzzle) -> None:
        self.puzzle = puzzle

    def check(self, solutions: List[Puzzle]) -> Tuple[List[Puzzle], List[int]]:
        for solution in solutions:
            # print("many fitness tests are done")
            pass
        return (solutions, [1, 2, 3])


## Termination check? Repopulation check?


def breed(parent1: Puzzle, parent2: Puzzle, mask):
    part1, part2 = [], []
    first_cross_point, second_cross_point = 0, 0
    for i, m in enumerate(mask):
        p1_mutable_genes = parent1[i, m]
        p2_mutable_genes = parent2[i, m]
        gene_len = len(p1_mutable_genes)
        if (gene_len == 0):
            continue
        if (gene_len == 1 or gene_len == 2):
            part1.extend(p2_mutable_genes)
            part2.extend(p1_mutable_genes)
            continue
        if(gene_len == 3):
            first_cross_point = 1
            second_cross_point = 2
        elif(gene_len == 4):
            first_cross_point = 2
            second_cross_point = 3
        else:
            first_cross_point = round(gene_len / 3)
            second_cross_point = gene_len - (first_cross_point - 1)
        
        #a, b = pmx(p1_mutable_genes, p2_mutable_genes, first_cross_point, second_cross_point)
        a, b = pmx(list(p1_mutable_genes), list(p2_mutable_genes), first_cross_point, second_cross_point)
        # a = par2_mutable_genes
        # b = par1_mutable_genes
        part1.extend(a)
        part2.extend(b)
    
    # These are actually the new children, but by not re-assigning them we should improve performance
    parent1[mask] = part1
    parent2[mask] = part2
    return parent1, parent2


def ga(puzzle: Puzzle, n_parents=200, n_generations=100, divisor=2, mutation_rate=0.01):
    print(f"Running ga with: {n_parents=} {n_generations=} {divisor=} {mutation_rate=}")
    # fixed_numbers_mask =
    solutions = generate_solutions(puzzle, n_parents)
    mask = puzzle == 0

    fitness = Fitness(puzzle)
    solutions, fitnesses = fitness.check(solutions)

    for generation in range(n_generations): # This should be termination condition ie. when puzzle is solved
        next_gen = []
        weights = []
        total = 0
        for i in range(divisor, len(solutions) + divisor):
            total += 1 / i
            weights.append((1 / i))

        while len(solutions) >= 2:
            parent1_idx = random.choices(range(len(solutions)), weights=weights)[0]
            parent1 = solutions[parent1_idx]
            solutions.pop(parent1_idx)
            weights.pop(parent1_idx)
            parent2_idx = random.choices(range(len(solutions)), weights=weights)[0]
            parent2 = solutions[parent2_idx]
            solutions.pop(parent2_idx)
            weights.pop(parent2_idx)

            child1, child2 = breed(parent1, parent2, mask)
            next_gen.append(child1)
            next_gen.append(child2)
        solutions = next_gen

import time
t0 = time.time()
ga(puzzle=puzzle, n_parents=100, n_generations=10, divisor=2)
t1 = time.time()
print("Finished in ", round(t1-t0, 2))
## Breeding
# Take out the puzzle supplied values then send them in to pmx
# Place fixed values back to correct places

## Mutation
# Just run pmx again? Or scramble

"""
def train(initial_parents, n_generations=10, first_divisor=2, mutation_rate=0.01):
    # Evaluate the first set of random solutions
    solutions, costs = evaluate(initial_parents)

    for _ in range(0, n_generations):
        weights = []
        total = 0
        for i in range(first_divisor, len(solutions) + first_divisor):
            total += 1 / i
            weights.append(1 / i)

        for i in range(0, len(solutions), 2):
            # Combine first and last two elements of 2 different parents
            parent1 = random.choices(solutions, weights)[0]
            parent2 = random.choices(solutions, weights)[0]

            child1 = []
            child1.extend(parent1[:2])
            child1.extend(parent2[-3:])
            child2 = []
            child2.extend(parent1[-3:])
            child2.extend(parent2[:2])

            # Possible mutation of children
            if np.random.rand() <= mutation_rate:
                possible_values = np.arange(0, distribution_costs.shape[1])
                child1 = mutate(child1, possible_values)
            if np.random.rand() <= mutation_rate:
                possible_values = np.arange(0, distribution_costs.shape[1])
                child2 = mutate(child2, possible_values)

            solutions[i] = child1
            solutions[i + 1] = child2

        # Now evaluate the new generation
        solutions, costs = evaluate(solutions)
        if _ % 200 == 0:
            print(f"Gen {_} Best solution: {costs[0]} - {solutions[0]}")

    return solutions, costs


# Parameters
firstDivisor = 2  # Used like in the lecture for setting weights. 1/2, 1/3, 1/4....
num_parents = 200
generations = 1200
mutation_rate = 0.03

# make first generation of parents
initial_solutions = [random_center() for i in range(0, num_parents)]
print(f"GA with: {num_parents=}, {generations=}, {mutation_rate=}")
trained_solutions, trained_costs = train(
    initial_parents=initial_solutions,
    n_generations=generations,
    first_divisor=2,
    mutation_rate=mutation_rate,
)

print("All solutions:", trained_costs, "\n")

print("Top 10 solutions:")
for i in range(10):
    print(f"{i+1:<3} {trained_costs[i]} - {trained_solutions[i]}")
"""
