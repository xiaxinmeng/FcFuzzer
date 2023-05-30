class B:

    def __add__(self, other):
        if not isinstance(other, B):
            return other