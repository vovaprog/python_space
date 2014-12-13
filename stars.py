import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as consts
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as mlines

import numpy.lib.recfunctions as rfn

from matplotlib.patches import Circle, Arc
from mpl_toolkits.mplot3d import Axes3D 
import mpl_toolkits.mplot3d.art3d as art3d

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


v53a=1
hipparcus=2
yale=3

use_catalog=v53a

if use_catalog == v53a:
#========================================= load 1 ============================================================

	print "cat"

#	data = np.loadtxt('data/v53a_5.tsv', skiprows=50, delimiter='|', usecols=(1, 2, 3, 4, 5, 6),
#                  dtype=[('hd', 'int'), ('glong', 'float'), ('glat', 'float'), ('dist_lyr', 'float'), ('vmag', 'float'),('name', 'S20')])

#HR|HD|Const|GLON|GLAT|Dist|Vmag|Name

	data = np.loadtxt('data/v53a_6.tsv', skiprows=60, delimiter='|', usecols=(1, 2, 3, 4, 5, 6,7 ),
                  dtype=[('hd', 'int'), ('con','S20'), ('glong', 'float'), ('glat', 'float'), ('dist_lyr', 'float'), ('vmag', 'float'),('name', 'S20')])


	data = np.sort(data, order=['vmag'])

	#data = data[0:29]

	dt=data



#getting most distant visible star
#https://ru.wikipedia.org/wiki/VV_%D0%A6%D0%B5%D1%84%D0%B5%D1%8F
#HD 208816
#http://simbad.u-strasbg.fr/simbad/sim-id?Ident=VV_Cep
#histogram - distance to visible stars
#	dt=dt[dt["vmag"]<6.5]

#	dt=dt[dt["dist_lyr"]<300]
#	plt.hist(dt['dist_lyr'],bins=150)
#	plt.show()

#	dt = np.sort(dt,order=['dist_lyr'])

#	print dt.size
#	print dt

	#print "max visible star dist lyr: " + dt.max("dist_lyr") #str(np.amax(dt["dist_lyr"]))

#	exit()



#========================================= load 1 ============================================================


#========================================= load 2 ============================================================
elif use_catalog== hipparcus:
	print "hipparcus"

	data = np.loadtxt('data/stars5.tsv', skiprows=50, delimiter='|', usecols=(0, 1, 2, 3, 4),
        	          dtype=[('glong', 'float'), ('glat', 'float'), ('vmag', 'float'), ('parallax', 'float'), ('hd', 'int')])

	names = np.loadtxt('data/names1.tsv', skiprows=47, delimiter='|', usecols=(0, 1), dtype=[('hd', 'int'), ('name', 'S20')])

	dt = rfn.join_by('hd',data,names,jointype='leftouter',defaults={'name':'123'})

	dt=np.sort(dt, order=['vmag'])

	print data[data["parallax"]==0]

	dt = dt[dt["parallax"]!=0]
	#dt = dt[0:99]

#	rfn.append_fields(dt, "dist", dtypes='S20')
	dt = add_field(dt, [('dist', float)])
	dt = add_field(dt, [('dist_lyr', float)])

	dt["dist"]=1/(dt["parallax"]/1000.0)
	dt["dist_lyr"]=parsec_to_lightyear(dt["dist"])




#	dt=dt[dt["vmag"]<6.5]

#	dt = np.sort(dt,order=['dist_lyr'])

#	print dt.size
#	print dt

	#print "max visible star dist lyr: " + dt.max("dist_lyr") #str(np.amax(dt["dist_lyr"]))

#	exit()

#========================================= load 2 ============================================================



#========================================= load yale ============================================================
elif use_catalog==yale:
	print "yale"

	data = np.loadtxt('data/yale_i50_2.tsv', skiprows=45, delimiter='|', usecols=(0, 1, 2, 3, 4),
        	          dtype=[('hd', 'int'), ('glong', 'float'), ('glat', 'float'), ('vmag', 'float'), ('parallax', 'float') ])
#				converters = {0:lambda s: s, 4: lambda s: float(s or 0)})

	names = np.loadtxt('data/names1.tsv', skiprows=47, delimiter='|', usecols=(0, 1), dtype=[('hd', 'int'), ('name', 'S20')])

	dt = rfn.join_by('hd',data,names,jointype='leftouter',defaults={'name':'123'})

	dt=np.sort(dt, order=['vmag'])

#	print data[data["parallax"]==0]

#	dt = dt[dt["parallax"]!=0] 
	#dt = dt[0:19]

	dt = add_field(dt, [('dist', float)])
	dt = add_field(dt, [('dist_lyr', float)])

	dt["parallax"]=np.abs(dt["parallax"])

	dt["dist"]=1/(dt["parallax"])
	dt["dist_lyr"]=parsec_to_lightyear(dt["dist"])
	
	print dt

#========================================= load yale ============================================================



#np.append(dt,)

#exit()

#Ursa major
#dt=dt[ dt["con"] == "UMa"]
#dt=dt[0:8]


#Orion
#dt=dt[ dt["con"] == "Ori"]
#dt=dt[0:7]

#Cas
#dt=dt[ dt["con"] == "Cas"]
#dt=dt[0:5]



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



polaris = dt[dt["hd"]==8890]

#print polaris

dt = dt[0:29]



center_x=1000 * np.cos(0) * np.cos(0)
center_y=1000 * np.cos(0) * np.sin(0)
center_z=1000 * np.sin(0)


p1_x=1000 * np.cos(0) * np.cos(np.radians(45))
p1_y=1000 * np.cos(0) * np.sin(np.radians(45))
p1_z=1000 * np.sin(0)

p2_x=1000 * np.cos(0) * np.cos(np.radians(315))
p2_y=1000 * np.cos(0) * np.sin(np.radians(315))
p2_z=1000 * np.sin(0)


p3_x=1000 * np.cos(0) * np.cos(np.radians(135))
p3_y=1000 * np.cos(0) * np.sin(np.radians(135))
p3_z=1000 * np.sin(0)

p4_x=1000 * np.cos(0) * np.cos(np.radians(225))
p4_y=1000 * np.cos(0) * np.sin(np.radians(225))
p4_z=1000 * np.sin(0)



#================================= Galaxies near Milky Way ======================================


#================================= Galaxies near Milky Way ======================================

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
        ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["name"]+" "+str(r["vmag"]), markersize=5, marker=marker)
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

