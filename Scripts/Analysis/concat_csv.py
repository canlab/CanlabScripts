#!/usr/bin/env python
import numpy as np
import pandas as pd
import sys

dataframes=[pd.read_csv(x,dtype={'Condition':np.int32, 'Trial':np.int32}, engine='c') for x in sys.argv[1:]]
combined_df=pd.concat(dataframes, ignore_index=True)

combined_df.to_csv("combined_table.csv", na_rep=float('NaN'), index=False)

