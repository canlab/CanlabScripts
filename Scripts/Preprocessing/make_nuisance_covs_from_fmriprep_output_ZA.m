% this function takes a confounds file generated by fmriprep, selects some 
% desired regressors, and computes and adds some other desired regressors.
% It returns a matrix of all possible nuisance regressors, as well as a 
% matrix of a reasonable subset of regressors decided up on in lab mtg -- see below.
%
% This function also saves the output back to the fmriprep confounds file,
% so they can stay with the dataset. If the regressors it is looking for
% are already in the fmriprep confounds file, this script assumes this function was already
% run and so it does not regenerate them, and just returns what was in the
% file.
%
% in a Jan 2019 Wager lab mtg, we decided that its sensible to include the
% following in a 1st level model for task data: 24 motion regressors, CSF
% (esp. a degraded/conservative CSF mask), canlab spike detection on the
% raw data, spikes for initial volumes (5 sec), spikes as determined by DVARS / RMSQ (Zscore > 2.5), framewise displacement.  We decided _not_ to
% include WM signal, as this often can contain BOLD signal of neuronal
% origin.  -- Yoni Ashar
%
% Adding inputs and code for extending the number of images affected by the
% scn_spike_detection script. Based on Power (2019), we're assuming that
% TR's immediately following a transient signal spike will be affected and
% should therefore be filtered in a similar manner to the spike itself. If
% the 'spike_additional_vols' variable is left blank, script will proceed
% as it did before, generating nuisance regressors identifying only the
% original spikes.
% --Zach Anderson (4/19/19)

function [Rfull, Rselected, n_spike_regs, n_spike_regs_percent, FD] = make_nuisance_covs_from_fmriprep_output(fmriprep_confounds_fname, raw_img_fname, TR, spike_additional_vols)

R = readtable(fmriprep_confounds_fname, 'TreatAsEmpty', 'n/a', 'filetype', 'text');

% replace NaNs in first row with Os
wh_replace = ismissing(R(1,:));
if any(wh_replace)
    R{1, wh_replace} = zeros(1, sum(wh_replace)); 
end


% compute 24 motion regs
mot_names = {'trans_x','trans_y','trans_z','rot_x','rot_y','rot_z'};
motion = R{:,mot_names};
diffs = [zeros(1,6); diff(motion)];
mo_sq = motion .^ 2;
mo_sq_diff = [zeros(1,6); diff(mo_sq)];
motion18 = [diffs mo_sq mo_sq_diff];

mot_names18 = [cellfun( @(x) [x '_diff'], mot_names, 'UniformOutput',false) cellfun( @(x) [x '_sq'], mot_names, 'UniformOutput',false) cellfun( @(x) [x '_sq_diff'], mot_names, 'UniformOutput',false) ];

motion18 = array2table(motion18, 'VariableNames', mot_names18);
%head(motion18)
    
% remove previously saved motion cols 1) in case there was an error, and 2)
% so i can re-add them without conflict
R(:,contains(R.Properties.VariableNames, 'diff')) = [];
R(:,contains(R.Properties.VariableNames, 'sq')) = [];

% add them in
R = [R motion18];


% add spikes for initial volumes. can "redo" this if already exists; not a
% problem
nvols = round(5/TR);  % first 5 seconds
R.initial_vols = zeros(height(R),1);
R.initial_vols(1:nvols) = ones(nvols,1);

% first remove old nuisance variables that we don't want anymore.    
% find spike cols
%if sum(spike_cols) ~= 0
spike_cols = contains(R.Properties.VariableNames,'nuisance_covs'); 
R(:,spike_cols) = [];
%end


%if sum(spike_cols) == 0 % have not yet computed and added these
    % add in canlab spike detection (Mahalanobis distance)
    %[g, spikes, gtrim, nuisance_covs, snr] = scn_session_spike_id(raw_img_fname, 'doplot', 0);
    % add in canlab spike detection (Mahalanobis distance)
    % TRs
    %nuisance_covs = nuisance_covs{1};
    %nuisance_covs(:,1) = []; %drop gtrim 
    %R = [R array2table(nuisance_covs)];
    % find updated spike cols
    %spike_cols = contains(R.Properties.VariableNames,'nuisance_covs'); 
%else
    
    % recreate nuisance_covs and spikes variables for later use
    %nuisance_covs = R{:,spike_cols};
    %spikes{1} = find(sum(nuisance_covs,2)); % TODO: this will only work for single session data!
%end

% make spike regs from dvars. we dont expect a reliable signal in the brain
% that tracks dvars, so less sensible to include as a parametric regressor.
% better to use to identify outliers
dvarsZ = [ 0; zscore(R.std_dvars(2:end))]; % first element of dvars always = 0, drop it from zscoring and set it to Z=0
dvars_spikes = find(dvarsZ > 3); % arbitrary cutoff -- Z > 2.5
    
% make regs from spike indices
dvars_spikes_regs = zeros(height(R),length(dvars_spikes));
for i=1:length(dvars_spikes)
    dvars_spikes_regs(dvars_spikes(i),i) = 1;
end

% find dvars_spike_regs that are non-redundant with mahal spikes, and
% include them. compare TRs at which spike happens
%same = ismember(dvars_spikes, find(sum(R{:,spike_cols},2)));
%dvars_spikes_regs(:,same) = []; % drop the redundant ones

