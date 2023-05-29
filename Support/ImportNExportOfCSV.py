from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import csv, time, os


global driver, wait60, wait15, wait900


#### getChorome
#### getLoginPage
#### Login
#### Traverse to required page
#### Export/Import file
#### Logout
#### close Chrome


# paths
loginPagePath = r"https://www.tapathi.com/admin_1t5r0f/admin/"
logoutPagePath = r"https://www.tapathi.com/admin_1t5r0f/admin/auth/logout/"
homePagePath = r'https://www.tapathi.com/admin_1t5r0f/admin/dashboard/'
importPagePath = r"https://www.tapathi.com/admin_1t5r0f/admin/import/index/key/921aad383b19a48b349faf730f74bd5423039d99f7380b5316fe305091614b43/"
exportPagePath = r"https://www.tapathi.com/admin_1t5r0f/admin/export/index/key/b2add0f1f49a4f457d90e444101c8dcd57f09a14e5022440f3b9912b322c2340/"

# webstore object Ids or class names to access and automate 
username_id = "username"
pswd_id = "login"
signIn_class = "action-login"

system_class = "item-system  parent"
system_id = "menu-magento-backend-system"
export_class = "item-system-convert-export"
import_class = "item-system-convert-import"

exEntityType_id = "entity"  # for selecting products using send_keys("Products")
exFilCreatedAtFrom_id="export_filter_created_at" # set created_at filter from date in (MM/D/YYYY for day less than 10th) format 
exFilCreatedAtTo_id="export_filter_created_at_to" # set created_at filter to date in (MM/D/YYYY for day less than 10th) format 
exSubmit_class="action-"  #click to continue

imEntityType_id = "entity"  # for selecting products using send_keys("Products")
imImportBehavior_id = "basic_behavior"   # select behavior as Delete using send_keys("Delete")
imImportFileWithPath_id = "import_file"   # select import file using send_keys("FileWithPath")
imImportImgFolderPath_id = "import_images_file_dir"   # select images folder using send_keys("FileWithPath")
imCheckButton_id = "upload_button"   # click to check data
imImportBtn_class = "scalable" # driver.find_element_by_class_name("scalable").click()

### Error message--->      (Checked rows: 1, checked entities: 1, invalid rows: 0, total errors: 1)
# responseMsg1 = driver.find_element_by_xpath('//div[@id="import_validation_messages"]/div/div[@class="message message-notice notice"][1]').text
# responseMsg2 = driver.find_element_by_xpath('//div[@id="import_validation_messages"]/div/div[2]').text


def itemClick(item, ID=True, value="", delay=30):
    wait = WebDriverWait(driver, delay)
    try:
        if ID:
            obj = wait.until(EC.element_to_be_clickable((By.ID, item)))
            # if send:
                # obj.send_keys(value)
            # else:
                # obj.click()
        else:
            obj = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, item)))
            # if send:
                # obj.send_keys(value)
            # else:
                # obj.click()
        if value != "":
            obj.send_keys(value)
        else:
            obj.click()
    except:
        print("\n******************************************************************\n"\
              "***    exception occurred during clicking on ",obj.text,"   ***\n"
              "******************************************************************\n")
# ----------------------------------------------------------------------
# Function: getChromeDriver
# Usage: getChromeDriver()
# Inputs: None
# Returns: Chrome Driver object
# Purpose: To get the chrome driver to be created and return the driver handle
# ----------------------------------------------------------------------
def getChromeDriver():

    global driver, wait60, wait15, wait900
    
    # driver = webdriver.Chrome(ChromeDriverManager().install())
    chrome_options = webdriver.ChromeOptions()
#    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("window-size=1024,768")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("start-maximized")
    desired = chrome_options.to_capabilities()
    driver = webdriver.Chrome(executable_path=r'C:\Users\jvanka\Downloads\chromedriver_win32\chromedriver.exe',options=chrome_options,desired_capabilities=desired)
#     driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=chrome_options)
     #driver = webdriver.Chrome(executable_path='/home/syamala_narala/vendorautomation/code/chromedriver.exe')
     #driver = webdriver.Chrome()
    
    # waits 
    wait15 = WebDriverWait(driver,15)
    wait60 = WebDriverWait(driver,60)
    wait900 = WebDriverWait(driver,900)

    time.sleep(3)
    return driver

