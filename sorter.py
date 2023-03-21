#categorize groups and subgroups, and start organizing items
import json

with open("cleaned.json",'r') as f:
    items = json.load(f)

groups = {}
subs = {}

for i in items:
    if items[i]['group'] not in groups: groups[items[i]['group']] = [i]
    else: groups[items[i]['group']].append(i)
    if items[i]['subgroup'] not in subs: subs[items[i]['subgroup']] = [i]
    else: subs[items[i]['subgroup']].append(i)

#should get rid of environment group, because not needed

for i in groups.keys():
    print(i)

print()
print(groups["environment"])