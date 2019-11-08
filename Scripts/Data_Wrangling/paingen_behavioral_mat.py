#!/usr/bin/env python3

import os

print("Only running on MAT files, at the moment! Because, I, Clayton Schneider, do not know the other filename endings offhand.\n")

thisdir = input("Want me to check top-level files in this directory? y or n\n")
if (thisdir == "n"):
    subdir = input("Then I will check subdirs of this directory? y or n\n")

skippedDirs = []
checkedDirs = []

skippedFiles = []
checkedFiles = []

def renamefiles():
    for fname in os.listdir():
        try:
            dotindex = fname.find('.')
            ftype = fname[dotindex:]
            if ftype != ".mat":
                raise Exception('Found non-matlab file')
            
            if("clc" in fname):
                task = "clc"
            elif("conc" in fname):
                task = "conc"
            elif("ptt" in fname):
                task = "ptt"
            elif("ppt" in fname):
                task = "ptt"
            elif("p1" in fname):
                task = "p"
            elif("p2" in fname):
                task = "p"
            elif("p3" in fname):
                task = "p"
            elif("p4" in fname):
                task = "p"
            elif("pain1" in fname):
                task = "p"
            elif("pain2" in fname):
                task = "p"
            elif("pain3" in fname):
                task = "p"
            elif("pain4" in fname):
                task = "p"
            elif("P1" in fname):
                task = "p"
            elif("P2" in fname):
                task = "p"
            elif("P3" in fname):
                task = "p"
            elif("P4" in fname):
                task = "p"
            else:
                raise Exception('Could not read task type, may not be supported')
                
            nums = ''.join([n for n in fname if n.isdigit()])
            
            if (task == "ptt"):
                if (len(nums) != 3) & (fname[dotindex-1] != "1"):
                    raise Exception('Incorrect number of numbers (lol) read from fname')
                newfname = "PGs"+nums[:3]+"_"+task+"1"+ftype
            else:
                if (len(nums) != 4):
                    raise Exception('Incorrect number of numbers (lol) read from fname')
                newfname = "PGs"+nums[:3]+"_"+task+nums[3]+ftype

            if(newfname != fname):
                os.rename(fname, newfname)
                checkedFiles.append((fname, newfname))
            
        except:
            skippedFiles.append(fname)


if thisdir=="y":
    renamefiles()

elif subdir=="y":
    for subfolder in os.listdir():
        if ((len(subfolder) != 3) | (subfolder.isdigit()==False)):
            skippedDirs.append(subfolder)
        else:
            os.chdir(subfolder)
            renamefiles()
            os.chdir('..')
            checkedDirs.append(subfolder)

if(len(skippedDirs)>0):
    print("I skipped these folders:\n", skippedDirs, "\n")

if(len(skippedFiles)>0):
    print("I skipped these files:\n", skippedFiles, "\n")

#print("I went and checked these folders:\n")
#for folder in checkedDirs:
#    print(folder, "\n")

for change in checkedFiles:
    print("I changed", change[0], "to", change[1], "\n")
