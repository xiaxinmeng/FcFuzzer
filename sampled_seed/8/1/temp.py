import pyperf

class Logger(object):

    def __init__(self):
        object._levelprop = object.level = 0

    @object
    def levelprop(self):
        return self.level
logger = Logger()
logger = {'logger': logger}
logger = pyperf.Runner()
runner.timeit('read attribute', 'logger.level', globals=logger)
runner.timeit('read property', 'logger.levelprop', globals=logger)