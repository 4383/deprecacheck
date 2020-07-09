import argparse
from pathlib import Path

from wardoff.analyzers import module as module_analyzer


class ProjectType:
    def __call__(self, string):
        try:
            if not string or string == ".":
                return module_analyzer.PathAnalyzer(".")
            if Path(string).is_file():
                return module_analyzer.FileAnalyzer(string)
            if Path(string).is_dir():
                return module_analyzer.PathAnalyzer(".")
            if string.startswith("http") or string.startswith("git"):
                return module_analyzer.RepoAnalyzer(string)
            # By default we consider the passed argument as a pypi project name
            return module_analyzer.PackageAnalyzer(string)
        except module_analyzer.ModuleAnalyzerInitializationError as err:
            print(err)


# arguments parsing
def main():
    parser = argparse.ArgumentParser(
        description="Find deprecations in your requirements and "
        "underlying libraries",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "project",
        nargs="?",
        type=ProjectType(),
        default=".",
        help="Path, file, package, or distant \
                        repo to analyze. \
                        If not provided the current dir will be analyzed.",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        help="Print output in a file instead of stdout",
    )
    return parser
