from pathlib import Path
import unittest

from wardoff import argparser
from wardoff import PathAnalyzer
from wardoff import FileAnalyzer
from wardoff import RepoAnalyzer
from wardoff import PackageAnalyzer


BASE_PATH = Path(__file__).parent
REQUIREMENT_SAMPLE = BASE_PATH.joinpath(BASE_PATH,
    "..", "..", "test-requirements.txt")


class TestArguments(unittest.TestCase):
    def test_argparser(self):
        parser = argparser()
        # Current dir (implicit)
        parser.parse_args([])
        # Current dir (explicit)
        parser.parse_args(["."])
        # Specific file
        parser.parse_args([str(REQUIREMENT_SAMPLE)])
        # Specific package (hosted on pypi)
        parser.parse_args(["amqp"])
        # Specific repository (hosted on github)
        parser.parse_args(["https://github.com/openuado/niet"])

        with self.assertRaises(SystemExit):
            parser.parse_args([".", "--unknow", "boum"])

    def test_argparser_returned_project_analyzer(self):
        parser = argparser()
        # Current dir (implicit)
        args = parser.parse_args([])
        analyzer = args.project
        self.assertIsInstance(analyzer, PathAnalyzer)
        # Current dir (explicit)
        args = parser.parse_args(["."])
        analyzer = args.project
        self.assertIsInstance(analyzer, PathAnalyzer)
        # Specific file
        args = parser.parse_args([str(REQUIREMENT_SAMPLE)])
        analyzer = args.project
        self.assertIsInstance(analyzer, FileAnalyzer)
        # Specific package (hosted on pypi)
        args = parser.parse_args(["amqp"])
        analyzer = args.project
        self.assertIsInstance(analyzer, PackageAnalyzer)
        # Specific repository (hosted on github)
        args = parser.parse_args(["https://github.com/openuado/niet"])
        analyzer = args.project
        self.assertIsInstance(analyzer, RepoAnalyzer)
        # Specific repository (hosted on github)
        args = parser.parse_args(["git@github.com:openuado/niet"])
        analyzer = args.project
        self.assertIsInstance(analyzer, RepoAnalyzer)


class TestPathAnalyser(unittest.TestCase):
    def test_initialize(self):
        pass
