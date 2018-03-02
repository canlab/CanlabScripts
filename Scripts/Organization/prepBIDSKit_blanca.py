import os
import sys

usage = "\nThis script converts raw dicoms in primsa_fit folder to pre BIDSkit format.  This is the format that BIDSkit expects for conversion to BIDS, which is basically a list of all the dicoms.  This script makes hard links to the files so they are not duplicated.  \n\nExample usage: \n> python prepbidsfromblanca.py /work/ics/data/archive/human/dicom/prisma_fit/twager/olp4cbp_200097 /work/ics/data/projects/wagerlab/labdata/data/OLP4CBP/Imaging/raw \n"


# Set the base directory in Blanca where raw dicoms are stored.
# Usually '/work/ics/data/archive/human/dicom/prisma_fit/twager/YOURSTUDY/' Your study on Blanca

if len(sys.argv) < 3:
    print(usage)
    sys.exit()

rawdir = sys.argv[1] 
outdir = sys.argv[2] 

if not os.path.isdir(outdir+'/dicoms'):
    os.mkdir(outdir+'/dicoms')

# Get the list of subjects
subjectdirs = os.listdir(rawdir)

# Each subject could have multiple runs.
for sdir in subjectdirs:
    if os.path.isdir(rawdir+'/'+sdir): # is a dir, not a file
        print("processing subject " + sdir)
        if not os.path.isdir(outdir+'/dicoms/'+sdir):
            os.mkdir(outdir+'/'+'dicoms'+'/'+sdir) # make the output dir if doesn't exist

        sessdirs = sorted(os.listdir((rawdir+'/'+sdir))) # get the sessions
        sesscount = len(sessdirs)
        for sessdir in range(1,sesscount+1):
            rdir = outdir+'/'+'dicoms' +'/'+ sdir+'/'+ str(sessdir)
            
            # if the session dir already exists, skip
            if os.path.isdir(rdir):
                print("  - " + sdir + '/' + str(sessdir) + " already exists, skipping")
                continue
            else:
                os.mkdir(rdir)
                print("  - " + sdir + '/' + str(sessdir) + " being processed")
            taskdirs = os.listdir((rawdir+'/'+sdir+'/'+ str(sessdirs[sessdir-1])))
            for tdir in taskdirs:
                dicoms = os.listdir((rawdir+'/'+sdir+'/'+ str(sessdirs[sessdir-1]) +'/'+tdir))
                for dicom in dicoms:
                    if os.path.isfile((rawdir+'/'+sdir+'/'+ str(sessdirs[sessdir-1]) +'/'+tdir+'/'+dicom)):
                        os.link((rawdir+'/'+sdir+'/'+ str(sessdirs[sessdir-1]) +'/'+tdir+'/'+dicom),(rdir + '/' + dicom))
