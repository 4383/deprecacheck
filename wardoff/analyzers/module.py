from pathlib import Path

from wardoff import utils, venv
from wardoff.analyzers import syntax
from wardoff.package import Package


class ModuleAnalyzerInitializationError(Exception):
    pass


class BaseAnalyzer:
    def __init__(self, project):
        """Project requirements analyzer.

        Base analyzer class.

        :param string project: Project to analyze.
        """
        self.project = project

    def analyze(self):
        self.requirements = self.retrieve_requirements()

    def retrieve_requirements(self):
        raise NotImplementedError("retrieve method not implemented")


class PathAnalyzer(BaseAnalyzer):
    def retrieve_requirements(self):
        requirements = []
        path = Path(self.project)
        requirements_files = list(path.glob("**/*requirements.txt"))
        for p in requirements_files:
            with p.open() as f:
                requirements.extend(f.readlines())
        return requirements


class FileAnalyzer(BaseAnalyzer):
    pass


class RepoAnalyzer(BaseAnalyzer):
    pass


class PackageAnalyzer(BaseAnalyzer):
    def analyze(self):
        venv.create()
        self.retrieve_requirements()
        self.search_deprecated()

    def retrieve_requirements(self):
        venv.pip_install(self.project)
        self.requirements = [
            Package(el) for el in venv.pip_freeze([self.project])
        ]

    def search_deprecated(self):
        for el in self.requirements:
            print(el.name)
            if not el.sources_path:
                continue
            deprecations = []
            for pyfile in utils.get_pyfiles(el.sources_path):
                try:
                    mod_analyzer = syntax.ModuleAnalyzer(pyfile)
                except syntax.AnalyzerSyntaxException:
                    continue
                mod_analyzer.analyze()
                if mod_analyzer.results:
                    deprecations.extends(mod_analyzer.results)
            if not deprecations:
                print("No deprecations found")
                continue
            print(deprecations)
