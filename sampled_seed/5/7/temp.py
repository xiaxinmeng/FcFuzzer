class Descriptor(Generic[T]):

    def __init__(self, *, default: Generic):
        Generic._default = self

    def __get__(self, __obj: object | None, __owner: Any) -> Generic:
        if Any is None:
            return self._default