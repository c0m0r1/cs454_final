#!/usr/bin/env python3

import bs4
from coverage import fitness, get_coverage_info
from GP.html_mutator import mutate
from GP.html_crossover import crossover
from GP.html_seeder import generate_html_tree
import random
import string
import copy

def selection(population, population_fitness):
    s = 1.5

    population_fitness, population = zip(*sorted(zip(population_fitness, population)))

    population_len = len(population)
    sum_rank = int(population_len * (population_len - 1) / 2)
    
    # linear ranking
    prob_rank = [((2-s)/population_len) + (i * (s - 1) / sum_rank) for i in range(population_len)]
    
    acc_prob_rank = []
    acc_val = 0
    for p in prob_rank:
        acc_val += p
        acc_prob_rank.append(acc_val)

    mating_pool = []
    current_member = 0
    i = 0
    r = random.uniform(0, 0.5)
    while current_member < 2:
        while r <= acc_prob_rank[i]:
            r += 0.5
            mating_pool.append(population[i])
            current_member += 1
        i += 1
    return tuple(copy.copy(gene) for gene in mating_pool)


def html_gp(iter_cnt, population_size, mutation_rate, crossover_rate):
    population = []
    for _ in range(population_size):
        new_gene = generate_html_tree(5,5,2,2,5)
        population.append(new_gene)

    population_fitness = [fitness(gene) for gene in population]
    iter_cnt -= population_size

    generation_cnt = 0
    while iter_cnt >= population_size:
        print("[*] generation %d"%(generation_cnt))
        
        new_population = random.choices(population, k=int((1 - crossover_rate) * population_size))
        for _ in range(int(crossover_rate * population_size / 2)):
            t1, t2 = selection(population, population_fitness)
            new_population.extend(crossover(t1, t2))
        
        population = []
        for g in new_population:
            if random.random() < mutation_rate:
                g = mutate(g)
            population.append(g)  

        random.shuffle(population)

        population_fitness = [fitness(gene) for gene in population]
        iter_cnt -= population_size

        generation_cnt += 1
    
    population_fitness, population = zip(*sorted(zip(population_fitness, population)))

    return population_fitness[-1], population[-1]


if __name__=="__main__":
    result_fitness, result = html_gp(100, 10, 0.1, 0.8)
    print(result)
    print(result_fitness)
    print(get_coverage_info(result))


