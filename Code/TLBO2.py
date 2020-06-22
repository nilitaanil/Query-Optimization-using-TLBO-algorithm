import cost_calc2
import math
from random import *
import numpy as np
from tabulate import tabulate

QP = cost_calc2.queryPlan
costs = cost_calc2.costDict

# Step 1: Fix the population size
population_size = len(costs)
print("population size=", population_size)

# Step 2: Fix the maximum number of iterations which is the termination criteria
max_iteration = 20

# solution for each generation and the fitness value of solution
costs_array = []
fitness_array = []
for i in range(population_size):
    # converting cost dictionary to array
    costs_array.append(costs[i + 1])
decision_var = len(np.array(costs_array)[1, :])


# Step 3: Find out the fitness value for each member in the population
def fitness_func(member):
    result = 0
    for m in range(len(member)):
        result += math.pow(member[m], 2)
    return result


# Step 4: selecting the best learner or teacher from the population based on minimum fitness value
def sel_teacher():
    print("fitness value of each cost row= ", np.apply_along_axis(fitness_func, 1, costs_array))
    global fitness_array
    fitness_array = np.apply_along_axis(fitness_func, 1, costs_array)
    pos_teacher = np.where(fitness_array == np.amin(fitness_array))[0][0]
    print("position of teacher = ", pos_teacher)
    return pos_teacher


# Step 5: determine mean of each cost of the population
def mean_column_costs():
    means = np.array(costs_array).mean(axis=0)
    return means


# Step 6: Generation of new solution - Teacher phase of each student
def gen_new_soln():
    global costs_array
    global fitness_array
    X_best = np.array(costs_array[sel_teacher()])
    X_mean = mean_column_costs()

    Tf = round(random()) + 1  # Tf same for all variables of a solution
    for k in range(population_size):
        X = costs_array[k]
        r = np.random.rand(decision_var)  # r to be calculated for each variable in the solution
        X_new = X + r * (X_best - (Tf * X_mean))

        # Step 7: Before calculating fitness value for x_new, checking whether values in x_new are in between the lb
        # and ub condition of the fitness func
        X_new[(X_new < -5.12)] = -5.12
        X_new[(X_new > 5.12)] = 5.12
        # Step 8: Calculating the fitness value of the bounded solution
        fitness_x_new = fitness_func(X_new)
        # Step 9: Perform greedy selection to update the population
        fitness_teacher = fitness_func(X_best)
        if fitness_x_new < fitness_teacher:  # X_new is the best solution
            costs_array[k] = X_new
            fitness_array[k] = fitness_x_new

        # Learners Phase
        xl = np.array(costs_array[k])
        while True:
            y = np.random.randint(population_size)
            if k != y: break
        partner = costs_array[y]
        fitness_partner = fitness_func(partner)
        rl = np.random.rand(decision_var)
        if fitness_array[k] < fitness_partner:
            Xlnew = xl + rl * (xl - partner)
        else:
            Xlnew = xl - rl * (xl - partner)
        Xlnew[(Xlnew < -5.12)] = -5.12
        Xlnew[(Xlnew > 5.12)] = 5.12
        fitness_learner = fitness_func(Xlnew)
        if fitness_learner < fitness_array[k]:
            costs_array[k] = Xlnew
            fitness_array[k] = fitness_learner


def selection_sort(x):
    for i in range(len(x)):
        swap = i + np.argmin(x[i:])
        (x[i], x[swap]) = (x[swap], x[i])
    return x


def pos_sorted_index(fitness_array_before, fitness_array_after):
    pos = []
    for items in fitness_array_after:
        pos.append(np.where(fitness_array_before == items)[0][0])
    return pos


for iteration in range(max_iteration):
    gen_new_soln()
fitness_array_before = np.array(fitness_array)
print("fitness array before sorting =", fitness_array_before)
fitness_array_after = selection_sort(fitness_array)
print("fitness array after sorting =", fitness_array_after)
sorted_index = pos_sorted_index(fitness_array_before, fitness_array_after)
print ("sorted indices = ", sorted_index)

table = []
for i in range(population_size):
    table.append([i + 1, sorted_index[i] + 1, fitness_array[i]])
print(tabulate(table, headers=["Rank", "QEP No.", "Fitness Value"]))
