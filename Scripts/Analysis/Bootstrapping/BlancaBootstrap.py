#!/projects/luch0518/software/anaconda/bin/python

# This script divides up 5000 bootstrap samples into 20 jobs and automatically submits them to the blanca cluster.  It creates a shell script with an embedded matlab template file separately for each cluster job.  
# Requires that the matlab .mat file load a fmri_data object with the .Y filled in and named 'data' 
# Really fast - takes about 5 min to do 5000 samples
# Need to run Collate script to integrate samples together.
# It’s pretty kludgy and difficult to read, but should only require modifying the number of samples, paths, and filenames.  Everything else should work fine for most uses.n  It uses my own builds of python and SPM, which should be accessible to our lab (/projects/luch0518/software).  You will probably need to add this to your environment paths. I tested it a few times on two data files, but definitely let me know right away if you discover any bugs.  Sometimes a job might get dropped for some random reason that I can’t figure out.  Because all of the jobs are independent you can just rerun the number of jobs that didn’t work and replace them with the new ones.  (e.g., if boot_5 is missing -> mv boot_1.mat boot_5.mat, then set nJobs to 1, and rerun the script).  

# ToDo:  can turn into function and take inputs

import subprocess

nJobs = 3
nBoot = 250 
algorithm = 'cv_svm'
filein = 'PTSD_CsplusVCsminus_Ext_Data_bootstrap.mat'
fileout = 'CS+vsCS-_Ext_PtvCtl_boostrap'
rPath = '/projects/luch0518/software'
fPath = '/work/wagerlab/labdata/current/Yuval_Luke/Analyses'
cPath = '/projects/luch0518/ClusterJobs'
		
for i in range(1,nJobs+1):
	#Create Qsub call	
	qsub_call = 'qsub -q blanca-ics -l nodes=1:ppn=1 -m e -M  ' + email + ' -o ' + cPath + '/ClusterJobs/bootstrap_' + str(i) + '_output.txt -e ' + cPath + '/ClusterJobs/bootstrap_' + str(i) + '_error.txt'
	
	#Create matlab script
	matlab_script = '/curc/tools/x_86_64/rh6/matlab/matlab-2014a/bin/matlab -r \"rPath = \'' + rPath + '\';addpath(genpath(fullfile(rPath,\'Repository\',\'trunk\')));addpath(genpath(fullfile(rPath,\'lasso\')));addpath(genpath(fullfile(rPath,\'spider\')));addpath(genpath(fullfile(rPath,\'spm8_r5236\'))); fPath = \'' + fPath + '\';load(fullfile(fPath,\'' + filein + '\'));[cverr, stats, optout] = predict(data, \'algorithm_name\', \'' + algorithm  + '\', \'nfolds\', 1, \'bootweights\',\'bootsamples\',' + str(nBoot) + ', \'savebootweights\');save(fullfile(fPath,\'' + fileout + '_' + str(i) + '.mat\'),\'stats\',\'-v7.3\');quit;\" -nodisplay -nosplash -nodesktop'
	
	#write matlab bash script to file
	with open( cPath + '/boot_' + str(i) + '.sh', "w") as text_file:
    		text_file.write(matlab_script)	

	#Submit matlab script on cluster.
	subprocess.call(qsub_call + ' ' + cPath + '/boot_' + str(i) + '.sh', shell=True)


