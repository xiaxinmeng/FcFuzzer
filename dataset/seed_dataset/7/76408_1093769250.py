@singledispatch
def generic(arg): ...

@generic.register
def _(arg: str): ...

@generic.register
def _(arg: int): ...