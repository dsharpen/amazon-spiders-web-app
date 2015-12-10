import unicodecsv
import os
import pprint
import csv
import collections, datetime



def flat_file_headers(category_name):
	
	flat_file_name = flat_file_type(category_name)
	path_to_file = os.path.realpath('utilities/FlatFile_Templates/%s' %(flat_file_name))
	input_file = open(path_to_file, 'r')

	header_dict = collections.OrderedDict()

	for row in csv.reader(input_file):
		for column in row:
			header_dict[column] = ''

	return header_dict

def flat_file_type(category_name):
	dict = {
			# 'Electronics' : '.csv',
			'Sports Equipment': 'Sports_Equipment.csv',
			# 'Health and Beauty': 'Accessories.csv',
			# "Women's Fashion Accessories" : 'Accessories.csv',
			'Toys and Games': 'Toys.csv',
			"Men's Fashion Shoes": 'shoes.csv',
			"Other Sports Shoes": 'shoes.csv',
			"Women's Sports Shoes": 'shoes.csv',
			"Men's Running Shoes": 'shoes.csv',
			"Women's Running Shoes": 'shoes.csv',
			"Women's Fashion Shoes": 'shoes.csv',
			}
			
	return dict[category_name]	



def default_values(item_name, category_name):

	dict = flat_file_headers(category_name)	
	dict['external_product_id_type'] = 'asin'
	dict['update_delete'] = 'update'
	dict['condition_type'] = 'New'
	dict['quantity'] = 10
	dict['item_package_quantity'] = 1
	dict['fulfillment_latency'] = 15
	feed_dict = {
			# 'Electronics' : '.csv',
			'Sports Equipment': 'SportingGoods',
			# 'Health and Beauty': 'Accessories.csv',
			# "Women's Fashion Accessories" : 'Accessories.csv',
			'Toys and Games': 'Toys.csv',
			"Men's Fashion Shoes": 'shoes',
			"Other Sports Shoes": 'shoes',
			"Women's Sports Shoes": 'shoes',
			"Men's Running Shoes": 'shoes',
			"Women's Running Shoes": 'shoes',
			"Women's Fashion Shoes": 'shoes',
			}
	dict['feed_product_type'] = feed_dict[category_name]
	# feed_defaults = {'shoes': { 'outer_material_type1' = 'Synthetic',
 #    							'outer_material_type2' = 'Mesh',
 #    							'lifestyle' = 'Casual'
	# 							}
	# 				}

	return dict



def get_browse_nodes():
	'''
	Dictionary of Amazon.com browse nodes as keys and relative Amazon.in browse nodes as values
	'''
	path_to_file = os.path.realpath('utilities/%s' %('BrowseNodeMapping.csv'))

	input_file = open(path_to_file, 'r')
	mapping_dict ={}	
	for row in csv.reader(input_file):
		mapping_dict[row[0]] = row[1]

	return mapping_dict

def initialize_csv(output_file, category_name):

	path = ('Outputs/%s' %(output_file.split('-')[0]) )
	if not os.path.exists(path):
		os.makedirs(path)

	output = open(os.path.join(path, output_file+'.csv'), 'wb')
	mywriter = unicodecsv.writer(output)
	header_dict = flat_file_headers(category_name)
	header_row = []
	for row in header_dict:
		header_row.append(row)

	mywriter.writerow(header_row)
	return mywriter


def write__csv(dict, mywriter):
	csv_row = []	
	for key, value in dict.iteritems():
		csv_row.append(value)	

	mywriter.writerow(csv_row)

def calculate_filesize(filename):
	path = os.path.realpath('Outputs/%s/%s' %(filename.split('-')[0], filename+'.csv'))
	
	filesize = (float(os.path.getsize(path))/1000000)
	return filesize
