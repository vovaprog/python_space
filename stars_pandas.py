import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
from matplotlib.patches import Arc
import mpl_toolkits.mplot3d.art3d as art3d

from spaceutils import parallax_millisecond_to_light_year, show_maximized_plot


data = pd.read_csv('data/stars.tsv', sep='|', skiprows=range(43)+[44, 45])
names = pd.read_csv('data/stars_names.tsv', sep='|', skiprows=range(32)+[33, 34])
constellations = pd.read_csv('data/stars_cons.tsv', sep='|', skiprows=range(34)+[35, 36])


data.rename(columns={'_Glon': 'glong', '_Glat': 'glat'}, inplace=True)

data = pd.merge(data, names, how='left', on='HD')
data = pd.merge(data, constellations, how='left', on='HD')


data = data[data['Plx'] != 0]
data['Plx'] = data['Plx'].abs()

data['dist'] = parallax_millisecond_to_light_year(data['Plx'])
data["glong"] = np.radians(data["glong"])
data["glat"] = np.radians(data["glat"])

data["x"] = data["dist"] * np.cos(data["glat"]) * np.cos(data["glong"])
data["y"] = data["dist"] * np.cos(data["glat"]) * np.sin(data["glong"])
data["z"] = data["dist"] * np.sin(data["glat"])

data.drop_duplicates('HD', inplace=True)

data.sort_values(by='Vmag', inplace=True)


polaris = data[data["HD"] == 8890]

SUN_TO_CENTER_DISTANCE = 27200.0


# ================================================================================================


def show_stars(dt, view_range, count_show_with_legend, plot_name, scatter=False):
    ax = plt.subplot(111, projection='3d')

    ax.plot((0,), (0,), (0,), 'o', color='orange', markersize=10, label='sun')

    ax.plot([0, view_range], [0, 0], [0, 0], label='to galaxy center')

    arc = Arc((27200, 0, 0), SUN_TO_CENTER_DISTANCE * 2, SUN_TO_CENTER_DISTANCE * 2,
              theta1=180 - np.degrees([view_range / SUN_TO_CENTER_DISTANCE])[0],
              theta2=180 + np.degrees([view_range / SUN_TO_CENTER_DISTANCE])[0])
    ax.add_patch(arc)
    art3d.pathpatch_2d_to_3d(arc, z=0)

    ax.plot([0, polaris["x"]], [0, polaris["y"]], [0, polaris["z"]], label='polaris')

    if scatter:
        ax.scatter(dt['x'], dt['y'], dt['z'], c=dt['Vmag'], cmap=plt.cm.Spectral)
    else:
        counter = 0

        for row_index, r in dt.iterrows():
            marker = mlines.Line2D.filled_markers[counter % mlines.Line2D.filled_markers.__len__()]

            if counter < count_show_with_legend:
                name = r["name"] if type(r["name"]) == str else '?'
                ax.plot([r["x"]], [r["y"]], [r["z"]], 'o',
                        label=name + " " + str(r["Vmag"]) + " " + str(int(r["dist"])) + "ly",
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

    ax.auto_scale_xyz([-view_range, view_range], [-view_range, view_range], [-view_range, view_range])

    show_maximized_plot(plot_name)


# ================================================================================================


dt_stars = data[0:1000]
show_stars(dt_stars, 1000, 0, "1000 brightest stars", True)

dt_stars = data[0:30]
show_stars(dt_stars, 1000, 30, "30 brightest stars")


dt_ursa = data[data["Cst"] == "UMa"]
show_stars(dt_ursa, 200, 6, "ursa major")


dt_orion = data[data["Cst"] == "Ori"]
show_stars(dt_orion, 600, 7, "orion")


dt_filtered = data[data['dist'] < 6000]
plt.hist(dt_filtered['dist'], bins=100)
plt.xlabel('distance light years')
plt.ylabel('number of stars')
show_maximized_plot("star histogram")

