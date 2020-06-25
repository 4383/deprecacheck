import ast
import io
import tokenize


def walk(root, results=[], previous=None):
    previous = root
    for node in ast.iter_child_nodes(root):
        if isinstance(node, ast.Raise):
            results.append({previous.lineno: node.lineno})
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.ClassDef):
            results = walk(node, results)
    return results


class ModuleAnalyzer:

    def __init__(self, module_path):
        self.ast = None
        self.code = None
        self.tokens = None
        with open(module_path, 'r') as fp:
            content = fp.read()
            self.code = io.BytesIO(content.encode('utf-8'))
            self.ast = ast.parse(content)
        self.tokens = [el for el in tokenize.tokenize(self.code.readline)]

    def tokenizer(self):
        for el in self.tokens:
            print(el)

    def runast(self):
        results = walk(self.ast)
        return results
