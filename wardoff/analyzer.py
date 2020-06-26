import ast
import io
import tokenize


# order is important because we will retrieve by
# trying to find by name in substring and so PendingDeprecationWarning
# and DeprecationWarning could collid
DEPRECATIONS = [
    PendingDeprecationWarning,
    DeprecationWarning,
    FutureWarning,
]


class AnalyzerException(Exception):
    pass


def walk(root, results=[], previous=None):
    previous = root
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Raise):
            results.append({
                "lineno": "{func}:{raised}".format(
                    func=previous.lineno, raised=node.lineno),
                "def": previous,
                "raise": node,
            })
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            results = walk(node, results)
    return results


def get_node_source(source, node):
    return ast.get_source_segment(source, node)


TOKENS_TYPES = {
    "ENCODING": 62,
    "NAME": 1,
    "OP": 54,
    "NEWLINE": 4,
    "INDENT": 5,
}


class ModuleAnalyzer:

    def __init__(self, module_path):
        self.ast = None
        self.code = None
        self.tokens = None
        self.results = None
        self.content = None
        with open(module_path, 'r') as fp:
            self.content = fp.read()
            self.code = io.BytesIO(self.content.encode('utf-8'))
            self.ast = ast.parse(self.content)
        self.tokens = [el for el in tokenize.tokenize(self.code.readline)]

    def tokenizer(self, snippet):
        if not isinstance(snippet, io.BytesIO):
            snippet = io.BytesIO(snippet.encode('utf-8'))
        return [el for el in tokenize.tokenize(snippet.readline)]

    def extract_function_name(self, tokens):
        name = None
        ignored = ['def']
        for token in tokens:
            if int(token.type) == TOKENS_TYPES['OP']:
                return name
            if int(token.type) == TOKENS_TYPES['ENCODING']:
                continue
            if token.string in ignored:
                continue
            name = token.string

    def extract_exception_message(self, tokens):
        pass

    def runast(self):
        self.results = walk(self.ast, results=[])
        return self.results

    def retrieve_code(self):
        if not self.results:
            raise AnalyzerException(
                "No results available, please call runast first")
        source_lines = []
        for el in self.results:
            raise_line = get_node_source(self.content, el['raise'])
            for depr in DEPRECATIONS:
                if depr.__name__ not in raise_line:
                    continue
                def_line = get_node_source(self.content, el['def'])
                source_lines.append({'def': def_line, 'raise': raise_line})
                break
        return source_lines
