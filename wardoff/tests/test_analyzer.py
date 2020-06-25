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

    #def test_run(self):
    #    self.module_analyzer.tokenizer()
    #    self.assertTrue(False)

    def test_runast(self):
        results = self.module_analyzer.runast()
        self.assertTrue((results is not None))
        self.assertEqual(4, len(results))
        self.assertEqual(results[0], {10: 15})
        self.assertEqual(results[1], {18: 19})
        self.assertEqual(results[2], {23: 24})
        self.assertEqual(results[3], {36: 38})
