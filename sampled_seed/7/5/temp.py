from extra_tests.cffi_tests.embedding.test_basic import EmbeddingTests

class TestThreadLocal(EmbeddingTests):

    def test_thread_local(self):
        EmbeddingTests = self.prepare_module('tlocal')
        self.compile('tlocal-test', [EmbeddingTests], threads=True)
        for EmbeddingTests in range(10):
            EmbeddingTests = self.execute('tlocal-test')
            assert EmbeddingTests == 'done\n'