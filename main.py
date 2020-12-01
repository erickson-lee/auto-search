#!/usr/local/bin/python

import tool
import sys
from datetime import datetime

def main():

    keyword = "花蓮美食"
    now = datetime.now() 
    file_name = './result/' \
                + now.strftime("%Y%m%d%H%M%S") \
                + '_' \
                + keyword \
                + '.txt'

    s = tool.AutoSearcher()
    #s.change_region() # default Taiwan
    res = s.search_and_collect(keyword)
    original_stdout = sys.stdout 

    with open(file_name, "a") as f:
        for line in res:
            # Change the standard output to the file
            sys.stdout = f 
            print(*line, sep = ", ")
            # Reset the standard output
            sys.stdout = original_stdout 

        f.close()

if __name__ == "__main__":
    main()
