#!/bin/bash

module add freesurfer

pushd /work/ics/projects/auto_analysis/blanca_analysis/human/twager/olp4cbp_200097/AUTO_ANALYSIS/prisma_fit

for d in M*/ ; do
    printf $d*/analysis/fs_5.3/M*/surf
    printf "\n"
    cd /work/ics/projects/auto_analysis/blanca_analysis/human/twager/olp4cbp_200097/AUTO_ANALYSIS/prisma_fit/$d*/analysis/fs_5.3/M*/surf
    if [ ! -d /projects/jdclark/brain_stls/$d ]; then
        mkdir /projects/jdclark/brain_stls/$d
        cp ./rh.pial /projects/jdclark/brain_stls/$d
	cp ./lh.pial /projects/jdclark/brain_stls/$d
	cd /projects/jdclark/brain_stls/$d
	mris_convert rh.pial rh.stl
	mris_convert lh.pial lh.stl
    fi
done

popd