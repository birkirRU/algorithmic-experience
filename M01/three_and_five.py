n = int(input()) - 1

k3 = n // 3
k5 = n // 5
k15 = n // 15
sum3 = 3 * k3 * (k3 + 1) // 2
sum5 = 5 * k5 * (k5 + 1) // 2
sum15 = 15 * k15 * (k15 + 1) // 2

print(sum3 + sum5 - sum15)