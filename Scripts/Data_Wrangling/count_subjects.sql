-- Count all of the unique subjects
select count(distinct subject_id) from occasions
where (pilot=0 or pilot is null) and (bad_data=0 or bad_data is null) and (no_show=0 or no_show is null)

-- Count all behavioral subjects
select count(distinct subject_id) from occasions
where (pilot=0 or pilot is null) and (bad_data=0 or bad_data is null) and (no_show=0 or no_show is null)
and (fmri=0 or fmri is null)
and study_id in (1,2,3,4,5,8,9,10,11,12,13,14,15,16,17,19,20,21,24,25,27,28,30,31,32,33,37,38,39,40,41,42,43,45,47,50)

-- Count behavioral biomarker subjects
select count(distinct subject_id) from occasions
where (pilot=0 or pilot is null) and (bad_data=0 or bad_data is null) and (no_show=0 or no_show is null)
and (fmri=0 or fmri is null)
and study_id in (9,10,11,12,19,20,21,25,27,28,33,37,43)
and study_id>29

-- Count behavioral placebo subjects
select count(distinct subject_id) from occasions
where (pilot=0 or pilot is null) and (bad_data=0 or bad_data is null) and (no_show=0 or no_show is null)
and (fmri=0 or fmri is null)
and study_id in (8,13,14,15,16,17,24,27,30,31,32,33,38,39,40,41,42,43,45,50)

-- Count all fmri subjects
select count(distinct subject_id) from occasions
where (pilot=0 or pilot is null) and (bad_data=0 or bad_data is null) and (no_show=0 or no_show is null)
and (fmri=1 or fmri is null)
and study_id in (8,15,17,18,19,20,33,34,35,37,46,47,49)

-- Count all fmri subjects
select count(distinct subject_id) from occasions
where (pilot=0 or pilot is null) and (bad_data=0 or bad_data is null) and (no_show=0 or no_show is null)
and ((fmri=1 or fmri is null) and study_id in (8,15,17,18,19,20,33,34,35,37,46,47,49))

-- Count fmri biomarker subjects
select count(distinct subject_id) from occasions
where (pilot=0 or pilot is null) and (bad_data=0 or bad_data is null) and (no_show=0 or no_show is null)
and (fmri=1 or fmri is null)
and study_id in (18,19,20,33,37,46,49)
and study_id>29

-- Count fmri placebo subjects
select count(distinct subject_id) from occasions
where (pilot=0 or pilot is null) and (bad_data=0 or bad_data is null) and (no_show=0 or no_show is null)
and (fmri=1 or fmri is null)
and study_id in (8,15,17,19,34,35,49)