

import os 


def postfix(original_file, new_file):
    """ Add the content of new_content to the end of original_file and remove new_content """

    with open(original_file, 'a') as fout:
        with open(new_file) as fin:
            fout.write(fin.read())
    os.remove(fin.name)


def prefix(original_file, new_file):
    """ Add the content of new_content to the end of original_file and remove new_content """

    with open(new_file, 'a') as fout:
        with open(original_file) as fin:
            fout.write(fin.read())
    os.remove(fin.name)
    os.rename(fout.name, fin.name)

