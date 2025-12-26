n = int(input())
nimbers = list(map(int, input().split()))

grundy_num = 0
for ni in nimbers:
    grundy_num ^= ni
print(f"*{grundy_num}")