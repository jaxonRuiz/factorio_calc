#get a list of all relevant items, by cross checking all products/ingredients in recipes, then filter for items on json
import json

with open("cleaned.json",'r') as f:
    recipes = json.load(f)

items = []

def get_items(d): #func to get items as just names from dictionary
    out = []
    for name in d:
        out.append(name)
    return out

def check_distinct(input): #func to check if item is already in list
    for i in input:
        name = i["name"]
        if name not in items: items.append(name)

for i in recipes:
    ingredients = recipes[i]['ingredients']
    products = recipes[i]["products"]
    check_distinct(ingredients)
    check_distinct(products)


print(items)
    

    
#should get rid of environment group, because not needed
#maybe use hash table to search through items when necessary cuz they're not sorted. 
#or maybe sort them alphabetically and use advanced searching algorithm...
