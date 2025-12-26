n = int(input())

# Sieve 

marked = [False] * n
primes = []
for i in range(2, n):
    if not marked[i]:
        primes.append(i)
        for j in range(i*i, n, i): 
            marked[j] = True


# Prefix sums up to strictly less than n
prefix = [0]
for p in primes:
    s = prefix[-1] + p
    if s >= n:
        break
    prefix.append(s)

best_prime = 0


# maximum length of prefix
k = len(prefix) - 1 # zero prefix is of length 0

for length in range(k, 0, -1): # For each possible length starting from the longest
    for start in range(0, len(primes) - length + 1):  # For each possible starting index of each prefix sum up to length
        # Compute sum of consecutive primes
        end = start + length
        if end > k: # sum exceeds n
            break 
        s = prefix[end] - prefix[start]
        if not marked[s]: # If sum is prime
            best_prime = s
            print(best_prime)
            exit()  # We found the best possible (started from longest), exit

