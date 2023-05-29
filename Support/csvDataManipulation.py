import pandas as pd
import os, copy

# read category data file meta_titile, keywords & description
cFilePath = r"C:\Users\jvanka\Downloads\Tapathi\PyImageInsertion\JP\Support"
cFileName = r"categoryList.csv"

# read category data
# cData = pd.read_csv(os.path.join(cFilePath, cFileName))

# local variables
meta_title_suffix = "online from weavers | "

# # exported CSV
# rCsvPath = r"C:\Users\jvanka\Downloads\Tapathi"
# rCsvName = r"export_catalog_product_20220226_034518.csv"

# # create file with updated data to import
# wCsvName = r"export_catalog_product_20220226_034518_new.csv"

# # read exported csv data
# data = pd.read_csv(os.path.join(rCsvPath, rCsvName))

# # read product names
# nameList = data["name"]

# # creating dummy structures for data updating
# meta_title = copy.deepcopy(nameList)
# meta_keywords = copy.deepcopy(nameList)
# meta_description = copy.deepcopy(nameList)
# category = copy.deepcopy(nameList)

def getMetaDetails(category, name, catCSV):

    meta_title = ""
    meta_keywords = ""
    meta_description = ""
    # category = Category

    # read category data
    cData = pd.read_csv(catCSV)

    # nameList[0].replace("handloom saree","-").split("-")

    # cat = {"MAGP": "Mangalagiri silk sarees | latest mangalagiri pattu saree", "CNDP": "Chenderi sarees |  Designer silk chenderi sarees", "KUPP": "Kuppadam silk sarees | Kuppadam saree", "UPSF": "Uppada soft silk sarees | latest uppada soft pattu saree"}

    # for i in range(len(nameList)):
    if "handloom saree" in name:
        splitName = name.replace("handloom saree","-").split("-")
    elif " sarees with " in name.lower():
        splitName = name.replace(" sarees with ","- with ").replace(" Sarees with ","- with ").split("-")
    elif " lehangas with " in name.lower():
        splitName = name.replace(" lehangas with ","- with ").replace(" Lehangas with ","- with ").split("-")
    elif " lehengas with " in name.lower():
        splitName = name.replace(" lehengas with ","- with ").replace(" Lehengas with ","- with ").split("-")
    else:
        splitName = name.replace("handloom saree","-").split("-")
    iCat = splitName[2].strip()[:4]

    # get index of specific category
    cIndex = [j for j in range(len(cData["uniq_id"])) if cData["uniq_id"][j] == iCat][-1]

    meta_title = cData["meta_title"][cIndex] + splitName[1] + meta_title_suffix + splitName[2]
    meta_keywords = cData["meta_keywords"][cIndex]
    meta_description = cData["meta_description"][cIndex]
    if cData["Category"][cIndex] != category:
        print(cData["Category"][cIndex])
        category = str(cData["Category"][cIndex])
    
    return [meta_title, meta_keywords, meta_description, category]
    
# data["meta_title"] = copy.deepcopy(meta_title)
# data["meta_keywords"] = copy.deepcopy(meta_keywords)
# data["meta_description"] = copy.deepcopy(meta_description)
# data["base_image_label"] = copy.deepcopy(nameList)
# data["small_image_label"] = copy.deepcopy(nameList)
# data["thumbnail_image_label"] = copy.deepcopy(nameList)
# data["additional_image_labels"] = copy.deepcopy(nameList)

# newData = pd.DataFrame(columns=['sku','categories','name','meta_title','meta_keywords','meta_description','base_image_label','small_image_label','thumbnail_image_label','additional_image_labels'],
                       # data=data[['sku','categories','name','meta_title','meta_keywords','meta_description','base_image_label','small_image_label','thumbnail_image_label','additional_image_labels']].values)

# newData.to_csv(os.path.join(rCsvPath, wCsvName), index=False)

