from recipe_container import *
#just temp file to work on factorio calculator remotely without messing with out of date github
with open("recipe.json","r") as f:
        raw = json.load(f)

container = Container(raw)
container.delete_group("smelting-crafting")
container.delete_group("environment")
container.delete_subgroup("recycling")

prod = ProductionUnit("automation-science-pack",container)
prod.full_traverse()
print(prod)


#currently production unit gets all required ingredients.

#function to get a flat list of all items needed.
"""IN PRODUCTION NODE CHANGE INIT CONTAINER TO RECIPE_SET"""
#replace self with root
def update_dic(new_dic,base_dic): #updates dictionary values
    print(new_dic)
    
    for item in new_dic.keys():
        if item in base_dic:
            base_dic[item] += new_dic[item]
        else:
            base_dic[item] = new_dic[item]
    return base_dic

#will need to modify to fit in the class
def collect_totals(cur:ProductionUnit,running_dic={}):
    if len(cur.branch_nodes) > 0: #recursive case
        for i in range(len(cur.branch_nodes)):
            if cur.node.head['name'] not in running_dic.keys(): #if item is new, creates new entry in running dictionary
                running_dic[cur.node.head["name"]] = cur.node.ingredients[i]["amount"]
            else:#else just adds quantity to running total
                print("adding quantity")
                running_dic[cur.node.head["name"]] += cur.node.ingredients[i]["amount"]
            
            #ADD: prod.branch_nodes[i]. TO FRONT OF COLLECT_TOTALS() CALL WHEN PUTTING IN CLASS
            
            if len(cur.branch_nodes[i].branch_nodes) >0:
                running_dic = update_dic(collect_totals(cur.branch_nodes[i],running_dic),running_dic) #issue is here. new dic not being read
                #correctly. 

    else: #base case if raw item (no ingredients)
        print('raw item found')
        return running_dic
   
print(prod.node.ingredients)
print()

d=collect_totals(prod)
print(d)