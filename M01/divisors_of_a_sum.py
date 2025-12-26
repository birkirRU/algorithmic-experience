
n = int(input())

n_smaller = n
n_larger = n + 1

prime_count = {}

num_positive_divisors = 1

i = 2
biggest = 1
while i * i <= n_smaller:
    exponent = 0
    while n_smaller % i == 0:
        n_smaller //= i
        exponent += 1
    if exponent > 0:
        if prime_count.get(f"{i}") is None:
            prime_count[f"{i}"] = exponent
        else:
            prime_count[f"{i}"] += exponent
    i += 1


if n_smaller > 1:
    if prime_count.get(f"{n_smaller}") is None:
        prime_count[f"{n_smaller}"] = 1
    else:
        prime_count[f"{n_smaller}"] += 1


i = 2
while i * i <= n_larger:
    exponent = 0
    while n_larger % i == 0:
        n_larger //= i
        exponent += 1
    if exponent > 0:
        if prime_count.get(f"{i}") is None:
            prime_count[f"{i}"] = exponent
        else:
            prime_count[f"{i}"] += exponent
    i += 1

if n_larger > 1:
    if prime_count.get(f"{n_larger}") is None:
        prime_count[f"{n_larger}"] = 1
    else:
        prime_count[f"{n_larger}"] += 1

# Take one exponent of two 

prime_count["2"] -= 1

for key in prime_count:
    num_positive_divisors *= prime_count[key] + 1
print(num_positive_divisors)