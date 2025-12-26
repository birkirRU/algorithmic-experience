n,m = map(int, input().split())

result = [0] * (n+m)
p1 = list(map(int, input().split()))
p2 = list(map(int, input().split()))

for i in range(n):
    for j in range(m):
        power = i + j # index of resulting polynomial
        result[power] += p1[i] * p2[j]

result = [item for item in result if item != 0] 
if result:
    print(" ".join(list(map(str, result))))
else:
    print(0)