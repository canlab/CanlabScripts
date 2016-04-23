#!/usr/local/bin/fish

find /Volumes/engram/labdata/projects/r21stress/BOLD -type d -name 'qc_images' > dirnames.txt

set -l dirnames (cat dirnames.txt)
set -l length (count $dirnames)

echo $local

for index in (seq $length)
	set -l subname (basename (dirname $dirnames[$index]) )
	echo $subname
	mkdir -p qc_images/$subname
	cp -r $dirnames[$index]/* qc_images/$subname
	pushd qc_images/$subname
	for file in *
		mv $file {$subname}_{$file}
	end
	popd
end

tar -czf qc_images.tar.gz qc_images

