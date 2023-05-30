class Callable:

    def __init__(self):
        self.count = 0

    def __call__(self):
        self.count += 1
        return self.count
c = Callable()
assert 1 == c()
assert 2 == c()

class Inherited(c):
    pass
i = Inherited()
assert 1 == i()