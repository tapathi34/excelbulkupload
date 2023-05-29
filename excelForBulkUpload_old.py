import os, time, importlib
from os.path import join
from Support.csvDataManipulation_old import *
from Support.Support import * #Support as sup
import pandas as pd

META_CSV_WITH_PATH = ReadXML("META_CSV_WITH_PATH")


header = ["sku", "attribute_set_code", "product_type", "categories", "product_websites", "name", "description", "short_description", "weight", "product_online", "tax_class_name", "visibility", "price", "special_price", "special_price_from_date", "meta_title", "meta_keywords", "meta_description", "base_image", "base_image_label", "small_image", "small_image_label", "thumbnail_image", "thumbnail_image_label", "display_product_options_in", "msrp_display_actual_price_type", "country_of_manufacture", "additional_attributes", "qty", "out_of_stock_qty", "use_config_min_qty", "is_qty_decimal", "allow_backorders", "use_config_backorders", "min_cart_qty", "use_config_min_sale_qty", "max_cart_qty", "use_config_max_sale_qty", "is_in_stock", "notify_on_stock_below", "use_config_notify_stock_qty", "manage_stock", "use_config_manage_stock", "use_config_qty_increments", "qty_increments", "use_config_enable_qty_inc", "enable_qty_increments", "is_decimal_divided", "website_id", "deferred_stock_update", "use_config_deferred_stock_update"]

HandloomCategories = ["handloom sarees","stitching services", "fabrics",
                "kuppadam pattu sarees",
                "kanchi lehengas", "soft silk kanchipuram sarees", "kanchi pattu sarees",
                "uppada soft silk sarees","uppada pattu sarees",
                "pochampally ikkat pure silk sarees", "ikkat lehengas",
                "gadwal pattu sarees",
                "paithani pure silk sarees",
                "chanderi soft silk sarees", "chenderi silk sarees",
                "linen sarees",
                "kollam pattu sarees",
                "tripura silk sarees", 
                "organza sarees",
                "banarasi sarees",
                "chiffon sarees", 
                "kora sarees",
                "georgette sarees",
                "uppada cotton sarees", "uppada tissue sarees", "gadwal sico sarees",
                "gadwal cotton sarees", "uppada sico sarees","pochampally ikkat cotton sarees", "ikkat cotton sarees",
                "venkatagiri pattu sarees",
                "mangalagiri pattu sarees", "mangalagiri sico sarees",
                "lichi sarees",
                "maggam work",
                "computer embroidery"]


