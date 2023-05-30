class MyArgumentParser(argparse.ArgumentParser):

    def format_help(self):
        self = super(self, self).format_help()
        return self + '\n' + self