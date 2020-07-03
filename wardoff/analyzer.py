import ast
import io
import tokenize

# order is important because we will retrieve by
# trying to find by name in substring and so PendingDeprecationWarning
# and DeprecationWarning could collid
BASE_DEPRECATIONS = [
    PendingDeprecationWarning,
    DeprecationWarning,
    FutureWarning,
]


class AnalyzerException(Exception):
    pass


def walk(root, results=[], previous=None):
    """Recursively walk through an AST tree to looking for all exceptions.

    Here we don't care about the type of the raised exception, we just
    want to get all of them.

    This function is recursive that mean that while a node have classes or
    functions inside of it, then they (child node) will be analyzed too.

    :param ast root: AST node to walk through.
    :param list results: List of results to append.
    :param ast previous: AST node previously analyzed.
    :return: List of results founds
    """
    previous = root
    for node in ast.iter_child_nodes(root):
        # an Exception is raised? If yes then we add her to results.
        if isinstance(node, ast.Raise):
            results.append(
                {
                    "lineno": "{func}:{raised}".format(
                        func=previous.lineno, raised=node.lineno
                    ),
                    "def": previous,
                    "raise": node,
                }
            )
        # We just care about the exceptions raised in class or function.
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            results = walk(node, results)
    return results


def get_node_source(source, node):
    """Retrieve the original source code (human readable) of a node.

    :param list source: List of line of source code.
    :param ast node: AST node to retrieve in source code list.
    """
    return ast.get_source_segment(source, node)


# We don't need to list all tokens types only few of them
# are useful here
NEEDED_TOKENS_TYPES = {
    "ENCODING": 62,
    "NAME": 1,
    "OP": 54,
    "NEWLINE": 4,
    "INDENT": 5,
}


class ModuleAnalyzer:
    def __init__(self, module_path, custome_deprecations=None):
        """Analyzer that aim to detect deprecations.

        This class allow you to analyze a specified module to
        detect if it contains deprecated things.

        If a deprecation warning is raised somewhere in a function this
        function will be consider as deprecated and will be added to results.

        Are considered as deprecated functions where one of the following
        exceptions are raised:
        - DeprecationWarning
        - FutureWarning
        - PendingDeprecationWarning

        To retrieve this information this class will analyze the AST syntaxe
        of the module to retrieve all functions/classes where the previous
        exceptions are raised.

        When deprecations are found in a module this analyzer will
        tokenize its code to retrieve the called function name wherein the
        deprecation is raised.

        You can pass custome deprecations to looking for by example if
        you want to also detect the debtcollector's deprecations exceptions.

        :param string module_path: Path of module to analyze.
        :param list custome_deprecations: List of custome deprecation types
                                          to looking for.
        :return: Return a list of results (function name, exceptions type).
        """
        self.ast = None
        self.code = None
        self.tokens = None
        self.results = None
        self.content = None
        if custome_deprecations and isinstance(custome_deprecations, list):
            global BASE_DEPRECATIONS
            BASE_DEPRECATIONS.extends(custome_deprecations)
        with open(module_path, "r") as fp:
            self.content = fp.read()
            self.code = io.BytesIO(self.content.encode("utf-8"))
            self.ast = ast.parse(self.content)
        self.tokens = [el for el in tokenize.tokenize(self.code.readline)]

    def tokenizer(self, snippet):
        if not isinstance(snippet, io.BytesIO):
            snippet = io.BytesIO(snippet.encode("utf-8"))
        return [el for el in tokenize.tokenize(snippet.readline)]

    def extract_function_name(self, tokens):
        name = None
        ignored = ["def"]
        for token in tokens:
            if int(token.type) == NEEDED_TOKENS_TYPES["OP"]:
                return name
            if int(token.type) == NEEDED_TOKENS_TYPES["ENCODING"]:
                continue
            if token.string in ignored:
                continue
            name = token.string

    def extract_exception_type_and_message(self, tokens):
        name = None
        ignored = ["def"]
        for token in tokens:
            if int(token.type) == NEEDED_TOKENS_TYPES["OP"]:
                return name
            if int(token.type) == NEEDED_TOKENS_TYPES["ENCODING"]:
                continue
            if token.string in ignored:
                continue
            name = token.string

    def runast(self):
        self.results = walk(self.ast, results=[])
        return self.results

    def retrieve_code(self):
        if not self.results:
            raise AnalyzerException(
                "No results available, please call runast first"
            )
        source_lines = []
        for el in self.results:
            raise_line = get_node_source(self.content, el["raise"])
            for depr in BASE_DEPRECATIONS:
                if depr.__name__ not in raise_line:
                    continue
                def_line = get_node_source(self.content, el["def"])
                source_lines.append({"def": def_line, "raise": raise_line})
                break
        return source_lines
