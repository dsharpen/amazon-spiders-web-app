import re, demjson
from mycsv import default_values, write__csv
from utilities.amazon_api import parse_pricing
from converter import clean_images
import pprint

def clean_variants(variant_script, image_script, parent_dict, mywriter, category_name):
            
            variant_theme = variant_script.split('dimensions":[')[-1].split('],')[0].replace('"','').split(',')
            
            '''
                # Contains the types of variants(sizes, colors etc.). Used also to denote the mapping of variants found in the Variant JavaScript
            ''' 

            variant_script = variant_script.split('dimensionValuesDisplayData')[-1].split('"deviceType')[0]
            variant_script = re.findall('"(.*?)]',variant_script.split("hidePopover")[0])

            image_script = image_script.split('data["colorImages"] =')[-1].split('data["heroImage"] = {};')[0].rsplit(';',1)[0]     
            image_script = demjson.decode(image_script)      

            '''
                # A dictionary of variants with ASINs as keys and a dict of dict to store variant values
            '''
            variant_dict = {}
            
            
            for list in variant_script:
                Images_Found = False
                image_values = ''

                asin = list.split('[')[0].replace(':{"','').replace('":','')               
                variant_dict[asin] = {}            
                variant_dict[asin]['Images'] = []   
                variants_list = list.split('[')[-1].replace('"','').split(',')

                for value, theme in zip(variants_list, variant_theme):                    
                    variant_dict[asin][theme.strip()] = value

                    if value in image_script:
                        Images_Found = True
                        for images in image_script[value]:
                            variant_dict[asin]['Images'].append(images['large'])
                    else:
                        image_values +=  value + ' '
                
                if not Images_Found:
                    try:                        
                        for images in image_script[image_values.strip(' ')]:                        
                            variant_dict[asin]['Images'].append(images['large'])
                    except:
                        pass
                    
            '''Finding out the Price of Each Variant'''         
            price_dict = {}
            price_dict = parse_pricing(variant_dict)

            '''Creating Variant Dictionaries for .csv format''' 
            variant_dict, variation_theme = create_variants(variant_dict, price_dict, parent_dict, mywriter, category_name)
            return variant_dict, variation_theme

def create_variants(variant_dict, price_dict, parent_dict, mywriter, category_name):
            dict = {}
            variation_theme = None                        
            for asin, variant in variant_dict.iteritems():
                try:
                    dict[asin] = {}
                    product_name = parent_dict['item_name']
                    variant_name = get_variant_name(variant, product_name)
                    dict[asin] = default_values(variant_name, category_name)                
                    dict[asin].update(parent_dict)
                    dict[asin]['item_name'] = variant_name
                    dict[asin]['item_sku'] = dict[asin]['part_number'] = 'LYS' + asin
                    dict[asin]['external_product_id'] = asin
                    dict[asin]['standard_price'] = price_dict[asin]
                    dict[asin].update(clean_images(variant['Images']))
                    dict[asin]['parent_child'] = 'child'
                    dict[asin]['parent_sku'] = parent_dict['external_product_id']
                    dict[asin]['relationship_type'] = 'Variation'                   
                    
                    if set(('color_name','size_name')).issubset(variant):                        
                        dict[asin]['variation_theme'] = 'SizeName-ColorName'
                        dict[asin]['size_name'] = variant['size_name']
                        dict[asin]['color_name'] = variant['color_name']

                    elif 'color_name' in variant:
                        dict[asin]['color_name'] = variant['color_name']
                        dict[asin]['variation_theme'] = 'ColorName'                

                    elif 'style_name' in variant:
                        dict[asin]['style_name'] = variant['style_name']
                        dict[asin]['variation_theme'] = 'StyleName'                      
                    else:
                        dict[asin]['size_name'] = variant['size_name']
                        dict[asin]['variation_theme'] = 'SizeName'

                    variation_theme = dict[asin]['variation_theme']
                except:                    
                    del dict[asin]
                    pass            

            
            return dict, variation_theme

def get_variant_name(variant, product_name):
    
    if set(('color_name','size_name')).issubset(variant):
        variant_name = '%s %s %s' %(product_name.split(',')[0],variant['color_name'],variant['size_name'])
    elif 'color_name' in variant:
        variant_name = '%s %s ' %(product_name.split(',')[0],variant['color_name'])
    elif 'size_name' in variant:
        variant_name = '%s %s' %(product_name.split(',')[0],variant['size_name'])
    else:
        variant_name = product_name

    return variant_name
# 