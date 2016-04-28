load BMRK5_FreeAssoc_MturkRatings.mat

N=subject;
vm=valence_mean;
clear valence_totals;
clear valence_numbers;
clear added_subjects;
valence_totals{1}=0;
valence_numbers{1}=0;
added_subjects{1}=subject(1);
subject_counters{1}=0;
subject_index=1;
subject_counter=1;

for i=1:length(N)
  if any(find(cell2mat(added_subjects)==subject(i)))
    subject_index=find(cell2mat(added_subjects)==subject(i));
  else
    subject_counter=subject_counter+1;
    added_subjects{subject_counter}=subject(i);
    subject_index=subject_counter;
    valence_totals{subject_counter}=0;
    valence_numbers{subject_counter}=0;
  end
  if isnan(vm(i))
    fprintf('NaN at index %d in subject %d...\n',i,N(i));
  else
    valence_totals{subject_index}=valence_totals{subject_index} + vm(i);
    valence_numbers{subject_index}=valence_numbers{subject_index} +1;
  end
end

subj_list=cell2mat(added_subjects)
avg_list=cell2mat(valence_totals) ./ cell2mat(valence_numbers)

varlist={'N', 'vm', 'subject_counters', 'subject_index', 'subject_counter', 'added_subjects', 'valence_totals', 'valence_numbers','i'};
clear(varlist{:});
clear varlist;
