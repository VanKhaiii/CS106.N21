from ortools.algorithms import pywrapknapsack_solver
import random
from itertools import islice
import testcasePrepocessing as TCP
import time

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

TIME_LIMIT = 120

def ggorTool(n,capacities,weights,values):
    solver = pywrapknapsack_solver.KnapsackSolver(
      pywrapknapsack_solver.KnapsackSolver.
      KNAPSACK_MULTIDIMENSION_BRANCH_AND_BOUND_SOLVER, 'KnapsackExample')

    solver.Init(values, weights, capacities)
    solver.set_time_limit(120.0)
    computed_value = solver.Solve()

    total_weight = 0
    for i in range(len(values)):
        if solver.BestSolutionContains(i):
            total_weight += weights[0][i]
    return [computed_value,total_weight]
    

def solve(name):
    fin = open(name)
    lines=fin.read().splitlines()
    
    n=int(lines[1])
    capacities=[]
    values=[]
    weights=[]
    tmp=[]
    total_cap=int(lines[2])
    total_weight=0
    #Mathematical observation
    for line in islice(lines, 4, None):
        data = line.split()
        values.append(int(data[0]))
        tmp.append(int(data[1]))
        total_weight=total_weight+int(data[1])
    weights.append(tmp)
    total_cap=min(total_cap,total_weight)
    capacities.append(total_cap)
    return  ggorTool(n,capacities,weights,values)


def solve_ggorTool():

    TestCases = TCP.Get_All_TestCases()
    file_test_path='.\\Dataset\\kplib-master\\'
    data=[]
    
    for name in TestCases:
        file_name=file_test_path+name
        print('GG Or Tool: ',file_name)
        start=time.time()
        optimal_answer= solve(file_name)
        end=time.time()
        print('Done.')
        tmp=[]
        for e in name:
            if(e=='\\'):
                tmp.append('_')
            else:
                tmp.append(e)
        data.append([optimal_answer[0],optimal_answer[1],'TRUE' if(end-start < TIME_LIMIT) else 'FALSE'])
    return data