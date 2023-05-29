import xlsxwriter
import os
import glob
from datetime import datetime
import time
import argparse

# HandloomCategories = ["handloom sarees","stitching services", "fabrics",
                # "kuppadam pattu sarees",
                # "kanchi lehengas", "soft silk kanchipuram sarees", "kanchi pattu sarees",
                # "uppada soft silk sarees","uppada pattu sarees",
                # "pochampally ikkat pure silk sarees", "ikkat lehengas",
                # "gadwal pattu sarees",
                # "paithani pure silk sarees",
                # "chanderi soft silk sarees", "chenderi silk sarees",
                # "linen sarees",
                # "kollam pattu sarees",
                # "tripura silk sarees", 
                # "organza sarees",
                # "banarasi sarees",
                # "chiffon sarees", 
                # "kora sarees",
                # "georgette sarees",
                # "uppada cotton sarees", "uppada tissue sarees", "gadwal sico sarees",
                # "gadwal cotton sarees", "uppada sico sarees","pochampally ikkat cotton sarees", "ikkat cotton sarees",
                # "venkatagiri pattu sarees",
                # "mangalagiri pattu sarees", "mangalagiri sico sarees",
                # "lichi sarees",
                # "maggam work",
                # "computer embroidery"]

# vendorList = ["ganjianand205@gmail.com"]



print("\nExection Stated-",datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
#Handling Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--inputconf",help="which type of Configuration file need to run.Such as tirupara or kanchi or managalagiri..etc")
parser.add_argument("--supportloc",help="provide suupport file with path which has handloom categories and vendor email addresses")
parser.add_argument("--outputloc",help="which location genated Excel file need to save")
args = parser.parse_args()

print("\nType of Configuration file given as Input:",args.inputconf)
print("\nOutput Excel file storing location:",args.outputloc)

#Read configuration files
with open(args.inputconf,'r') as f:
    a=f.read()

# Handle newline characters and special characters
#a.replace("\n\r", "\n\r")

#Converting dictionary
parameters=dict(eval(a))
print ("config parameters: ", parameters)
imageFolderLocation=os.path.join(parameters["images_folder_location"],"*")

# read support details and covert into dictionary
with open(args.supportloc,'r') as s:
    support=s.read()

#Converting dictionary
suppDetails=dict(eval(support))

if parameters["category"].lower() not in suppDetails['HandloomCategories']:
    print ("*"*50)
    print ("Category is not listed. Check category is mentioned as per the website")
    print ("*"*50)
    exit ()
elif parameters["vendor"] not in suppDetails['vendorList']:
    print ("*"*50)
    print ("Vendor email is not listed. Correct vendor email in configuration file and try")
    print ("*"*50)
    exit ()

#Time logic
def TimeStamp():
    time.sleep(0.0000001)
    timeWithDate = str(datetime.utcnow())

    for each in ["-"," ",":","."]:
        timeWithDate = timeWithDate.replace(each,"")

    return timeWithDate

# Create an new Excel file and add a worksheet.
excelName=os.path.join(args.outputloc,parameters["category"]+".xlsx")
workbook = xlsxwriter.Workbook(excelName)
worksheet = workbook.add_worksheet()
cell_format = workbook.add_format()


cell_format.set_pattern(1)  # This is optional when using a solid fill.
cell_format.set_bg_color('green')
cell_format.set_bold()
cell_format.set_italic()
cell_format.set_align("left")
cell_format.set_border()

cell_format1 = workbook.add_format()
cell_format1.set_text_wrap()
cell_format1.set_border()

border_format=workbook.add_format()
border_format.set_border()

#Header Creation for the file
worksheet.write("A1","Vendor",cell_format)
worksheet.write("B1","Category",cell_format)
worksheet.write("C1","Price",cell_format)
worksheet.write("D1","Special Price",cell_format)
worksheet.write("E1","Description",cell_format)
worksheet.write("F1","Saree Color Names",cell_format)
worksheet.write("G1","Design Name",cell_format)
worksheet.write("H1","Displayed Image",cell_format)
worksheet.write("I1","New Name For Image",cell_format)

# Loop for all images and Insert an image.
for i in glob.glob(imageFolderLocation):
    NewNameForImage=parameters["category"]+"-"+TimeStamp()+".jpg"
    os.rename(i,os.path.join(parameters["images_folder_location"],NewNameForImage))
    
listOfImages=glob.glob(imageFolderLocation)
print("\nTotal images:",len(listOfImages),",","All image list in given folder:",listOfImages)
# Widen the first column to make the text clearer.
worksheet.set_column(first_col=1,last_col=7,width=23)
worksheet.set_default_row(height=148)

for i in range(2,len(listOfImages)+2):
    A="A"+str(i)
    worksheet.write(A,parameters["vendor"],border_format)
    B="B"+str(i)
    worksheet.write(B,parameters["category"],border_format)
    C="C"+str(i)
    worksheet.write(C,parameters["price"],border_format)
    D="D"+str(i)
    worksheet.write(D,parameters["special_price"],border_format)
    E="E"+str(i)
    worksheet.write(E,parameters["description"],cell_format1)
    F="F"+str(i)
    worksheet.write(F,"",border_format)
    G="G"+str(i)
    worksheet.write(G,"",border_format)
    I="I"+str(i)
    NewNameForImage=listOfImages[i-2].split("\\")[-1]
    worksheet.write(I,NewNameForImage,cell_format1)
    H="H"+str(i)
    worksheet.insert_image(H,listOfImages[i-2],{'x_scale': 0.3, 'y_scale': 0.3,'x_offset':3,'y_offset':3,'positioning':1})
    
    
#closing the file
workbook.close()
print("\nExection Completed-",datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])
