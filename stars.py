import numpy as np
import numpy.lib.recfunctions as rfn
import numpy.ma as ma

import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Arc
import mpl_toolkits.mplot3d.art3d as art3d


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


def parsec_to_lightyear(dist):
    LIGHT_YEARS_IN_PARSEC = 3.2615638
    return dist * LIGHT_YEARS_IN_PARSEC

# ================================================================================================




dt = np.loadtxt('data/stars_data.tsv', skiprows=46, delimiter='|', usecols=(0, 1, 2, 3, 4),
                dtype=[('glong', 'float'), ('glat', 'float'), ('vmag', 'float'), ('parallax', 'float'), ('hd', 'int')])

names = np.loadtxt('data/stars_names.tsv', skiprows=35, delimiter='|', usecols=(0, 1),
                   dtype=[('hd', 'int'), ('name', 'S20')])

constellations = np.loadtxt('data/stars_cons.tsv', skiprows=37, delimiter='|', usecols=(0, 1),
                            dtype=[('hd', 'int'), ('con', 'S20')])

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

dt["glong"] = np.radians(dt["glong"])
dt["glat"] = np.radians(dt["glat"])

dt["x"] = dt["dist"] * np.cos(dt["glat"]) * np.cos(dt["glong"])
dt["y"] = dt["dist"] * np.cos(dt["glat"]) * np.sin(dt["glong"])
dt["z"] = dt["dist"] * np.sin(dt["glat"])

polaris = dt[dt["hd"] == 8890]

dt = np.sort(dt, order=['vmag'])

center_x = 1000 * np.cos(0) * np.cos(0)
center_y = 1000 * np.cos(0) * np.sin(0)
center_z = 1000 * np.sin(0)


def show_stars(dt, range_x, range_y, range_z, count_show_with_legend, plot_name):
    ax = plt.subplot(111, projection='3d')

    ax.plot((0,), (0,), (0,), 'o', color='orange', markersize=10, label='sun')


    # center galaxy
    ax.plot([0, center_x], [0, center_y], [0, center_z], label='center galaxy')

    arc = Arc((27200, 0, 0), 54400, 54400, theta1=176, theta2=184)
    ax.add_patch(arc)
    art3d.pathpatch_2d_to_3d(arc, z=0)


    #polaris
    ax.plot([0, polaris["x"][0]], [0, polaris["y"][0]], [0, polaris["z"][0]], label='polaris')

    ax.set_color_cycle(['r', 'g', 'b', 'y', 'c', 'm'])

    counter = 0

    for r in dt:

        marker = mlines.Line2D.filled_markers[counter % 8]

        if counter < count_show_with_legend:
            ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["name"] + " " + str(r["vmag"]), markersize=5,
                    marker=marker)
        else:
            ax.plot([r["x"]], [r["y"]], [r["z"]], '.', markersize=2)

        counter += 1

    ax.legend()

    ax.set_xlabel('ly')
    ax.set_ylabel('ly')
    ax.set_zlabel('ly')

    ax.auto_scale_xyz(range_x, range_y, range_z)

    plt.figure(1).tight_layout(pad=0)

    show_maximized_plot(plot_name)


dt_stars = dt[0:29]
show_stars(dt_stars, [-1000, 1000], [-1000, 1000], [-1000, 1000], 1000, "brightest stars")


dt_ursa = dt[dt["con"] == "UMa"]
show_stars(dt_ursa, [-200, 200], [-200, 200], [-200, 200], 6, "ursa major")


dt_orion = dt[dt["con"] == "Ori"]
show_stars(dt_orion, [-600, 600], [-600, 600], [-600, 600], 7, "orion")


dt_filtered = dt[dt['dist'] < 8000]
plt.hist(dt_filtered['dist'], bins=150)
plt.xlabel('distance light years')
plt.ylabel('number of stars')
show_maximized_plot("star histogram")