def excelForBulkUpload(inputCsv, catCsv, outputCsv):
    
    # read data from the inputCsv
    inputData = pd.read_excel(inputCsv)

    # read data from category.csv
    cData = pd.read_csv(catCsv)
    
    # output data frame
    outDF = pd.DataFrame()
    # print (inputData)
    
    email=''
    sku = []
    categories = []
    name = []
    description = []
    short_description = []
    special_price_from_date = []
    price = []
    special_price = []
    meta_title = []
    meta_keywords = []
    meta_description = []
    base_image = []
    base_image_label = []
    small_image = []
    small_image_label = []
    thumbnail_image = []
    thumbnail_image_label = []
    # outDF['sku'] = []
    # outDF['categories'] = []
    if len(inputData['Vendor']) == 0:
        return "No products"
    for row in range(len(inputData['Vendor'])):
        
        # get SKU keyword using email in inputCsv
        email = inputData['Vendor'][row].lower()
        pswd_ID = VendorLoginDetails(email) #Support.VendorLoginDetails(email)
        # print (inputData.loc[[row]])
        today = datetime.today()
        print (email, pswd_ID, today)

        Category = inputData['Category'][row]
        if Category not in HandloomCategories:
            Category = 'handloom sarees'

        nameSuffix = "TRPP0001"
        catIndex = [j for j in range(len(cData["Category"])) if cData["Category"][j] == Category][-1]
        catUniqID = cData['Uniq_ID'][catIndex]
        catValue = cData['Value'][catIndex]
        nameSuffix = catUniqID + str(catValue).zfill(7)
        print (nameSuffix)
        
        # increment value for next product
        cData['Value'][catIndex] = catValue + 1
        
        Name = inputData['Saree Color Names'][row] + " " + Category + " with " + inputData['Design Name'][row] + " design - " + nameSuffix

        metaDetails = getMetaDetails(Category, Name, META_CSV_WITH_PATH)

        price_orig = float(inputData['Price'][row])
        splprice_orig = float(inputData['Special Price'][row])
        # getting price and special_price depends on category and vendor
        if (Category.lower() == "maggam work" or Category.lower() == "computer embroidery"):
            Price = str(int((price_orig - 100) * 1.3) + 100)  # str(row[productPrice])
            SpecialPrice = str(
                int((splprice_orig - 100) * 1.15) + 100)  # str(row[productSpecialPrice])
        elif "ikkat" in Category.lower():
            Price = str(int((price_orig - 100) * 1.5) + 100)  # str(row[productPrice])
            SpecialPrice = str(
                int((splprice_orig - 100) * 1.165) + 100)  # str(row[productSpecialPrice])
        elif email == 'tapathirksarees@gmail.com':
            if int(row[productPrice]) <= 700:
                Price = str(int((price_orig-100) * 3) + 100)
                SpecialPrice = str(int((splprice_orig-100) * 2) + 100)
            else:
                Price = str(int((price_orig-100) * 2.5) + 100)
                SpecialPrice = str(int((splprice_orig-100) * 1.7) + 100)
        elif email == 'ganjianand205@gmail.com':
            Price = str(int((price_orig-100) * 1.6) + 100)
            SpecialPrice = str(int((splprice_orig-100) * 1.25) + 100)
        else:
            Price = str(int((price_orig-100) * 1.8) + 100)          #str(row[productPrice])
            if row[productPrice] > str(2000.0):
                SpecialPrice = str(int((splprice_orig-100) * 1.2) + 100)          #str(row[productSpecialPrice])
            else:
                SpecialPrice = str(int((splprice_orig-100) * 1.3) + 100)          #str(row[productSpecialPrice])

        
        # dummy lines are Categories, Name, meta_title, meta_description, meta_keywords
        # outDF['sku'][row] = str(pswd_ID[1]) + str(TimeStamp()) # str(pswd_ID[1]) + str(Support.TimeStamp())
        sku.append(str(pswd_ID[1]) + str(TimeStamp())) # str(pswd_ID[1]) + str(Support.TimeStamp())
        # outDF['categories'][row] = Category
        categories.append(metaDetails[3])
        # name.append("name"
        name.append(Name)
        # description.append(inputData['Description']
        description.append(inputData['Description'][row])
        # short_description.append(inputData['Description']
        short_description.append(inputData['Description'][row])
        # price.append(Price
        price.append(Price)
        # special_price.append(SpecialPrice
        special_price.append(SpecialPrice)
        # special_price_from_date.append(datetime.strftime(today, '%m/%d/%y')
        special_price_from_date.append(datetime.strftime(today, '%m/%d/%y'))
        # meta_title.append("This is meta_title"
        meta_title.append(metaDetails[0])
        # meta_keywords.append("these, are, meta, keywords"
        meta_keywords.append(metaDetails[1])
        # meta_description.append("This is meta_description" 
        meta_description.append(metaDetails[2]) 
        # base_image.append(inputData['New Name For Image']
        base_image.append(inputData['New Name For Image'][row])
        # base_image_label.append(inputData['New Name For Image']
        base_image_label.append(inputData['New Name For Image'][row])
        # small_image.append(inputData['New Name For Image']
        small_image.append(inputData['New Name For Image'][row])
        # small_image_label.append(inputData['New Name For Image']
        small_image_label.append(inputData['New Name For Image'][row])
        # thumbnail_image.append(inputData['New Name For Image']
        thumbnail_image.append(inputData['New Name For Image'][row])
        # thumbnail_image_label.append(inputData['New Name For Image']
        thumbnail_image_label.append(inputData['New Name For Image'][row])
        
        
        # constants
        # outDF['attribute_set_code'][row] = 'Default'
        # outDF['product_type'][row] = 'simple'
        # outDF['product_websites'][row] = 'base'
        # outDF['weight'][row] = '2.5'
        # outDF['product_online'][row] = '1'
        # outDF['tax_class_name'][row] = 'None'
        # outDF['visibility'][row] = 'Catalog, Search'
        # outDF['display_product_options_in'][row] = 'Block after Info Column'
        # outDF['msrp_display_actual_price_type'][row] = 'Use config'
        # outDF['country_of_manufacture'][row] = 'india'
        # outDF['additional_attributes'][row] = '"has_options=0,quantity_and_stock_status=In Stock,required_options=0"'
        # outDF['qty'][row] = '10'
        # outDF['out_of_stock_qty'][row] = '0'
        # outDF['use_config_min_qty'][row] = '1'
        # outDF['is_qty_decimal'][row] = '0'
        # outDF['allow_backorders'][row] = '0'
        # outDF['use_config_backorders'][row] = '1'
        # outDF['min_cart_qty'][row] = '1'
        # outDF['use_config_min_sale_qty'][row] = '0'
        # outDF['max_cart_qty'][row] = '0'
        # outDF['use_config_max_sale_qty'][row] = '1'
        # outDF['is_in_stock'][row] = '1'
        # outDF['notify_on_stock_below'][row] = '3'
        # outDF['use_config_notify_stock_qty'][row] = '1'
        # outDF['manage_stock'][row] = '0'
        # outDF['use_config_manage_stock'][row] = '1'
        # outDF['use_config_qty_increments'][row] = '1'
        # outDF['qty_increments'][row] = '1'
        # outDF['use_config_enable_qty_inc'][row] = '1'
        # outDF['enable_qty_increments'][row] = '0'
        # outDF['is_decimal_divided'][row] = '0'
        # outDF['website_id'][row] = '1'
        # outDF['deferred_stock_update'][row] = '0'
        # outDF['use_config_deferred_stock_update'][row] = '1'
        
    # end of for loop
    print (len(price), price)
    print (len(sku), sku)
    outDF['sku']                      =    sku
    outDF['categories']               =    categories
    outDF['name']                     =    name
    outDF['description']              =    description
    outDF['short_description']        =    short_description
    outDF['price']                    =    price
    outDF['special_price']            =    special_price
    outDF['special_price_from_date']  =    special_price_from_date
    outDF['meta_title']               =    meta_title
    outDF['meta_keywords']            =    meta_keywords
    outDF['meta_description']         =    meta_description
    outDF['base_image']               =    base_image
    outDF['base_image_label']         =    base_image_label
    outDF['small_image']              =    small_image
    outDF['small_image_label']        =    small_image_label
    outDF['thumbnail_image']          =    thumbnail_image
    outDF['thumbnail_image_label']    =    thumbnail_image_label

    # constants
    dataLen = len(inputData['Vendor'])
    outDF['attribute_set_code'] = ['Default'] * dataLen
    outDF['product_type'] = ['simple'] * dataLen
    outDF['product_websites'] = ['base'] * dataLen
    outDF['weight'] = ['2.5'] * dataLen
    outDF['product_online'] = ['1'] * dataLen
    outDF['tax_class_name'] = ['None'] * dataLen
    outDF['visibility'] = ['Catalog, Search'] * dataLen
    outDF['display_product_options_in'] = ['Block after Info Column'] * dataLen
    outDF['msrp_display_actual_price_type'] = ['Use config'] * dataLen
    outDF['country_of_manufacture'] = ['india'] * dataLen
    outDF['additional_attributes'] = ['"has_options=0,quantity_and_stock_status=In Stock,required_options=0"'] * dataLen
    outDF['qty'] = ['10'] * dataLen
    outDF['out_of_stock_qty'] = ['0'] * dataLen
    outDF['use_config_min_qty'] = ['1'] * dataLen
    outDF['is_qty_decimal'] = ['0'] * dataLen
    outDF['allow_backorders'] = ['0'] * dataLen
    outDF['use_config_backorders'] = ['1'] * dataLen
    outDF['min_cart_qty'] = ['1'] * dataLen
    outDF['use_config_min_sale_qty'] = ['0'] * dataLen
    outDF['max_cart_qty'] = ['0'] * dataLen
    outDF['use_config_max_sale_qty'] = ['1'] * dataLen
    outDF['is_in_stock'] = ['1'] * dataLen
    outDF['notify_on_stock_below'] = ['3'] * dataLen
    outDF['use_config_notify_stock_qty'] = ['1'] * dataLen
    outDF['manage_stock'] = ['0'] * dataLen
    outDF['use_config_manage_stock'] = ['1'] * dataLen
    outDF['use_config_qty_increments'] = ['1'] * dataLen
    outDF['qty_increments'] = ['1'] * dataLen
    outDF['use_config_enable_qty_inc'] = ['1'] * dataLen
    outDF['enable_qty_increments'] = ['0'] * dataLen
    outDF['is_decimal_divided'] = ['0'] * dataLen
    outDF['website_id'] = ['1'] * dataLen
    outDF['deferred_stock_update'] = ['0'] * dataLen
    outDF['use_config_deferred_stock_update'] = ['1'] * dataLen
        
    # write data into output file
    outDF.to_csv(outputCsv, index=False)
    cData.to_csv(catCsv, index=False)
    
    return ["Success", email]

# if __name__ == "__main__":
    # inputfile = r'C:\Users\jvanka\Downloads\Tapathi\PyImageInsertion\JP\excelgenation\tripuraCopy.xlsx'
    # outputfile = r'C:\Users\jvanka\Downloads\Tapathi\PyImageInsertion\JP\excelgenation\output_tripura.csv'
    # categoryCsv = r'C:\Users\jvanka\Downloads\Tapathi\PyImageInsertion\JP\Support\Category.csv'
    
    # excelForBulkUpload(inputfile, categoryCsv, outputfile)
