#!/bin/bash

INPUT_TYPE=tif
RESIZE_SCALE=0.9
RESIZE_PCT="90%"

INPUT_DIR=./${INPUT_TYPE}/*
OUTPUT_DIR=./${INPUT_TYPE}-${RESIZE_SCALE}

for iname in ${INPUT_DIR} ; do
    oname=${OUTPUT_DIR}/$(basename $iname)
    echo ${iname} - ${oname}
    convert ${iname} -scale ${RESIZE_PCT} ${oname}
done