# The main body of the code happens here

# Loading all the necessary libraries
from GenerateNetworklib import *
from RandomWalklib import *
from Plotlib import *
from kSDlib import *

import os, sys, random, time

# Providing a descriptive name
name = 'k_500_4_20_1p5'

Nodes = 500
x0 = 4
x1 = 20
alpha = -1.5

iterations = 1000

# Generating the network  
AM = generateNetworkPL(Nodes, x0, x1, alpha, name)
nAM = [row[:] for row in AM]

plotNetwork(AM, name)
deglist = getDegreeFrequency(AM)
deg = getDegreeListS(AM)

# In order to prevent unconnected nodes
if 0 in deglist:
    print 'Isolated node '
    sys.exit(0)

# Generating the kshell decomposition
WW = generateKShellDecomposition(AM)
plotNetworkKShellRadius(nAM, WW, name)

# A series of random walks are generated
RWs = generateRealizations(nAM, iterations)

RWsSuper = generateRealizationsSuper(nAM, iterations, WW)

RWsOrder = generateRealizationsSuper(nAM, iterations, deg)

# the statistics of the random walks are plotted
plotRandomWalkStatsSuperOrder(RWs, RWsSuper, RWsOrder, name)
