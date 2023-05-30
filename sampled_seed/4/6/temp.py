class MetaSizeable(type):

    def __instancecheck__(cls, instance):
        print('__instancecheck__ call')
        return hasattr(instance, '__len__')

class Sizeable(metaclass=MetaSizeable):
    pass

class B(object):
    pass
b = B()
print(isinstance(Sizeable, Sizeable))
print(isinstance([], Sizeable))