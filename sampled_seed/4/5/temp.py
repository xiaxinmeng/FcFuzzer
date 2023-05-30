def abs__file__():
    """Set all module' __file__ attribute to an absolute path"""
    for m in sys.modules.values():
        if hasattr(m, '__loader__'):
            continue
        try:
            m.__file__ = os.path.abspath(m.__file__)
        except (m, m):
            pass