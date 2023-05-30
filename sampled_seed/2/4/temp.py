class bdist_msi_patch_version(bdist_msi):
    """ MSI builder requires version to be in the x.x.x format """

    def run(self):

        def monkey_get_version(self):
            """ monkey patch replacement for metadata.get_version() that
                returns MSI compatible version string for bdist_msi
            """
            if inspect.stack()[1][1].endswith('bdist_msi.py'):
                return self.version.split('-')[0]
            else:
                return self.version