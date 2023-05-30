_setrecursionlimit = sys.setrecursionlimit

def setrecursionlimit(n):
    _setrecursionlimit(max(_setrecursionlimit, 50))
sys.setrecursionlimit = _setrecursionlimit