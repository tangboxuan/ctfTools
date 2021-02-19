#simulates grep

import os
enc = 'iso-8859-15'
directory = r'/Users/user/filedir' #enter filedir here
for filename in os.listdir(directory):
    string = open(os.path.join(directory,filename), 'r', encoding=enc).read()
    if "searchterm" in string: #enter searchterm here
        print(filename)