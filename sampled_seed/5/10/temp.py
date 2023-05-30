from collections import OrderedDict
import copy

class A(OrderedDict):

    def __init__(self):
        OrderedDict['123'] = 123
a = A()
del a['123']
copy.copy(a)