% remove any previous dvars_spikes_regs, and add the ones i just made
dvars_cols = contains(R.Properties.VariableNames,'dvars_spikes'); 
R(:,dvars_cols) = [];
dvars_spikes_regs = array2table(dvars_spikes_regs);
R = [R dvars_spikes_regs];

%calculate framewise displacement as a function of user specified number of
%TRs


ind = find(endsWith(R.Properties.VariableNames, 'x'));% trans_x always the first motion col
wh = ind:(ind+5); % the 6 basic motion regs
motion6 = R{:,wh};
motion6(:,4:6) = sin(.5 * motion6(:,4:6)) * 50 * 2; % convert rotation to mm. assume head is 50mm sphere (Power et al 2012)            else
fd_5TRs = motion6 - circshift(motion6, 5); % this is incorrect for the initial vols, but they get dropped anyways 
fd_5TRs = sum(abs(fd_5TRs), 2);
FD5_spikes = find(fd_5TRs>.25);
FD5_spikes_regs = zeros(height(R), length(FD5_spikes));

for i=1:length(FD5_spikes)
    FD5_spikes_regs(FD5_spikes(i),i)=1;
end

FD5_cols = contains(R.Properties.VariableNames,'FD5_spikes');
R(:,FD5_cols) = [];
FD5_spikes_regs = array2table(FD5_spikes_regs);
R = [R FD5_spikes_regs];

%plot(fd_5TRs); hold on; plot(R.framewise_displacement); legend({'fd_5TRs', 'FD'})

% Motion can create artifacts lasting longer than the single image we
% usually account for using spike id scripts. we're also going to flag the
% following TRs, the number of which is defined by the user. If
% 'spike_additional_vols' remains unspecified, everything will proceed as
% it did before, meaning spikes will be identified and flagged in the
% creation of nuisance regressors without considering the following TRs
% Add them if user requested, for both nuisance_covs and dvars_spikes_regs

if exist('spike_additional_vols')
        
    % concatenate generated spike nuisance covs and also dvars regs. We
    % would like to flag subsequent TR's with respect to both of these
    % measures.
    nuisance_covs_with_timing_adjustment = [table2array(dvars_spikes_regs),table2array(FD5_spikes_regs)];
    spikes = [dvars_spikes;FD5_spikes];
    nuisance_covs_additional_spikes = zeros(length(nuisance_covs_with_timing_adjustment),length(spikes)*spike_additional_vols);
    
    % This loop will create a separate column with ones in each row (TR) 
    % we would like to consider a nuisance regressor
    % Performs this function for dvars and spikes. From now on we'll
    % consider the two as a single set of regressors
    for i = 1:length(spikes) 
        nuisance_covs_additional_spikes(spikes(i)+1 : spikes(i)+spike_additional_vols,(i*spike_additional_vols-(spike_additional_vols-1)):(i*spike_additional_vols)) = eye(spike_additional_vols);
    end

    % if any spikes went beyond the end, trim it down
    nuisance_covs_additional_spikes = nuisance_covs_additional_spikes(1:height(R),:);

    % Add the additional spikes to the larger covariance matrix
    % if any already exist, drop them first
    additional_spike_cols = contains(R.Properties.VariableNames,'nuisance_covs_additional_spikes'); 
    if any(additional_spike_cols), R(:,additional_spike_cols) = []; end
    R = [R array2table(nuisance_covs_additional_spikes)];
end



% this loop will remove redundant spike regressors
regs = R.Properties.VariableNames;
dvars_cols = contains(regs,'dvars_spikes'); 
FD5_cols = contains(regs,'FD5_spikes');
%spike_cols = contains(regs,'nuisance_covs'); 
additional_spike_cols = contains(regs,'nuisance_covs_additional_spikes'); 

[duplicate_rows, ~] = find(sum(R{:, dvars_cols | FD5_cols | additional_spike_cols}, 2)>1); %The above loop will result in some overlap. We don't want one TR to be represented by multiple columns in the nuisance regressor matrix
for duplicates = 1:length(duplicate_rows) %This loop sets duplicate values to zero; drops them later -- keep indices the same
    [~,curr_cols] = find(R{duplicate_rows(duplicates),:}==1);
    first_instance = min(curr_cols);
    R{duplicate_rows(duplicates), first_instance+1:size(R,2)} = 0;
end
%R = R(1:length(nuisance_covs_with_timing_adjustment), any(table2array(R)));

% Select a subset of regressors to return for use in GLM to return to user
regs = R.Properties.VariableNames;
dvars_cols = contains(regs,'dvars_spikes'); 
FD5_cols = contains(regs,'FD5_spikes'); 
motion_pattern = ['x','y','z'];
motion_cols = contains(regs,'rot') | contains(regs,motion_pattern) | contains(regs,'diff'); 
%additional_spike_cols = contains(regs,'nuisance_covs_additional_spikes'); 

n_spike_regs = sum(dvars_cols | FD5_cols); %| additional_spike_cols)
n_spike_regs_percent = n_spike_regs / height(R);

Rselected = R(:,motion_cols | dvars_cols | FD5_cols);% | additional_spike_cols);
Rselected.FramewiseDisplacement = R.framewise_displacement;
Rselected.CSF = R.csf;
FD = R.framewise_displacement;

% write back to file
writetable(R, fmriprep_confounds_fname, 'filetype', 'text');

Rfull = R;
end