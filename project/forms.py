from flask_wtf import Form
from wtforms import RadioField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email
from Spiders.StartUrls.start_urls import generate_urls_dict
import pprint

class SpidersForm(Form):
	start_urls_dict  = generate_urls_dict()
	choices = []

	for index, category in enumerate(start_urls_dict,1):
		choices.append((category, category))
	
	spider_choice = RadioField(
				'Choose a Spider:',
				validators = [DataRequired()],
				choices = choices
						 )

