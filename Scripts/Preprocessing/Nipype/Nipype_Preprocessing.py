# This script will run preprocessing on the Columbia PTSD data set and serves as a template for all potential studies.
# See the ipython notebook for a description of everything and instructions on how to use it.
# Written by Luke Chang 9/14 luke.chang@colorado.edu

from nipype.interfaces import spm
import nipype.interfaces.io as nio		   # Data i/o
import nipype.interfaces.utility as util	 # utility
from nipype.pipeline.engine import Node, Workflow
from nipype.interfaces.base import BaseInterface, TraitedSpec, File, traits
import nipype.algorithms.rapidart as ra	  # artifact detection
from nipype.interfaces.nipy.preprocess import ComputeMask
import nipype.interfaces.matlab as mlab
import os
import nibabel as nib
from IPython.display import Image
import glob

# Specify various inputs files for pipeline
# spm_path = '/projects/ics/software/spm/spm8_r5236/'
spm_path = '/Users/lukechang/Documents/Matlab/spm8/'
canonical_file = spm_path + 'canonical/single_subj_T1.nii'
template_file = spm_path + 'templates/T1.nii'

# Set the way matlab should be called
# mlab.MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash -nojvm -noFigureWindows")
mlab.MatlabCommand.set_default_matlab_cmd("matlab -nodesktop -nosplash")
mlab.MatlabCommand.set_default_paths(spm_path)


###############################
## Functions
###############################

def get_n_slices(volume):
	import nibabel as nib
	nii = nib.load(volume)
	return nii.get_shape()[2]

def get_ta(tr, n_slices):
	return tr - tr/float(n_slices)

def get_slice_order(volume):
	import nibabel as nib
	nii = nib.load(volume)
	n_slices = nii.get_shape()[2]
	return range(1,n_slices+1)

def get_vox_dims(volume):
	import nibabel as nib
	if isinstance(volume, list):
		volume = volume[0]
	nii = nib.load(volume)
	hdr = nii.get_header()
	voxdims = hdr.get_zooms()
	return [float(voxdims[0]), float(voxdims[1]), float(voxdims[2])]

class Plot_Coregistration_Montage_InputSpec(TraitedSpec):
	wra_img = File(exists=True, mandatory=True) 
	canonical_img = File(exists=True, mandatory=True)
	title = traits.Str("Normalized Functional Check", usedefault=True)
	
class Plot_Coregistration_Montage_OutputSpec(TraitedSpec):
	plot = File(exists=True)

class Plot_Coregistration_Montage(BaseInterface):
	# This function creates a plot of an axial montage of the average normalized functional data 
	# with the spm MNI space single subject T1 overlaid. Useful for checking normalization
	input_spec = Plot_Coregistration_Montage_InputSpec
	output_spec = Plot_Coregistration_Montage_OutputSpec

	def _run_interface(self, runtime):
		import nibabel as nib
		from nilearn import plotting, datasets, image
		from nipype.interfaces.base import isdefined
		import numpy as np
		import pylab as plt
		import os
		
		wra_img = nib.load(self.inputs.wra_img)
		canonical_img = nib.load(self.inputs.canonical_img)
		title = self.inputs.title
		mean_wraimg = image.mean_img(wra_img)
		
		if title != "":
			filename = title.replace(" ", "_")+".pdf"
		else:
			filename = "plot.pdf"
		
		fig = plotting.plot_anat(mean_wraimg, title="wrafunc & canonical single subject", cut_coords=range(-40, 40, 10), display_mode='z')
		fig.add_edges(canonical_img)	 
		fig.savefig(filename)
		fig.close()
		
		self._plot = filename
		
		runtime.returncode=0
		return runtime
	
	def _list_outputs(self):
		outputs = self._outputs().get()
		outputs["plot"] = os.path.abspath(self._plot)
		return outputs
	
