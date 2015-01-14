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

from numpy.ma.core import MaskedConstant


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


# ================================================================================================



messier_to_ngc = np.loadtxt('data/star info/messier_to_ngc.tsv', skiprows=43, delimiter='|', usecols=(0, 1, 2),
                            dtype=[('ngc_string', 'S20'), ('type', 'S20'), ('messier', 'S20')])

distance_data = np.loadtxt('data/star info/nebula_seds_data.tsv', skiprows=2, delimiter='|', usecols=(1, 2),
                           dtype=[('ngc', 'int'), ('dist', 'int')])

dt = np.loadtxt('data/star info/nebula all 1.tsv', skiprows=47, delimiter='|', usecols=(0, 1, 2),
                dtype=[('glong', 'float'), ('glat', 'float'), ('ngc_string', 'S20')])

fill_with_zeros = np.zeros(messier_to_ngc.size, dtype=int)
messier_to_ngc = rfn.append_fields(messier_to_ngc, ['ngc'], [fill_with_zeros])
messier_to_ngc = ma.filled(messier_to_ngc, 0.0)

for r in messier_to_ngc:
    if type(r["ngc_string"]) != MaskedConstant:
        r["ngc"] = int(str(r["ngc_string"]).strip().replace("I", "100"))
        r["type"] = r["type"].strip()

fill_with_zeros = np.zeros(dt.size, dtype=int)
dt = rfn.append_fields(dt, ['ngc'], [fill_with_zeros])
dt = ma.filled(dt, 0.0)

for r in dt:
    match = re.search('NGC\\s+([0-9]+)', r["ngc_string"])

    if match is not None:
        r["ngc"] = int(match.group(1))
    else:
        match = re.search('IC\\s+([0-9]+)', r["ngc_string"])
        if match is not None:
            r["ngc"] = int("100" + match.group(1))

result, indexes = np.unique(dt['ngc'], return_index=True)
dt = dt[indexes]

result, indexes = np.unique(messier_to_ngc['ngc'], return_index=True)
messier_to_ngc = messier_to_ngc[indexes]

result, indexes = np.unique(distance_data['ngc'], return_index=True)
distance_data = distance_data[indexes]

dt = np.sort(dt, order=['ngc'])
messier_to_ngc = np.sort(messier_to_ngc, order=['ngc'])
distance_data = np.sort(distance_data, order=['ngc'])

dt = rfn.join_by('ngc', dt, messier_to_ngc, jointype = 'leftouter')
dt = ma.filled(dt, 0.0)

dt = dt[(dt["type"] == "Nb") | (dt["type"] == "C+N")]

dt = rfn.join_by('ngc', dt, distance_data, jointype = 'leftouter')
dt = ma.filled(dt, 0.0)

fill_with_zeros = np.zeros(dt.size)

dt = rfn.append_fields(dt, ['x', 'y', 'z'], [fill_with_zeros, fill_with_zeros, fill_with_zeros])
dt = ma.filled(dt, 0.0)

dt = np.sort(dt, order=['messier'])

for r in dt:
    r["messier"] = re.sub("\s+", " ", r["messier"])

dt["glong"] = np.radians(dt["glong"])
dt["glat"] = np.radians(dt["glat"])

dt["x"] = dt["dist"] * np.cos(dt["glat"]) * np.cos(dt["glong"])
dt["y"] = dt["dist"] * np.cos(dt["glat"]) * np.sin(dt["glong"])
dt["z"] = dt["dist"] * np.sin(dt["glat"])

SUN_TO_CENTER_DISTANCE = 27200

center_x = 5000 * np.cos(0) * np.cos(0)
center_y = 5000 * np.cos(0) * np.sin(0)
center_z = 5000 * np.sin(0)


def show_nebulas(dt):
    ax = plt.subplot(111, projection='3d')

    ax.plot((0,), (0,), (0,), 'o', color='orange', markersize=10, label='sun')

    # center galaxy
    ax.plot([0, center_x], [0, center_y], [0, center_z], label='center galaxy')

    arc = Arc((SUN_TO_CENTER_DISTANCE, 0, 0), 2 * SUN_TO_CENTER_DISTANCE, 2 * SUN_TO_CENTER_DISTANCE, theta1=170,
              theta2=190)
    ax.add_patch(arc)
    art3d.pathpatch_2d_to_3d(arc, z=0)

    counter = 0

    for r in dt:
        marker = mlines.Line2D.filled_markers[counter % mlines.Line2D.filled_markers.__len__()]

        ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["messier"] + " " + str(int(r["dist"])), markersize=5,
                marker=marker)

        counter += 1

    ax.legend()

    ax.set_xlabel('ly')
    ax.set_ylabel('ly')
    ax.set_zlabel('ly')

    ax.auto_scale_xyz([-6000, 6000], [-6000, 6000], [-6000, 6000])

    plt.figure(1).tight_layout(pad=0)

    show_maximized_plot('nebulas')


show_nebulas(dt)
