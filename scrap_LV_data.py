# python
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime as date
from os import path
from collections import ChainMap
import re

final_result = {}

today_date = date.today().strftime("%Y-%m-%d")

final_result["date"] = today_date
final_result["precise_date"] = date.today().strftime("%Y-%m-%d, %H:%M")


# Players Part
    
raw_htmls = open("lvtophtmls.txt","r").read().split(",")

attribute_colours = {"str": "red", "agi": "orange", "end": "yellow", "int": "olive", "lck": "green"}
ext_attributes_colours = {"lvl": "red", "rank": "yellow", "fame": "green", "power": "olive"}
achievement_colours = {"explores": "green", "quests": "olive", "monsters": "yellow", "caravan": "orange", "vault": "pink", "survival": "red"}

final_result["players"] = []
final_result["tribes"] = []

print("Scraping Player Data...")
for html in raw_htmls:
    soup = BeautifulSoup(requests.get(html).text, 'html.parser')

    # Name
    try:
        class_soup = soup.find("div", class_="sub header")
        class_soup.find("i").decompose()
    except AttributeError:
        print("nonetype at: " + html)

    
    player_class = class_soup.get_text().strip()
        
    name_soup = soup.find("h1")
    name_soup.find("div").decompose()
    player_name = re.sub("[\(\[].*?[\)\]]", "", name_soup.get_text()).strip()
    print(player_name)
        
    # Attributes
    attributes = [{attribute: int(soup.find(class_=f"{colour} inverted statistic").find("div", class_="value").get_text().strip().replace(',',''))} for attribute, colour in attribute_colours.items()]
    attributes = dict(ChainMap(*attributes))
    attributes['total']=sum(attributes.values())
    soup.find(class_="ui inverted segment").decompose()

    # External Attributes
    ext_attributes = [{attribute: soup.find(class_=f"{colour} inverted statistic").find("div", class_="value").get_text().strip()} for attribute, colour in ext_attributes_colours.items()]
    ext_attributes = dict(ChainMap(*ext_attributes))

    soup.find(class_="ui inverted segment").decompose()

    #Achievement Attributes
    ach_attributes = [{attribute: soup.find(class_=f"{colour} inverted statistic").find("div", class_="value").get_text().strip()} for attribute, colour in achievement_colours.items()]
    ach_attributes = dict(ChainMap(*ach_attributes))

    soup.find(class_="ui inverted segment").decompose()

    # Assign to JSON
    final_result["players"].append({"name": player_name, "class": player_class, "attributes": attributes, "ext_attributes": ext_attributes, "ach_attributes": ach_attributes})

print(json.dumps(final_result))

filename = f"database/{today_date}.json"
listObj = []

with open(filename, 'w') as json_file:
    json.dump(final_result, json_file,
                        indent=4,
                        separators=(',',': '))

print(f"Successfully created {today_date} to the JSON file")