class PlotRealignmentParametersInputSpec(TraitedSpec):
	realignment_parameters = File(exists=True, mandatory=True)
	outlier_files = File(exists=True)
	title = traits.Str("Realignment parameters", usedefault=True)
	dpi = traits.Int(300, usedefault = True)
	
class PlotRealignmentParametersOutputSpec(TraitedSpec):
	plot = File(exists=True)

class PlotRealignmentParameters(BaseInterface):
	#This function is adapted from Chris Gorgolewski's code and generates a plot of the realignment parameters

	input_spec = PlotRealignmentParametersInputSpec
	output_spec = PlotRealignmentParametersOutputSpec
	
	def _run_interface(self, runtime):
		from nipype.interfaces.base import isdefined
		import numpy as np
		import pylab as plt
		import os
		realignment_parameters = np.loadtxt(self.inputs.realignment_parameters)
		title = self.inputs.title
		
		F = plt.figure(figsize=(8.3,11.7))
		F.text(0.5, 0.96, self.inputs.title, horizontalalignment='center')
		ax1 = plt.subplot2grid((2,2),(0,0), colspan=2)
		handles =ax1.plot(realignment_parameters[:,0:3])
		ax1.legend(handles, ["x translation", "y translation", "z translation"], loc=0)
		ax1.set_xlabel("image #")
		ax1.set_ylabel("mm")
		ax1.set_xlim((0,realignment_parameters.shape[0]-1))
		ax1.set_ylim(bottom = realignment_parameters[:,0:3].min(), top = realignment_parameters[:,0:3].max())
		
		ax2 = plt.subplot2grid((2,2),(1,0), colspan=2)
		handles= ax2.plot(realignment_parameters[:,3:6]*180.0/np.pi)
		ax2.legend(handles, ["pitch", "roll", "yaw"], loc=0)
		ax2.set_xlabel("image #")
		ax2.set_ylabel("degrees")
		ax2.set_xlim((0,realignment_parameters.shape[0]-1))
		ax2.set_ylim(bottom=(realignment_parameters[:,3:6]*180.0/np.pi).min(), top= (realignment_parameters[:,3:6]*180.0/np.pi).max())
		
		if isdefined(self.inputs.outlier_files):
			try:
				outliers = np.loadtxt(self.inputs.outlier_files)
			except IOError as e:
				if e.args[0] == "End-of-file reached before encountering data.":
					pass
				else:
					raise
			else:
				if outliers.size > 0:
					ax1.vlines(outliers, ax1.get_ylim()[0], ax1.get_ylim()[1])
					ax2.vlines(outliers, ax2.get_ylim()[0], ax2.get_ylim()[1])
		
		if title != "":
			filename = title.replace(" ", "_")+".pdf"
		else:
			filename = "plot.pdf"
		
		F.savefig(filename,papertype="a4",dpi=self.inputs.dpi)
		plt.clf()
		plt.close()
		del F
		
		self._plot = filename
		
		runtime.returncode=0
		return runtime
	
	def _list_outputs(self):
		outputs = self._outputs().get()
		outputs["plot"] = os.path.abspath(self._plot)
		return outputs

class Create_Covariates_InputSpec(TraitedSpec):	
	realignment_parameters = File(exists=True, mandatory=True) 
	spike_id = File(exists=True, mandatory=True)

class Create_Covariates_OutputSpec(TraitedSpec):
	covariates = File(exists=True)

