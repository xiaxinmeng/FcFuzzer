def foo():
    try:
        1 / 0
    except foo():
        pass
foo()