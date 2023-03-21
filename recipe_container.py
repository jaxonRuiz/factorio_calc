#main class used to store basic data reading and processing
#functionality to filter all recipes to only pull relevant recipes given a final output product.
#can use a recursion tree style structure to crawl down and grab relevant items
#then use linear programming (and manual settings to restrict locked recipes if needed) to optimize
#and/or get ratios needed, expanded out to calculate quantities needed given a goal.

import json



#can maybe use live data from updating factorio json file to work things, if i can get the live json file.
flag = True
#ctrl-f "if self.flag: print" to find all debug flags.""

class container():
    def __init__(self):
        self.raw_data = {}
        self.raw_items = {}
        self.uniques = {"groups":{},"sub-groups":{}} #store unique recipe categorizations and items
        self.all_items = [] #maybe dictionary to make it easier to search for recipes that fit with item..?
        #self.production_sets = [] contain all needed items/recipes to get a chosen final item. 
        #should have another class to organize production lines and segment relevant recipes/items

    def load_raw(self,input_file,live_data=False):
        with open("input_file","r") as f:
            raw = json.load(f)

        #func to filter attributes. returns dictionary
        def filter_attributes(item):
            out = {}
            #attributes to keep
            out["name"] = item["name"]
            out["group"] = item["group"]["name"]
            out["subgroup"] = item["subgroup"]["name"]
            keep = ["energy","ingredients","products"] 
            for category in keep:
                out[category] = item[category]
            return out 

        #removing
        for item in raw:
            if not raw[item]["hidden"] and not live_data: #condition that item is visible and live_data setting is off
                self.raw_data[item] = filter_attributes(raw[item]) #add item to output dict
            elif not raw[item]["hidden"] and raw[item]["enabled"]: #effectivly checks for enabled condition as well, if live_data setting enabled 
                if flag: print("\n!! live items setting enabled! !!\n") #make sure this flag doesnt come up when not using live data!
                self.raw_data[item] = filter_attributes(raw[item]) #adding item to output is both enabled and not hidden.

        self.update_data()

    def update_data(self):

        for i in self.raw_data:
            #placing all recipes in uniques groups, and adding names under these dictionaries        
            if self.raw_data[i]['group'] not in self.uniques["groups"]: self.uniques["groups"][self.raw_data[i]['group']] = [i] #adding first entry for new group
            else: self.uniques["groups"][self.raw_data[i]['group']].append(i)

            if self.raw_data[i]['subgroup'] not in self.uniques["sub-groups"]: self.uniques["sub-groups"][self.raw_data[i]['subgroup']] = [i]
            else: self.uniques["sub-groups"][self.raw_data[i]['subgroup']].append(i)

            #adding items. may change to dictionary instead of list to store source recipes?
            if self.raw_data[i]["ingredients"] not in self.all_items: self.all_items.append(self.raw_data[i]['ingredients'])
            if self.raw_data[i]["products"] not in self.all_items: self.all_items.append(self.raw_data[i]['products'])

    def delete_group(self, to_delete): #remove entire group from raw_data
        pass
    def delete_recipe(self, to_delete): #delete single recipe
        pass


    #finding recipes from items
    def find_recipes(self, in_item): #pull ALL recipes containing an item
        pass
    def find_producers(self, in_item): #find which recipes PRODUCE an item
        pass
    def find_consumers(self, in_item): #find which recipes USE an item
        pass

    def export(self):
        with open("cleaned.json","w") as output:
            json.dump(self.raw_data,output,indent=4)

if __name__ == "__main__":
    pass
