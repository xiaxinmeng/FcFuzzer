import weakref

class Object:
    def __init__(self, arg):
        self.arg = arg

def test_set_callback_attribute():
    x = Object(1)
    callback = lambda ref: None
    ref1 = weakref.ref(x, callback)
    with ReferencesTestCase.assertRaises(AttributeError):
        ref1.__callback__ = lambda ref: None


test_set_callback_attribute()
