import re
import demjson
import unicodecsv
import pprint
import os
from mycsv import default_values, get_browse_nodes
un_mapped_node_file = False

def clean_browsenodes(browsenodes_list, category_name):
    dict = {}
    mapping_dict = get_browse_nodes()
    
    '''
                Creating a csv of unmapped browse nodes
    
    '''
    global un_mapped_node_file
    
    if not un_mapped_node_file:
        path = ('Outputs/%s' %(category_name))
        if not os.path.exists(path):
            os.makedirs(path)        
        un_mapped_node_file = open(os.path.join(path, 'UnMapped_Nodes_%s.csv'%(category_name)), 'wb')


    mywriter = unicodecsv.writer(un_mapped_node_file)
    count = 1
    for index, node in enumerate(browsenodes_list,1):        
        
        if node in mapping_dict:            
            dict['recommended_browse_nodes'+str(count)] = mapping_dict[node]
            count += 1
        else:
            dict['recommended_browse_nodes'+str(count)] = 'unmapped-%s' %(node)
            mywriter.writerow([node])


    return dict


def clean_dimensions(dimensions):
    if dimensions:
        dimensions = dimensions[0].split('inches')[0].strip(' ').split('x')                    
        if 'inches' in dimensions[0]:
            item_dimensions_unit_of_measure = 'IN'
        else:
            item_dimensions_unit_of_measure = ''

        item_length,item_height,item_width = dimensions[0], dimensions[1], dimensions[0]
    else:
        item_length = item_width = item_height = item_dimensions_unit_of_measure = ''

    return item_length, item_height, item_width, item_dimensions_unit_of_measure

def clean_department_name(item_name):
    if 'women' in item_name.lower():
                department_name1 = target_gender = 'Women'
    else:
                department_name1 = target_gender  = 'Men'
    return department_name1

def clean_bullet_points(bullet_points):
    dict = {}
    for index, feature in enumerate(bullet_points,1):
                dict['bullet_point'+str(index)] = dict['generic_keywords'+str(index)] = feature
                if index == 5:
                    break
    dict['outer_material_type1'] = 'Synthetic'
    dict['outer_material_type2'] = 'Mesh'
    dict['lifestyle1'] = 'Casual'
    return dict

def calculate_price(cost_price, *args):
    '''
    Takes price in dollars and returns price with margins in rupees 
    '''
    if '-' in cost_price:
        cost_price = cost_price.split('-')[1] 

    cost_price = float(cost_price) * 69
    Amazon_Commission = 11/100
    VAT = 14.5/100
    if args:
        for volume in args:            
            international_shipping = 1500*volume
    else:        
        international_shipping = 1500

    customs = (cost_price*30/100 + international_shipping)*33/100    
    delivery = 300
    
    selling_price = cost_price

    while selling_price:
        selling_price += 1
        deductions =  (selling_price*VAT) + (selling_price*Amazon_Commission)+ delivery + customs + international_shipping         
        net_profit = (selling_price - cost_price - deductions)/selling_price*100

        if net_profit>16:  
            print cost_price, selling_price, 'X'          
            return selling_price
            break
            
def clean_images(images):
    
    dict = {}
    dict['main_image_url'] =  images[0]
    for index,image in enumerate(images[1:],1):
        dict['other_image_url'+str(index)] = image
        if index == 7:
            break
    return dict


    