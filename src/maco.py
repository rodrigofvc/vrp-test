from ant import Ant
from solution import Solution
import numpy as np
import copy

def initialize_multiple_matrix(days, n_costumers):
    matrices = {'AM': [], 'PM': []}
    for d in range(days):

        m = np.ones((n_costumers,n_costumers))
        matrices['AM'].append(m)

        m_ = np.ones((n_costumers,n_costumers))
        matrices['PM'].append(m_)
    return matrices

def get_costumers_day_timetable(costumers, timetable_day):
    timetable = -1
    if timetable_day == 'AM':
        timetable = 0
    elif timetable_day == 'PM':
        timetable = 1
    else:
        raise()
    costumers_dh = []
    for costumer in costumers[1:]:
        if costumer.timetable == timetable:
            costumers_dh.append(costumer)
    if len(costumers_dh) == 0:
        raise()
    return costumers_dh

def non_dominated(A, P):
    for p in P:
        dominated = False
        for a in A:
            if a.dominates(p):
                dominated = True
        if not dominated:
            A.append(p)

    for a in A:
        for p in P:
            if p.dominates(a):
                if a in A:
                    A.remove(a)

    return A

def ants_arc_ij(timetable, day, i, j, P, Q):
    delta_ijdh = 0
    for p in P:
        for vehicle in p.assigments_vehicles[timetable]:
            if vehicle.visited_costumer_ijdh(day, i, j):
                delta_ijdh += Q / vehicle.get_time(day)
    return delta_ijdh

def update_arc_ij(timetable, day, matrix_dh, i, j, rho, Q, P):
    matrix_dh = (1-rho) * matrix_dh[i][j] + ants_arc_ij(timetable, day, i, j, P, Q)

def update_pheromone(pheromone_matrix, P, rho, Q):
    timetables = pheromone_matrix.keys()
    for h in timetables:
        matrix_h = pheromone_matrix[h]
        for d, matrix_dh in enumerate(matrix_h):
            n = matrix_dh.shape[0]
            for i in range(n):
                for j in range(n):
                    if i != j:
                        update_arc_ij(h, d, matrix_dh, i, j, rho, Q, P)

def maco(n_ants, rho, days, alpha, beta, gamma, delta, Q, max_iterations, costumers, timetables, vehicles):
    n_costumers = len(costumers)
    pheromone_matrix = initialize_multiple_matrix(days, n_costumers)
    A = []
    for i in range(max_iterations):
        P = []
        for k in range(n_ants):
            s = Solution(timetables, days)
            for h in timetables:
                vehicles_timetable = copy.deepcopy(vehicles)
                costumers_h = get_costumers_day_timetable(costumers, h)
                costumers_timetable = copy.deepcopy(costumers_h)
                for d in range(days):
                    depot = costumers[0]
                    ant = Ant(depot)
                    ant.build_solution(pheromone_matrix, d, h, alpha, beta, gamma, delta, Q, costumers_timetable, vehicles_timetable)
                s.add_assigment_vehicles(vehicles_timetable, costumers_timetable, h)
            P.append(s)
        for a in A:
            print (a.get_fitness())
        #update_pheromone(pheromone_matrix, P, rho, Q)
        A = non_dominated(A, P)
