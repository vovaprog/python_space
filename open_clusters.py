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
        if match != None:
            return int("100" + match.group(1))
        else:
            return 0

def convert_distance(s):
    s = s.strip()
    return int(s) if s != '' else 0

dt = np.loadtxt('data/star info/open clusters 2.tsv', skiprows=42, delimiter='|', usecols=(0, 1, 2, 3),
                dtype=[('glong', 'float'), ('glat', 'float'), ('ngc', 'int'), ('dist', 'int')],
                converters={2: convert_ngc, 3: convert_distance})


def convert_ngc2(ngc_string):
    ngc_string = ngc_string.strip().replace("I", "100")
    return int(ngc_string)

messier_to_ngc = np.loadtxt('data/star info/messier_to_ngc.tsv', skiprows=43, delimiter='|', usecols=(0, 1, 2),
                            dtype = [('ngc', 'int'), ('type', 'S20'), ('messier', 'S20')],
                            converters = {0: convert_ngc2, 1: lambda s: str(s).strip()})


#================================================================================================


result, indexes = np.unique(messier_to_ngc['ngc'], return_index=True)
messier_to_ngc = messier_to_ngc[indexes]

result, indexes = np.unique(dt['ngc'], return_index=True)
dt = dt[indexes]


dt = rfn.join_by('ngc', dt, messier_to_ngc, jointype='leftouter', usemask=False)

dt = dt[(dt["type"] == "OC") | (dt["type"] == "C+N")]


fill_with_zeros = np.zeros(dt.size)

dt = rfn.append_fields(dt, ['x', 'y', 'z'], [fill_with_zeros, fill_with_zeros, fill_with_zeros], usemask=False)


#================================================================================================

dt["dist"] = parsec_to_lightyear(dt["dist"])

dt["glong"] = np.radians(dt["glong"])
dt["glat"] = np.radians(dt["glat"])

dt["x"] = dt["dist"] * np.cos(dt["glat"]) * np.cos(dt["glong"])
dt["y"] = dt["dist"] * np.cos(dt["glat"]) * np.sin(dt["glong"])
dt["z"] = dt["dist"] * np.sin(dt["glat"])

dt = np.sort(dt, order=['messier'])


#================================================================================================


SUN_TO_CENTER_DISTANCE = 27200


center_x = 5000 * np.cos(0) * np.cos(0)
center_y = 5000 * np.cos(0) * np.sin(0)
center_z = 5000 * np.sin(0)


#================================================================================================

ax = plt.subplot(111, projection='3d')

ax.plot([0], [0], [0], 'o', color='orange', markersize=10, label='sun')

ax.plot([0, center_x], [0, center_y], [0, center_z], label='galaxy center')

arc = Arc((SUN_TO_CENTER_DISTANCE, 0, 0), 2 * SUN_TO_CENTER_DISTANCE, 2 * SUN_TO_CENTER_DISTANCE, theta1=170, theta2=190)
ax.add_patch(arc)
art3d.pathpatch_2d_to_3d(arc, z=0)


counter = 0

for r in dt:

    marker = mlines.Line2D.filled_markers[counter % mlines.Line2D.filled_markers.__len__()]

    ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["messier"] + "   " + str(int(r["dist"])) + " ly", markersize=5, marker=marker)

    counter += 1

ax.legend()

ax.set_xlabel('ly')
ax.set_ylabel('ly')
ax.set_zlabel('ly')

ax.auto_scale_xyz([-6000, 6000], [-6000, 6000], [-6000, 6000])

show_maximized_plot('open clusters')





