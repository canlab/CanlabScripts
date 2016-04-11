% This script changes the matlabpath so that it includes spm8
% but not spm12. It assumes that both the spm8 and spm12 directories
% are contained within the same directory. 

m_path=strsplit(path(),':');
spm12path_map= strfind(m_path,'spm12');
pathlength=length(m_path);

%Finding the spm12 directory in the current matlab path
for i=1:pathlength
  if any(spm12path_map{i});
    spm12path=m_path{i};
    rmpath(spm12path);
  end
end

orig_dir=pwd();
cd(spm12path);
% This assumes that spm8 and spm12 have the same parent directory.
cd('../spm8'); 
spm8path=pwd();
cd(orig_dir);

addpath(spm8path);
savepath;%Permanently saves the new path.

