% this function is based on Yoni Ashar's make_nuisance_covs_from_fmriprep_output2020 function
%
% this function takes a confounds file generated by fmriprep for one run
% and creates a nuisance covariate matrix with the following regressors:
%
% :Usage:
%       [nuis_matrix, n_spike_regs, n_spike_regs_percent] = make_nuisance_covs_from_fmriprep_output(fmriprep_confounds_fname, TR, FD_spike_cutoff, spike_additional_vols, ndummies, fast_TR, varargin)
%
% 1) spikes for framewise displacement > .25mm. If fast_TR = true, Head Motion Parameter Estimates (HMPs) are filtered
%    according to Power 2019 and back-computed to ~2 seconds back, rather than 1 frame back
% 2) spikes for DVARS std_dvars > 1.5. If fast_TR = true, disabled -- DVARS not a good indicator of motion in fastTR data (Power 2019)
% 3) number of volumes to flag following the spikes identified in #1 and #2 above. n = spike_additional_vols
% 4) 24 motion covs (based on unfiltered HMPs): HMPs, diff(HMPs), squared HMPs, squared diffs
% 5) optional regressors, as specified below
%
%
% :Inputs:
%
%
%   **FD_spike_cutoff:**
%        Threshold for determining framewise displacement-based spikes. By
%        convention, for resting state scans, .2 is considered strict and
%        .5 is considered liberal
%
%   **spike_additional_vols:**
%        How many additional vols to flag following the spike
%
% :Optional inputs:
%
%   **ndummies:**
%        Followed by how many initial vols to drop from the cov matrix. 
%        These volumes should get dropped from fMRI data elsewhere)
%
%   **fastTR:**
%        If fastTR, modifying spike regressor calculation according to
%        Power 2019 for fast TRs.
%
%   **dvars:**
%       Using the standardized derivative of RMS variance over voxels (or DVARS) [Power2012] to determine spikes.
%       Followed by the cutoff. 1.5 might be a suitable one (https://fmriprep.org/en/stable/outputs.html)
%
%   ** Pass in 'csf' 'wm' 'gs' 'aCompCor' or 'tCompCor' for: avg CSF signal, avg WM signal, global signal, six anatomical CompCor components, six temporal CompCor components 
%
%  
%
% output: the nuisance covariate matrix defined above, how many spikes detected, 
%             what % of vols flagged as spikes, TR labelled as spikes,
%             and FD for each TR
%
% Note: Variables and labels must be as specified in fmriprep output circa
% 2020.  Check and verify that it's working for you!
%
% -- Yoni Ashar, July 2020
%
% 12/24/2021: Feng Zhou fixed a bug related to the calculation of FD,
%             shift ndummies, fastTR, and DVARS based spikes to optional inputs, 
%             and used std_dvars instead of zscore(dvars) to identify dvars based spikes

function [nuis_matrix, n_spike_regs, n_spike_regs_percent, allspikes, fd] = make_nuisance_covs_from_fmriprep_output(fmriprep_confounds_fname, TR, FD_spike_cutoff, spike_additional_vols, varargin)

if FD_spike_cutoff < .2 || FD_spike_cutoff > .7
    warning('Atypical FD spike cutoff chosen. See documentation');
end

gs = false; wm = false; csf = false; aCompCor = false; tCompCor = false; fast_TR = false; dvars = false; ndummies = 0;
for i = 1:length(varargin)
    if ischar(varargin{i})
        switch varargin{i}
            case 'gs'
                gs = true;
            case 'wm'
                wm = true;
            case 'csf'
                csf = true;
            case 'aCompCor'
                aCompCor = true;
            case 'tCompCor'
                tCompCor = true;
            case 'fastTR'
                fast_TR = true;
            case 'dvars'
                dvars = true; dvars_spike_cutoff = varargin{i + 1};
            case 'ndummies'
                ndummies = varargin{i + 1};
        end
    end
end



% disp('You have chosen the following options:');
% gs, wm, csf, aCompCor, tCompCor, antpost

R = readtable(fmriprep_confounds_fname, 'TreatAsEmpty', 'n/a', 'filetype', 'text');

R = R(ndummies+1:end,:);

% compute 24 motion regs
mot_names = {'trans_x','trans_y','trans_z','rot_x','rot_y','rot_z'};
motion = R{:,mot_names};
diffs = [zeros(1,6); diff(motion)];
mo_sq = motion .^ 2;
mo_sq_diff = [zeros(1,6); diff(mo_sq)];
motion24 = [motion diffs mo_sq mo_sq_diff];



% --- DEFINE OUTLIERS / SPIKES --- %

% FD-based spikes. First, compute FD following Power 2019
motion(:,4:6) = (motion(:,4:6) / (2*pi)) * 100 * pi; % fraction of circle (radians / 2pi) * diameter (pi*d).   convert rotation to mm. assume head is 50mm sphere (Power et al 2012)

if fast_TR % filter and compare to ~2sec prev rather than framewise
    fd = filtFD(motion, TR);
else    
    fd = sum(abs(diff(motion)),2);
    fd = [0; fd];
end

% define spikes based off FD
FD_spikes = fd > FD_spike_cutoff;

% DVARS based spikes -- Z > 3. Omit first vol and replace w/ 0 (=unflagged)
% dvars_spikes = [0; zscore(R.dvars(2:end)) > 3];
if dvars
    dvars_spikes = [0; R.std_dvars(2:end) > dvars_spike_cutoff];
else
    dvars_spikes = zeros(size(FD_spikes));
end

if fast_TR
    dvars_spikes = zeros(size(FD_spikes)); % DVARS is not a reliable indicator of motion in fast-TR data -- Power 2019. force to 0.
end

% combine all my spikes
allspikes = FD_spikes | dvars_spikes; 

% add additional spike vols for vols following the spike. If
% spike_additional_vols is zero, nothing happens, as desired.
origspikes = find(allspikes);
for k=1:length(origspikes) % Iterate over spikes
origspike_k = origspikes(k);
    for i=1:spike_additional_vols % Iterate over additional vols
        if origspike_k+i <= length(allspikes) % dont make a spike past the end
            allspikes(origspike_k+i) = 1;
        end
    end
end

% make into 0/1 spike regressors
allspikes = find(allspikes);
spikes_regs = zeros(height(R), length(allspikes));

for i=1:length(allspikes)
    spikes_regs(allspikes(i),i) = 1;
end

% -- CREATE NUIS MATRIX W/ MOTION, SPIKES, CSF, GS
% note that GS is from within the brain mask, as computed w/ fMRIprep
% use zscore to keeps all signals (also e.g., linear trend) on similar scales
nuis_matrix = [motion24 spikes_regs];

if gs, nuis_matrix = [nuis_matrix zscore(R.global_signal)]; end
if csf, nuis_matrix = [nuis_matrix zscore(R.csf)]; end
if wm, nuis_matrix = [nuis_matrix zscore(R.white_matter)]; end
if aCompCor
    whcol = ~cellfun(@isempty, strfind(R.Properties.VariableNames, 'a_comp_cor'));
    nuis_matrix = [nuis_matrix zscore(R{:,whcol})]; 
end
if tCompCor
    whcol = ~cellfun(@isempty, strfind(R.Properties.VariableNames, 't_comp_cor'));
    nuis_matrix = [nuis_matrix zscore(R{:,whcol})]; 
end
    

% compute and output how many spikes total
n_spike_regs = length(allspikes);
n_spike_regs_percent = 100*n_spike_regs / height(R);


end


% filters out pseudomotion freq from HMPs (see Power et al 2019) and
% computes FD wrt to about 2 sec prev
function [fd, motion6] = filtFD(motion6, TR)

    % filter all the HMPs
    nyq = (1/TR)/2;
    stopband = [.1 .5];
    [B, A] = butter(10, stopband/nyq, 'stop');

    for i=1:6
        motion6(:,i) = filtfilt(B,A,motion6(:,i));
    end

    % compute how many vols previous will equal 2-3 sec time lag -- See
    % Power et al 2019
    diff_distance = ceil(2/TR);
    
    % compute diffs wrt to 5 vols previous
    diffs = motion6 - circshift(motion6, diff_distance); % this is incorrect for the initial vols; set to zero on next line
    diffs(1:diff_distance, :) = 0;
    
    fd = sum(abs(diffs),2);
    
end