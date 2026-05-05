def sum_of_nested_lists(n=[1,2,[3,4],[5,6]]):
    total = 0
    for e in n:
        if type(e) == list:
            total += sum_of_nested_lists(e)
        else:
            total += e

    return total

def sum_of_list(n=[1,2,3,4]):
    total = 0
    for e in n:total +=e
    return total

def factorial(n=5):
    if n == 1:return 1
    return n*factorial(n-1)

def harmonic_series(n=3):
    if n <2:return 1
    return (1/n) + harmonic_series(n-1)

def hcf(a=12,b=14):
    l,h = min(a,b),max(a,b)
    if l == 0:return h
    if l == 1:return 1
    return hcf(l, h%l)

print(sum_of_nested_lists())
print(sum_of_list())
print(factorial())
print(harmonic_series())
print(hcf())