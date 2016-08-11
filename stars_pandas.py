import pandas as pd

data = pd.read_csv('data/stars.tsv', skiprows=range(43)+[44,45])

print data

names = pd.read_csv('data/stars_names.tsv', skiprows=range(32)+[33,34]) 

print names

#constellations = pd.read_csv('data/stars_cons.tsv')
