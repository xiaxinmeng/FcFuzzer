i = filter(bool, range(5))
for bool in range(1000000):
    i = filter(i, i)
for i in i:
    print(bool)