import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import mpl_toolkits.mplot3d.art3d as art3d
import re
import numpy.lib.recfunctions as rfn
from matplotlib.patches import Arc

from spaceutils import parsec_to_lightyear, show_maximized_plot


#================================================================================================


def convert_ngc(ngc_string):
    match = re.search('NGC\\s+([0-9]+)', ngc_string)

    if match is not None:
        return int(match.group(1))
    else:
        match = re.search('IC\\s+([0-9]+)', ngc_string)
        if match is not None:
            return int("100" + match.group(1))
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


result, indexes = np.unique(ngc_to_messier['ngc'], return_index=True)
ngc_to_messier = ngc_to_messier[indexes]

result, indexes = np.unique(data['ngc'], return_index=True)
data = data[indexes]


data = rfn.join_by('ngc', data, ngc_to_messier, jointype='leftouter', usemask=False)

data = data[(data["type"] == "OC") | (data["type"] == "C+N")]


fill_with_zeros = np.zeros(data.size)

data = rfn.append_fields(data, ['x', 'y', 'z'], [fill_with_zeros, fill_with_zeros, fill_with_zeros], usemask=False)


#================================================================================================

data["dist"] = parsec_to_lightyear(data["dist"])

data["glong"] = np.radians(data["glong"])
data["glat"] = np.radians(data["glat"])

data["x"] = data["dist"] * np.cos(data["glat"]) * np.cos(data["glong"])
data["y"] = data["dist"] * np.cos(data["glat"]) * np.sin(data["glong"])
data["z"] = data["dist"] * np.sin(data["glat"])

data = np.sort(data, order=['messier'])


#================================================================================================


SUN_TO_CENTER_DISTANCE = 27200


ax = plt.subplot(111, projection='3d')

ax.plot([0], [0], [0], 'o', color='orange', markersize=10, label='sun')

ax.plot([0, 5000], [0, 0], [0, 0], label='to galaxy center')

arc = Arc((SUN_TO_CENTER_DISTANCE, 0, 0), 2 * SUN_TO_CENTER_DISTANCE, 2 * SUN_TO_CENTER_DISTANCE, theta1=170, theta2=190)
ax.add_patch(arc)
art3d.pathpatch_2d_to_3d(arc, z=0)


counter = 0

for r in data:

    marker = mlines.Line2D.filled_markers[counter % mlines.Line2D.filled_markers.__len__()]

    ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["messier"] + "   " + str(int(r["dist"])) + " ly", markersize=5, marker=marker)

    counter += 1

ax.legend()

ax.set_xlabel('ly')
ax.set_ylabel('ly')
ax.set_zlabel('ly')

ax.auto_scale_xyz([-6000, 6000], [-6000, 6000], [-6000, 6000])

show_maximized_plot('open clusters')





