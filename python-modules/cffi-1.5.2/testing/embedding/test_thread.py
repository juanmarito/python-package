from testing.embedding.test_basic import EmbeddingTests


class TestThread(EmbeddingTests):
    def test_first_calls_in_parallel(self):
        add1_cffi = self.prepare_module('add1')
        self.compile('thread1-test', [add1_cffi], threads=True)
        for i in range(50):
            output = self.execute('thread1-test')
            assert output == ("starting\n"
                              "preparing...\n" +
                              "adding 40 and 2\n" * 10 +
                              "done\n")

    def _take_out(self, text, content):
        assert content in text
        i = text.index(content)
        return text[:i] + text[i+len(content):]

    def test_init_different_modules_in_different_threads(self):
        add1_cffi = self.prepare_module('add1')
        add2_cffi = self.prepare_module('add2')
        self.compile('thread2-test', [add1_cffi, add2_cffi], threads=True)
        output = self.execute('thread2-test')
        output = self._take_out(output, "preparing")
        output = self._take_out(output, ".")
        output = self._take_out(output, ".")
        # at least the 3rd dot should be after everything from ADD2
        assert output == ("starting\n"
                          "prepADD2\n"
                          "adding 1000 and 200 and 30\n"
                          ".\n"
                          "adding 40 and 2\n"
                          "done\n")

    def test_alt_issue(self):
        add1_cffi = self.prepare_module('add1')
        add2_cffi = self.prepare_module('add2')
        self.compile('thread2-test', [add1_cffi, add2_cffi],
                     threads=True, defines={'T2TEST_AGAIN_ADD1': '1'})
        output = self.execute('thread2-test')
        output = self._take_out(output, "adding 40 and 2\n")
        assert output == ("starting\n"
                          "preparing...\n"
                          "adding -1 and -1\n"
                          "prepADD2\n"
                          "adding 1000 and 200 and 30\n"
                          "done\n")

    def test_load_in_parallel_more(self):
        add2_cffi = self.prepare_module('add2')
        add3_cffi = self.prepare_module('add3')
        self.compile('thread3-test', [add2_cffi, add3_cffi], threads=True)
        for i in range(150):
            output = self.execute('thread3-test')
            for j in range(10):
                output = self._take_out(output, "adding 40 and 2 and 100\n")
                output = self._take_out(output, "adding 1000, 200, 30, 4\n")
            assert output == ("starting\n"
                              "prepADD2\n"
                              "done\n")
