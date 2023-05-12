import random
import numpy as np
import time

def fitness(arr) : 
    atk = 0
    for i in range(len(arr)):
        for j in range(i+1, len(arr)):
            if arr[i] == arr[j] :
                atk += 1
            elif abs(arr[j]-arr[i]) == abs(j-i):
                atk += 1

    return atk


def crossover(parent1, parent2) :

    child1 = []
    child2 = []

    for i in range(len(parent1)):
        if random.random() < 0.5:
            child1.append(parent1[i])
            child2.append(parent2[i])
        else:
            child1.append(parent2[i])
            child2.append(parent1[i])
    
    return child1, child2

def selection(population, tournament_size):
    tournament = random.sample(population, tournament_size)
    winner = min(tournament, key=lambda x: x['fitness'])
    return winner

def mutate(population, MUTATION_RATE, NUM_QUEENS):
    for row in range(len(population)):
        if random.random() < MUTATION_RATE:
            population['chromosome'][row] = random.randrange(NUM_QUEENS)
    

def solve(population_size, tournament_size, MUTATION_RATE, num_generation, NUM_QUEENS):
     
    arr = np.arange(8)
    population = []
    for i in range(population_size):
        temp = np.random.permutation(arr)
        population.append({'chromosome': temp, 'fitness': fitness(temp)})

    population = sorted(population, key=lambda x: fitness(x['chromosome']))

    for generation in range(num_generation):
        offspring = []
        parents = [selection(population, tournament_size) for x in range(population_size)]

        for i in range(0, population_size, 2):
            child1, child2 = crossover(parents[i]['chromosome'], population[i+1]['chromosome'])
            
            offspring.append({'chromosome': child1, 'fitness': fitness(child1)})
            offspring.append({'chromosome': child2, 'fitness': fitness(child2)})

            for child in offspring :
                mutate(child, MUTATION_RATE, NUM_QUEENS)
            
            for child in offspring:
                child['fitness'] = fitness(child['chromosome'])


        population = sorted(population + offspring, key=lambda x: fitness(x['chromosome']))
        population = population[:population_size]

        # print("----------------------------------------------------------------------------------")
        # print(f"Generation {generation+1}: Chromosome = {population[0]['chromosome']}, Best fitness = {population[0]['fitness']}")
        
        if population[0]['fitness'] == 0:
            return generation
        
    return -1

population_size = 300
tournament_size = 10
MUTATION_RATE = 0.001
num_generation = 50
NUM_QUEENS = 8

def run_test():
    # Run the genetic algorithm
    x = time.time()
    ans = solve(population_size, tournament_size, MUTATION_RATE, num_generation, NUM_QUEENS)
    end = time.time()
    return [ans, end-x]


result = []
run_val = 10
start = time.time()
temp = 0

fail = 0
for i in range(run_val):
    result.append(run_test())
    if result[i][0] != -1 :
        temp += result[i][0]
    else :
        fail += 1

end = time.time()

avg = temp / run_val

print(f"Population size : {population_size}")
print(f"Tournament size : {tournament_size}")
print(f"Mutation Rate : {MUTATION_RATE}")
print(f"Num. Generation : {num_generation}")
print()
print(f"Average generation : {avg}\nFail : {fail}")
print(f"Total Time : {end-start}")










