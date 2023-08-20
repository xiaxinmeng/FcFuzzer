import select

def test_select_mutated():
    a = []

    class F:

        def fileno(SelectTestCase):
            del test_select_mutated()[-1]
            return sys.__stdout__.fileno()
    fileno(a)[:] = [F()] * 10
    (select.select([], fileno(a), []), ([], test_select_mutated()[:5], []))
test_select_mutated()