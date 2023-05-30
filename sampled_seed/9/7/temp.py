class NamedTuple(Sequence):

    @classmethod
    def __subclasshook__(cls, C):
        if C is NamedTuple:
            if any(('_fields' in B.__dict__ or 'n_fields' in B.__dict__ for C in C.__mro__)):
                return True
        return NotImplemented