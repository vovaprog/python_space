import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import mpl_toolkits.mplot3d.art3d as art3d
import re
import numpy.lib.recfunctions as rfn
from matplotlib.patches import Circle

from spaceutils import parsec_to_lightyear, show_maximized_plot


#================================================================================================

PLEIADES_MAGIC_ID = 20000000
HYADES_MAGIC_ID = 20000001
ORION_NEBULA_NGC = 1976


def convert_ngc(ngc_string):
    match = re.search('NGC\\s+([0-9]+)', ngc_string)
    if match is not None:
        return int(match.group(1))
    else:
        match = re.search('IC\\s+([0-9]+)', ngc_string)
        if match is not None:
            return int("100" + match.group(1))
        elif 'Melotte 22' in ngc_string:
            return PLEIADES_MAGIC_ID
        elif 'Melotte 25' in ngc_string:
            return HYADES_MAGIC_ID
        else:
            return 0


def convert_distance(s):
    s = s.strip()
    return int(s) if s != '' else 0

data = np.loadtxt('data/open_clusters.tsv', skiprows=42, delimiter='|', usecols=(0, 1, 2, 3),
                dtype=[('glong', 'float'), ('glat', 'float'), ('ngc', 'int'), ('dist', 'int')],
                converters={2: convert_ngc, 3: convert_distance})


def convert_ngc2(ngc_string):
    ngc_string = ngc_string.strip().replace("I", "100")
    return int(ngc_string)

ngc_to_messier = np.loadtxt('data/ngc_to_messier.tsv', skiprows=43, delimiter='|', usecols=(0, 1, 2),
                            dtype = [('ngc', 'int'), ('type', 'S20'), ('messier', 'S20')],
                            converters = {0: convert_ngc2, 1: lambda s: str(s).strip()})


#================================================================================================


fill_with_zeros = np.zeros(data.size)

data = rfn.append_fields(data, ['x', 'y', 'z'], [fill_with_zeros, fill_with_zeros, fill_with_zeros], usemask=False)

data["dist"] = parsec_to_lightyear(data["dist"])

data["glong"] = np.radians(data["glong"])
data["glat"] = np.radians(data["glat"])

data["x"] = data["dist"] * np.cos(data["glat"]) * np.cos(data["glong"])
data["y"] = data["dist"] * np.cos(data["glat"]) * np.sin(data["glong"])
data["z"] = data["dist"] * np.sin(data["glat"])


#================================================================================================


data_all = np.copy(data)


#================================================================================================


result, indexes = np.unique(ngc_to_messier['ngc'], return_index=True)
ngc_to_messier = ngc_to_messier[indexes]

result, indexes = np.unique(data['ngc'], return_index=True)
data = data[indexes]


data = rfn.join_by('ngc', data, ngc_to_messier, jointype='leftouter', usemask=False)

data = data[(data["type"] == "OC") | (data["type"] == "C+N") | (data["ngc"] == PLEIADES_MAGIC_ID) | (data["ngc"] == HYADES_MAGIC_ID) | (data["ngc"]==ORION_NEBULA_NGC)]

data["messier"][data["ngc"] == PLEIADES_MAGIC_ID] = "M  45 (pleiades)"
data["messier"][data["ngc"] == HYADES_MAGIC_ID] = "hyades"
data["messier"][data["messier"] == "M  44"] = "M  44 (beehive)"
data["messier"][data["messier"] == "M  42"] = "M  42 (orion nb)"

#================================================================================================


data = np.sort(data, order=['messier'])


#================================================================================================


SUN_TO_CENTER_DISTANCE = 27200
MILKY_WAY_RADIUS = 110000 / 2


def show_open_clusters(messier,data,box_size):
    ax = plt.subplot(111, projection='3d')
    
    ax.plot([0], [0], [0], 'o', color='orange', markersize=10, label='sun')

    circle = Circle((SUN_TO_CENTER_DISTANCE, 0, 0), SUN_TO_CENTER_DISTANCE, fill=False, color='blue')
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0)
    
    circle = Circle((SUN_TO_CENTER_DISTANCE, 0, 0), MILKY_WAY_RADIUS, fill=False, color='blue')
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0)

    if messier:
        counter = 0
        
        for r in data:
        
            marker = mlines.Line2D.filled_markers[counter % mlines.Line2D.filled_markers.__len__()]
        
            ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["messier"] + "   " + str(int(r["dist"])) + " ly", markersize=5, marker=marker)
            
            counter += 1

        try:
            ax.legend(numpoints=1, fontsize=10)  # call with fontsize fails on debian 7
        except:
            ax.legend(numpoints=1)
        
    else:
        ax.scatter(data["x"], data["y"], data["z"])
    
    ax.set_xlabel('ly')
    ax.set_ylabel('ly')
    ax.set_zlabel('ly')
    
    ax.auto_scale_xyz([-box_size, box_size], [-box_size, box_size], [-box_size, box_size])
    
    show_maximized_plot('open clusters')


#================================================================================================

show_open_clusters(False, data_all, 20000)

show_open_clusters(True, data, 6000)

