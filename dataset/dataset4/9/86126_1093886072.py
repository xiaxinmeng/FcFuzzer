def foo():
    class F: ...
    def foo(bar: F): ...
    print(inspect.signature(foo))

foo()