#!/usr/bin/env python3
import os

skippedFiles = []
checkedFiles = []

def renamefiles():
    for fname in os.listdir():
        try:
            hyphens = [pos for pos, char in enumerate(fname) if char == '-']
            beforeslice = fname[:hyphens[0]+1]
            numslice = fname[hyphens[0]+1:hyphens[1]]
            afterslice = fname[hyphens[1]:]

            nums = ''.join([n for n in numslice if n.isdigit()])

            nums = nums.zfill(3)

            newfname = beforeslice+nums+afterslice

            if(newfname != fname):
                os.rename(fname, newfname)
                checkedFiles.append((fname, newfname))

        except:
            skippedFiles.append(fname)

renamefiles()

if len(skippedFiles)>0:
    print("I skipped these files:\n", skippedFiles, "\n")

for change in checkedFiles:
    print("I changed", change[0], "to", change[1], "\n")



            
