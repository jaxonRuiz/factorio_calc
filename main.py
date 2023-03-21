import os

#its scuffy but i can use this to run things i guess...
def s(file):
    return "C:/Users/bluea/anaconda3/envs/home/python.exe c:/Users/bluea/OneDrive/Documents/.STUFF/code/personal_code/python/factorio_calculator_v1/" + file 

def run_item_sorter():
    os.system(s("item_sorter.py"))

def run_sorter():
    os.system(s("sorter.py"))

def run_cleaner():
    os.system(s("cleaner.py"))