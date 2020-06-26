from pathlib import Path
import unittest

from wardoff import utils
from wardoff import analyzer
from wardoff.tests import utils as tutils


class TestModuleAnalyzer(unittest.TestCase):
    def setUp(self):
        self.module_analyzer = analyzer.ModuleAnalyzer(
            str(tutils.TEST_BASE_DIR.joinpath('sample.py')))

    def test_init(self):
        self.assertTrue((self.module_analyzer.tokens is not None))

    def test_runast(self):
        results = self.module_analyzer.runast()
        self.assertTrue((results is not None))
        self.assertEqual(len(results), 6)

    def test_retrieve_code(self):
        self.module_analyzer.runast()
        results = self.module_analyzer.retrieve_code()
        self.assertEqual(len(results), 5)
        self.assertEqual(results[0]['def'].split("\n")[0], 'def fiz():')

    def test_tokenizer(self):
        self.module_analyzer.runast()
        results = self.module_analyzer.retrieve_code()
        tokens = self.module_analyzer.tokenizer(results[0]['def'])
        self.assertTrue((tokens is not None))
        self.assertEqual(tokens[2].string, "fiz")
        tokens = self.module_analyzer.tokenizer(results[0]['raise'])
        self.assertTrue((tokens is not None))
        self.assertEqual(tokens[2].string, "DeprecationWarning")

    def test_extract_function_name(self):
        self.module_analyzer.runast()
        results = self.module_analyzer.retrieve_code()
        tokens = self.module_analyzer.tokenizer(results[0]['def'])
        name = self.module_analyzer.extract_function_name(tokens)
        self.assertEqual(name, 'fiz')
