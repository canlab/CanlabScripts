# This script converts raw dicoms in primsa_fit folder to "pre BIDSkit" format, i.e., the format that BIDSkit expects for conversion to BIDS
# "pre-BIDSkit format" is basically a list of all the dicoms.  This script makes "hard links" to the files so they are not duplicated.
# Example usage:
#   > python prepbidsfromblanca.py /work/ics/data/archive/human/dicom/prisma_fit/twager/olp4cbp_200097 /work/ics/data/projects/wagerlab/labdata/data/OLP4CBP/Imaging/raw

import os
import sys

# Set the base directory in Blanca where raw dicoms are stored.
# Usually '/work/ics/data/archive/human/dicom/prisma_fit/twager/YOURSTUDY/' Your study on Blanca
rawdir = sys.argv[1] 
outdir = sys.argv[2] 


os.mkdir(outdir+'/'+'dicoms')
# Get the list of subjects
subjectdirs = os.listdir(rawdir)

# Each subject could have multiple runs.
for sdir in subjectdirs:
    if os.path.isdir(rawdir+'/'+sdir): # is a dir, not a file
        print "creating dicom hard links for subject " + sdir
        if !os.path.isdir(rawdir+'/'+sdir):
            os.mkdir(outdir+'/'+'dicoms'+'/'+sdir) # make the output dir if doesn't exist

        sessdirs = sorted(os.listdir((rawdir+'/'+sdir))) # get the sessions
	sesscount = len(sessdirs)
        for sessdir in range(1,sesscount+1):
            rdir = outdir+'/'+'dicoms' +'/'+ sdir+'/'+ str(sessdir)
            
            # if the session dir already exists, skip
            if os.path.isdir(rdir):
                print "  " + rdir + " already exists, skipping creation of hard links"
                continue
            else:
                os.mkdir(rdir)
            
            taskdirs = os.listdir((rawdir+'/'+sdir+'/'+ str(sessdirs[sessdir-1])))
            for tdir in taskdirs:
                dicoms = os.listdir((rawdir+'/'+sdir+'/'+ str(sessdirs[sessdir-1]) +'/'+tdir))
                for dicom in dicoms:
                    if os.path.isfile((rawdir+'/'+sdir+'/'+ str(sessdirs[sessdir-1]) +'/'+tdir+'/'+dicom)):
                        os.link((rawdir+'/'+sdir+'/'+ str(sessdirs[sessdir-1]) +'/'+tdir+'/'+dicom),(rdir + '/' + dicom))
