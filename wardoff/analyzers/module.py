from pathlib import Path


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
    pass
