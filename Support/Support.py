import xml.etree.ElementTree as ET
import os, paramiko, time
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
from resizeimage import resizeimage
global sftp, ssh
from stat import S_ISDIR, S_ISREG
import numpy as np
import pandas as pd
# Establishing connection to server
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client = ssh.connect(hostname='43.225.53.216', username='root', password='gB3xIWAXty#7', port=22)
#print(dir(ssh))
sftp = ssh.open_sftp()

'''
global SERVER_FOLDER_PATH_FOR_CSV_UPDATE, SFTP_CHDIR_IMAGES, SFTP_CHDIR_TXT, SFTP_CHDIR_VENDOR_CREDENTIALS
global CSV_FILEPATH, CSV_FILENAME


def xml_Read():

    tree = ET.parse('TaptahiVendorAutomation.xml')
    root = tree.getroot()

    for elem in root:
        if elem.tag == "SERVER_FOLDER_PATH_FOR_CSV_UPDATE":
            SERVER_FOLDER_PATH_FOR_CSV_UPDATE = elem.text
        elif elem.tag == "SFTP_CHDIR_IMAGES":
            SFTP_CHDIR_IMAGES = elem.text
        elif elem.tag == "SFTP_CHDIR_TXT":
            SFTP_CHDIR_TXT = elem.text
        elif elem.tag == "SFTP_CHDIR_VENDOR_CREDENTIALS":
            SFTP_CHDIR_VENDOR_CREDENTIALS = elem.text
        elif elem.tag == "CSV_FILEPATH":
            CSV_FILEPATH = elem.text
        elif elem.tag == "CSV_FILENAME":
            CSV_FILENAME = elem.text

    print("SERVER_FOLDER_PATH_FOR_CSV_UPDATE: ",SERVER_FOLDER_PATH_FOR_CSV_UPDATE)
    print("SFTP_CHDIR_IMAGES: ",SFTP_CHDIR_IMAGES)
    print("SFTP_CHDIR_TXT: ",SFTP_CHDIR_TXT)
    print("SFTP_CHDIR_VENDOR_CREDENTIALS: ",SFTP_CHDIR_VENDOR_CREDENTIALS)
    print("CSV_FILEPATH: ",CSV_FILEPATH)
    print("CSV_FILENAME: ",CSV_FILENAME)


'''

# for parsing XML and it returns required field passing through argument (tag)
def ReadXML(tag):

    try:
        tree = ET.parse('BulkUploadAutomation.xml')
        root = tree.getroot()
    except:
        print(xmlFile +" is not present or Element Tree is not installed")
        return "Error"


    for elem in root:
        if elem.tag == tag:
            #print (tag, ": ", elem.text)
            return elem.text

    return "Invalid tag expected from TapathiVendorAutomation.xml"


# for fetching vendor details using email
# it returns password and vendor unique name (vendorID)
def VendorLoginDetails(email):

    # read path from XML
    LOGIN_DETAILS_PATH_IN_LOC = ReadXML("LOGIN_DETAILS_PATH_IN_LOC")

    f = open(os.path.join(LOGIN_DETAILS_PATH_IN_LOC,"Vendor_Login_Details.txt"),'r')
    credentials = f.readlines()

    for details in credentials:
        if email in details:
            pswd_ID = details.split(',')[1:]
            pswd_ID = [pswd_ID[0],pswd_ID[1][:-2]]

            return pswd_ID


def TimeStamp():
    time.sleep(0.0000001)
    timeWithDate = str(datetime.utcnow())

    for each in ["-"," ",":","."]:
        timeWithDate = timeWithDate.replace(each,"")

    return timeWithDate


def Watermark(image, Path):

    castellar_Path = ReadXML("CASTELLAR_PATH")     # "C:\\Users\\Jyothi Prakash\\Downloads"
    tapathi_watermark_RED = 255
    tapathi_watermark_GREEN = 255
    tapathi_watermark_BLUE = 255

    img = Image.open(os.path.join(Path,image))
    # img=img.resize(size,Image.ANTIALIAS)
    width, height = img.size
    draw = ImageDraw.Draw(img)
    text = "www.tapathi.com Uploaded to www.tapathi.com"
    # font = ImageFont.truetype('C:\\E857920_Data\\python\\Personal\\CASTELAR.ttf ", 100)  # arial.ttf
    font = ImageFont.truetype(os.path.join(castellar_Path, "Castellar.ttf"), 20)  # arial.ttf
  
    x = int(1)
    y = int(height / 2)
    # x=width-textwidth-margin
    # y=height-texthight-margin
    # draw.text((x, y), text, fill=(255, 255, 0), font=font)
    draw.text((x, y), text,
              fill=(int(tapathi_watermark_RED), int(tapathi_watermark_GREEN), int(tapathi_watermark_BLUE)), font=font)

    #outFile_watermark = image.split('\\')[-1]
    #print(outFile_watermark)

    if not os.path.exists(os.path.join(Path, 'Watermark')):
        os.makedirs(os.path.join(Path, 'Watermark'))
    WaterMark_Imag_Output_path = os.path.join(Path,'Watermark')

    outFile_watermark = os.path.join(WaterMark_Imag_Output_path, image)
    img.save(outFile_watermark)
    return WaterMark_Imag_Output_path

