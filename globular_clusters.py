import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d
import scipy.constants as consts


# ================================================================================================

def set_graph_title(s):
    plt.title(s)
    fig = plt.gcf()
    fig.canvas.set_window_title(s)


def maximize_plot_window():
    fig_manager = plt.get_current_fig_manager()
    backend_name = plt.get_backend().lower()
    if backend_name.find('qt') >= 0:
        fig_manager.window.showMaximized()
    elif backend_name.find('tk') >= 0:
        maxsz = fig_manager.window.maxsize()
        fig_manager.resize(maxsz[0] - 100, maxsz[1] - 100)


def show_maximized_plot(Title):
    set_graph_title(Title)
    maximize_plot_window()
    plt.show()
    plt.close()


def kiloparsec_to_lightyear(dist):
    LIGHT_YEARS_IN_PARSEC = 3.2615638
    return dist * consts.kilo * LIGHT_YEARS_IN_PARSEC

# ================================================================================================




dt = np.loadtxt('data/globular_cluster_data1.tsv', skiprows=49, delimiter='|', usecols=(0, 1, 2, 3, 4, 5, 6, 7, 8),
                dtype=[('id', 'S20'), ('name', 'S20'), ('glong', 'float'), ('glat', 'float'), ('dist', 'float'),
                       ('x', 'float'), ('y', 'float'), ('z', 'float'), ('vmag', 'float')])

dt = np.sort(dt, order=['name'])

dt["x"] = kiloparsec_to_lightyear(dt["x"])
dt["y"] = kiloparsec_to_lightyear(dt["y"])
dt["z"] = kiloparsec_to_lightyear(dt["z"])
dt["dist"] = kiloparsec_to_lightyear(dt["dist"])

SUN_TO_CENTER_DISTANCE = 27200
MILKY_WAY_RADIUS = 110000 / 2

center_x = SUN_TO_CENTER_DISTANCE * np.cos(0) * np.cos(0)
center_y = SUN_TO_CENTER_DISTANCE * np.cos(0) * np.sin(0)
center_z = SUN_TO_CENTER_DISTANCE * np.sin(0)


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

            if r["name"].startswith('M '):
                ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["name"] + " " + str(int(r["dist"])), markersize=5, marker=marker)

            counter += 1

        ax.legend()
    else:
        ax.scatter(dt['x'], dt['y'], dt['z'])


    ax.set_xlabel('ly')
    ax.set_ylabel('ly')
    ax.set_zlabel('ly')

    ax.auto_scale_xyz([-35000, 85000], [-60000, 60000], [-60000, 60000])

    plt.figure(1).tight_layout(pad=0)

    show_maximized_plot('globular clusters')


show_globular_clusters(dt, False)

show_globular_clusters(dt, True)


