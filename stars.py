import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as consts
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as mlines

import numpy.lib.recfunctions as rfn
import numpy.ma as ma

from matplotlib.patches import Circle, Arc
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.art3d as art3d


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


# ================================================================================================


def parsec_to_lightyear(dist):
    LIGHT_YEARS_IN_PARSEC = 3.2615638
    return dist * LIGHT_YEARS_IN_PARSEC


dt = np.loadtxt('data/stars5.tsv', skiprows=50, delimiter='|', usecols=(0, 1, 2, 3, 4),
                dtype=[('glong', 'float'), ('glat', 'float'), ('vmag', 'float'), ('parallax', 'float'), ('hd', 'int')])

#names = np.loadtxt('data/names1.tsv', skiprows=47, delimiter='|', usecols=(0, 1),
#                   dtype=[('hd', 'int'), ('name', 'S20')])

names = np.loadtxt('data/cst3.tsv', skiprows=43, delimiter='|', usecols=(1, 2, 3),
                   dtype=[('hd', 'int'), ('con','S20'), ('name', 'S20')])


#constellations = np.loadtxt('data/constellations.tsv', skiprows=38, delimiter='|', usecols=(0, 1),
#                   dtype=[('hd', 'int'), ('con', 'S20')])

sirius = dt[dt["hd"] == 48915]
print sirius

#result = rfn.find_duplicates(names,key='hd')

result,indexes=np.unique(names['hd'],return_index=True)

names=names[indexes]

print indexes

dt = rfn.join_by('hd', dt, names, jointype='leftouter')


sirius = dt[dt["hd"] == 48915]
print sirius

#exit()


#polaris = dt[dt["hd"] == 8890]

#print polaris

#dt = rfn.join_by('hd', dt, constellations, jointype='leftouter')

#dt["name"] = ma.filled(dt["name"], '')
#dt["con"] = ma.filled(dt["con"], '')


#polaris = dt[dt["hd"] == 8890]

#print polaris

#exit()



fill_with_zeros = np.zeros(dt.size)

dt = rfn.append_fields(dt, ['x', 'y', 'z', 'dist'],
                       [fill_with_zeros, fill_with_zeros, fill_with_zeros, fill_with_zeros])

sirius = dt[dt["hd"] == 48915]
print sirius



dt = dt[dt["parallax"] != 0]

sirius = dt[dt["hd"] == 48915]
print sirius



dt["dist"] = 1 / (dt["parallax"] / 1000.0)
dt["dist"] = parsec_to_lightyear(dt["dist"])


dt["glong"] = np.radians(dt["glong"])
dt["glat"] = np.radians(dt["glat"])


dt["x"] = dt["dist"] * np.cos(dt["glat"]) * np.cos(dt["glong"])
dt["y"] = dt["dist"] * np.cos(dt["glat"]) * np.sin(dt["glong"])
dt["z"] = dt["dist"] * np.sin(dt["glat"])


polaris = dt[dt["hd"] == 8890]

#print polaris

dt = np.sort(dt, order=['vmag'])


dt = dt[0:29]


sirius = dt[dt["hd"] == 48915]
print sirius



center_x = 1000 * np.cos(0) * np.cos(0)
center_y = 1000 * np.cos(0) * np.sin(0)
center_z = 1000 * np.sin(0)






def show_brightest_stars(dt):
    ax = plt.subplot(111, projection='3d')

    ax.plot((0,), (0,), (0,), 'o', color='orange', markersize=10, label='sun')


    arc = Arc((27200, 0, 0), 54400, 54400, theta1=176, theta2=184)
    ax.add_patch(arc)
    art3d.pathpatch_2d_to_3d(arc, z=0)


    #polaris
    ax.plot([0, polaris["x"][0]], [0, polaris["y"][0]], [0, polaris["z"][0]], label='polaris')


    #center galaxy
    ax.plot([0, center_x], [0, center_y], [0, center_z], label='center galaxy')

    ax.set_color_cycle(['r', 'g', 'b', 'y', 'c', 'm'])

    counter = 0

    for r in dt:

        marker = mlines.Line2D.filled_markers[counter % 8]
        counter += 1

        ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["name"] + " " + str(r["vmag"]), markersize=5, marker=marker)


    ax.legend()


    ax.set_xlabel('ly')
    ax.set_ylabel('ly')
    ax.set_zlabel('ly')


    ax.auto_scale_xyz([-1000, 1000], [-1000, 1000], [-1000, 1000])

    plt.figure(1).tight_layout(pad=0)

    show_maximized_plot('brightest stars')

print dt

show_brightest_stars(dt)



#Ursa major
#dt_ursa=dt[ dt["con"] == "UMa"]
#dt_ursa=dt_ursa[0:8]

#print dt_ursa

#show_brightest_stars(dt_ursa)




#Orion
#dt=dt[ dt["con"] == "Ori"]
#dt=dt[0:7]

#Cas
#dt=dt[ dt["con"] == "Cas"]
#dt=dt[0:5]




#======== for orion ========================
    #    ax.plot((0,), (-1400,), (0,), 'o', color='orange', markersize=15, label='300')
    #    ax.plot((0,), (0,), (-1400,), 'o', color='orange', markersize=15, label='300')
    #======== for orion ========================

    #======== for cassiopea ========================
    #    ax.plot((0,), (0,), (300,), 'o', color='orange', markersize=15, label='300')
    #    ax.plot((0,), (0,), (-300,), 'o', color='orange', markersize=15, label='300')
    #    ax.plot((-600,), (0,), (0,), 'o', color='orange', markersize=15, label='300')
    #======== for cassiopea ========================


    #======= for ursa =======================
    #    ax.plot((-140,), (0,), (0,), 'o', color='orange', markersize=15, label='300')
    #    ax.plot((0,), (140,), (0,), 'o', color='orange', markersize=15, label='300')
    #======= for ursa =======================


    #    ax.plot((0,), (0,), (-350,), 'o', color='orange', markersize=15, label='300')

    #    ax.plot((center_x,), (center_y,), (center_z,), 'o', color='cyan', markersize=15, label='center')

    #    ax.plot((p1_x,), (p1_y,), (p1_z,), 'o', color='red', markersize=15, label='p1')
    #    ax.plot((p2_x,), (p2_y,), (p2_z,), 'o', color='orange', markersize=15, label='p2')
    #    ax.plot((p3_x,), (p3_y,), (p3_z,), 'o', color='magenta', markersize=15, label='p3')
    #    ax.plot((p4_x,), (p4_y,), (p4_z,), 'o', color='green', markersize=15, label='p3')




    #circle = Circle((0, 0), 100,fill=False,color='red')
    #ax.add_patch(circle)
    #art3d.pathpatch_2d_to_3d(circle, z=0)