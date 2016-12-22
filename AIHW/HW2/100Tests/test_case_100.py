#!/usr/bin/env python
# coding=utf-8

import os
import time
import gc
import re
from glob import glob

FILE_PATH = "/media/sunil/Others/AI_project/game/Input/"

def fetch_input_files(file_path):
    result = glob(file_path + "*.in")
    if not result:
        raise Exception("Invalid path:"+ file_path)
    return result

def main():
    os.system('\\rm -rf results')
    os.system('mkdir -p results')
    timeout_files = list()

    for idx, input_file in enumerate(fetch_input_files(FILE_PATH)):
        os.system('cp '+ input_file + ' ./input.txt')
        print "Executing test case: "+ input_file 
        start_time = time.time()
        os.system('python ./homework.py')
        gc.collect()
        time_val = int((time.time() - start_time) * 1000)
        print "Runing time: " + str(time_val) + " ms"
        if time_val > 300000:
            timeout_files.append([input_file, time_val])

        (base_path, file_name) = os.path.split(input_file)
        match = re.search("\d+", file_name)
        if match:
            output_file = base_path + "/" + match.group() + ".out"
            print "Finding the output diff with: "+ output_file
            print 'diff ./output.txt ' + output_file
            print 'mv ./output.txt '+ "./results/output" + match.group() + ".txt"
            os.system('dos2unix ./output.txt ')
            os.system('dos2unix '+ output_file)
            os.system('diff ./output.txt ' + output_file)
            os.system('mv ./output.txt '+ "./results/output" + match.group() + ".txt")
        else:
            raise Exception("Appropriate output file not found")
        print "========================================================================"
    print timeout_files

if __name__ == "__main__":
    main()
