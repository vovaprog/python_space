import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as mlines
import numpy.lib.recfunctions as rfn

from spaceutils import megaparsec_to_lightyear, show_maximized_plot


#================================================================================================


data = np.loadtxt('data/galaxies.tsv', skiprows=7, delimiter='|', usecols=(1, 2, 3, 4, 5),
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


#================================================================================================


def show_local_group(dt):

    dt = dt[dt['dist'] < 1.0]

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

    ax.legend()

    ax.set_xlabel('Mpc')
    ax.set_ylabel('Mpc')
    ax.set_zlabel('Mpc')

    ax.view_init(elev=10, azim=-25)

    show_maximized_plot('local group')


#================================================================================================


def show_galaxies(dt, view_mode):

    if view_mode == 0:
        box_size = 10.0
        dt = dt[dt['dist'] < box_size]
    elif view_mode == 1:
        box_size = 30.0
        dt = dt[dt['dist'] < box_size]
    elif view_mode == 2:
        box_size = 70.0
        dt = dt[dt['dist'] < box_size]
        dt = dt[dt['dist'] > 30.0]
    elif view_mode == 3:
        box_size = 120.0
        dt = dt[dt['dist'] < box_size]
        dt = dt[dt['dist'] > 40.0]

    ax = plt.subplot(111, projection='3d')
    ax.scatter(0, 0, 0, color='red')

    ax.scatter(dt['x'], dt['y'], dt['z'], c=dt['vel'], cmap=plt.cm.jet)

    ax.set_color_cycle(['r', 'g', 'm', 'c', 'y', 'b'])

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
        elif view_mode == 1:
            if str(r['name']) == 'NGC4477':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='virgo cluster')
            elif str(r['name']) == 'NGC1365':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='fornax cluster')
        elif view_mode == 2 or view_mode == 3:
            if str(r['name']) == 'NGC4696B':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='centaurus cluster')
            elif str(r['name']) == 'NGC3309':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='hydra cluster')
            elif str(r['name']) == 'NGC4874':
                ax.plot([0, r['x']], [0, r['y']], [0, r['z']], label='coma cluster')

    ax.legend()

    if view_mode == 0:
        ax.view_init(elev=10, azim=40)
    elif view_mode == 1:
        ax.view_init(elev=5, azim=-150)
    elif view_mode == 2 or view_mode == 3:
        ax.view_init(elev=0, azim=-70)

    ax.set_xlabel('Mpc')
    ax.set_ylabel('Mpc')
    ax.set_zlabel('Mpc')

    ax.auto_scale_xyz([-box_size, box_size], [-box_size, box_size], [-box_size, box_size])

    show_maximized_plot('galaxies ' + str(int(box_size)) + ' Mpc')


#================================================================================================


show_local_group(data)


show_galaxies(data, 0)
show_galaxies(data, 1)
show_galaxies(data, 2)
show_galaxies(data, 3)


