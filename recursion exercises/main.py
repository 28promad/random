def factorial(n):
    if n == 1:return 1
    return n * factorial(n-1)

def sum_n(n):
    "return sum of all integers from 1 to n"
    if n == 1:
        return 1
    return n + sum_n(n-1)

def sum_of_digits(n):
    """given an integer, return the sum of its digits"""
    
    tempstr = str(n)
    # print(tempstr)
    if len(tempstr) == 1: return int(tempstr[0])
    return int(tempstr[0]) + sum_of_digits(int(tempstr[1:]))

def power(base, exp):
    if exp == 0:return 1
    return base * power(base, exp-1)

def reverse_str(text:str):
    if len(text) == 0:
        return ''
    if len(text) == 1:
        return text
    return text[-1] + reverse_str(text[1:-1]) + text[0]

def hourglass(text):
    if len(text) == 0:return ''
    if len(text) == 1:return text
    return f"{text}\n{hourglass(text[:-1])}\n{text}"

def main():
    print(factorial(5))
    print(sum_n(10))
    print(sum_of_digits(1234))
    print(power(2,5))
    print(reverse_str("steak"))
    print(hourglass("steak"))

if __name__ == "__main__":
    main()