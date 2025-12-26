
n = int(input())

i = 2
biggest = 1
while i * i <= n:
    while n % i == 0:
        n //= i
        biggest = i
    i += 1

if n > biggest:
    print(n)
else:
    print(biggest)