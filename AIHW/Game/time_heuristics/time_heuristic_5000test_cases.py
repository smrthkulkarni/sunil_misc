#!/usr/bin/env python
# coding=utf-8

import os
import time
import gc
import re
from glob import glob

FILE_PATH_INPUT = "/media/sunil/Others/AI_project/game/testcases5000/INPUT/"

def fetch_input_files(file_path):
    result = glob(file_path + "*.in")
    if not result:
        raise Exception("Invalid path:"+ file_path)
    return result

def main():
    for idx, input_file in enumerate(fetch_input_files(FILE_PATH_INPUT)):
        print input_file
        os.system('cp '+ input_file + ' ./input.txt')        
        os.system('python ./time_heuristic_script.py')
        gc.collect()

if __name__ == "__main__":
    main()
