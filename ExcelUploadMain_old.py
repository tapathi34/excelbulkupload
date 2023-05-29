import os
from Support import Support as sup
import excelForBulkUpload_old as fullCsv
from Support import ImportNExportOfCSV as impExp

import importlib

importlib.reload(fullCsv)
importlib.reload(sup)
importlib.reload(impExp)
# importlib.reload(Support.Support)
                 
returnValue = ''
imgDirWithPath = ''


# # Update XML file
# # get excels from website
# # send those files to fullCsv
# # Update paths

xmlFile = r'BulkUploadAutomation.xml'

# SER_CSV_PATH = ReadXML(xmlFile, "SER_CSV_PATH")
# LOC_CSV_PATH = ReadXML(xmlFile, "LOC_CSV_PATH")
# FULLCSV_LOC_PATH = ReadXML(xmlFile, "FULLCSV_LOC_PATH")
# CAT_CSV_WITH_PATH = ReadXML(xmlFile, "CAT_CSV_WITH_PATH")

SER_CSV_PATH = sup.ReadXML("SER_CSV_PATH")
LOC_CSV_PATH = sup.ReadXML("LOC_CSV_PATH")
FULLCSV_LOC_PATH = sup.ReadXML("FULLCSV_LOC_PATH")
CAT_CSV_WITH_PATH = sup.ReadXML("CAT_CSV_WITH_PATH")
META_CSV_WITH_PATH = sup.ReadXML("META_CSV_WITH_PATH")
LOGIN_ID = sup.ReadXML("LOGIN_ID")
LOGIN_PSWD = sup.ReadXML("LOGIN_PSWD")
IMG_DIR_PATH = sup.ReadXML("IMG_DIR_PATH")
# imgDirWithPath = 

# Fetch files from website using XML file which contains folder paths
#filenames = os.listdir(SER_CSV_PATH)
#excelList = [filename for filename in filenames if filename.endswith(".xlsx")]
#for eachFile in excelList:
sup.fetching_files_to_local(SER_CSV_PATH, LOC_CSV_PATH)

# loop through fetched excel files to create final Csvs with full details
# filenames = os.listdir(LOC_CSV_PATH)
# excelList = [filename for filename in filenames if filename.endswith(".xlsx")]
# print(csvList)

for root,subDirs,files in os.walk(LOC_CSV_PATH):
    for file in files:
        if file.endswith(".xlsx"):
            fileName,fileExt = os.path.splitext(file)
            returnValue, email = fullCsv.excelForBulkUpload(os.path.join(root,file), CAT_CSV_WITH_PATH, os.path.join(FULLCSV_LOC_PATH, fileName+'_output.csv'))
            print(returnValue)
            if returnValue == "Success":
                ## here you can call function to upload FULL CSV into the website
                pass
            else:
                # write the error into the log file
                pass
            # import csv with full details into the webstore
            # dir should be /var/import/images/<subdirectory>
            imgDirWithPath = IMG_DIR_PATH + '/' + email + '/' + fileName
            impExp.importFileToAddProducts (FULLCSV_LOC_PATH, imgDirWithPath, LOGIN_ID, LOGIN_PSWD)  
    # else:
        # print("1. csv files not exist in folder")
# else:
    # print("2. csv files not exist in folder")