class Create_Covariates(BaseInterface):
	# This function creates a matrix of the nuisance covariates used for the GLM.
	# Note that the output file has headers and also has NaNs that may need to be accounted for.
	input_spec = Create_Covariates_InputSpec
	output_spec = Create_Covariates_OutputSpec

	def _run_interface(self, runtime):
		import pandas as pd
		import numpy as np

		ra = pd.read_table(self.inputs.realignment_parameters, header=None, sep=r"\s*", names=['ra' + str(x) for x in range(1,7)])
		spike = pd.read_table(self.inputs.spike_id, header=None,names=['Spikes'])

		ra = ra-ra.mean() #mean center
		ra[['rasq' + str(x) for x in range(1,7)]] = ra**2 #add squared
		ra[['radiff' + str(x) for x in range(1,7)]] = pd.DataFrame(ra[ra.columns[0:6]].diff()) #derivative
		ra[['radiffsq' + str(x) for x in range(1,7)]] = pd.DataFrame(ra[ra.columns[0:6]].diff())**2 #derivatives squared

		#build spike regressors
		for i,loc in enumerate(spike['Spikes']):
			ra['spike' + str(i+1)] = 0
			ra['spike' + str(i+1)].iloc[loc] = 1

		filename = 'covariates.csv'
		ra.to_csv(filename, index=False) #write out to file
		self._covariates = filename

		runtime.returncode=0
		return runtime

	def _list_outputs(self):
		outputs = self._outputs().get()
		outputs["covariates"] = os.path.abspath(self._covariates)
		return outputs

	
