#-------------------------------------------------------------------------------------------
# ACW.
# Calculation of the average cubic weight for a list of products in JSON.
# Usage: python acw.py url
# See README for more details.
#-------------------------------------------------------------------------------------------

import sys
import json
import pprint
import urllib2
from operator import mul

# Class representing a product
#-------------------------------------------------------------------------------------------
class Product(object):

	def __init__(self, data, dimtype):	
		self._data = data
		self._dimention_type = dimtype
		
	# Getters of attributes and dimensions
	def get_attribute(self, name):
		return self._data[name] if name in self._data else None

	def get_dimensions(self):
		return map(lambda x: str(x), self.get_attribute(self._dimention_type).keys())
	
	def get_size(self, dimname):
		return self.get_attribute(self._dimention_type)[dimname]
		
	# Calculation of the average cubic weight in cubic meters
	def get_average_cubic_weight(self, cubic_conv_factor = 250., cm2m_factor = 100.):		
		product = reduce(mul, map(lambda dim: self.get_size(dim), self.get_dimensions()), 1)
		return (product / cm2m_factor**3) * cubic_conv_factor

# Utility function to open the API endpoint and convert it to a JSON data string
#-------------------------------------------------------------------------------------------
def get_api_endpoint(url):

	try: 
		# Open url and dump response to a JSON string
		data = json.load(urllib2.urlopen(url))
	except (urllib2.URLError, ValueError), e: 
		sys.exit(e)
	return data["objects"]

# Main program
#-------------------------------------------------------------------------------------------
def main(target_category):

	# Read the API endpoint
	if len(sys.argv) != 2:
		sys.exit("Usage: python acw.py url")
		
	url = sys.argv[1] # Assuming that url is valid
	objects = get_api_endpoint(url)
	
	# Loop over objects, build products, calculate average cubic weights, and store
	data = dict()
	for object in objects:
		product = Product(object, "size")
		category = product.get_attribute("category")
		# find desired product
		if category == target_category:
			data[product.get_attribute("title")] = product.get_average_cubic_weight()
	
	return data # return results
			
# Calling main with one specific category ("Air Conditioners") and printing results
#-------------------------------------------------------------------------------------------
if __name__ == "__main__":

	target_category = "Air Conditioners"
	result = main(target_category)
	print ("Average cubic weight (ACW) for the \"%s\" category:" % target_category)
	print ("\n".join(" {0: <60} => {1: <10} (kg)".format(k, v) for k, v in result.items()))

