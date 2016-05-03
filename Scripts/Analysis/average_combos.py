#! /usr/bin/env python

import numpy as np
import scipy as sp
import pandas as pd

data=pd.read_csv("clean-file.txt",sep="\t")
mean_means=data.groupby(['subject','seed'],as_index=False)['valence_mean'].mean()
pd.set_option('display.max_rows', len(mean_means))
print mean_means