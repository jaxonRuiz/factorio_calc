#main class used to store basic data reading and processing
#functionality to filter all recipes to only pull relevant recipes given a final output product.
#can use a recursion tree style structure to crawl down and grab relevant items
#then use linear programming (and manual settings to restrict locked recipes if needed) to optimize
#and/or get ratios needed, expanded out to calculate quantities needed given a goal.

import json



#can maybe use live data from updating factorio json file to work things, if i can get the live json file.
flag = False
#ctrl-f "if self.flag: print" to find all debug flags.""

class Container():
    def __init__(self,raw,live_data=False):
        self.raw_data = {}
        self.raw_items = {}
        self.uniques = {"groups":{},"sub-groups":{}} #store unique recipe categorizations and items
        self.all_items = [] #maybe dictionary to make it easier to search for recipes that fit with item..?
        #self.production_sets = [] contain all needed items/recipes to get a chosen final item. 
        #should have another class to organize production lines and segment relevant recipes/items

        #func to filter attributes. returns dictionary
        def filter_attributes(item:dict):
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
            #maybe get rid of type?
            if self.raw_data[i]["ingredients"] not in self.all_items: self.all_items.append(self.raw_data[i]['ingredients'])
            if self.raw_data[i]["products"] not in self.all_items: self.all_items.append(self.raw_data[i]['products'])

    def delete_group(self, to_delete): #remove entire group from raw_data
        delete_set = []
        for i in self.raw_data:
            if self.raw_data[i]["group"] == to_delete:
                delete_set.append(i)
        for j in delete_set:
            del self.raw_data[j]
        del self.uniques['groups'][to_delete]
        self.update_data()

    def delete_subgroup(self, to_delete): #remove entire group from raw_data
        delete_set = []
        for i in self.raw_data:
            if self.raw_data[i]["subgroup"] == to_delete:
                delete_set.append(i)
        for j in delete_set:
            del self.raw_data[j]
        del self.uniques['sub-groups'][to_delete]
        self.update_data()
        
    def delete_recipe(self, to_delete): #delete single recipe
        pass


    #finding recipes from items
    def find_recipes(self, in_item): #pull ALL recipes containing an item
        pass
    def find_producers(self, in_item:str): 
        """find which recipes PRODUCE an item"""
        #so if i put in petroleum gas, basic/advanced oil processing pops up, as well as any other recipes that PRODUCE petroleum
        out = []
        for i in self.raw_data:
            recipe = self.raw_data[i]
            
            items = [name["name"] for name in recipe["products"]]
            if in_item in items:
                out.append(recipe)
                #if flag:print(in_item + " is made in: " + (recipe["name"]))
        
        return out #returns a list of all producering recipes
        #! LIST IS OF DICTIONARY VALUES. SHOULD STANDARDIZE STR INPUTS AND DICTIONARY OUTPUTS ?


    def find_consumers(self, in_item:str): #find which recipes USE an item
        """find which recipes CONSUME an item"""
        out = []
        for i in self.raw_data:
            recipe = self.raw_data[i]
            
            items = [name["name"] for name in recipe["ingredients"]]
            if in_item in items:
                out.append(recipe)
                #if flag:print(in_item + " is used in: " + (recipe["name"]))
        return out #returns list of consuming recipes

    def find_products(self,recipe:str): 
        """returns list of item dictionaries"""
        out = []
        names = [product["name"] for product in self.raw_data[recipe]["products"]]
        quantity = [product["amount"] for product in self.raw_data[recipe]["products"]]
        probability = []
        for product in self.raw_data[recipe]["products"]:
            try:
                probability.append(product["probability"])
            except:
                probability.append(1)
        for i in range(len(names)):
            dichaha =      {"name": names[i],
                             "amount": quantity[i],
                             "probability": probability[i]}
            out.append(dichaha)

        return out #returns list of dictionary values of items
    
    def find_ingredients(self,recipe:str): 
        """returns list of item dictionaries"""
        out = []
        names = [ingredient["name"] for ingredient in self.raw_data[recipe]["ingredients"]]
        quantity = [ingredient["amount"] for ingredient in self.raw_data[recipe]["ingredients"]]
        
        for i in range(len(names)):
            dichaha =      {"name": names[i],
                             "amount": quantity[i]}
            out.append(dichaha)
        return out #returns list of dictionary values of ITEMS
    def getGroups(self):
        return list(self.uniques["groups"].keys())
    def getSubgroups(self):
        return list(self.uniques["sub-groups"].keys())
    
    def export(self,name="cleaned.json"):
        with open(name,"w") as output:
            json.dump(self.raw_data,output,indent=4)



