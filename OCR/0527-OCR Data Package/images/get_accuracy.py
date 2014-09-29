#!/bin/env python

import sys
import tempfile
import subprocess
import time

if __name__ == "__main__":
    # Ensure we got 2 arguments
    if(len(sys.argv) != 3):
        print("usage: %s  IMAGE_FILE  TEXT_FILE" % sys.argv[0])
        sys.exit(1)
    
    img_path = sys.argv[1]
    txt_path = sys.argv[2]
    
    # Create Named Temporary File for Tesseract output
    with tempfile.NamedTemporaryFile(suffix=".txt") as tf:
        # Tesseract expects a "base" name, so strip the .txt
        tmp_path = tf.name
        tmp_base = tf.name[0:-4]
        # Run Tesseract
        cmd_tess = ['tesseract', img_path, tmp_base]
        sub_tess = subprocess.Popen(cmd_tess, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_tess = sub_tess.communicate()
        # Ensure Tesseract didn't error out
        if(sub_tess.returncode != 0):
            print("error: tesseract returned %d -- cmd: %s" % (sub_tess.returncode, ' '.join(cmd_tess)))
            sys.exit(2)
        
        # Run wdiff
        cmd_wdiff = ['wdiff', '-s', '-1', '-2', '-3', tmp_path, txt_path]
        sub_wdiff = subprocess.Popen(cmd_wdiff, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out_wdiff = sub_wdiff.communicate()
        # Ensure wdiff didn't error out 
        # nb wdiff seems to have a weird return value:
        #       0 when it completes successfully and the files match
        #       1 when it completes successfully but the files did not match
        #       2 otherwise
        if(sub_wdiff.returncode not in [0,1]):
            print("error: wdiff returned %d -- cmd: %s" % (sub_wdiff.returncode, ' '.join(cmd_wdiff)))
            print("stderr: %s" % out_wdiff[1])
            sys.exit(3)
            
        # Parse wdiff output
        try:
            common_a = int(out_wdiff[0].splitlines()[0].split()[4][0:-1])
            common_b = int(out_wdiff[0].splitlines()[1].split()[4][0:-1])
        except Exception:
            common_a = 0
            common_b = 0
        avg_acc = (common_a + common_b)/2.0
        #print(common_a)
        #print(common_b)
        #print(avg_acc)
        
        print("%d, %d, %s" % (common_a, common_b, avg_acc))
        
    