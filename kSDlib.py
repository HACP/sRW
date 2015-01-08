# This library generates the kshell decomposition

# Loading the necessary libraries
from Plotlib import *
from scipy.stats import *
import numpy as np
import time

# Some inialization and degree survays
def initializeKShellList(AM):
    return [0 for ii in range(len(AM))]

def getDegreeFrequency(AM):
    dList = []
    for item in range(len(AM)):
        dList.append(sum(AM[item]))
    u = np.unique(np.array(dList))
    return u

def getDegreeFrequencyNZ(AM):
    dList = []
    for item in range(len(AM)):
        ss = sum(AM[item])
        if ss > 0:
            dList.append(sum(AM[item]))
    u = np.unique(np.array(dList))
    return u

def getDegreeList(AM):
    dList = []
    for ii in range(len(AM)):
        dList.append([ii, sum(AM[ii])])
    return dList

def getDegreeListS(AM):
    dList = []
    for ii in range(len(AM)):
        dList.append(sum(AM[ii]))
    return dList

def getDegreeListSorted(AM):
    dList = []
    for ii in range(len(AM)):
        dList.append([ii, sum(AM[ii])])
    
    dList.sort(key=lambda x:x[1], reverse=True)
    return dList

def getDegreeListK(AM,k):
    dList = getDegreeListSorted(AM)
    dListK = [] 
    for items in dList:
        if items[1] == k:
            dListK.append(items[0])
    return dListK

def getDegreeListLowerK(AM,k):
    dList = getDegreeListSorted(AM)
    dListK = [] 
    for items in dList:
        if items[1] <= k:
            dListK.append(items[0])
    return dListK

def getDegreeListLowerKNZ(AM,k):
    dList = getDegreeListSorted(AM)
    dListK = []
    for items in dList:
        if 0 < items[1] <= k:
            dListK.append(items[0])
    return dListK

# The trimming of the network occurs in phases, in which a nodes with degree less than the input value is inhibited 
# This is represented as a node with zero connections or a zero column-row in the adjacency matrix
def inhibitNode(AM, node):
    Nodes = len(AM)

    for ii in range(Nodes):
        AM[ii][node] = 0
        AM[node][ii] = 0
    return AM

def inhibitNodeList(AM, nodeList):
    for nn in nodeList:
        AM = inhibitNode(AM, nn)
    return AM

def inhibitKShell(AM, k):
    if len(getDegreeFrequency(AM))>1:
        kAM = AM
        kS = [] 
        count  = 0
        plotNetwork(kAM, 'IM_' + str(count))
        for k1 in range(1,k+1):
            count = count + 1
            while len(getDegreeListK(kAM,k1)):
                dLK = getDegreeListLowerK(AM,k1)
                kAM = inhibitNodeList(AM, dLK)
                kS = kS + dLK
            plotNetwork(kAM, 'IM_' + str(count))
            
        return [kAM, kS]
    else:
        print 'All the nodes have the same degree'
        return
    
def inhibitKShellA(AM,k):
    deglist0 = getDegreeList(AM)
    Nodes = len(AM)
    iAM = AM
    nlk = []
    
    degNZ = getDegreeFrequencyNZ(AM)
    if len(degNZ)==1:
        print 'All nodes have the same degree ' + str(degNZ)
        return [AM, getDegreeListLowerKNZ(AM,k)]
    else:
        while len(getDegreeListLowerKNZ(iAM,k))>0:
            nl = getDegreeListLowerKNZ(iAM,k)
            iAM = inhibitNodeList(iAM, nl)
            nlk = nlk + nl
        if len(nlk) == Nodes:
            print 'What now boss?'
        deglist0 = getDegreeList(AM)

        return [iAM, nlk]

def generateKShellDecomposition(AM):
    time0 = time.time()
    print 'Generating kShell decomposition'
    WW = []
    kAM = [AM,0]
    kdeglist = getDegreeFrequencyNZ(kAM[0])
    k = 1
    while len(kdeglist)>1:
        kAM = inhibitKShellA(kAM[0], k)
        plotNetwork(kAM[0], 'k_' + str(k))
        kdeglist = getDegreeFrequencyNZ(kAM[0])
        WW.append(getDegreeList(kAM[0]))
        k = k + 1
    
    nl =  generateKShellIndex(AM, WW)
    time1 = time.time()
    deltat = "%.2f" % (time1-time0)
    print 'kShell decomposition ... done ... (' + deltat + ' s)'

    return nl

def generateKShellIndex(AM, WW):
    time0 = time.time()
    print 'Starting kShell decomposition'
    nl = initializeKShellList(AM)
    for ii in reversed(range(len(WW))):
        for jj in range(len(WW[ii])):
            if WW[ii][jj][1] > 0 and nl[jj] == 0:
                nl[jj] = ii + 1
    for kk in range(len(nl)):
        nl[kk] = nl[kk] + 1
        
    time1 = time.time()
    deltat = "%.2f" % (time1-time0)
    print 'kShell decomposition ... done ... (' + deltat + ' s)'
    return nl

# A first anzatz of the learning function is the product of the k value of each node
def generateKShellFunction(nAM, WW):
    ksF = []
    for ix in range(len(nAM)):
        ksrow = []
        for iy in range(len(nAM)):
            if nAM[ix][iy] == 1:
                ksrow.append(WW[ix]*WW[iy])
            else:
                ksrow.append(0)
        ksF.append(ksrow)
    return ksF

def generateKShellNorm(nAM, WW):
    ksF = generateKShellFunction(nAM, WW)
    ss = 0.0
    for ii in range(len(ksF)):
        for jj in range(ii):
            ss = ss + ksF[ii][jj]

    for ii in range(len(ksF)):
        for jj in range(len(ksF)):
            ksF[ii][jj] = ksF[ii][jj]/ss

    return ksF
