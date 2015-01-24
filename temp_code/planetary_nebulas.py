import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Circle
import mpl_toolkits.mplot3d.art3d as art3d
import scipy.constants as consts
import re
import numpy.lib.recfunctions as rfn
import numpy.ma as ma
from matplotlib.patches import Arc

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




messier_to_ngc = np.loadtxt('data/star info/messier_to_ngc.tsv', skiprows=43, delimiter='|', usecols=(0, 1, 2),
                dtype=[('ngc', 'S20'), ('type', 'S20'), ('messier', 'S20')])


dt = np.loadtxt('data/star info/planetary nebula all.tsv', skiprows=43, delimiter='|', usecols=(0, 1, 2,3),
                dtype=[('glat', 'float'), ('glong', 'float'), ('ngc', 'S20'),('dist_pc','S20')])



for r in messier_to_ngc:
	r["ngc"]=int(r["ngc"].strip().replace("I","100"))
	r["type"]=r["type"].strip()	

for r in dt:
	r["dist_pc"]=r["dist_pc"].strip()
	if r["dist_pc"] != "":
		r["dist_pc"]=float(r["dist_pc"])
	else:
		r["dist_pc"]=0.0

	match = re.search('NGC\\s+([0-9]+)', r["ngc"])

	if match != None:
		r["ngc"]=int(match.group(1))
	else:
		match = re.search('IC\\s+([0-9]+)', r["ngc"])
		if match != None:
			r["ngc"]=int("100" + match.group(1))		


result, indexes = np.unique(messier_to_ngc['ngc'], return_index=True)
messier_to_ngc = messier_to_ngc[indexes]

result, indexes = np.unique(dt['ngc'], return_index=True)
dt = dt[indexes]



dt = rfn.join_by('ngc', dt, messier_to_ngc, jointype='leftouter')

dt = dt[dt["type"]=="Pl"]



fill_with_zeros = np.zeros(dt.size)
dt = rfn.append_fields(dt, ['x', 'y', 'z','dist'],
                       [fill_with_zeros, fill_with_zeros, fill_with_zeros, fill_with_zeros])


dt["dist"]=dt["dist_pc"]
dt["dist"]=parsec_to_lightyear(dt["dist"])


dt = np.sort(dt, order=['messier'])


dt["glong"] = np.radians(dt["glong"])
dt["glat"] = np.radians(dt["glat"])

dt["x"] = dt["dist"] * np.cos(dt["glat"]) * np.cos(dt["glong"])
dt["y"] = dt["dist"] * np.cos(dt["glat"]) * np.sin(dt["glong"])
dt["z"] = dt["dist"] * np.sin(dt["glat"])





SUN_TO_CENTER_DISTANCE = 27200
MILKY_WAY_RADIUS = 110000 / 2

center_x = 3000 * np.cos(0) * np.cos(0)
center_y = 3000 * np.cos(0) * np.sin(0)
center_z = 3000 * np.sin(0)


def show_planetary_nebulas(dt):
    ax = plt.subplot(111, projection='3d')

    ax.plot((0,), (0,), (0,), 'o', color='orange', markersize=10, label='sun')

    ax.plot([0, center_x], [0, center_y], [0, center_z], label='center galaxy')

    arc = Arc((SUN_TO_CENTER_DISTANCE, 0, 0), 2*SUN_TO_CENTER_DISTANCE, 2*SUN_TO_CENTER_DISTANCE, theta1=174, theta2=186)
    ax.add_patch(arc)
    art3d.pathpatch_2d_to_3d(arc, z=0)


    counter = 0

    for r in dt:

        marker = mlines.Line2D.filled_markers[counter % 8]

        ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["messier"] + " " + str(int(r["dist"])), markersize=5, marker=marker)

        counter += 1

    ax.legend()

    ax.set_xlabel('ly')
    ax.set_ylabel('ly')
    ax.set_zlabel('ly')

    ax.auto_scale_xyz([-3000, 3000], [-3000, 3000], [-3000, 3000])

    plt.figure(1).tight_layout(pad=0)

    show_maximized_plot('planetary nebulas')


show_planetary_nebulas(dt)


