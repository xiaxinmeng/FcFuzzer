def f():
    global TARGET
    TARGET = [(TARGET := VAR) for VAR in ITERABLE]