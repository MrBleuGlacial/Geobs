import os
import shutil

source_path = "C:\\GEOBS\\MTD_GuyaneSIG"
dest_path = "C:\\GEOBS\\MTD_GuyaneSIG_dest"
cmpt = 0

for i in os.listdir(source_path):
    tmp_path = source_path + '\\' + i
    if (not(os.path.isfile(tmp_path))and(i!='private')and(i!='public')):
        file_path = tmp_path+'\\metadata\\metadata.xml'
        #print os.path.isfile(file_path)
        file_path_dest = dest_path + '\\' + str(cmpt) + '.xml'
        cmpt += 1
        print file_path
        os.rename(file_path,file_path_dest)
print "---Done---"

