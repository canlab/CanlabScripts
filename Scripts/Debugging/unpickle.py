#!/usr/bin/env python

####################################################################
# This program is designed to display the information contained in #
# the .pklz files created by python scripts that use the nipy      #
# framework. It unzips, unpickles, and displays the resulting      #
# debugging information.                                           #
####################################################################

import pickle
import gzip
from sys import argv

crashdump=pickle.load(gzip.open(argv[1]))

print crashdump['node']
for item in crashdump['traceback']:
    print item
