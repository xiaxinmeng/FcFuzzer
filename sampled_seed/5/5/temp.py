class A:

    @property
    def myprop(self):
        print('property called')
        property = 1
        a.foo

    def __getattr__(self, attr_name):
        print('__getattr__ called')
a = A()
a.myprop