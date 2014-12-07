# http://edd.ifa.hawaii.edu/
# http://edd.ifa.hawaii.edu/dfirst.php

import sys

sys.path.append('../modules')

import numpy as np
import matplotlib.pyplot as plt
import scipy.constants as consts
from scipy.optimize import curve_fit
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.lines as mlines
from astropy import units as u

from plot_utils import set_graph_title, maximize_plot_window, show_maximized_plot
from astronomy_utils import MegaParsecToLightYear

import matplotlib.cm as cm


#data = np.loadtxt('data/galaxies_around_milky_way_data.txt', skiprows=5, delimiter='|', usecols=(1, 4, 5, 6),
data = np.loadtxt('data/GalaxiesData3.txt', skiprows=5, delimiter='|', usecols=(1, 2, 3, 4, 5),
                  dtype=[('distance', 'float'), ('glong', 'float'), ('glat', 'float'), ('vel', 'float'), ('name', 'S20')])

data = np.sort(data, order=['distance'])

DistanceAll = data['distance']
glong = data['glong']
glat = data['glat']
velAll = data['vel']
namesAll = data['name']

print np.amin(velAll)

plt.hist(velAll,30)
plt.show()

#exit()

# ==============================================================================================================



glong = np.radians(glong)
glat = np.radians(glat)

xAll = DistanceAll * np.cos(glat) * np.cos(glong)
yAll = DistanceAll * np.cos(glat) * np.sin(glong)
zAll = DistanceAll * np.sin(glat)


#============================== Galaxies near Milky Way ===================================

DistanceFilter = DistanceAll < 1.0

distance = DistanceAll[DistanceFilter]
x = xAll[DistanceFilter]
y = yAll[DistanceFilter]
z = zAll[DistanceFilter]
names = namesAll[DistanceFilter]

DistanceLyr = MegaParsecToLightYear(distance)

#plt.figure(facecolor="black")



ax = plt.subplot(111, projection='3d')

#radius = 50 000 lyr
ax.plot((0,), (0,), (0,), 'o', color='cyan', markersize=15, label='milky way')


#NameFilter = names == 'NGC0224'

#print x[NameFilter]
#print y[NameFilter]
#print z[NameFilter]

#ax.plot((x[NameFilter][0],), (y[NameFilter][0],), (z[NameFilter][0],),'.',label='Andromeda' + ' ('+ ('{0:,.0f}'.format(DistanceLyr[NameFilter][0])) +')',markersize=20,marker='o',color='red')

#show_maximized_plot('galaxies around milky way')
#exit()

ax.set_color_cycle(['r', 'g', 'b', 'y', 'c', 'm'])

for i in range(0, x.size):
    if names[i] == 'NGC0224':
        MarkerSz = 20  # radius = 110 000 lyr
        GalaxyName = 'Andromeda glx'
        Marker = 'o'
    elif names[i] == 'NGC0598':
        # radius = 25000-30000 lyr
        MarkerSz = 10
        GalaxyName = 'Triangulum glx'
        Marker = 'o'
    else:
        MarkerSz = 5
        GalaxyName = names[i]
        Marker = mlines.Line2D.filled_markers[i % 8]

    #	ax.plot((x[i],), (y[i],), (z[i],),'.',label=GalaxyName + ' ('+ '{0:,.0f}'.format(DistanceLyr[i]) +')',markersize=MarkerSz,marker=Marker)
    #,color=plt.cm.jet(i)

    ax.plot([x[i]], [y[i]], [z[i]], '.', label=GalaxyName + ' (' + '{0:,.0f}'.format(DistanceLyr[i]) + ')',
            markersize=MarkerSz, marker=Marker)

#ax.legend(fontsize=11)

ax.legend()

ax.set_xlabel('Mpc')
ax.set_ylabel('Mpc')
ax.set_zlabel('Mpc')

ax.view_init(elev=10, azim=-25)

plt.figure(1).tight_layout(pad=0)

show_maximized_plot('local galactic group')

#exit()

#================================ big map ====================================================

def ShowScatter(DistanceLimit):
    DistanceFilter = DistanceAll < DistanceLimit

    #distance = DistanceAll[DistanceFilter]
    velDist = velAll[DistanceFilter]
    xDist = xAll[DistanceFilter]
    yDist = yAll[DistanceFilter]
    zDist = zAll[DistanceFilter]
    #names = namesAll[DistanceFilter]

    ax = plt.subplot(111, projection='3d')
    ax.scatter(0, 0, 0, color='red')


    ax.scatter(xDist, yDist, zDist, c=velDist,
               #cmap=plt.cm.gnuplot)
        #cmap=plt.cm.bwr)
        cmap=plt.cm.jet)


    # colors = cm.rainbow(np.linspace(0, 1, 10))
    #
    # for clr in colors:
    #     print clr
    #
    # lowBound=-500.0
    # upBound=0.0
    #
    # for i in range(0,10):
    #     velFilter=((velDist>lowBound) & (velDist<upBound))
    #
    #     x=xDist[velFilter]
    #     y=yDist[velFilter]
    #     z=zDist[velFilter]
    #
    #     print x.size
    #
    #     ax.scatter(x, y, z, color=colors[i])
    #
    #     lowBound+=500.0
    #     upBound+=500.0



    #
    # velFilter = velDist <= 0
    #
    # x=xDist[velFilter]
    # y=yDist[velFilter]
    # z=zDist[velFilter]
    #
    # ax.scatter(x, y, z, color=colors[0])
    #
    #
    # velFilter = ((velDist > 0) & (velDist<= 1000))
    #
    # x=xDist[velFilter]
    # y=yDist[velFilter]
    # z=zDist[velFilter]
    #
    # ax.scatter(x, y, z, color= colors[1]) #'blue')
    #
    #
    # velFilter = ((velDist > 1000) & (velDist<= 2000))
    #
    # x=xDist[velFilter]
    # y=yDist[velFilter]
    # z=zDist[velFilter]
    #
    # ax.scatter(x, y, z,color='red')
    #
    #
    # velFilter = ((velDist > 2000) & (velDist<= 3000))
    #
    # x=xDist[velFilter]
    # y=yDist[velFilter]
    # z=zDist[velFilter]
    #
    # ax.scatter(x, y, z,color='green')



    ax.set_xlabel('Mpc')
    ax.set_ylabel('Mpc')
    ax.set_zlabel('Mpc')

    show_maximized_plot('galaxies ' + str(DistanceLimit) + ' Mpc')


#ShowScatter(10)
ShowScatter(25)
#ShowScatter(50)
