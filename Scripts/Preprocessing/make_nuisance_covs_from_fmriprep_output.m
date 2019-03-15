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
% raw data, spikes for initial volumes (5 sec), DVARS / RMSQ, framewise displacement.  We decided _not_ to
% include WM signal, as this often can contain BOLD signal of neuronal
% origin.  -- Yoni Ashar

function [Rfull, Rselected] = make_nuisance_covs_from_fmriprep_output(fmriprep_confounds_fname, raw_img_fname, TR)

confound_fname_csv = [fmriprep_confounds_fname(1:end-3) 'csv']; % replace tsv with csv
copyfile(fmriprep_confounds_fname, confound_fname_csv); % dumb hack to appease matlab -- readtable will only work with .csv, not .tsv
R = readtable(confound_fname_csv, 'TreatAsEmpty', 'n/a');

regs = R.Properties.VariableNames;

% replace NaNs in first row with Os
wh_replace = ismissing(R(1,:));
if any(wh_replace)
    R{1, wh_replace} = zeros(1, sum(wh_replace)); 
end


% find motion cols
motion_cols = contains(regs,'rot') | contains(regs,'trans') | contains(regs,'diff'); 

if sum(motion_cols) < 24 % have not yet computed diffs and squared diffs
    
    % compute squared, diffs, and squared diffs of motion
    R.trans_x_sq = R.trans_x .^ 2; R.trans_y_sq = R.trans_y .^ 2; R.trans_z_sq = R.trans_z .^ 2;
    R.rot_x_sq = R.rot_x .^ 2; R.rot_y_sq = R.rot_y .^ 2; R.rot_z_sq = R.rot_z .^ 2;

    R.diffX = [0; diff(R.rot_x)]; R.diffY = [0; diff(R.rot_y)]; R.diffZ = [0; diff(R.rot_z)];
    R.diffRotX = [0; diff(R.rot_x)]; R.diffRotY = [0; diff(R.rot_y)]; R.diffRotZ = [0; diff(R.rot_z)];

    R.diffXsq = R.diffX .^ 2; R.diffy_sq = R.diffY .^ 2; R.diffz_sq = R.diffZ .^ 2;
    R.diffRotXsq = R.diffRotX .^ 2; R.diffRoty_sq = R.diffRotY .^ 2; R.diffRotz_sq = R.diffRotZ .^ 2;

    % find updated motion cols
    motion_cols = contains(regs,'rot') | contains(regs,'trans') | contains(regs,'diff'); 
    
elseif sum(motion_cols) > 24
    error('Too many motion columns?!')
else
    % we have 24 regs -- motion cols already computed. do nothing.
end

% add spikes for initial volumes. can "redo" this if already exists; not a
% problem
nvols = round(5/TR);  % first 5 seconds
R.initial_vols = zeros(height(R),1);
R.initial_vols(1:nvols) = ones(nvols,1);

% find spike cols
spike_cols = contains(regs,'nuisance_covs'); 

if sum(spike_cols) == 0 % have not yet computed and added these

    % add in canlab spike detection (Mahalanobis distance)
    [g, spikes, gtrim, nuisance_covs, snr] = scn_session_spike_id(raw_img_fname, 'doplot', 0);

    nuisance_covs = nuisance_covs{1};
    nuisance_covs(:,1) = []; %drop gtrim 
    R = [R array2table(nuisance_covs)];

    % find updated spike cols
    spike_cols = contains(regs,'nuisance_covs'); 

end


Rfull = R;

% Select reasonable subset
Rselected = R(:,motion_cols | spike_cols);
Rselected.dvars = R.dvars;
Rselected.framewise_displacement = R.framewise_displacement;
Rselected.csf = R.csf;

% write back to file
writetable(R, confound_fname_csv);
movefile(confound_fname_csv, fmriprep_confounds_fname); % revert to .tsv to appease BIDS spec


end