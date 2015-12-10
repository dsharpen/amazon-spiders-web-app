import requests
from pprint import pprint
from datetime import datetime
import hashlib
import hmac
import base64
import csv
import re
from utilities import converter
from config import AWS_AccessKeyId, AWS_AssociateTag, AWS_SecretKey

def parse_pricing(variant_dict):
				price_dict = {}
				item_ids = ''
				x = 0
				for asin,variants in variant_dict.iteritems():					
					item_ids += asin + ','					
					'''
					 	Limiting 10 ASINs per resposne
					'''
					if item_ids.count(',') == 10:
						'''Using the Amazon Product Advertising API for find Pricese for each Varaint ASIN in item_id'''
						try:						
							price_dict.update(Variant_Lookup(item_ids))
						except:
							pass
						item_ids = ''										
				
				price_dict.update(Variant_Lookup(item_ids))
				return price_dict

def Variant_Lookup(item_id):
		
		# Keyword ='Carboflex 130'
		
		Operation = 'ItemLookup'
		ResponseGroup = 'Offers'
		SearchIndex = 'All'
		Service = 'AWSECommerceService'
		Timestamp = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.000Z")
		Timestamp = Timestamp.replace(":","%3A")

		string = """GET
webservices.amazon.com
/onca/xml
AWSAccessKeyId=%s&AssociateTag=%s&ItemId=%s&Operation=%s&ResponseGroup=%s&Service=%s&Timestamp=%s""" %(AWS_AccessKeyId, AWS_AssociateTag, item_id.replace(',','%2C'), Operation, ResponseGroup.replace(',','%2C'), Service, Timestamp)
		
		signature = (base64.b64encode(hmac.new("lQoQOPJ+aqny5BtehWFTFjm9Lbdu1OcVlJC7ncx4", msg=string, digestmod=hashlib.sha256).digest())).replace("=","%3D").replace("+","%2B")
		path = 'http://webservices.amazon.com/onca/xml?AWSAccessKeyId=%s&AssociateTag=%s&ItemId=%s&Operation=%s&ResponseGroup=%s&Service=%s&Timestamp=%s' %(AWS_AccessKeyId, AWS_AssociateTag, item_id.replace(',','%2C'), Operation, ResponseGroup, Service, Timestamp)
		
		response = requests.request('GET', path + '&Signature='+signature)				

		variant_dict = {}

		
		for variation in re.findall('<ASIN>(.*?)</Item>', response.text):
				try:
					ASIN = variation.split('</ASIN')[0]													
					ASIN_price = re.findall('\$(.*?)</FormattedPrice>',variation)[0].strip('$')
					ASIN_price = converter.calculate_price(ASIN_price)
					variant_dict[ASIN] = ASIN_price									
				except:
					pass
						
		return variant_dict
			

if __name__ == '__main__':
	item_id = 'B00YDHYL88,B00NUZBIJE,B00NUZDXAQ,B00NUZJ2ME,B00NUZBDSA,B00YDHYAUM,B00NUZBVFK,B00NUZC5WS,B00NUZDJGO,B00NUZB0BA,'	
	print create_request(item_id)
	
	