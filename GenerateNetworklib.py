#This library contains the tools needed to generate a betwork

# load necessary libraries
import math, random
import sys, time

import pylab as P
import numpy as np

from Plotlib import *

def generateNetworkPL(Nodes, x0, x1, alpha, name):
    time0 = time.time()
    # generating the number of connections per node following a power law
    V = [] 
    
    for i in range(Nodes):
        y = random.random()
        x = pow((pow(x1, alpha + 1) - pow(x0, alpha + 1))*y + pow(x0, alpha + 1), 1./(alpha + 1))
        V.append(int(math.floor(x)))
    
    plotNodeDistribution(V, name)

    # initialize Adjaceny Matrix 
    AM = [[0 for ix in range(Nodes)] for iy in range(Nodes)]

    #Generating all avialable pairs
    pairs = []
    for ix in range(Nodes):
        for iy in range(ix):
            if ix != iy:
                pairs.append([ix, iy])

    #Generating connections

    print 'Starting generating Network'
    count = 0
    while sum(V) > 1 and count < 10000:
        count = count + 1
        link = random.randrange(len(pairs))
        
        v1 = pairs[link][0]
        v2 = pairs[link][1]
        
        if V[v1]>0 and V[v2]>0:
            V[v1] = V[v1] - 1
            V[v2] = V[v2] - 1
            AM[v1][v2] = 1
            AM[v2][v1] = 1
            
            del pairs[link]
        sys.stdout.write(str(sum(V)) + '\r')
        sys.stdout.flush()
    print sum(V)
    time1 = time.time()

    deltat = "%.2f" % (time1-time0)
    print 'Generating Network ... done (' + deltat + ' s)'
    return AM