class Node(): #contains head of recipe chain, and its ingredients. used together to make a production line
    def __init__(self, head_recipe:str,recipe_set:Container): 
        data = recipe_set #store main dataset for use
        self.ingredients = [] #all ingredients of a given recipe
        self.products = [] #all outputs of a given recipe
        self.ind = 0 #used to make looping easier lol
        self.producer = "RAW" #stores recipe names that make head item. will be 'EMPTY' if item is raw
        self.head = {'name':"RAW"} #use head for actual naming i guess
        try:
            self.head = data.raw_data[head_recipe] #full data set if ever needed
        except:
            if flag: print("===[raw item found: "+head_recipe+"]===")
            self.head = {'name':head_recipe}
        else:
            self.producer = head_recipe
            self.ingredients = data.find_ingredients(self.producer)
            self.products = data.find_products(self.producer)

            self.ind = range(len(self.ingredients)) #for easier looping
            if flag:
                self.__str__()
                

    def get_key_product(self):
        for item in self.products:
            print(item)
            if item['name'] == self.head['name']:
                return item #only returns desired product for filtering
    def __str__(self):
            print("recipe: " + self.producer)
            print(f"products: {self.products}")
            print(f"key product: {self.get_key_product()}")
            print(f"ingredients: {self.ingredients}")
            print()


flag=False
class ProductionUnit(Node): 
    def __init__(self,root_recipe:str,recipe_set:Container):
        self.node = Node(root_recipe,container)
        self.data = recipe_set
        self.branch_nodes = [] #contains nodes
    
    def full_traverse(self): #THIS IS RECURSION CODE, ITS NOT CHECKING CHILD NODES CORRECTLY (or maybe it works? recycling recipes just fucked it up i think)
        if self.node.producer != "RAW": #only goes if not a raw item
            #do i need to clear branch nodes? prob wont use this func multiple times, but whatever
            self.branch_nodes.clear()
            for i in self.node.ind:
                try: #checking for RAW. may be better solution
                    #print(self.node.ingredients[i]["name"])
                    self.branch_nodes.append(ProductionUnit(self.node.ingredients[i]["name"],self.data)) #should go and repeat process with each ingredient of head.
                    self.branch_nodes[i].full_traverse()
                except:
                    print("something happened during full_traversal")
                    pass

    def print_rec(self,spacer=0):
        out = "\n"
        for i in range(spacer):
            out+=" | "
        out+="["
        out += self.node.head['name']
        out+=": "
        if self.node.producer == "RAW": 
                out+= "RAW"
        for i in range(len(self.branch_nodes)):
            out += self.branch_nodes[i].print_rec(spacer+1)
        out+="]"
        return out
    
    def __str__(self):
        out = self.print_rec()
        return out

"""
processing step ideas:

-DFS recursion search to get all needed recipes (branching through possible paths based on multiple recipes)

-start from given point, standardize to 1/s, and apply to all ingredients. standardize their ingredients from there

-create specified class to store root recipe, and have branching connections downwards as needed. maintain node connections through own class. probably this.
more redundant, but i get to make my own tools by hand...
^i think do this idea for now.
"""

if __name__ == "__main__":
    with open("recipe.json","r") as f:
        raw = json.load(f)

    container = Container(raw)
    print(container.getGroups())

    #container.delete_group("smelting-crafting")
    #container.delete_subgroup("recycling")
    print(container.getGroups())

    #input to production unit is recipe. for ui, maybe have a way to get recipe from item..
    rootNode = ProductionUnit("se-rocket-launch-pad",container)
    rootNode.full_traverse()
    print(rootNode)

    #use memoization optimization for recursive calls...