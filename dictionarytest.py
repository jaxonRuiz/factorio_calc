d = {
    1:"one",
    "ayy": [1,2,3],
    "nest": {
    "lookit":"me!"
    }
}

print(d[1]) #>one
print(d["ayy"][0]) #>1
print(d["nest"]["lookit"]) #>me!
print(d["nest"]) #>{'lookit': 'me!'}
d['new'] = 'fren'
print()
for i in d:
    print(type(i))