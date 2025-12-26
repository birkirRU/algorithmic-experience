
import math
import random

a, b, c, d = map(int, input().split())

# (a^2 + b^2) = p
# (c^2 + d^2) = q

# Two solutions of the multiplication p*q
# p*q = (a^2 + b^2)*(c^2 + d^2)
#     = (ac - bd)^2 + (ad + bc)^2 
#     = (ac + bd)^2 + (ad - bc)^2

p = a*a + b*b
q = c*c + d*d
pq = p*q

side1 = a*c-b*d
side2 = a*d+b*c

side3 = a*c+b*d
side4 = a*d-b*c

def fmt(x):
    return f"({x})" if x < 0 else f"{x}"

print(f"{fmt(side1)}^2 + {fmt(side2)}^2 = {pq}")
print(f"{fmt(side3)}^2 + {fmt(side4)}^2 = {pq}")