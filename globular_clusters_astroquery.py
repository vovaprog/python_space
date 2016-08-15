import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d
from astroquery.vizier import Vizier

from spaceutils import show_maximized_plot, kiloparsec_to_lightyear


# =====================================================================================================


catalog_list = Vizier.find_catalogs('VII/202')
Vizier.ROW_LIMIT = 1000000
catalogs = Vizier.get_catalogs(catalog_list.keys())
data = catalogs[0]


# =====================================================================================================

data.sort('Name')

data["X"] = kiloparsec_to_lightyear(data["X"])
data["Y"] = kiloparsec_to_lightyear(data["Y"])
data["Z"] = kiloparsec_to_lightyear(data["Z"])
data["Rsun"] = kiloparsec_to_lightyear(data["Rsun"])

SUN_TO_CENTER_DISTANCE = 27200
MILKY_WAY_RADIUS = 110000 / 2


# =====================================================================================================


def show_globular_clusters(dt, messier):
    ax = plt.subplot(111, projection='3d')

    ax.plot((0,), (0,), (0,), 'o', color='orange', markersize=7, label='sun')

    circle = Circle((SUN_TO_CENTER_DISTANCE, 0, 0), SUN_TO_CENTER_DISTANCE, fill=False, color='blue')
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0)

    circle = Circle((SUN_TO_CENTER_DISTANCE, 0, 0), MILKY_WAY_RADIUS, fill=False, color='blue')
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0)

    circle = Circle((0, 0, 0), 1000, fill=False, color='red')
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0)

    if messier:
        counter = 0

        for r in dt:
            marker = mlines.Line2D.filled_markers[counter % mlines.Line2D.filled_markers.__len__()]

            if str(r["Name"]).startswith('M'):
                ax.plot([r["X"]], [r["Y"]], [r["Z"]], 'o', label=str(r["Name"]) + "   " + str(r["Rsun"]), markersize=5, marker=marker)

            counter += 1

        ax.legend(numpoints=1, fontsize=10)

    else:
        ax.scatter(dt['X'], dt['Y'], dt['Z'])

    ax.set_xlabel('ly')
    ax.set_ylabel('ly')
    ax.set_zlabel('ly')

    ax.auto_scale_xyz([-35000, 85000], [-60000, 60000], [-60000, 60000])

    show_maximized_plot('globular clusters')


# =====================================================================================================


show_globular_clusters(data, False)

show_globular_clusters(data, True)


