import json

temp = {"name": "Bob", "languages": "English", "numbers": [2, 1.6, "null"]}
with open("recipe.json","r") as f:
    raw = json.load(f)
print(len(raw))
#func to filter attributes
def filter_attributes(item):
    out = {}
    #attributes to keep
    out["name"] = item["name"]
    out["group"] = item["group"]["name"]
    out["subgroup"] = item["subgroup"]["name"]
    keep = ["energy","ingredients","products"] 
    for category in keep:
        out[category] = item[category]
    
    return out #returns contents as dictionary


#cleaning out unneeded attributes
clean = {}
uniques = {"groups":[],"sub-groups":[]}
for item in raw:
    if not raw[item]["hidden"]:
        clean[item] = filter_attributes(raw[item])
    



with open("cleaned.json","w") as output:
    json.dump(clean,output,indent=4)