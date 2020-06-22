#scrapes Vietnamese Recipe Collection from Saveur Magazine

from bs4 import BeautifulSoup
import requests
import re
import json
import time


all_my_recipes = []

url = "https://www.saveur.com/article/collection/vietnamese-recipes/"

results_page = requests.get(url)
results_page_html = results_page.text
soup = BeautifulSoup(results_page_html, "html.parser")

recipes = soup.find_all('h3')

for recipe in recipes:

	my_recipe_data = {
	"title" : None, 
	"url" : None,
	"description" : None,
	"ingredients" : None,
	"instructions" :None,
	}

	# print("----------------")

	title = recipe.find('a')
	title_text = title.text
	my_recipe_data['title'] = title_text

	url = title['href']
	url = "https://www.saveur.com/" + url
	my_recipe_data['url'] = url
	

	recipe_request = requests.get(url)
	recipe_html = recipe_request.text
	recipe_soup = BeautifulSoup(recipe_html, "html.parser")

	description = recipe_soup.find('meta')
	description = description["content"]
	my_recipe_data["description"] = description
	
	ingredients = recipe_soup.find('ul', attrs={"class": "ingredients"})
	ingredients = ingredients.text
	ingredients = ingredients.replace('\n', ";")
	ingredients = ingredients.replace(";;;", "; ")
	ingredients = ingredients.replace(";; ", "")
	my_recipe_data['ingredients'] = ingredients

	try: 
		instructions = recipe_soup.find("ol", attrs={"class": "instructions multiple"})
		instructions = instructions.text
		instructions = instructions.replace('\n', ";")
		instructions = instructions.replace(';;', ";")
		my_recipe_data['instructions'] = instructions
	except AttributeError: 
		pass

	time.sleep(5)

	print(my_recipe_data)

	all_my_recipes.append(my_recipe_data)

with open('Vietnamese_Recipe_Collection_Saveur.json', 'w') as file_object:
	json.dump(all_my_recipes, file_object, indent=2)
	print("chef's kiss!")


