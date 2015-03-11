#!/projects/luch0518/software/anaconda/bin/python

# This script divides up 5000 bootstrap samples into 20 jobs and automatically submits them to the blanca cluster.  It creates a shell script with an embedded matlab template file separately for each cluster job.  
# Requires that you set the filename of the output of Blanca_Bootstrap.py and the number of parallel jobs that were run so that they can be integrated.
# Really fast - takes about 5 min
# Will write out Z and p Images and also images thresholded p < 0.001 uncorrected and fdr q < .05 cluster extent=10 voxels
# Make sure that all files exist before running this, otherwise it will error.


# ToDo:  
# 1) can turn into function and take inputs
# 2) could add checks to make sure all of the files exist that are supposed to and rerun them if not, before collating.

import subprocess

nJobs = 20 #number of jobs specified in previous script
nCores = 1 #Number of cores to request for each job
filein = 'SVM_Reg_vs_Neg_boostrap_trialmean' #Name of file output used in previous script
rPath = '/projects/luch0518/software' #Path to software libraries
fPath = '/work/wagerlab/labdata/current/Gianaros_Luke/Data' #Path to Data
cPath = '/projects/luch0518/ClusterJobs' #Path to folder with cluster output
email = 'luke.chang@colorado.edu' #Email Address.

#Create Qsub call	
# qsub_call = 'qsub -q blanca-ics -l nodes=1:ppn=1 -m e -M  ' + email + ' -o ' + cPath + '/Collate_Bootstrap_output.txt -e ' + cPath + '/Collate_Bootstrap_error.txt'
qsub_call = 'sbatch -A UCB00000358 --qos=blanca-ics -N 1 --ntasks-per-node=' + str(nCores) + ' --mail-type=end --mail-user=' + email + ' --output ' + cPath + '/Collate_Bootstrap_output.txt -e ' + cPath + '/Collate_Bootstrap_error.txt'
	
#Create matlab script
matlab_script = '/curc/tools/x_86_64/rh6/matlab/matlab-2014a/bin/matlab -r \"rPath = \'' + rPath + '\';addpath(genpath(fullfile(rPath,\'CanlabCore\',\'CanlabCore\')));addpath(genpath(fullfile(rPath,\'spm8_r5236\'))); fPath = \'' + fPath + '\'; w = []; for i = 1:' + str(nJobs) + ';load(fullfile(fPath,[\'' + filein + '_\' num2str(i)  \'.mat\']));w = [w;stats.WTS.w];end;load(fullfile(fPath,\'' + filein + '_1.mat\'));dat = stats.weight_obj; wste = nanstd(w); wmean = nanmean(w); wste(wste==0) = Inf;wZ = wmean./wste;wP = 2*(1-normcdf(abs(wZ)));out = statistic_image();out.dat=wZ\';out.p = wP\';out.volInfo = dat.volInfo;thr=threshold(out,.05,\'fdr\',\'k\',10);t=replace_empty(thr);th=dat;th.dat=wZ\';th.dat(~logical(t.sig))=0;th.fullpath = fullfile(fPath,[\'' + filein + '\' \'_boot_fdr05_k10.nii\']);write(th,\'mni\');out=statistic_image();out.dat=wZ\';out.p = wP\';out.volInfo = dat.volInfo;thr=threshold(out,.001,\'unc\');t=replace_empty(thr);th=dat;th.dat=wZ\';th.dat(~logical(t.sig))=0;th.fullpath = fullfile(fPath,[\'' + filein + '\' \'_boot_001unc.nii\']);write(th,\'mni\');z=dat;z.dat = wZ\';z.fullpath=fullfile(fPath,[\'' + filein + '\' \'_boot_Z.nii\']);write(z,\'mni\');p=dat;p.dat=wP\';p.fullpath=fullfile(fPath,[\'' + filein + '\' \'_boot_pVal.nii\']);write(p,\'mni\');quit;\" -nodisplay -nosplash -nodesktop'

#write matlab bash script to file
with open( cPath + '/Collate_Bootsamples.sh', "w") as text_file:
	text_file.write(matlab_script)	

#Submit matlab script on cluster.
subprocess.call(qsub_call + ' ' + cPath + '/Collate_Bootsamples.sh', shell=True)


