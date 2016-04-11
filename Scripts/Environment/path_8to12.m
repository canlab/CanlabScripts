% This script changes the matlabpath so that it includes spm12
% but not spm8. It assumes that both the spm8 and spm12 directories
% are contained within the same directory.

m_path=strsplit(path(),':');
spm8path_map= strfind(m_path,'spm8');
pathlength=length(m_path);

%This finds the spm8 path in the current matlab path
for i=1:pathlength
  if any(spm8path_map{i});
    spm8path=m_path{i};
    rmpath(spm8path)
  end
end

%Finding spm12
orig_dir=pwd(); %We'll need this later
cd(spm8path);
cd('../spm12'); % Assumes spm12 is in the same parent directory.
spm12path=pwd();
cd(orig_dir);

addpath(spm12path);

