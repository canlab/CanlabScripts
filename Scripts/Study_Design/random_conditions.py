#!/usr/bin/python

from random import shuffle,seed
from os import urandom
seed(urandom(512))

conditions=['Placebo','Oxytocin']

for subject in range(1,41):
    subjstr=str(subject)
    shuffle(conditions)
    print (subjstr+"A"),conditions[0]
    print (subjstr+"B"),conditions[1]

