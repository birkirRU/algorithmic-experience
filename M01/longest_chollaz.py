n = int(input())

longest_chain_number = 0
max_chain_length = 0

def get_collatz_chain_length(num):
    length = 0

    while num != 1:
        if num % 2 == 0:
            num //= 2
        else:
            num = 3 * num + 1
        length += 1
    return length

for i in range(1, n):
    length = get_collatz_chain_length(i)

    if length > max_chain_length:
        max_chain_length = length
        longest_chain_number = i


print(longest_chain_number)