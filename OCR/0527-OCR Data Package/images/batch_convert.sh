#!/bin/bash

INPUT_TYPE=tif
OUTPUT_TYPE=jpg

INPUT_DIR=./${INPUT_TYPE}/*
OUTPUT_DIR=./${OUTPUT_TYPE}

for iname in $INPUT_DIR ; do
    oname=${OUTPUT_DIR}/$(basename ${iname%.*}.${OUTPUT_TYPE})
    echo $iname
    echo $oname
    convert $iname $oname
done