def create_preproc_func_pipeline(data_dir=None, subject_id=None, task_list=None):

	###############################
	## Set up Nodes
	###############################

	#Setup Data Source for Input Data
	#	 data_dir = '/Users/lukechang/Dropbox/PTSD/Data/Imaging'
	#	 task_list = ['s1_r1Cond','s1_r1Ext','s1_r2Rec','s1_r2Ren']
	ds = Node(nio.DataGrabber(infields=['subject_id', 'task_id'], outfields=['func', 'struc']),name='datasource')
	ds.inputs.base_directory = os.path.abspath(data_dir + '/' + subject_id)
	ds.inputs.template = '*'
	ds.inputs.sort_filelist = True
	ds.inputs.template_args = {'func': [['task_id']], 'struc':[]}
	ds.inputs.field_template = {'func': 'Functional/Raw/%s/func.nii','struc': 'Structural/SPGR/spgr.nii'}
	ds.inputs.subject_id = subject_id
	ds.inputs.task_id = task_list
	ds.iterables = ('task_id',task_list)
	# ds.run().outputs #show datafiles

	# #Setup Data Sinker for writing output files
	# datasink = Node(nio.DataSink(), name='sinker')
	# datasink.inputs.base_directory = '/path/to/output'
	# workflow.connect(realigner, 'realignment_parameters', datasink, 'motion.@par')
	# datasink.inputs.substitutions = [('_variable', 'variable'),('file_subject_', '')]

	#Get Timing Acquisition for slice timing
	tr = 2
	ta = Node(interface=util.Function(input_names=['tr', 'n_slices'], output_names=['ta'],  function = get_ta), name="ta")
	ta.inputs.tr=tr

	#Slice Timing: sequential ascending 
	slice_timing = Node(interface=spm.SliceTiming(), name="slice_timing")
	slice_timing.inputs.time_repetition = tr
	slice_timing.inputs.ref_slice = 1

	#Realignment - 6 parameters - realign to first image of very first series.
	realign = Node(interface=spm.Realign(), name="realign")
	realign.inputs.register_to_mean = True

	#Plot Realignment
	plot_realign = Node(interface=PlotRealignmentParameters(), name="plot_realign")

	#Artifact Detection
	art = Node(interface=ra.ArtifactDetect(), name="art")
	art.inputs.use_differences	  = [True,False]
	art.inputs.use_norm			 = True
	art.inputs.norm_threshold	   = 1
	art.inputs.zintensity_threshold = 3
	art.inputs.mask_type			= 'file'
	art.inputs.parameter_source	 = 'SPM'
	
	#Coregister - 12 parameters, cost function = 'nmi', fwhm 7, interpolate, don't mask
	#anatomical to functional mean across all available data.
	coregister = Node(interface=spm.Coregister(), name="coregister")
	coregister.inputs.jobtype = 'estimate'

	# Segment structural, gray/white/csf,mni, 
	segment = Node(interface=spm.Segment(), name="segment")
	segment.inputs.save_bias_corrected = True
	
	#Normalize - structural to MNI - then apply this to the coregistered functionals
	normalize = Node(interface=spm.Normalize(), name = "normalize")
	normalize.inputs.template = os.path.abspath(template_file)

	#Plot normalization Check
	plot_normalization_check = Node(interface=Plot_Coregistration_Montage(), name="plot_normalization_check")
	plot_normalization_check.inputs.canonical_img = canonical_file
	
	#Create Mask
	compute_mask = Node(interface=ComputeMask(), name="compute_mask")
	#remove lower 5% of histogram of mean image
	compute_mask.inputs.m = .05
		
	#Smooth
	#implicit masking (.im) = 0, dtype = 0
	smooth = Node(interface=spm.Smooth(), name = "smooth")
	fwhmlist = [8]
	smooth.iterables = ('fwhm',fwhmlist)

	#Create Covariate matrix
	make_covariates = Node(interface=Create_Covariates(), name="make_covariates")
   
	###############################
	## Create Pipeline
	###############################

	Preprocessed = Workflow(name="Preprocessed")
	Preprocessed.base_dir = os.path.abspath(data_dir + '/' + subject_id + '/Functional')

	Preprocessed.connect([  
						(ds, ta, [(('func', get_n_slices), "n_slices")]),
						(ta, slice_timing, [("ta", "time_acquisition")]),
						(ds, slice_timing, [('func', 'in_files'),
											(('func', get_n_slices), "num_slices"),
											(('func', get_slice_order), "slice_order"),
											]),
						(slice_timing, realign, [('timecorrected_files', 'in_files')]),
						(realign, compute_mask, [('mean_image','mean_volume')]),
						(realign,coregister, [('mean_image', 'target')]),
						(ds,coregister, [('struc', 'source')]),
						(coregister,segment, [('coregistered_source', 'data')]),
						(segment, normalize, [('transformation_mat','parameter_file'),
											 ('bias_corrected_image', 'source'),]),
						(realign,normalize, [('realigned_files', 'apply_to_files'),
											 (('realigned_files', get_vox_dims), 'write_voxel_sizes')]),
						(normalize, smooth, [('normalized_files', 'in_files')]),
						(compute_mask,art,[('brain_mask','mask_file')]),
						(realign,art,[('realignment_parameters','realignment_parameters')]),
						(realign,art,[('realigned_files','realigned_files')]),
						(realign,plot_realign, [('realignment_parameters', 'realignment_parameters')]),
						(normalize, plot_normalization_check, [('normalized_files', 'wra_img')]),
						(realign, make_covariates, [('realignment_parameters', 'realignment_parameters')]),
						(art, make_covariates, [('outlier_files', 'spike_id')]),
					  ])
	return Preprocessed

###############################
## Script
###############################

# Create Pipeline for subject
sublist = sorted([x.split('/')[-1] for x in glob.glob(data_dir + '/subj*')])

#Run through list of subjects backwards (useful if you want to run two different nodes simultaneously forward and reverse)
for sub in reversed(sublist):
    #Glob Subject runs as they vary
    runlist = [x.split('/')[-1] for x in glob.glob(data_dir + '/' + sub + '/Functional/Raw/*')]
    Preprocessed = create_preproc_func_pipeline(data_dir=data_dir, subject_id = sub, task_list=runlist)

    print  data_dir + '/' + sub

    # Write out pipeline as a DAG
    Preprocessed.write_graph(dotfilename=data_dir + '/' + sub + "/Functional/Preprocessed_Workflow.dot.svg",format='svg')
#     Preprocessed.write_graph(data_dir + '/' + subject_id + "/Preprocessed_Workflow.dot.png")
#     Image(filename=data_dir + '/' + sub + "/Functional/Preprocessed_Workflow.dot.png")
    Preprocessed.run(plugin='MultiProc', plugin_args={'n_procs' : 12}) 
#     Run on workstation in parallelPreprocessed.run(plugin='PBS') #Run on Blanca in parallel


