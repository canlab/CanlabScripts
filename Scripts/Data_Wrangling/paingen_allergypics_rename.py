#!/usr/bin/env python3

import os

skippedDirs = []
checkedDirs = []

def renamefiles():
    for fname in os.listdir():
        try:
            nums = ''.join([n for n in fname if n.isdigit()])
            if(len(nums) != 3):
                raise Exception("Looks like there's not three numbers in this filename.")
            newname = "PGs"+nums[:3]
            if(newname != fname):
                os.rename(fname, newname)
                checkedDirs.append((fname, newname))
        except:
            skippedDirs.append(fname)

renamefiles()

if(len(skippedDirs)>0):
    print("I skipped these folders:\n", skippedDirs, "\n")

if(len(checkedDirs)>0):
    for change in checkedDirs:
        print("I changed", change[0], "to", change[1], "\n")
else:
    print("I didn't make any changes.")
