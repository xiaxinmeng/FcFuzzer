def f(arbitrary, *positional, **most_keywords):
    all_positional = (arbitrary,) + positional
    ...