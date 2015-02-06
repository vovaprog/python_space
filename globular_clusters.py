import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d
import re

from spaceutils import show_maximized_plot, kiloparsec_to_lightyear


#=====================================================================================================


def convert_messier(ngc_string):
    match = re.search('M\\s+([0-9]+)', ngc_string)
    if match is not None:
        return int(match.group(1))
    else:
        return 0


data = np.loadtxt('data_release/globular_clusters.tsv', skiprows=49, delimiter='|', usecols=(1, 4, 5, 6, 7),
                  dtype=[('messier', 'int'), ('dist', 'float'), ('x', 'float'), ('y', 'float'), ('z', 'float')],
                  converters={1: convert_messier})


#=====================================================================================================


data = np.sort(data, order=['messier'])

data["x"] = kiloparsec_to_lightyear(data["x"])
data["y"] = kiloparsec_to_lightyear(data["y"])
data["z"] = kiloparsec_to_lightyear(data["z"])
data["dist"] = kiloparsec_to_lightyear(data["dist"])

SUN_TO_CENTER_DISTANCE = 27200
MILKY_WAY_RADIUS = 110000 / 2

center_x = SUN_TO_CENTER_DISTANCE * np.cos(0) * np.cos(0)
center_y = SUN_TO_CENTER_DISTANCE * np.cos(0) * np.sin(0)
center_z = SUN_TO_CENTER_DISTANCE * np.sin(0)


#=====================================================================================================


def show_globular_clusters(dt, messier):
    ax = plt.subplot(111, projection='3d')

    ax.plot((0,), (0,), (0,), 'o', color='orange', markersize=10, label='sun')

    circle = Circle((center_x, center_y, center_z), SUN_TO_CENTER_DISTANCE, fill=False, color='blue')
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0)

    circle = Circle((center_x, center_y, center_z), MILKY_WAY_RADIUS, fill=False, color='blue')
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0)

    circle = Circle((0, 0, 0), 2000, fill=False, color='blue')
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0)


    if messier:
        counter = 0

        for r in dt:
            marker = mlines.Line2D.filled_markers[counter % mlines.Line2D.filled_markers.__len__()]

            if r["messier"] > 0:
                ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label="M" + str(r["messier"]) + "   " + str(int(r["dist"])), markersize=5, marker=marker)

            counter += 1

        ax.legend()
    else:
        ax.scatter(dt['x'], dt['y'], dt['z'])


    ax.set_xlabel('ly')
    ax.set_ylabel('ly')
    ax.set_zlabel('ly')

    ax.auto_scale_xyz([-35000, 85000], [-60000, 60000], [-60000, 60000])

    show_maximized_plot('globular clusters')


#=====================================================================================================


show_globular_clusters(data, False)

show_globular_clusters(data, True)


