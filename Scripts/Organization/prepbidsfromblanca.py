# This script converts raw dicoms in primsa_fit folder to "pre BIDSkit" format, i.e., the format that BIDSkit expects for conversion to BIDS
# "pre-BIDSkit format" is basically a list of all the dicoms.  This script makes "hard links" to the files so they are not duplicated.

import os

# Set the base directory in Blanca where raw dicoms are stored.
# Usually '/work/ics/data/archive/human/dicom/prisma_fit/twager/YOURSTUDY/' Your study on Blanca
rawdir = '/work/ics/data/archive/human/dicom/prisma_fit/twager/olp4cbp_200097'
outdir = '/work/ics/data/projects/wagerlab/labdata/projects/BIDS/OLP4CBP'

os.mkdir(outdir+'/'+'sourcedata')
# Get the list of subjects
subjectdirs = os.listdir(rawdir)

# Each subject could have multiple runs.
for sdir in subjectdirs:
    if os.path.isdir(rawdir+'/'+sdir): # is a dir, not a file
        os.mkdir(outdir+'/'+'sourcedata'+'/'+sdir) # make the output dir
        sessdirs = sorted(os.listdir((rawdir+'/'+sdir))) # get the sessions
	sesscount = len(sessdirs)
        for sessdir in range(1,sesscount+1):
            rdir = outdir+'/'+'sourcedata' +'/'+ sdir+'/'+ str(sessdir)
            os.mkdir(rdir)
            taskdirs = os.listdir((rawdir+'/'+sdir+'/'+ str(sessdirs[sessdir-1])))
            for tdir in taskdirs:
                dicoms = os.listdir((rawdir+'/'+sdir+'/'+ str(sessdirs[sessdir-1]) +'/'+tdir))
                for dicom in dicoms:
                    if os.path.isfile((rawdir+'/'+sdir+'/'+ str(sessdirs[sessdir-1]) +'/'+tdir+'/'+dicom)):
                        os.link((rawdir+'/'+sdir+'/'+ str(sessdirs[sessdir-1]) +'/'+tdir+'/'+dicom),(rdir + '/' + dicom))
