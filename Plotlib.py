# Tools for plotting

# load necessary libraries                                                                                                                                                
import math, random
import sys

import pylab as P
import numpy as np

# Plotting the node distribution
def plotNodeDistribution(V, name):
    P.figure()
    n, bins, patches = P.hist(V, 50, normed = True, histtype = 'stepfilled', color = 'b', alpha = 0.15)
    P.xlabel('node degree')
    P.ylabel('frequency')
    P.savefig('node_distribution_'+ name + '.png')
    return

# Representing the network in a circular graph, where the radius of the node is 
# proportional to the degree

def plotNetwork(AM, name):

    # Plotting the nodes

    nodes = len(AM)

    radius = 5.

    X = []
    Y = []
    S = []
    for ii in range(nodes):
        theta = ii*2*math.pi/nodes
        X.append(radius*math.cos(theta))
        Y.append(radius*math.sin(theta))
        S.append(sum(AM[ii]))
  
    cS = []
    for item in S:
        if max(S)>min(S):
            zz =1.*(item - min(S))/(max(S)-min(S))
        else:
            zz = max(S)
        cs = 1000.*zz*zz*zz + 50
        cS.append(cs)
        

    fig = P.figure()
    ax = fig.add_subplot(111)

    P.axis('off')
    ax.scatter(X,Y, s=cS, edgecolor = '', c = 'lightblue')

    # Plotting the edges

    for ix in range(nodes):
        for iy in range(ix):
            if AM[ix][iy] > 0:
                thetax = ix*2*math.pi/nodes
                thetay = iy*2*math.pi/nodes
                P.plot([radius*math.cos(thetax), radius*math.cos(thetay)], [radius*math.sin(thetax), radius*math.sin(thetay)], 'k-', linewidth = .1)

    ax.set_aspect(1./ax.get_data_ratio())
    fig.savefig('network_'+ name + '.png')
    return
    
    # Once the k-shell decomposition is generated, the network can be represented using the position of the k-shell as a radius 
# Therefore the innermost nodes correspond to lower values of k_s and the largest k_s nodes are located in the outer layers

def plotNetworkKShellRadius(AM, kshell_list, name):
    # Plotting the edges in concentric circles with radii proportional to the k_s value
    nodes = len(AM)

    X = []
    Y = []
    S = []
    for ii in range(nodes):
        radius = kshell_list[ii]
        theta = ii*2*math.pi/nodes
        X.append(radius*math.cos(theta))
        Y.append(radius*math.sin(theta))
        S.append(sum(AM[ii]))
  
    cS = []
    for item in S:
        if max(S)>min(S):
            zz =1.*(item - min(S))/(max(S)-min(S))
        else:
            zz = max(S)
        cs = 1000.*zz*zz*zz + 50
        cS.append(cs)
        

    fig = P.figure()
    ax = fig.add_subplot(111)

    P.axis('off')

    # Generating the color code - red for larger k shell value and blue for the lowest value

    color_list = generateColor(kshell_list)

    ax.scatter(X,Y, s=cS, edgecolor = '', c = color_list, alpha = 0.5)

    # Plotting the edges

    for ix in range(nodes):
        for iy in range(ix):
            if AM[ix][iy] > 0:
                P.plot([X[ix],X[iy]], [Y[ix], Y[iy]], 'k-', linewidth = .1)
    ax.set_aspect(1./ax.get_data_ratio())

    fig.savefig('network_kshell_'+ name + '.png')

    return

# This function generates the color code in the network representation
def generateColor(nl):
    maxx = max(nl)
    minn = min(nl)
    cl = []
    for item in nl:
        x = (item - minn)/(maxx - minn)
        cl.append(x)
    return cl
