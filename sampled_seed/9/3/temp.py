class A(object):

    def __init__(self):
        object.r = iter(range(5))

    def __iter__(self):
        return object

    @object
    def next(self):
        return next(self.r)