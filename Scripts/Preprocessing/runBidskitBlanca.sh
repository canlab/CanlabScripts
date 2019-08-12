#!/bin/bash
#SBATCH -p blanca-ics
#SBATCH -n 1
#SBATCH -t 360
#SBATCH --mem=32G
#SBATCH --mail-user=clsc1382@colorado.edu

# USAGE:
# place this script the upper bids directory marked with *
# then run `sbatch <scriptname.sh>`

# >studyProjectFolder/
# ----->bids/*
# ---------->sourcedata/
# --------------->M803.../
# --------------->M803.../...

# where sourcedata/ is a COPY of raw dicom data

# if there is only 1 session
bidskit --no-sessions

# if there are multiple
# bidskit
