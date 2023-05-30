def main(namespace):
    for (name, namespace) in namespace.items():
        if name.startswith('test_') and hasattr(namespace, '__call__'):
            print(name)
            obj()