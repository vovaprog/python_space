import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.art3d as art3d
import re
import numpy.lib.recfunctions as rfn
from matplotlib.patches import Arc

from spaceutils import parsec_to_lightyear, show_maximized_plot


#================================================================================================

def convert_ngc(ngc_string):
    match = re.search('NGC\\s+([0-9]+)', ngc_string)

    if match is not None:
        return int(match.group(1))
    else:
        return 0


dt = np.genfromtxt('data/nebulas.tsv', skiprows=51, delimiter='|', usecols=(0, 1, 2, 3, 4),
                   dtype=[('glat', 'float'), ('glong', 'float'), ('ngc', 'int'), ('type', 'S20'), ('messier', 'S20')],
                   converters={3: lambda s: str(s).strip()})

nebula_distance = np.loadtxt('data/nebulas_distance_seds.tsv', skiprows=2, delimiter='|', usecols=(1, 2),
                             dtype=[('ngc', 'int'), ('dist', 'int')])

planetary_nebula_distance = np.loadtxt('data/nebulas_distance_planetary.tsv', skiprows=38, delimiter='|',
                                       usecols=(0, 1),
                                       converters={0: convert_ngc}, dtype=[('ngc', 'int'), ('dist', 'int')])


#================================================================================================


planetary_nebula_distance['dist'] = parsec_to_lightyear(planetary_nebula_distance['dist'])

nebula_distance = np.append(nebula_distance, planetary_nebula_distance)


#================================================================================================


result, indexes = np.unique(dt['ngc'], return_index=True)
dt = dt[indexes]

result, indexes = np.unique(nebula_distance['ngc'], return_index=True)
nebula_distance = nebula_distance[indexes]

dt = np.sort(dt, order=['ngc'])
nebula_distance = np.sort(nebula_distance, order=['ngc'])


#================================================================================================


dt = rfn.join_by('ngc', dt, nebula_distance, jointype='leftouter', usemask=False, defaults={'dist': 0})

result, indexes = np.unique(dt['messier'], return_index=True)
dt = dt[indexes]


#================================================================================================


fill_with_zeros = np.zeros(dt.size)
dt = rfn.append_fields(dt, ['x', 'y', 'z'], data=[fill_with_zeros, fill_with_zeros, fill_with_zeros], usemask=False)

dt["glong"] = np.radians(dt["glong"])
dt["glat"] = np.radians(dt["glat"])

dt["x"] = dt["dist"] * np.cos(dt["glat"]) * np.cos(dt["glong"])
dt["y"] = dt["dist"] * np.cos(dt["glat"]) * np.sin(dt["glong"])
dt["z"] = dt["dist"] * np.sin(dt["glat"])


#================================================================================================


dt = np.sort(dt, order=['messier'])

SUN_TO_CENTER_DISTANCE = 27200


#================================================================================================


ax = plt.subplot(111, projection='3d')

ax.plot((0,), (0,), (0,), 'o', color='orange', markersize=10, label='sun')

ax.plot([0, 5000], [0, 0], [0, 0], label='to galaxy center')

arc = Arc((SUN_TO_CENTER_DISTANCE, 0, 0), 2 * SUN_TO_CENTER_DISTANCE, 2 * SUN_TO_CENTER_DISTANCE, theta1=170,
          theta2=190)
ax.add_patch(arc)
art3d.pathpatch_2d_to_3d(arc, z=0)

for r in dt:

    if r['type'] == 'Pl':
        marker = 'o'
        planetary_suffix = ' (pl)'
    else:
        marker = '^'
        planetary_suffix = ''

    ax.plot([r["x"]], [r["y"]], [r["z"]], 'o', label=r["messier"] + "   " + str(int(r["dist"])) + planetary_suffix,
            markersize=6,
            marker=marker)

ax.legend(numpoints=1)

ax.set_xlabel('ly')
ax.set_ylabel('ly')
ax.set_zlabel('ly')

ax.auto_scale_xyz([-7000, 7000], [-7000, 7000], [-7000, 7000])

show_maximized_plot('nebulas')

