
import os
import fnmatch


def combine_file_snippets(project_dir):
    """ Recusively search for files ending in posfix/prefix and join them th their originals """

    for dirpath, dirnames, filenames in os.walk(project_dir):

        if '.git' in dirnames:
            dirnames.remove('.git')

        print('Scanning files:', filenames)

        postfix_files = fnmatch.filter(filenames, '*_postfix*')
        prefix_files = fnmatch.filter(filenames, '*_prefix*')

        for postfile in postfix_files:
            original = os.path.join(dirpath, postfile.replace('_postfix', ''))
            print('Looking for original file:', original)
            if os.path.exists(original):
                postfile = os.path.join(dirpath, postfile)
                postfix(original, postfile)
                print('Postfixing', original)

        for prefile in prefix_files:
            original = os.path.join(dirpath, prefile.replace('_prefix', ''))       
            if os.path.exists(original):
                prefile = os.path.join(dirpath, prefile)
                prefix(original, prefile)
                print('Prefixing', original)


def postfix(original_file, postfix_file):
    """ Add the content of postfix_file to the end of original_file and remove postfix_file """

    with open(original_file, 'a') as fout:
        with open(postfix_file) as fin:
            fout.write(fin.read())
    os.remove(fin.name)


def prefix(original_file, prefix_file):
    """ Add the content of prefix_file to the begining of original_file and remove prefix_file """

    with open(prefix_file, 'a') as fout:
        with open(original_file) as fin:
            fout.write(fin.read())
    os.remove(fin.name)
    os.rename(fout.name, fin.name)
