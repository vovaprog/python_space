# http://edd.ifa.hawaii.edu/
# http://edd.ifa.hawaii.edu/dfirst.php

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as consts
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as mlines


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


def megaparsec_to_lightyear(dist):
    LIGHT_YEARS_IN_PARSEC = 3.2615638
    return dist * consts.mega * LIGHT_YEARS_IN_PARSEC


#================================================================================================


data = np.loadtxt('data/GalaxiesData3.txt', skiprows=5, delimiter='|', usecols=(1, 2, 3, 4, 5),
                  dtype=[('distance', 'float'), ('glong', 'float'), ('glat', 'float'), ('vel', 'float'),
                         ('name', 'S20')])

data = np.sort(data, order=['distance'])

distance_all = data['distance']
glong = data['glong']
glat = data['glat']
velocity_all = data['vel']
names_all = data['name']


#================================================================================================


glong = np.radians(glong)
glat = np.radians(glat)

x_all = distance_all * np.cos(glat) * np.cos(glong)
y_all = distance_all * np.cos(glat) * np.sin(glong)
z_all = distance_all * np.sin(glat)


#================================= Galaxies near Milky Way ======================================

distance_filter = distance_all < 1.0

distance = distance_all[distance_filter]
x = x_all[distance_filter]
y = y_all[distance_filter]
z = z_all[distance_filter]
names = names_all[distance_filter]

distance_lyr = megaparsec_to_lightyear(distance)


ax = plt.subplot(111, projection='3d')

#radius = 50 000 lyr
ax.plot((0,), (0,), (0,), 'o', color='cyan', markersize=15, label='milky way')


ax.set_color_cycle(['r', 'g', 'b', 'y', 'c', 'm'])

for i in range(0, x.size):
    if names[i] == 'NGC0224':
        marker_size = 20  # radius = 110 000 lyr
        galaxy_name = 'Andromeda glx'
        marker = 'o'
    elif names[i] == 'NGC0598':
        marker_size = 10  # radius = 25000-30000 lyr
        galaxy_name = 'Triangulum glx'
        marker = 'o'
    else:
        marker_size = 5
        galaxy_name = names[i]
        marker = mlines.Line2D.filled_markers[i % 8]

    ax.plot([x[i]], [y[i]], [z[i]], '.', label=galaxy_name + ' (' + '{0:,.0f}'.format(distance_lyr[i]) + 'ly)',
            markersize=marker_size, marker=marker)

#ax.legend(fontsize=11)

ax.legend()

ax.set_xlabel('Mpc')
ax.set_ylabel('Mpc')
ax.set_zlabel('Mpc')

ax.view_init(elev=10, azim=-25)

plt.figure(1).tight_layout(pad=0)

show_maximized_plot('local galactic group')


#=================================== big map ====================================================

def show_galaxies(distance_limit):

    distance_filter = distance_all < distance_limit

    vel = velocity_all[distance_filter]
    x = x_all[distance_filter]
    y = y_all[distance_filter]
    z = z_all[distance_filter]

    ax = plt.subplot(111, projection='3d')
    ax.scatter(0, 0, 0, color='red')

    ax.scatter(x, y, z, c=vel, cmap=plt.cm.jet)  # gnuplot bwr

    ax.set_xlabel('Mpc')
    ax.set_ylabel('Mpc')
    ax.set_zlabel('Mpc')

    show_maximized_plot('galaxies ' + str(distance_limit) + ' Mpc')

#================================================================================================

show_galaxies(10)
show_galaxies(25)
show_galaxies(50)
