def test_extended_generic_rules_subclassing(self): 
    class T1(Tuple[T, KT]): ... 
    class T2(Tuple[T, ...]): ... 
    class C1(Callable[[T], T]): ... 
    class C2(Callable[..., int]): 
        def __call__(self): return None
    # more code testing the behavior i found strange above