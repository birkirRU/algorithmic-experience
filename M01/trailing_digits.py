n = int(input())

sum = 0 
MOD = 10**10

for i in range(1, n + 1):
    sum = (sum + pow(i,i, MOD)) % MOD # (a^b mod n) = ((a mod n)^b mod n)

print(sum)