# ----------------------------------------------------------------------
# Name : login(driver, username, password)
# Inputs : username - User name 
#          password - password set by admin
#          driver - chrome driver
# Output : True - sucessful login
#          False - logn failed
# Usage : login(driver, adminUsername, adminPassword)
# ----------------------------------------------------------------------
def login(driver, username, pswd):

    try:
        driver.get(loginPagePath)
        time.sleep(1)
    except:
        #driver = webdriver.Chrome(ChromeDriverManager().install())
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless')
        #chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument("window-size=1024,768")
        chrome_options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=chrome_options)
        #driver = webdriver.Chrome()
        driver.get(loginPagePath)

    if loginPagePath in (str(driver.current_url)):
        wait15.until(EC.element_to_be_clickable((By.ID, username_id))).send_keys(username)
        wait15.until(EC.element_to_be_clickable((By.ID, pswd_id))).send_keys(pswd)
        wait15.until(EC.element_to_be_clickable((By.CLASS_NAME, signIn_class))).submit()
        time.sleep(5)

    # checking whether we landed in vendor page or not. if not sending creating log and skipping.
    for i in range(60):
        if (homePagePath in str(driver.current_url)):
            print("Successfully Logged-in")
            break
    else:
        if (homePagePath not in str(driver.current_url)):
            print("\n*****************************************************************\n" \
                  "                   Wrong credentials                             \n" \
                  "*****************************************************************\n")
            return False
    return True


def importFileToDeleteProducts(fileWithPath, loginUserName, loginPswd):
    ## Here loginUserName and loginPswd are admin credentials
    ## fileWithPath should be in CSV format with complete path
    ##     - fileWithPath is /complete/path/of/file/filename.csv
    
    driver = getChromeDriver()
    
    loginStatus = login(driver, loginUserName, loginPswd)
    
    if not loginStatus:
        driver.close()
        time.sleep(2)
        return False
    
    wait15.until(EC.element_to_be_clickable((By.ID, system_id))).click()
    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, import_class))).click()
    wait60.until(EC.element_to_be_clickable((By.ID, imEntityType_id))).send_keys("Products")
    wait60.until(EC.element_to_be_clickable((By.ID, imImportBehavior_id))).send_keys("Delete")
    wait60.until(EC.element_to_be_clickable((By.ID, imImportFileWithPath_id))).send_keys(fileWithPath)
    wait60.until(EC.element_to_be_clickable((By.ID, imCheckButton_id))).click()
    time.sleep(15)
    
    
    wait900.until(EC.element_to_be_clickable((By.CLASS_NAME, imImportBtn_class)))
    msg_objs = driver.find_elements_by_class_name("message")
    for msg in msg_objs:
        m=msg.text
        if "Checked rows" in m and "invalid rows" in m and "total errors" in m:
            chkd_rows = int(m.split(',')[0].split(':')[1])
            chkd_entities = int(m.split(',')[1].split(':')[1])
            invalid_rows = int(m.split(',')[2].split(':')[1])
            total_errors = int(m.split(',')[3].split(':')[1])
    
            if (chkd_rows>10 and (invalid_rows > 10 or total_errors > 10)):
                # driver.find_element_by_class_name(imImportBtn_class).click()
                
                # # msg_objs = driver.find_elements_by_class_name("message")
                # # time.sleep(5)
                wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, imImportBtn_class))).click()
                time.sleep(2)
                # wait until upload operation is completed.
                # check for "Import successfully done" message 
                # if message not found until 900sec then return False
                for i in range(900):
                    im_msg_objs = driver.find_elements_by_class_name("message")
                    for msg in im_msg_objs:
                        if msg.text is "Import successfully done":
                            print("Importing data successfully completed")
                            time.sleep(1)
                            break
                else:
                    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, "admin__action-dropdown"))).click()
                    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, "account-signout"))).click()
                    driver.close()
                    time.sleep(5)

                    return True
                    
    
    
    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, "admin__action-dropdown"))).click()
    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, "account-signout"))).click()
    driver.close()
    time.sleep(5)

    return True
    

