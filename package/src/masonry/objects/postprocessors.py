""" These act on the file layout after a template layer has been applied
"""

import ast
import os
from pathlib import Path

from ..utils import rindex


class Preprocessor:

    def __init__(self, pattern):
        self.pattern = pattern
        self.exclude = None
        self.only = None

    def apply(self, dirpath):

        dirpath = Path(dirpath)

        glob_pattern = '*' + self.pattern + '*'

        filenames = dirpath.glob(glob_pattern)
        filenames = self._filter_filenames(filenames)

        updated_files = []

        for f in filenames:
            original_fname = f.name.replace(self.pattern, '')
            original = f.parent / original_fname

            if os.path.exists(original):
                changed_filename = self.process(str(f), str(original))
                updated_files.append(changed_filename)

        return updated_files

    def process(self, src, dest):
        raise NotImplementedError

    def _filter_filenames(self, filenames):

        filenames = [f for f in filenames if f.is_file()]
        if self.exclude:
            filenames = [f for f in filenames if not f.suffix or f.suffix not in self.exclude]
        if self.only:
            filenames = [f for f in filenames if f.suffix in self.only]

        return filenames


class FilePreprocessor(Preprocessor):

    """ Base Preprocessors for all non code files. """

    def __init__(self, pattern):
        super().__init__(pattern=pattern)
        self.exclude = '.py'


class CombineFilePrefix(FilePreprocessor):

    def __init__(self, pattern='_prefix'):
        super().__init__(pattern=pattern)

    def process(self, src, dest):
        """ Add the content of src file path to the begining of dest file path and remove src

        Return the updated filename
        """

        with open(src, 'a') as fout:
            with open(dest) as fin:
                fout.write(fin.read())
        os.remove(fin.name)
        os.rename(fout.name, fin.name)

        return fin.name


class CombineFilePostfix(FilePreprocessor):

    def __init__(self, pattern='_postfix'):
        super().__init__(pattern=pattern)

    def process(self, src, dest):
        """ Add the content of src to the end of dest file and remove src file.

        Return the updated filename
        """

        with open(dest, 'a') as fout:
            with open(src) as fin:
                fout.write(fin.read())
        os.remove(fin.name)

        return fout.name


class CodePreprocessor(Preprocessor):

    """Base Preprocessor for all Python Code files """

    def __init__(self, pattern):
        super().__init__(pattern=pattern)
        self.only = '.py'

    def process(self, src, dest):

        source_text = open(src).read().strip()
        destination_text = open(dest).read()
        destination_lines = destination_text.split('\n')
        destination_tree = ast.parse(destination_text)

        if not destination_tree.body:
            idx = 0
        else:
            idx = self._find_insertion_idx(destination_tree)

        if idx >= len(destination_tree.body):

            # Strip blank line before insertion
            if destination_lines[-1].strip() == '':
                del destination_lines[-1]

            # Append to file
            destination_lines.append('\n\n' + source_text + '\n')

        else:

            # Start with index at first line above object definition
            line_no = destination_tree.body[idx].lineno - 1  # line numbers count from 1
            line_no = self._get_previous_blank_line_no(destination_lines, line_no)

            # Strip blank lines before insertion
            if destination_lines[line_no - 1].strip() == '':
                del destination_lines[line_no - 1]
                line_no -= 1

            # perform the insertion
            destination_lines.insert(line_no, '\n\n' + source_text + '\n')

        all_text = '\n'.join(destination_lines)

        # Write to file
        with open(dest, 'w') as fout:
            fout.write(all_text)

        os.remove(src)

        return fout.name

    def _get_previous_blank_line_no(self, lines, idx):
        """Find a blank line before the object definition"""

        while True:
            if not lines[idx].strip():
                # found a blank line
                break
            else:
                idx -= 1

        return idx

    def _find_insertion_idx(self):
        raise NotImplementedError


class CombineCodePrefix(CodePreprocessor):

    def __init__(self, pattern='_prefix'):
        super().__init__(pattern=pattern)

    def _find_insertion_idx(self, module_ast):
        """Return prefix insertion point.

        This is the point in the code after any imports and constants, but before any functions or
        classes are defined.
        """

        # Inspect ast types present
        node_types = [type(x) for x in module_ast.body]
        func_class_pos = [x == ast.FunctionDef or x == ast.ClassDef for x in node_types]
        import_pos = [x == ast.Import or x == ast.ImportFrom for x in node_types]

        docstring_present = (
            isinstance(node_types[0], ast.Expr) and isinstance(node_types[0].value, ast.Str)
        )
        constants_pos = [isinstance(elem, ast.Assign) and elem.targets[0].id.isupper()
                         for elem in module_ast.body]

        last_node = module_ast.body[-1]
        ifname_present = isinstance(last_node, ast.If) and last_node.test.left.id == '__name__'

        if any(func_class_pos):
            # Insertion point is just before the first occurance of function or class
            insert_idx = func_class_pos.index(True)

        elif any(constants_pos):
            # Insertion point is after the last constant
            insert_idx = rindex(constants_pos, True)
            insert_idx += 1

        elif any(import_pos):
            # Insertion point is after all imports
            insert_idx = rindex(import_pos, True)
            insert_idx += 1

        elif docstring_present:
            # Insertion point is after docstring
            insert_idx = 1

        elif ifname_present:
            # Insertion point is before ifname
            insert_idx = -1

        return insert_idx


class CombineCodePostfix(CodePreprocessor):

    def __init__(self, pattern='_postfix'):
        super().__init__(pattern=pattern)

    def _find_insertion_idx(self, module_ast):
        """Return postfix insertion point.

        This is the point in the code after any functions or classes are defined, but before the
        ifname statement if present.
        """

        # Inspect ast types present
        node_types = [type(x) for x in module_ast.body]
        func_class_pos = [x == ast.FunctionDef or x == ast.ClassDef for x in node_types]

        last_node = module_ast.body[-1]
        ifname_present = isinstance(last_node, ast.If) and last_node.test.left.id == '__name__'

        if any(func_class_pos):
            # Insertion point is just after the last occurance of function or class
            insert_idx = rindex(func_class_pos, True)
            insert_idx += 1

        elif ifname_present:
            # Insertion point is before ifname
            insert_idx = -1

        else:
            # Insert at end of code
            insert_idx = len(module_ast.body)

        return insert_idx
