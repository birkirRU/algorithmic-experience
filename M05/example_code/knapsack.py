import pulp

problem = pulp.LpProblem("Knapsack", pulp.LpMaximize)

weight_limit, n = map(int, input().split())
values = []
weights = []
for i in range(n):
    value, weight = map(int, input().split())
    values.append(value)
    weights.append(weight)

# Create variables representing whether each item is taken or skipped
x = pulp.LpVariable.dicts("x", range(n), cat="Binary")

# Our objective is to maximize the value of the items taken
# Multiplying with a binary value is a nice way of getting
# 0 for each skipped item and the value of the item for each taken items
problem.setObjective(sum(values[i] * x[i] for i in range(n)))

# We must constrain how much is taken. Here we want to limit
# the total weight of the taken items in a similar way as above.
problem += sum(weights[i] * x[i] for i in range(n)) <= weight_limit


problem.solve(pulp.PULP_CBC_CMD(msg=False))
print(int(pulp.value(problem.objective)))
