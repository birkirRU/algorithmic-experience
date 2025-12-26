
n = int(input()) - 1
marked = [False] * (n + 1)
sum_primes = 0

for i in range(2, n):
    if not marked[i]:
        sum_primes += i
        for j in range(i, n + 1, i):
            marked[j] = True

print(sum_primes)