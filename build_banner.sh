#!/bin/bash

prefix=banner_${RANDOM}

convert 'covid19-vaccine-registration-guide-qatar-english.pdf[0]' ${prefix}_en.jpg
convert 'covid19-vaccine-registration-guide-qatar-urdu.pdf[0]' ${prefix}_ur.jpg
convert 'covid19-vaccine-registration-guide-qatar-tamil.pdf[0]' ${prefix}_ta.jpg
convert 'covid19-vaccine-registration-guide-qatar-sinhala.pdf[0]' ${prefix}_si.jpg
convert 'covid19-vaccine-registration-guide-qatar-hindi.pdf[0]' ${prefix}_hi.jpg

convert ${prefix}_en.jpg -crop 250x300+42+40 -border 5x10 -bordercolor white ${prefix}_en.jpg
convert ${prefix}_ur.jpg -crop 250x300+303+40 -border 5x10 -bordercolor white ${prefix}_ur.jpg
convert ${prefix}_ta.jpg -crop 250x300+42+40 -border 5x10 -bordercolor white ${prefix}_ta.jpg
convert ${prefix}_si.jpg -crop 250x300+42+40 -border 5x10 -bordercolor white ${prefix}_si.jpg
convert ${prefix}_hi.jpg -crop 250x300+42+40 -border 5x10 -bordercolor white ${prefix}_hi.jpg

convert ${prefix}_en.jpg ${prefix}_ur.jpg ${prefix}_ta.jpg ${prefix}_si.jpg ${prefix}_hi.jpg +append banner.jpg
convert banner.jpg -border 5x -bordercolor white banner.jpg

rm ${prefix}_en.jpg ${prefix}_ur.jpg ${prefix}_ta.jpg ${prefix}_si.jpg ${prefix}_hi.jpg
open banner.jpg