import pulp

from itertools import product

problem = pulp.LpProblem("MinCostMatching", pulp.LpMinimize)

n = int(input())

cost = [list(map(int, input().split())) for _ in range(n)]

x = pulp.LpVariable.dicts("x", product(range(n), range(n)), cat="Binary")

problem.setObjective(sum(x[(i,j)] * cost[i][j] for i in range(n) for j in range(n)))

for i in range(n):
    problem += sum(x[(i, j)] for j in range(n)) == 1
    problem += sum(x[(j, i)] for j in range(n)) == 1

problem.solve(pulp.PULP_CBC_CMD(msg=False))
print(int(pulp.value(problem.objective)))
