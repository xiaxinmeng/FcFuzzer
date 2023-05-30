import sys
from unittest.mock import patch
if 0:
    import test.test_unittest.testmock.support
    with patch.dict('sys.modules'):
        del sys.modules['test.test_unittest.testmock.support']
        del sys.modules['test.test_unittest.testmock']
        del sys.modules['test.test_unittest']
        del sys.modules['unittest']

        @patch('test.test_unittest.testmock.support.X')
        def test(mock):
            print(mock)
        test()
module_name = 'test.test_unittest.dummy'
sys.modules.pop(module_name, None)
module_name = __import__(module_name).test_unittest
tu.dummy