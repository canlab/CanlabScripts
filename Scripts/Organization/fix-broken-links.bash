#!/usr/bin/env bash

for link in $@;
do
    linktarget=$(readlink $link);
    if [ -f $linktarget]; then 
	echo $linktarget is a valid link
    else
	newtarget=$(echo $linktarget | sed 's/\/dreamio.*Analyses\///g')
	echo rm $link
	echo gln -s $newtarget `basename "$link"` -t `dirname $link`
    fi
done
