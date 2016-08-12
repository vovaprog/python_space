import pandas as pd
import numpy as np

from spaceutils import parallax_millisecond_to_light_year, show_maximized_plot


data = pd.read_csv('data/stars.tsv', sep='|', skiprows=range(43)+[44,45])
names = pd.read_csv('data/stars_names.tsv', sep='|', skiprows=range(32)+[33,34]) 
constellations = pd.read_csv('data/stars_cons.tsv', sep='|', skiprows=range(34)+[35,36])


data.rename(columns={'_Glon': 'glong', '_Glat': 'glat'}, inplace=True)

data = pd.merge(data, names, how='left', on='HD')
data = pd.merge(data, constellations, how='left', on='HD')


data = data[ data['Plx'] != 0]
data['Plx'] = data['Plx'].abs() 

data['dist'] = parallax_millisecond_to_light_year(data['Plx'])
data["glong"] = np.radians(data["glong"])
data["glat"] = np.radians(data["glat"])

data["x"] = data["dist"] * np.cos(data["glat"]) * np.cos(data["glong"])
data["y"] = data["dist"] * np.cos(data["glat"]) * np.sin(data["glong"])
data["z"] = data["dist"] * np.sin(data["glat"])

data.drop_duplicates('HD', inplace=True)

data.sort('Vmag', inplace=True)

print data

