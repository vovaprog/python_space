import numpy as np
import numpy.lib.recfunctions as rfn
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Arc
import mpl_toolkits.mplot3d.art3d as art3d

from spaceutils import parallax_millisecond_to_light_year, show_maximized_plot


#================================================================================================


data = np.loadtxt('data/stars.tsv', skiprows=46, delimiter='|', usecols=(0, 1, 2, 3, 4),
                dtype=[('glong', 'float'), ('glat', 'float'), ('vmag', 'float'), ('parallax', 'float'), ('hd', 'int')])

names = np.loadtxt('data/stars_names.tsv', skiprows=35, delimiter='|', usecols=(0, 1),
                   dtype=[('hd', 'int'), ('name', 'S20')])

constellations = np.loadtxt('data/stars_cons.tsv', skiprows=37, delimiter='|', usecols=(0, 1),
                            dtype=[('hd', 'int'), ('con', 'S20')])


#================================================================================================


result, indexes = np.unique(data['hd'], return_index=True)
data = data[indexes]

result, indexes = np.unique(names['hd'], return_index=True)
names = names[indexes]

result, indexes = np.unique(constellations['hd'], return_index=True)
constellations = constellations[indexes]

data = rfn.join_by('hd', data, names, jointype='leftouter', usemask=False, defaults={'name': '?'})

data = rfn.join_by('hd', data, constellations, jointype='leftouter',usemask=False, defaults={'con': '?'})

fill_with_zeros = np.zeros(data.size)

data = rfn.append_fields(data, ['x', 'y', 'z', 'dist'],
                       [fill_with_zeros, fill_with_zeros, fill_with_zeros, fill_with_zeros], usemask=False)


#================================================================================================


data = data[data["parallax"] != 0]

data["parallax"] = np.absolute(data["parallax"])


data["dist"] = parallax_millisecond_to_light_year(data["parallax"])


data["glong"] = np.radians(data["glong"])
data["glat"] = np.radians(data["glat"])

data["x"] = data["dist"] * np.cos(data["glat"]) * np.cos(data["glong"])
data["y"] = data["dist"] * np.cos(data["glat"]) * np.sin(data["glong"])
data["z"] = data["dist"] * np.sin(data["glat"])


#================================================================================================


polaris = data[data["hd"] == 8890]

data = np.sort(data, order=['vmag'])

SUN_TO_CENTER_DISTANCE = 27200.0


#================================================================================================


def show_stars(dt, range, count_show_with_legend, plot_name, scatter=False):
    ax = plt.subplot(111, projection='3d')

    ax.plot((0,), (0,), (0,), 'o', color='orange', markersize=10, label='sun')

    ax.plot([0, range], [0, 0], [0, 0], label='to galaxy center')

    arc = Arc((27200, 0, 0), SUN_TO_CENTER_DISTANCE * 2, SUN_TO_CENTER_DISTANCE * 2,
              theta1=180 - np.degrees(range / SUN_TO_CENTER_DISTANCE),
              theta2=180 + np.degrees(range / SUN_TO_CENTER_DISTANCE))
    ax.add_patch(arc)
    art3d.pathpatch_2d_to_3d(arc, z=0)

    ax.plot([0, polaris["x"][0]], [0, polaris["y"][0]], [0, polaris["z"][0]], label='polaris')

    if scatter:
        ax.scatter(dt['x'], dt['y'], dt['z'])
    else:
        counter = 0

        for r in dt:
            marker = mlines.Line2D.filled_markers[counter % mlines.Line2D.filled_markers.__len__()]

            if counter < count_show_with_legend:
                ax.plot([r["x"]], [r["y"]], [r["z"]], 'o',
                        label=r["name"] + " " + str(r["vmag"]) + " " + str(int(r["dist"])) + "ly",
                        markersize=5, marker=marker)
            else:
                ax.plot([r["x"]], [r["y"]], [r["z"]], '.', markersize=2)

            counter += 1

        try:
            ax.legend(numpoints=1, fontsize=10)  # call with fontsize fails on debian 7
        except:
            ax.legend(numpoints=1)


    ax.set_xlabel('ly')
    ax.set_ylabel('ly')
    ax.set_zlabel('ly')

    ax.auto_scale_xyz([-range, range], [-range, range], [-range, range])

    show_maximized_plot(plot_name)


#================================================================================================


dt_stars = data[0:30]
show_stars(dt_stars, 1000, 30, "30 brightest stars")


dt_stars = data[0:1000]
show_stars(dt_stars, 1000, 0, "1000 brightest stars", True)


dt_ursa = data[data["con"] == "UMa"]
show_stars(dt_ursa, 200, 6, "ursa major")


dt_orion = data[data["con"] == "Ori"]
show_stars(dt_orion, 600, 7, "orion")


dt_filtered = data[data['dist'] < 8000]
plt.hist(dt_filtered['dist'], bins=150)
plt.xlabel('distance light years')
plt.ylabel('number of stars')
show_maximized_plot("star histogram")

