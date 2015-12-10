import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess
from utilities import mycsv, converter, variants
from utilities.amazon_api import Variant_Lookup
from StartUrls import start_urls

import sys
import pprint
import re, demjson, unicodecsv
count_output = 0

class Main_Scrapper(CrawlSpider):
		name = 'main'
		rules = (
				# Rule (LinkExtractor(allow=(),restrict_xpaths=('//span[@class="pagnNext"]',)), follow= True),
				Rule (LinkExtractor(allow=(),restrict_xpaths=('//a[@class="pagnNext"]',)), follow= True),
				Rule (LinkExtractor(allow=(),restrict_xpaths=('//a[@class="a-link-normal s-access-detail-page s-overflow-ellipsis a-text-normal"] | //a[@class="a-link-normal s-access-detail-page  a-text-normal"]',)), 
					callback="parse_product" , follow= True),)

		
		# def parse(self, response):
		def parse_product(self, response):		
			print 'Parsing Product'			
			sel = Selector(response)
			global output_file, count_output, mywriter			
			
			if mycsv.calculate_filesize(output_file) > (22): #Limiting each output file to 22MB
				output_file = '%s-%s' %(output_file.split('-')[0], str(count_output))
				count_output += 1				
				mywriter = mycsv.initialize_csv(output_file, category_name)
			
			dict = {}	
			browse_nodes_list = [node.strip().split('=')[-1] for node in sel.xpath("//div[@id='wayfinding-breadcrumbs_feature_div']/ul//a/@href").extract()]						
			dict.update(converter.clean_browsenodes(browse_nodes_list,category_name))						
			
			dict['item_name'] = sel.xpath("//span[@id='productTitle']/text()").extract()[0]			
			dict['external_product_id'] = parent_ASIN = sel.xpath("//div[@id='tell-a-friend']/@data-dest").extract()[0].split('parentASIN=')[-1].split('&')[0]						
			dict['item_sku'] = dict['part_number'] = 'LYS' + dict['external_product_id'] 			
			try:
				dict['brand_name'] = sel.xpath("//a[@id='brand']/text()").extract()[0]
			except:
				dict['brand_name'] =  sel.xpath("//a[@id='brand']/@href").extract()[0].split("/")[1]
			dict['manufacturer'] = dict['brand_name']			
			dict['item_length'],dict['item_height'],dict['item_width'], dict['item_dimensions_unit_of_measure'] = converter.clean_dimensions(sel.xpath("//li[contains(text(),'inches')][contains(text(),'x')]/text()").extract())						
			dict['product_description'] = ' '.join(x for x in sel.xpath("//div[@id='productDescription']/p/text()").extract())			
			dict.update(converter.clean_bullet_points(sel.xpath("//ul[@class='a-vertical a-spacing-none']//span/text()").extract()))			
			dict['parent_child'] = 'Parent'		
			dict['department_name1'] = dict['target_gender'] = converter.clean_department_name(dict['item_name'])			
			dict['generic_keywords1'] = dict['generic_keywords'] = dict['item_name']			

			output__dict = mycsv.default_values(dict['item_name'],category_name)
			output__dict.update(dict)			
			variant_script = sel.xpath("//script[@language='JavaScript'][contains(text(),'window.isTwisterAUI = 1')]").extract()
			
			if ('shoes' in category_name.lower() and variant_script) or variant_script:
				print 'Variants'											
				'''
				Initializing Dictionaries for Variants(Asin, Variant Values), Pricing(Asin, Price) and Images(Asin, Images)
				'''
				variant_script = sel.xpath("//script[@language='JavaScript'][contains(text(),'window.isTwisterAUI = 1')]").extract()[0]
				image_script = sel.xpath("//script[@type='text/javascript'][contains(text(),'customerImages')]").extract()[0]				
				variant_dict, output__dict['variation_theme'] = variants.clean_variants(variant_script, image_script, dict, mywriter, category_name)

				'''Writing Parent Row'''
				mycsv.write__csv(output__dict, mywriter)				
				'''Writes Variants to CSV'''
				
				for asin, child_dict in variant_dict.iteritems():										
					mycsv.write__csv(child_dict, mywriter)

			else:				
				images = sel.xpath("//img[@id='landingImage']/@data-a-dynamic-image").extract()[0]
				images = re.findall(r'(http.*?.jpg)',images)
				output__dict['main_image_url'] = images[0]				
				for index, image in enumerate(images[1:],1):
					output__dict['other_image_url'+str(index)] = image
					if index == 3:
						break						

				output__dict['variation_theme'] = ''				
				output__dict['standard_price'] = converter.calculate_price(sel.xpath("//span[@id='priceblock_ourprice']/text()| //span[@id='priceblock_saleprice']/text()").extract()[0].split('-')[-1].strip('$'))				
				mycsv.write__csv(output__dict, mywriter)

# def start_crawl(choice):
		# print sys.argv[0]
		# global output_file, category_name		
		# category_name = choice
		# start_urls = get_start_urls(category_name)
		# output_file = category_name
		# mywriter = mycsv.initialize_csv(output_file, category_name)

		# process = CrawlerProcess()										
		# process.crawl(Main_Scrapper, start_urls = start_urls)		
		# process.start()		

if __name__ == '__main__':
		print 'Main Started'
		global start_urls, output_file, category_name
		category_name = ' '.join(arg.replace("Mens","Men's").replace("Womens","Women's") for arg in sys.argv[1:])
		start_urls = start_urls.get_start_urls(category_name)
		output_file = category_name
		mywriter = mycsv.initialize_csv(output_file, category_name)

		process = CrawlerProcess()										
		process.crawl(Main_Scrapper, start_urls = start_urls)
		# process.crawl(Main_Scrapper, start_urls = [
			# 'http://www.amazon.com/Timberland-Earthkeepers-Kempton-Oxford-Grain/dp/B00L2P58P4/'])
			# 'http://www.amazon.com/Magellan-eXplorist-510-Waterproof-Hiking/dp/B003Y5H17I'])
					

		process.start()		
