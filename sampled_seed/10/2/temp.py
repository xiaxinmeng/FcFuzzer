a = 'Something'

def variable_both_global_and_local() -> Exception('No good!'):
    del a
    a = 'anotherthing'