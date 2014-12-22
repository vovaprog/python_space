import numpy as np
import numpy.lib.recfunctions as rfn
import numpy.ma as ma

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
#from matplotlib.patches import Arc
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




dt = np.loadtxt('data/globular_cluster_data1.tsv', skiprows=49, delimiter='|', usecols=(0, 1, 2, 3, 4,5,6,7,8),
                dtype=[('id', 'S20'), ('name', 'S20'), ('glong', 'float'), ('glat', 'float'), ('dist', 'float'),
                       ('x1', 'float'), ('y1', 'float'), ('z1', 'float'), ('vmag', 'float')])

dt = np.sort(dt, order=['name'])

#print dt

#exit()

"""
result, indexes = np.unique(dt['hd'], return_index=True)
dt = dt[indexes]

result, indexes = np.unique(names['hd'], return_index=True)
names = names[indexes]

result, indexes = np.unique(constellations['hd'], return_index=True)
constellations = constellations[indexes]

dt = rfn.join_by('hd', dt, names, jointype='leftouter')
dt = rfn.join_by('hd', dt, constellations, jointype='leftouter')

dt["name"] = ma.filled(dt["name"], '')
dt["con"] = ma.filled(dt["con"], '')

fill_with_zeros = np.zeros(dt.size)

dt = rfn.append_fields(dt, ['x', 'y', 'z', 'dist'],
                       [fill_with_zeros, fill_with_zeros, fill_with_zeros, fill_with_zeros])

dt = dt[dt["parallax"] != 0]

dt["parallax"] = np.absolute(dt["parallax"])

dt["dist"] = 1 / (dt["parallax"] / 1000.0)
dt["dist"] = parsec_to_lightyear(dt["dist"])
"""

fill_with_zeros = np.zeros(dt.size)


dt = rfn.append_fields(dt, ['x', 'y', 'z'],
                       [fill_with_zeros, fill_with_zeros, fill_with_zeros])


dt["dist"]=kiloparsec_to_lightyear(dt["dist"])

dt["glong"] = np.radians(dt["glong"])
dt["glat"] = np.radians(dt["glat"])

dt["x"] = dt["dist"] * np.cos(dt["glat"]) * np.cos(dt["glong"])
dt["y"] = dt["dist"] * np.cos(dt["glat"]) * np.sin(dt["glong"])
dt["z"] = dt["dist"] * np.sin(dt["glat"])

#polaris = dt[dt["hd"] == 8890]

#dt = np.sort(dt, order=['vmag'])


SUN_TO_CENTER_DISTANCE = 27200
MILKY_WAY_RADIUS = 110000 / 2

center_x = SUN_TO_CENTER_DISTANCE * np.cos(0) * np.cos(0)
center_y = SUN_TO_CENTER_DISTANCE * np.cos(0) * np.sin(0)
center_z = SUN_TO_CENTER_DISTANCE * np.sin(0)


def show_stars(dt): #, range_x, range_y, range_z, count_show_with_legend, plot_name):
    ax = plt.subplot(111, projection='3d')

    ax.plot((0,), (0,), (0,), 'o', color='orange', markersize=10, label='sun')


    # center galaxy
    #ax.plot([0, center_x], [0, center_y], [0, center_z], label='center galaxy')

    #arc = Arc((27200, 0, 0), 54400, 54400, theta1=176, theta2=184)
    #ax.add_patch(arc)
    #art3d.pathpatch_2d_to_3d(arc, z=0)


    circle = Circle((center_x, center_y,center_z), SUN_TO_CENTER_DISTANCE,fill=False,color='blue')
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0)


    circle = Circle((center_x, center_y,center_z), MILKY_WAY_RADIUS,fill=False,color='blue')
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0)

    circle = Circle((0, 0, 0), 2000,fill=False,color='blue')
    ax.add_patch(circle)
    art3d.pathpatch_2d_to_3d(circle, z=0)





    #polaris
#    ax.plot([0, polaris["x"][0]], [0, polaris["y"][0]], [0, polaris["z"][0]], label='polaris')

    #ax.set_color_cycle(['r', 'g', 'b', 'y', 'c', 'm'])

    counter = 0

    for r in dt:

        marker = mlines.Line2D.filled_markers[counter % 8]

        #if counter < count_show_with_legend:
#            ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["name"] + " " + str(r["vmag"]), markersize=5,
#                    marker=marker)
#        else:
        if r["name"].startswith('M '):
            ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["name"] + " " + str(int(r["dist"])), markersize=5,
                    marker=marker)
        else:
            ax.plot([r["x"]], [r["y"]], [r["z"]], '.', markersize=1)

        counter += 1

    ax.legend()

    ax.set_xlabel('ly')
    ax.set_ylabel('ly')
    ax.set_zlabel('ly')

    ax.auto_scale_xyz([-25000,75000], [-50000,50000], [-50000,50000])

    plt.figure(1).tight_layout(pad=0)

    show_maximized_plot('brightest stars')


show_stars(dt)

exit()


dt_stars = dt[0:29]
show_stars(dt_stars, [-1000, 1000], [-1000, 1000], [-1000, 1000], 1000, "brightest stars")


dt_ursa = dt[dt["con"] == "UMa"]
show_stars(dt_ursa, [-200, 200], [-200, 200], [-200, 200], 6, "ursa major")


dt_orion = dt[dt["con"] == "Ori"]
show_stars(dt_orion, [-600, 600], [-600, 600], [-600, 600], 7, "orion")


