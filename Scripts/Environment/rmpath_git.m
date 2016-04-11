% This script removes all files in .git directories from the malabpath,
% as these give lots of irritating error messages when matlab starts up.

m_path=strsplit(path(),':');
gitpath_map= strfind(m_path,'.git');
pathlength=length(m_path);

%Finding the spm12 directory in the current matlab path
 for i=1:pathlength
   if any(gitpath_map{i});
     rmpath(m_path{i});
   end
 end

savepath;
