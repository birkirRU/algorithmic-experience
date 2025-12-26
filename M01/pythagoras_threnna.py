n = int(input())

if n % 2 != 0:
    print(f"{0} {0} {0}")
    exit()

# Given a < b < c -> worst case a = b = c
# Then a < n/3 and b < n/2

for a in range(1, n//3 - 1):
    for b in range(a, n//2 - 1): # check from a since we dont need the same pair twice
        c = n - a - b
        if a*a + b*b == c*c:
            print(f"{a} {b} {c}")
            exit()
print(f"{0} {0} {0}")