def importFileToAddProducts(fileWithPath, imgDirPath, loginUserName, loginPswd):
    ## Here loginUserName and loginPswd are admin credentials
    ## fileWithPath should be in CSV format with complete path
    ##     - fileWithPath is /complete/path/of/file/filename.csv
    ## imgDirPath should be a sub-directory in default image folder
    ##     For Type "Local Server" use relative path to <Magento root directory>/var/import/images, e.g. product_images, import_images/batch1.
    ##     For example, in case product_images, files should be placed into <Magento root directory>/var/import/images/product_images folder.
    
    # driver = getChromeDriver()
    
    loginStatus = login(driver, loginUserName, loginPswd)
    
    if not loginStatus:
        driver.close()
        time.sleep(2)
        return False
    
    wait15.until(EC.element_to_be_clickable((By.ID, system_id))).click()
    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, import_class))).click()
    wait60.until(EC.element_to_be_clickable((By.ID, imEntityType_id))).send_keys("Products")
    wait60.until(EC.element_to_be_clickable((By.ID, imImportBehavior_id))).send_keys("Add/Update")
    wait60.until(EC.element_to_be_clickable((By.ID, imImportFileWithPath_id))).send_keys(fileWithPath)
    wait60.until(EC.element_to_be_clickable((By.ID, imImportImgFolderPath_id))).send_keys(imgDirPath)
    wait60.until(EC.element_to_be_clickable((By.ID, imCheckButton_id))).click()
    time.sleep(15)
    print("Selected all fields.")
    
    
    wait900.until(EC.element_to_be_clickable((By.CLASS_NAME, imImportBtn_class)))
    msg_objs = driver.find_elements_by_class_name("message")
    for msg in msg_objs:
        m=msg.text
        if "Checked rows" in m and "invalid rows" in m and "total errors" in m:
            chkd_rows = int(m.split(',')[0].split(':')[1])
            chkd_entities = int(m.split(',')[1].split(':')[1])
            invalid_rows = int(m.split(',')[2].split(':')[1])
            total_errors = int(m.split(',')[3].split(':')[1])
    
            if (chkd_rows>10 and (invalid_rows > 10 or total_errors > 10)):
                # driver.find_element_by_class_name(imImportBtn_class).click()
                
                # # msg_objs = driver.find_elements_by_class_name("message")
                # # time.sleep(5)
                wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, imImportBtn_class))).click()
                time.sleep(2)
                # wait until upload operation is completed.
                # check for "Import successfully done" message 
                # if message not found until 900sec then return False
                for i in range(900):
                    im_msg_objs = driver.find_elements_by_class_name("message")
                    for msg in im_msg_objs:
                        if msg.text is "Import successfully done":
                            print("Importing data successfully completed")
                            time.sleep(1)
                            break
                else:
                    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, "admin__action-dropdown"))).click()
                    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, "account-signout"))).click()
                    driver.close()
                    time.sleep(5)

                    return True
                    
    
    
    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, "admin__action-dropdown"))).click()
    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, "account-signout"))).click()
    driver.close()
    time.sleep(5)

    return True
    

def exportProductsToCSV(loginUserName, loginPswd):
    ## Here loginUserName and loginPswd are admin credentials
    
    driver = getChromeDriver()
    
    loginStatus = login(driver, loginUserName, loginPswd)
    
    if not loginStatus:
        return False
    
    wait15.until(EC.element_to_be_clickable((By.ID, system_id))).click()
    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, export_class))).click()
    wait60.until(EC.element_to_be_clickable((By.ID, exEntityType_id))).send_keys("Products")
    wait60.until(EC.element_to_be_clickable((By.ID, exSubmit_id))).click()
    time.sleep(60)
    
    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, "admin__action-dropdown"))).click()
    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, "account-signout"))).click()
    driver.close()
    time.sleep(5)    

def exportProductsToCSVBasedonDate(loginUserName, loginPswd, fromDate, toDate):
    ## Here loginUserName and loginPswd are admin credentials
    ## fromDate and toDate are should be in below format
    ##    - MM/D/YYYY    if day is before 10th (i.e., 5thDec,2022 as 12/5/2022)
    ##    - MM/DD/YYYY    if day is on or after 10th (i.e., 25thMay,2022 as 05/25/2022)
    
    driver = getChromeDriver()
    
    loginStatus = login(driver, loginUserName, loginPswd)
    
    if not loginStatus:
        return False
    
    wait15.until(EC.element_to_be_clickable((By.ID, system_id))).click()
    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, export_class))).click()
    wait60.until(EC.element_to_be_clickable((By.ID, exEntityType_id))).send_keys("Products")
    wait60.until(EC.element_to_be_clickable((By.ID, exFilCreatedAtFrom_id))).send_keys(fromDate)
    wait60.until(EC.element_to_be_clickable((By.ID, exFilCreatedAtTo_id))).send_keys(toDate)
    wait60.until(EC.element_to_be_clickable((By.ID, exSubmit_id))).click()
    time.sleep(60)
    
    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, "admin__action-dropdown"))).click()
    wait60.until(EC.element_to_be_clickable((By.CLASS_NAME, "account-signout"))).click()
    driver.close()
    time.sleep(5)
    
# if __name__ == "__main__":

    # fileWithPath = r"C:\Users\jvanka\Downloads\Tapathi\TapathiAutomation\ImportNExport\export_catalog_product_20220123.csv"
    # loginUserName = 'Tapathi'
    # loginPswd = 'Anand@1991'
    
    # exportProductsToCSVBasedonDate(loginUserName, loginPswd, r"05/5/2022", r"05/15/2022")
    # # importFileToDeleteProducts(fileWithPath, loginUserName, loginPswd)
