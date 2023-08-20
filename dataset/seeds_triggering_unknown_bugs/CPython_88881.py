import select

def test_select_mutated():

    a = []

    class F:

        def fileno(SelectTestCase):
            del a[-1]
            return sys.__stdout__.fileno()
    a[:] = [F()] * 10
    select.select([], a, []), ([], a[:5], [])


test_select_mutated()