import os
from pathlib import Path

def viewStudyTree(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print('{}{}/'.format(indent, os.path.basename(root)))
        subindent = ' ' * 4 * (level+1)
        print("\n")
        #for f in files:
        #    print('{}{}'.format(subindent, f))

viewStudyTree(os.getcwd())