def photo_resize(image,path):

    fd_img = open(os.path.join(path,image), 'r+b')
    img = Image.open(fd_img)
    pixel=img.load()
    bg_color=pixel[10,10] # detecting colour from top of image for back ground
    img = resizeimage.resize_contain(img, [550, 650],bg_color=(224,224,224))
    '''if(PHOTO_RESIZE_BACKGROUND_COLOR == str('Y')):
        #print("color",bg_color)
    img = resizeimage.resize_contain(img, [550, 650], bg_color=(224,224,224))
    else:
        img = resizeimage.resize_contain(img, [550, 650], bg_color=bg_color)'''

    img = img.convert("RGB")
    # output_image_name =str(image).split('\\')[-1]

    '''if not os.path.exists(path + '\\Resize'):
        os.makedirs(path + '\\Resize')
    Img_Output_resize_path = path + '\\Resize'''

    output_image_name = os.path.join(ReadXML("IMG_FOLDER_PATH_IN_LOC"), image)
    img.save(output_image_name, img.format)
    fd_img.close()


def fetching_files_to_local(ser_directory, local_directory):

    # changing directory to the vendor required folder
    try:
        sftp.chdir(ser_directory)

    except:
        return ser_directory + " directory not found"

    # files = sftp.listdir()

    #if not len(files):
    #    return "NO_FILES"

    #print(files)
    if not(os.path.exists(local_directory)):
        os.makedirs(local_directory)

    # fetching files from server to local directory
    for entry in sftp.listdir_attr(ser_directory):
        mode = entry.st_mode
        if S_ISDIR(mode):
            ser_dir= os.path.join(ser_directory,'/',entry.filename)
            loc_dir=os.path.join(local_directory,entry.filename)
            if not(os.path.isdir(loc_dir)):
                os.mkdir(loc_dir)
            fetching_files_to_local(ser_dir, loc_dir)
        #for file in files:
        if S_ISREG(mode):
            sftp.get(entry.filename, os.path.join(local_directory,entry.filename))
    return "Success"

def fetching_one_file_to_local(ser_directory, file, local_directory):

    # changing directory to the vendor required folder
    try:
        sftp.chdir(ser_directory)
    except:
        return ser_directory + " directory not found"

    files = sftp.listdir()

    if file in files:
        if not (os.path.exists(local_directory)):
            os.makedirs(local_directory)

        # fetching files from server to local directory
        sftp.get(file, os.path.join(local_directory, file))
        #if not '.txt' or '.jpg' in file:
        #    #moving files to archive folder
        #    sftp.rename(ser_directory + '/' + file,'/var/www/vhosts/tapathi.com/httpdocs/Vendor_Info/Archive' + '/' + file)

        return "Success"

    else:
        return file + " File not present"


def moving_files_to_server_to_server(ser_directory, file, local_directory):

    # changing directory to the vendor required folder
    try:
        sftp.chdir(ser_directory)
    except:
        return ser_directory + " directory not found"
    files = sftp.listdir()

    if file in files:
        if not (os.path.exists(local_directory)):
            os.makedirs(local_directory)

        sftp.rename(ser_directory + '/' + file, '/var/www/vhosts/tapathi.com/httpdocs/Vendor_Info/Archive' + '/' + file)

        return "Success"

    else:
        return file + " File not present"

def createpath(path):
    if os.path.exists(path):
        pass
    else:
        os.makedirs(path)

def productNameUpdate(Category,prodNamePath):

    try:
        a = pd.read_csv(os.path.join(prodNamePath,"Category.csv"))
        b = a[a['Category'] == str(Category).lower()]['Value']
        c = a[a['Category'] == str(Category).lower()]['Uniq_ID']
        b = int(b) + 1
        a['Value'] = np.where(a['Category'] == str(Category).lower(), int(b), a['Value'])
        a.to_csv(os.path.join(prodNamePath,"Category.csv") ,index=False)
        return c.values[0] + str(b).zfill(7)
    except:
        return None

def copyFileToServer(ser_directory, file, local_directory):

        fileWithPath = os.path.join(local_directory,file)

        # changing directory to the vendor required folder
        try:
            sftp.chdir(ser_directory)
        except:
            return ser_directory + " directory not found"


        if (os.path.isfile(fileWithPath)):

            try:
                sftp.put(fileWithPath,ser_directory + '/' + file)
                return "Success"
            except:
                return file + " File not copied"

        else:
            return file + " File not present"

def delFilesRecursively(path, fileType = ""):
    try:
        files = os.listdir(path)
        for file in files:
            file = os.path.join(path,file)
            if os.path.isfile(file):
                os.remove(file)
            elif os.path.isdir(file):
                delFilesRecursively(file)
                os.rmdir(file)
                
        return "Success"
    except:
        return "Issue during deleting files in folder: " + path