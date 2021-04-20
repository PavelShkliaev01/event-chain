import random, os
import math
import matplotlib.colors
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import sys

import pylab

output_dir = 'movie'
img = 0
if not os.path.exists(output_dir): os.makedirs(output_dir)
def snapshot(pos, colors):
    global img
    pylab.subplots_adjust(left=0.10, right=0.90, top=0.90, bottom=0.10)
    pylab.gcf().set_size_inches(6, 6)
    pylab.axis([0, L, 0, L])
    # pylab.setp(pylab.gca(), xticks=[-L, 2*L], yticks=[-L, 2*L])
    pylab.setp(pylab.gca(), xticks=[0, L], yticks=[0, L])

    for (x, y), c in zip(pos, colors):
        circle = pylab.Circle((x, y), radius=sigma, fc=c)
        pylab.gca().add_patch(circle)
        ax = plt.axes()
        # ax.arrow(x, y, vx, vy, head_width=0.05, head_length=0.1, fc='k', ec='k')
    points = [[0.0, 0.0], [0.5, 0.0], [0.85, 0.6],[0.35, 0.6] ]  # the points to trace the edges.
    polygon = plt.Polygon(points, fill=None, edgecolor='r')
    pylab.gca().add_patch(polygon)
   # rect = plt.Rectangle((0, 0), L, L, angle = 0, fill = False)
    #pylab.gca().add_patch(rect)
    pylab.savefig(os.path.join(output_dir, '%d.png' % img), transparent=True)
    pylab.close()
    img += 1

N=16
L=1
density = 0.68
#sigma = math.sqrt((density * L * L) / (N*math.pi))
sigma = 0.025
# colors = []
colors = ['yellow', 'yellow', 'yellow','yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow', 'yellow',
'yellow', 'yellow', 'yellow']
# for i in range (N):
  # colors.append("r")

Positions = np.zeros([N,2])
# V = np.zeros([N,2])
steps = 40215;

for i in range (0 , 1000):
    # myfile =open("output "+str(i) + ".dat", "r")
    if os.path.exists("!output"+str(i) + ".dat"):
        data = np.loadtxt ("!output"+str(i) + ".dat")
        Positions = data[:,[0,1]]
    # V = data[:,[2,3]]
        snapshot(Positions, colors)
    else:
        break
