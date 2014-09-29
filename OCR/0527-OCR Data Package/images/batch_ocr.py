#!/bin/env python

import glob
import os
import subprocess
import sys
import time

SIZES = [
    #(1.0, 'tif'),
    #(0.9, 'tif-0.9'), 
    #(0.8, 'tif-0.8'),
    #(0.7, 'tif-0.7'),
    #(0.6, 'tif-0.6'),
    #(0.5, 'tif-0.5'),
    #(0.4, 'tif-0.4'),
    #(0.3, 'tif-0.3'),
    (0.2, 'tif-0.2'),
]

OUTPUT_PATH='output_batch_ocr.csv'

def run_set(csv, sizeTuple):
    scale = sizeTuple[0]
    ipath = sizeTuple[1]
    
    matchingFiles = glob.glob(os.path.join(ipath, '*.tif'))
    filesetSize   = len(matchingFiles)
    
    fileIndex = 1
    # Loop over each file
    for img_path in matchingFiles:
        # Print progress (without newline)
        sys.stdout.write("%3d/%3d: " % (fileIndex, filesetSize))
        sys.stdout.flush()
        fileIndex += 1
        
        # Extract file name from path
        img_file = img_path.split(os.path.sep)[-1]
        # Create path of truth text file
        img_base = '.'.join(img_file.split('.')[0:-1])
        txt_name = "%s.txt" % img_base
        txt_path = os.path.join('txt', txt_name)
        
        # Start Timer
        tic = time.time()
        
        # Call get_accuracy.py
        cmd = ['python', 'get_accuracy.py', img_path, txt_path]
        sub = subprocess.Popen(cmd, stdout = subprocess.PIPE)
        std = sub.communicate()
        out = std[0].strip()
        
        # End Timer
        toc = time.time()
        
        # Calculate time delta
        time_delta = toc - tic;
        
        # Check returncode
        if(sub.returncode != 0):
            print("error: get_accuracy returned %d -- cmd: %s" % (sub.returncode, ' '.join(cmd)))
            sys.exit(1)
        
        # Build entry row list
        lst = [img_base, scale, os.path.getsize(img_path), out, time_delta]
        row = ', '.join([str(i) for i in lst])
        
        # Display results
        print(row)
        
        # Write results to file
        csv.write(row)
        csv.write('\n')
        

if __name__ == "__main__":
    # Check whether the output file exists
    if(os.path.exists(OUTPUT_PATH)):
        print("error: output file [%s] exists.  (re)move it and re-run this script." % OUTPUT_PATH)
        exit(2)
    
    # Loop through the sizes, callling subfunction run_set for each
    with open(OUTPUT_PATH, 'w') as csv:
        for size in SIZES:
            run_set(csv, size)
            print("Done set: %s" % size[0])
            sys.exit()
            