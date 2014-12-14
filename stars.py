import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as consts
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as mlines

import numpy.lib.recfunctions as rfn

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

#================================================================================================


def add_field(a, descr):
    """Return a new array that is like "a", but has additional fields.

    Arguments:
      a     -- a structured numpy array
      descr -- a numpy type description of the new fields

    The contents of "a" are copied over to the appropriate fields in
    the new array, whereas the new fields are uninitialized.  The
    arguments are not modified.

    >>> sa = numpy.array([(1, 'Foo'), (2, 'Bar')], \
                         dtype=[('id', int), ('name', 'S3')])
    >>> sa.dtype.descr == numpy.dtype([('id', int), ('name', 'S3')])
    True
    >>> sb = add_field(sa, [('score', float)])
    >>> sb.dtype.descr == numpy.dtype([('id', int), ('name', 'S3'), \
                                       ('score', float)])
    True
    >>> numpy.all(sa['id'] == sb['id'])
    True
    >>> numpy.all(sa['name'] == sb['name'])
    True
    """
    if a.dtype.fields is None:
        raise ValueError, "`A' must be a structured numpy array"
    b = np.empty(a.shape, dtype=a.dtype.descr + descr)
    for name in a.dtype.names:
        b[name] = a[name]
    return b

def parsec_to_lightyear(dist):
    LIGHT_YEARS_IN_PARSEC = 3.2615638
    return dist * LIGHT_YEARS_IN_PARSEC




dt = np.loadtxt('data/stars5.tsv', skiprows=50, delimiter='|', usecols=(0, 1, 2, 3, 4),
                  dtype=[('glong', 'float'), ('glat', 'float'), ('vmag', 'float'), ('parallax', 'float'), ('hd', 'int')])

names = np.loadtxt('data/names1.tsv', skiprows=47, delimiter='|', usecols=(0, 1), dtype=[('hd', 'int'), ('name', 'S20')])

dt = rfn.join_by('hd',dt,names,jointype='leftouter',defaults={'name':'123'})


dt = dt[dt["parallax"] != 0]


#	rfn.append_fields(dt, "dist", dtypes='S20')
dt = add_field(dt, [('dist', float)])
dt = add_field(dt, [('dist_lyr', float)])

dt["dist"] = 1/(dt["parallax"]/1000.0)
dt["dist_lyr"] = parsec_to_lightyear(dt["dist"])




#Ursa major
#dt=dt[ dt["con"] == "UMa"]
#dt=dt[0:8]


#Orion
#dt=dt[ dt["con"] == "Ori"]
#dt=dt[0:7]

#Cas
#dt=dt[ dt["con"] == "Cas"]
#dt=dt[0:5]





#rfn.append_fields(dt,'x',dtypes='float')

dt=add_field(dt,[('x', float)])
dt=add_field(dt,[('y', float)])
dt=add_field(dt,[('z', float)])




#print dt

#================================================================================================


dt["glong"] = np.radians(dt["glong"])
dt["glat"] = np.radians(dt["glat"])

dt["x"] = dt["dist_lyr"] * np.cos(dt["glat"]) * np.cos(dt["glong"])
dt["y"] = dt["dist_lyr"] * np.cos(dt["glat"]) * np.sin(dt["glong"])
dt["z"] = dt["dist_lyr"] * np.sin(dt["glat"])



polaris = dt[dt["hd"] == 8890]



dt=np.sort(dt, order=['vmag'])

dt = dt[0:29]

for r in dt:
    print r["name"]+" "+str(r["dist_lyr"])


center_x=1000 * np.cos(0) * np.cos(0)
center_y=1000 * np.cos(0) * np.sin(0)
center_z=1000 * np.sin(0)




def show_galaxies_near_milky_way():



    ax = plt.subplot(111, projection='3d')


    #radius = 50 000 lyr
    ax.plot((0,), (0,), (0,), 'o', color='orange', markersize=15, label='sun')

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

    arc = Arc((27200,0,0),54400,54400,theta1 = 176,theta2=184)
    ax.add_patch(arc)
    art3d.pathpatch_2d_to_3d(arc, z=0)


    #polaris
    ax.plot([0,polaris["x"][0]], [0,polaris["y"][0]], [0, polaris["z"][0]],label='polaris')

    #center galaxy
    ax.plot([0, center_x], [0, center_y], [0, center_z],label='center galaxy')


    ax.set_color_cycle(['r', 'g', 'b', 'y', 'c', 'm'])

    counter=0

    #for i in range(0, x.size):
    for r in dt:
        #print str(r["x"])+" "+str(r["y"])+" "+str(r["z"])+" "+r["name"]

       	marker = mlines.Line2D.filled_markers[counter % 8]
        counter += 1

#	if counter<29:
        ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["name"]+" "+str(r["vmag"]) , markersize=5, marker=marker)
#	else:
#	        ax.plot([r["x"]], [r["y"]], [r["z"]], '.', markersize=3)
#		ax.plot([r["glat"]], [r["glong"]], [r["dist"]], 'o', label=r["name"], markersize=5, marker=marker)


    #ax.legend(fontsize=11)

    ax.legend()

#    ax.set_xlabel('Mpc')
#    ax.set_ylabel('Mpc')
#    ax.set_zlabel('Mpc')

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')


    #ax.view_init(elev=10, azim=-25)

    #plt.figure(1).tight_layout(pad=0)


    #plt.axis('equal')

    #ax.set_xlim3d(0, 2000)
    #ax.set_ylim3d(0,2000)
    #ax.set_zlim3d(0,2000)

    ax.auto_scale_xyz([-1000, 1000], [-1000, 1000], [-1000, 1000])

    plt.figure(1).tight_layout(pad=0)
    show_maximized_plot('local galactic group')
    #plt.show()

#for r in dt:
#    print r["name"]

show_galaxies_near_milky_way()

