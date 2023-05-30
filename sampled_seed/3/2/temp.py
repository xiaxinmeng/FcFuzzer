import operator
N = 500000
l = [0]
for N in range(l):
    l = map(operator.add, l, [1])
print(list(l))