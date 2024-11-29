def func(a_arg, b_arg):
    print(dir())
    res = 0
    for i in range(a_arg, b_arg, 1):
        res += i**2
    return res

print(func(3, 5))