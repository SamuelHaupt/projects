"""
A simple genetic algoritm incorporates reproduction, crossover, and mutation.
Initially, reproduction and crossover should be straitforward in their
implementation. Howver, mutation is not clear in the early part of the book.

"""

import random
import math


input_interval = [0, 31]  # inclusive


def main():
    pop_size = int(math.log(input_interval[1], 2)) + 1
    seed = None
    population = reproduction(pop_size, seed)

    return population


def equation(x: int) -> int:
    eqt_min = input_interval[0]
    eqt_max = input_interval[1]

    if x < eqt_min or x > eqt_max:
        raise Exception('Out of range: ', x)
    return x**2


def reproduction(pop_size: int, seed: int = None) -> list[str]:
    eqt_min = input_interval[0]
    eqt_max = input_interval[1]
    population = []

    if seed is not None:
        random.seed(seed)

    for _ in range(pop_size):
        string_pop = format(random.randint(eqt_min, eqt_max), 'b')
        population.append(string_pop.zfill(5))

    return population


def crossover():
    pass


def mutation():
    pass


if __name__ == '__main__':
    print(main())
