""" Post project creation hooks: 

Replace if __name__ statement in main.py

"""

import re
from pathlib import Path


def add_parse_args(old_file):

    old_file = Path(old_file)
    pattern = re.compile(r"""def main\(args=None\):\s""")

    with old_file.open('r') as old_fh:

        new_lines = []

        for line in old_fh:
            new_lines.append(line)
            if pattern.match(line):
                print(line)
                new_lines.append(next(old_fh))
                new_lines.append("\n")
                new_lines.append("    args = get_parser().parse_args(args)\n")
                new_lines.append("\n")

    with old_file.open('w') as old_fh:
        old_fh.writelines(new_lines)


add_parse_args('package/src/{{cookiecutter.package_name}}/main.py')
