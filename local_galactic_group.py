# http://edd.ifa.hawaii.edu/
# http://edd.ifa.hawaii.edu/dfirst.php

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as consts
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as mlines
import numpy.lib.recfunctions as rfn

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


dt = np.loadtxt('data/GalaxiesData3.txt', skiprows=5, delimiter='|', usecols=(1, 2, 3, 4, 5),
                  dtype=[('dist', 'float'), ('glong', 'float'), ('glat', 'float'), ('vel', 'float'),
                         ('name', 'S20')])

dt = np.sort(dt, order=['dist'])

# distance_all = data['distance']
# glong = data['glong']
# glat = data['glat']
# velocity_all = data['vel']
# names_all = data['name']


#================================================================================================



# glong = np.radians(glong)
# glat = np.radians(glat)

dt['glong'] = np.radians(dt['glong'])
dt['glat'] = np.radians(dt['glat'])




fill_with_zeros = np.zeros(dt.size)
dt = rfn.append_fields(dt, ['x', 'y', 'z', 'dist_ly'], data=[fill_with_zeros, fill_with_zeros, fill_with_zeros, fill_with_zeros], usemask=False)

dt['x'] = dt['dist'] * np.cos(dt['glat']) * np.cos(dt['glong'])
dt['y'] = dt['dist'] * np.cos(dt['glat']) * np.sin(dt['glong'])
dt['z'] = dt['dist'] * np.sin(dt['glat'])

dt['dist_ly'] = megaparsec_to_lightyear(dt['dist'])

#================================= Galaxies near Milky Way ======================================

center_x = 15 * np.cos(0) * np.cos(0)
center_y = 15 * np.cos(0) * np.sin(0)
center_z = 15 * np.sin(0)





def show_galaxies_near_milky_way(dt):
    #distance_filter = distance_all < 1.0

    #distance = distance_all[distance_filter]
    #x = x_all[distance_filter]
    #y = y_all[distance_filter]
    #z = z_all[distance_filter]
    #names = names_all[distance_filter]

    #distance_lyr = megaparsec_to_lightyear(distance)


    ax = plt.subplot(111, projection='3d')

    #radius = 50 000 lyr
    ax.plot((0,), (0,), (0,), 'o', color='cyan', markersize=15, label='milky way')





    ax.set_color_cycle(['r', 'g', 'b', 'y', 'c', 'm'])

    # for i in range(0, x.size):
    #     if names[i] == 'NGC0224':
    #         marker_size = 20  # radius = 110 000 lyr
    #         galaxy_name = 'Andromeda glx'
    #         marker = 'o'
    #     elif names[i] == 'NGC0598':
    #         marker_size = 10  # radius = 25000-30000 lyr
    #         galaxy_name = 'Triangulum glx'
    #         marker = 'o'
    #     else:
    #         marker_size = 5
    #         galaxy_name = names[i]
    #         marker = mlines.Line2D.filled_markers[i % 8]
    #
    #     ax.plot([x[i]], [y[i]], [z[i]], '.', label=galaxy_name + ' (' + '{0:,.0f}'.format(distance_lyr[i]) + 'ly)',
    #             markersize=marker_size, marker=marker)

    counter = 0

    for r in dt:
        if r['name'] == 'NGC0224':
            marker_size = 20  # radius = 110 000 lyr
            galaxy_name = 'Andromeda glx'
            marker = 'o'
        elif r['name'] == 'NGC0598':
            marker_size = 10  # radius = 25000-30000 lyr
            galaxy_name = 'Triangulum glx'
            marker = 'o'
        else:
            marker_size = 5
            galaxy_name = r['name']
            marker = mlines.Line2D.filled_markers[counter % mlines.Line2D.filled_markers.__len__()]

        ax.plot([r['x']], [r['y']], [r['z']], '.', label=galaxy_name + ' (' + '{0:,.0f}'.format(r['dist_ly']) + 'ly)',
                markersize=marker_size, marker=marker)

        counter += 1


    #ax.legend(fontsize=11)

    ax.legend()

    ax.set_xlabel('Mpc')
    ax.set_ylabel('Mpc')
    ax.set_zlabel('Mpc')

    ax.view_init(elev=10, azim=-25)

    plt.figure(1).tight_layout(pad=0)

    show_maximized_plot('local galactic group')


#=================================== big map ====================================================

def show_galaxies(dt, near):

    # distance_filter = distance_all < distance_limit
    #
    # vel = velocity_all[distance_filter]
    # x = x_all[distance_filter]
    # y = y_all[distance_filter]
    # z = z_all[distance_filter]

    if near:
        dt = dt[dt['dist'] < 15.0]
    else:
        dt = dt[dt['dist'] < 90.0]

    # if near:
    #     dt = dt[dt['dist'] < 15.0]
    # else:
    #     dt = dt[dt['dist'] > 90.0]



    ax = plt.subplot(111, projection='3d')
    ax.scatter(0, 0, 0, color='red')

    ax.scatter(dt['x'], dt['y'], dt['z'], c=dt['vel'], cmap=plt.cm.jet,s=5)


    # center galaxy
#    ax.plot([0, center_x], [0, center_y], [0, center_z], label='to galaxy center')



    for r in dt:
        if not near:
            if str(r['name']) == 'NGC4477':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='virgo')
            elif str(r['name']) == 'NGC1365':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Fornax')
            elif str(r['name']) == 'NGC003568':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Antlia Cluster')
            elif str(r['name']) == 'NGC4696B':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Centaurus Cluster')
            elif str(r['name']) == 'NGC3309':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Hydra Cluster')
            elif str(r['name']) == 'NGC4874':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Coma Cluster')
        else:
            if str(r['name']) == 'NGC3031':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='M81 group')
            elif str(r['name']) == 'NGC5236':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='M83 Group')
            elif str(r['name']) == 'NGC5128':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Centaurus A group')
            elif str(r['name']) == 'NGC5457':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='M101 Group')
            elif str(r['name']) == 'UGC05882':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='M96 group')
            elif str(r['name']) == 'IC0342':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='IC0342')
            elif str(r['name']) == 'NGC0224':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Andromeda')


    ax.legend()

    #ax.view_init(elev=1, azim=1)
    ax.view_init(elev=20, azim=-120)

    ax.set_xlabel('Mpc')
    ax.set_ylabel('Mpc')
    ax.set_zlabel('Mpc')

    #show_maximized_plot('galaxies ' + str(distance_limit) + ' Mpc')
    show_maximized_plot('galaxies ' + '???' + ' Mpc')

#================================================================================================



#dt_filtered=dt[dt['dist'] < 1.0]
#show_galaxies_near_milky_way(dt_filtered)

for r in dt:
    if str(r['name']).find('4874')>=0:
        print r['name']
#exit()

show_galaxies(dt, True)
show_galaxies(dt, False)


#show_galaxies(dt[dt['dist'] < 10.0])
#show_galaxies(dt[dt['dist'] < 35.0])
#show_galaxies(dt[dt['dist'] < 50.0])
