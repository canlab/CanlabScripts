#! /usr/bin/env python3

import os
from os import path, walk
import sys


#The first argument is the directory to shadow, the second argument
#is where to put the shadow directory.
source_dir=sys.argv[1]
fullsource=os.path.abspath(source_dir)
shadow_loc=os.path.abspath(sys.argv[2])

try:
    os.makedirs(shadow_loc)
except OSError:
    print("Destination directory exits; shadowing anyway...")
fulltree=walk(source_dir)
fulltree=[x for x in fulltree]

base_paths=[x[0].replace(source_dir,'') for x in fulltree]
dirnames=[x[1] for x in fulltree]
filenames=[x[2] for x in fulltree]

exists=False
os.chdir(shadow_loc)
for i in range(len(base_paths)):
    try:
        os.makedirs(base_paths[i])
    except OSError:#Catches when the directory on base_paths already exists or when the name is an empty string
        print("Base Path ", base_paths[i], " already exists or is empty.")
        pass
    try:
        os.chdir(base_paths[i])
    except OSError as e: #Catches when base_paths[i] can't be moved into.
        print(e, "\nError Location=2")
        os.chdir(shadow_loc)
        continue
    for filename in filenames[i]:
        source_fn=fullsource+"/"+base_paths[i]+"/"+filename
        try:
            os.link(source_fn,filename)
        except FileExistsError as e:
            print("File exists: ", filename)
        except PermissionError as e:
            print("File can't be copied because of permissions issues:\n", filename)
    os.chdir(shadow_loc)
if (exists):
    print("Some directories already existed. Not remade.") 
