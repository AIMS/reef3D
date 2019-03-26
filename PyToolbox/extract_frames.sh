#!/usr/bin/env bash


cd $1

for fname in *.*; do
    for vname in *.MP4; do
        ffmpeg -i "$fname/$vname" -qscale:v 2 -ss 6 -movflags use_metadata_tags -vf "fps=4" "${vname:0:2}"_"$fname"_V"${vname:9:2}"_%04d.jpg
    done
done 

