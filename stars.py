import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as consts
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as mlines

import numpy.lib.recfunctions as rfn

#Column	HR{1}	(I4)	[1/9110]+ "Bright Star" catalog <V/50> [NULL integer written as an empty string]	[ucd=]
#Column	HD{1}	(I6)	[1/225300] Henry Draper" catalog <III/135> [NULL integer written as an empty string]	[ucd=]
#Column	GLON{1}	(F6.2)	Galactic longitude	[ucd=]
#Column	GLAT{1}	(F6.2)	Galactic latitude	[ucd=]
#Column	Dist{1}	(I5)	Distance of star in light-years (5) [NULL integer written as an empty string]	[ucd=]
#Column	Vmag{1}	(F5.2)	[-1.46/5.03] Visual magnitude (magnitude visuelle)	[ucd=]
#Column	Name{2}	(a12)	Common name of the star / Nom usuel	[ucd=]


#data = np.loadtxt('data/stars4.tsv', skiprows=50, delimiter='|', usecols=(1, 2, 3, 4, 5, 6),
#                  dtype=[('hd', 'int'), ('glong', 'float'), ('glat', 'float'), ('distance', 'float'), ('vmag', 'float'),('name', 'S20')])


#data = np.loadtxt('data/stars5.tsv', skiprows=50, delimiter='|', usecols=(2, 4),#usecols=(0, 1, 2, 3, 4),
                  #dtype=[('glong', 'float'), ('glat', 'float'), ('vmag', 'float'), ('parallax', 'float'), ('hd', 'int')])
#                  dtype=[('vmag', 'float'), ('hd', 'int')])


#================================================================================================


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




data = np.loadtxt('data/stars5.tsv', skiprows=50, delimiter='|', usecols=(0, 1, 2, 3, 4),
                  dtype=[('glong', 'float'), ('glat', 'float'), ('vmag', 'float'), ('parallax', 'float'), ('hd', 'int')])





data = np.sort(data, order=['vmag'])

data = data[0:29]

for r in data:
    print r




names = np.loadtxt('data/names1.tsv', skiprows=47, delimiter='|', usecols=(0, 1), dtype=[('hd', 'int'), ('name', 'S20')])

dt = rfn.join_by('hd',data,names,jointype='leftouter',defaults={'name':'123'})

dt=np.sort(dt, order=['vmag'])

#print dt

#for r in dt:
#    print r["name"]
#    if r["name"] == '--' :
#        print "1"


#exit()

#rfn.append_fields(joined, "dist", dtypes='S20')
dt = add_field(dt, [('dist', float)])
dt = add_field(dt, [('dist_lyr', float)])
dt=add_field(dt,[('x', float)])
dt=add_field(dt,[('y', float)])
dt=add_field(dt,[('z', float)])

dt["dist"]=1/(dt["parallax"]/1000.0)
dt["dist_lyr"]=parsec_to_lightyear(dt["dist"])

print dt

#================================================================================================


dt["glong"] = np.radians(dt["glong"])
dt["glat"] = np.radians(dt["glat"])

dt["x"] = dt["dist"] * np.cos(dt["glat"]) * np.cos(dt["glong"])
dt["y"] = dt["dist"] * np.cos(dt["glat"]) * np.sin(dt["glong"])
dt["z"] = dt["dist"] * np.sin(dt["glat"])

#================================= Galaxies near Milky Way ======================================


#================================= Galaxies near Milky Way ======================================

def show_galaxies_near_milky_way():


    ax = plt.subplot(111, projection='3d')

    #radius = 50 000 lyr
    ax.plot((0,), (0,), (0,), 'o', color='cyan', markersize=15, label='milky way')


    ax.set_color_cycle(['r', 'g', 'b', 'y', 'c', 'm'])


    counter=0

    #for i in range(0, x.size):
    for r in dt:
        print str(r["x"])+" "+str(r["y"])+" "+str(r["z"])
        print r["name"]

        marker = mlines.Line2D.filled_markers[counter % 8]
        counter += 1

        ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["name"], markersize=5, marker=marker)

    #ax.legend(fontsize=11)

    ax.legend()

    ax.set_xlabel('Mpc')
    ax.set_ylabel('Mpc')
    ax.set_zlabel('Mpc')

    #ax.view_init(elev=10, azim=-25)

    #plt.figure(1).tight_layout(pad=0)

    show_maximized_plot('local galactic group')

#for r in dt:
#    print r["name"]

show_galaxies_near_milky_way()