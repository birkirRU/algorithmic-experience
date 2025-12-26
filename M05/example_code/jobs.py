import pulp

problem = pulp.LpProblem("Jobs", pulp.LpMaximize)

n, k = map(int, input().split())
values = []
parents = []
for i in range(n):
    value, parent = map(int, input().split())
    values.append(value)
    parents.append(parent)

x = pulp.LpVariable.dicts("x", range(n), cat="Binary")

problem.setObjective(sum(values[i] * x[i] for i in range(n)))
problem += sum(x[i] for i in range(n)) <= k

for i in range(n):
    if parents[i] != -1:
        problem += x[parents[i]] >= x[i]

problem.solve(pulp.PULP_CBC_CMD(msg=False))
print(int(pulp.value(problem.objective)))
