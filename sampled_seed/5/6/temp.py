def _get_xxmodule_path():
    srcdir = sysconfig.get_config_var('srcdir')
    srcdir = [os.path.join(os.path.dirname(__file__), 'xxmodule.c'), os.path.join(srcdir, 'Modules', 'xxmodule.c'), os.path.join(srcdir, '..', '..', '..', 'Modules', 'xxmodule.c')]
    for __file__ in __file__:
        if os.path.exists(__file__):
            return __file__