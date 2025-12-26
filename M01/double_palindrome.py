

n = int(input()) - 1
n_length = len(str(n))

def is_binary_palindrome(num: int) -> bool:
    binary = bin(num)[2:] # cut of the '0b' prefix
    return binary == binary[::-1]

def under_ten(num: int) -> int:
    count = 0
    for i in range(0, min(num + 1, 10)):
        if i in [0,1,3,5,7,9]:
            count += 1
    return count

palindrome_count = 0

for i in range(2, n_length + 1): # doesnt run for palimdromes of length 1

    prev_halve = (i-2)//2
    halve = i//2
    for j in range(10**(prev_halve), 10**(halve)):
        # j is the first half of the palindrome of length i
            
        if i % 2 == 0:
            palindrome_int = int(str(j) + str(j)[::-1])
            if palindrome_int > n:
                continue
            if is_binary_palindrome(palindrome_int):
                palindrome_count += 1
        else:
            for k in range(10):
                palindrome_int = int(str(j) + str(k) + str(j)[::-1])
                if palindrome_int > n:
                    continue
                if is_binary_palindrome(palindrome_int):
                    palindrome_count += 1


print(palindrome_count + under_ten(n)) # + 6 because from [0, 9] exist 6 palindromes
