import argparse
import sys
from pathlib import Path


class AnalyzerInitializationException(Exception):
    pass


class BaseAnalyzer():
    def __init__(self, project):
        self.project = project

    def analyze(self):
        self.requirements = self.retrieve_requirements()

    def retrieve_requirements(self):
        raise NotImplementedError("retrieve method not implemented")


class PathAnalyzer(BaseAnalyzer):
    def retrieve_requirements(self):
        requirements = []
        path = Path(self.project)
        requirements_files = list(path.glob('**/*requirements.txt'))
        for p in requirements_files:
            with p.open() as f:
                requirements.extend(f.readlines())
        return requirements


class FileAnalyzer(BaseAnalyzer):
    pass


class RepoAnalyzer(BaseAnalyzer):
    pass


class PackageAnalyzer(BaseAnalyzer):
    pass


class ProjectType:

    def __call__(self, string):
        try:
            if not string or string == '.':
                return PathAnalyzer('.')
            if Path(string).is_file():
                return FileAnalyzer(string)
            if Path(string).is_dir():
                return PathAnalyzer('.')
            if string.startswith('http') or string.startswith('git'):
                return RepoAnalyzer(string)
            # By default we consider the passed argument as a pypi project name
            return PackageAnalyzer(string)
        except AnalyzerInitializationException as err:
            print(err)


# arguments parsing
def argparser():
    parser = argparse.ArgumentParser(
        description='Find deprecations in your requirements and ' \
                    'underlying libraries',
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('project', nargs='?', type=ProjectType(), default='.',
                        help="Path, file, package, or distant \
                        repo to analyze. \
                        If not provided the current dir will be analyzed.")
    parser.add_argument('-o', '--output', type=argparse.FileType('w'),
                        help="Print output in a file instead of stdout")
    return parser
