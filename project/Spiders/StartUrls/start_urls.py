import csv
import os
import collections

def get_start_urls(category):
	start_urls_dict = generate_urls_dict()
	print category
	if category:
		print  start_urls_dict[category]
		url_list = start_urls_dict[category]		
	else:
		url_list = []
		for category, urls in start_urls_dict.iteritems():
			url_list += urls
	return url_list

def generate_urls_dict():
	'''
		Generates dictionary of all category URLS to be scrapped
	'''
	start_urls_dict = collections.OrderedDict()	
	path_to_file = os.path.realpath('StartUrls/Start_Urls.csv')	
	file = open(path_to_file, 'r')

	for row in csv.reader(file):		
		if row[1] not in start_urls_dict:
			start_urls_dict[row[1]] = []
		start_urls_dict[row[1]].append(row[0])
	file.close()


	return start_urls_dict
	
if __name__ == "__main__":
	start_urls()