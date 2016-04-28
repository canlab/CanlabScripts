load DB.mat

N=DB.N;
paintouch=DB.Pain_Touch;
Contrast=DB.Contrast;

pain=0;
touch=0;
both=0;
repeated=0;
added_contrasts={-1};
contrast_index=1;

for i=1:length(N)
  if any(find(cell2mat(added_contrasts)==Contrast(i)))
    repeated=repeated+1;
    continue
  else
    added_contrasts{contrast_index}=Contrast(i);
    contrast_index=contrast_index+1;
    if strcmp(paintouch(i), 'Pain')
      pain = pain + N(i);
    elseif strcmp(paintouch(i), 'Touch')
      touch= touch + N(i);
    else
      both=both+N(i);
    end
  end
end

pain
touch
both
repeated
