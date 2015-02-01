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


data = np.loadtxt('data/GalaxiesData3.txt', skiprows=5, delimiter='|', usecols=(1, 2, 3, 4, 5),
                  dtype=[('dist', 'float'), ('glong', 'float'), ('glat', 'float'), ('vel', 'float'),
                         ('name', 'S20')])

#================================================================================================

data['glong'] = np.radians(data['glong'])
data['glat'] = np.radians(data['glat'])

fill_with_zeros = np.zeros(data.size)
data = rfn.append_fields(data, ['x', 'y', 'z', 'dist_ly'], data=[fill_with_zeros, fill_with_zeros, fill_with_zeros, fill_with_zeros], usemask=False)

data['x'] = data['dist'] * np.cos(data['glat']) * np.cos(data['glong'])
data['y'] = data['dist'] * np.cos(data['glat']) * np.sin(data['glong'])
data['z'] = data['dist'] * np.sin(data['glat'])

data['dist_ly'] = megaparsec_to_lightyear(data['dist'])

data = np.sort(data, order=['dist'])

#================================= Galaxies near Milky Way ======================================

center_x = 1 * np.cos(0) * np.cos(0)
center_y = 1 * np.cos(0) * np.sin(0)
center_z = 1 * np.sin(0)





def show_galaxies_near_milky_way(dt):

    ax = plt.subplot(111, projection='3d')

    ax.plot((0,), (0,), (0,), 'o', color='cyan', markersize=15, label='milky way')

    ax.set_color_cycle(['r', 'g', 'b', 'y', 'c', 'm'])

    counter = 0

    for r in dt:
        if r['name'] == 'NGC0224':
            marker_size = 20
            galaxy_name = 'Andromeda glx'
            marker = 'o'
        elif r['name'] == 'NGC0598':
            marker_size = 10
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

def show_galaxies(dt, view_mode):

    # distance_filter = distance_all < distance_limit
    #
    # vel = velocity_all[distance_filter]
    # x = x_all[distance_filter]
    # y = y_all[distance_filter]
    # z = z_all[distance_filter]

    if view_mode == 0:
        dt = dt[dt['dist'] < 10.0]
        box_size = 9.0
    elif view_mode == 1:
        dt = dt[dt['dist'] < 30.0]
        box_size = 30.0
    else:
        dt = dt[dt['dist'] < 110.0]
        dt = dt[dt['dist'] > 70.0]


    # if near:
    #     dt = dt[dt['dist'] < 15.0]
    # else:
    #     dt = dt[dt['dist'] > 90.0]



    ax = plt.subplot(111, projection='3d')
    ax.scatter(0, 0, 0, color='red')

    #ax.scatter(dt['x'], dt['y'], dt['z'], c=dt['vel'], cmap=plt.cm.jet,s=15,lw=0)
    ax.scatter(dt['x'], dt['y'], dt['z'], c=dt['vel'], cmap=plt.cm.jet)


    # center galaxy
    #ax.plot([0, center_x], [0, center_y], [0, center_z], label='to galaxy center')



    for r in dt:
        if view_mode == 0:
            if str(r['name']) == 'NGC3031':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='M81 group')
            elif str(r['name']) == 'NGC5236':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='M83 group')
            elif str(r['name']) == 'NGC5128':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Centaurus A group')
            elif str(r['name']) == 'NGC5457':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='M101 group')
            elif str(r['name']) == 'UGC05882':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='M96 group')
            elif str(r['name']) == 'IC0342':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='IC342 group')
            elif str(r['name']) == 'NGC0224':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Andromeda galaxy')


            elif str(r['name']) == 'NGC_3992':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Ursa Major Cluster')



        elif view_mode == 1:
            if str(r['name']) == 'NGC4477':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='virgo cluster')
            elif str(r['name']) == 'NGC1365':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='fornax cluster')
            # elif str(r['name']) == 'NGC003568':
            #     ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Antlia Cluster')
            # elif str(r['name']) == 'NGC4696B':
            #     ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Centaurus Cluster')
            # elif str(r['name']) == 'NGC3309':
            #     ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Hydra Cluster')
            # elif str(r['name']) == 'NGC4874':
            #     ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Coma Cluster')
            #
            # elif str(r['name']) == 'NGC_3992':
            #     ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='Ursa Major Cluster')


    ax.legend()

    #ax.view_init(elev=20, azim=-120)

    if view_mode == 0:
        ax.view_init(elev=10, azim=30)
    elif view_mode == 1:
        ax.view_init(elev=5, azim=-150)

    ax.set_xlabel('Mpc')
    ax.set_ylabel('Mpc')
    ax.set_zlabel('Mpc')

    plt.figure(1).tight_layout(pad=0)

    #ax.auto_scale_xyz([-10, 10], [-10, 10], [-10, 10])
    ax.auto_scale_xyz([-box_size, box_size], [-box_size, box_size], [-box_size, box_size])

    #show_maximized_plot('galaxies ' + str(distance_limit) + ' Mpc')
    show_maximized_plot('galaxies ' + '???' + ' Mpc')

#================================================================================================


#data_filtered = data[data['dist'] < 1.0]
#show_galaxies_near_milky_way(data_filtered)



# for r in data:
#      if str(r['name']).find('3992')>=0:
#          print r['name']
#exit()

#show_galaxies(data, 0)
show_galaxies(data, 1)


#show_galaxies(dt[dt['dist'] < 10.0])
#show_galaxies(dt[dt['dist'] < 35.0])
#show_galaxies(dt[dt['dist'] < 50.0])
