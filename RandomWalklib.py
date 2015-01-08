import random, sys
import pylab as P
import numpy as np

# General tools needed for the random walk on a given network with adjacency matrix AM

# For a given node, find the neighbors
def getNeighbors(AM, node):
    Nodes = len(AM)
    V = []
    for ii in range(Nodes):
        if AM[ii][node] == 1:
            V.append(ii)
    return V

# If the current position of the random walker is given, the next step is chosen among the neighbors of the node
def generateNextStepSuper(AM, step, learn):

    Nodes = len(AM)

    nNodes = getNeighbors(AM, step)

    rrange = 0
    Rrange = []
    Rweights = []
    for item in nNodes:
        Rrange.append(rrange)
        Rweights.append(learn[item]**2)
        rrange = rrange + learn[item]**2
    Rrange.append(rrange)
    
    x = random.uniform(0, rrange)
    
    for ii in range(len(nNodes)):
        if Rrange[ii] < x < Rrange[ii+1]:
            binn = ii

    binr = random.randrange(len(nNodes))
    return nNodes[binn]
    
def generateNextStep(AM, step):

    Nodes = len(AM)

    nNodes = getNeighbors(AM, step)

    return nNodes[random.randrange(len(nNodes))]


# For each initial position a random walk is launched and it continues untill the entire network is visited or a maximum of 10000 steps 
def generateCompleteCoverage(AM):
    Nodes = len(AM)
    sNodes = [0 for ii in range(Nodes)]
    init = random.randrange(Nodes)
    sNodes[init] = 1

    steps = 0

    ns = init
    while sum(sNodes) < 0.9*Nodes and steps < 10000:
        ns = generateNextStep(AM, ns)
        sNodes[ns] = 1
        steps = steps + 1
        
    return [steps, sum(sNodes)]

def generateCompleteCoverageSuper(AM, learn):
    Nodes = len(AM)
    sNodes = [0 for ii in range(Nodes)]
    init = random.randrange(Nodes)
    sNodes[init] = 1

    steps = 0

    ns = init
    while sum(sNodes) < 0.9*Nodes and steps < 10000:
        ns = generateNextStepSuper(AM, ns, learn)
        sNodes[ns] = 1
        steps = steps + 1

    return [steps, sum(sNodes)]

# The realizations of a random walk can be repeated to generate a sample
def generateRealizations(AM, iterations):
    print 'Starting Random Walk'
    vS = []
    vC = []
    for ii in range(iterations):
        sys.stdout.write(str(ii) + ' of ' + str(iterations) + '\r')
        sys.stdout.flush()
        rw = generateCompleteCoverage(AM)

        if rw[0] == 1000:
            vS.append(rw[1])
        else:
            vC.append(rw[0])
        
    print 'Random Walk ... done'

    return [vS, vC]


def generateRealizationsSuper(AM, iterations, learn):
    print 'Starting Random Walk'
    vS = []
    vC = []
    for ii in range(iterations):
        sys.stdout.write(str(ii) + ' of ' + str(iterations) + '\r')
        sys.stdout.flush()
        rw = generateCompleteCoverageSuper(AM, learn)
        #print rw
        if rw[0] == 1000:
            vS.append(rw[1])
        else:
            vC.append(rw[0])

    print 'Random Walk ... done'
    
    return [vS, vC]


# The basic statistics of the distribution is presented using plotRandomWalkStats
def plotRandomWalkStats(randomwalks, name):
    
    if len(randomwalks[0]) > 0:
        fig = P.figure()
        n, bins, patches = P.hist(randomwalks[0], 50, normed=1, histtype='step')
        P.setp(patches,'facecolor', 'b', 'alpha', 0.5)
        
        fig.savefig('RWC_' + name + '.png')
        print 'Plot RW Coverage Stats ... done'
        
    if len(randomwalks[1]) > 0:
        figC = P.figure()
        n, bins, patches = P.hist(randomwalks[1], 50, normed=1, histtype='step')
        P.setp(patches,'facecolor', 'b', 'alpha', 0.5)
        P.xlabel('coverage steps')
        P.ylabel('frequency')

        
        figC.savefig('RWP_' + name + '.png')
        print 'Plot RW paths Stats ... done'


def plotRandomWalkStatsSuper(randomwalks, randomwalks_super, name):

    if len(randomwalks[0]) > 0:
        fig = P.figure()
        n, bins, patches = P.hist(randomwalks[0], 50, normed=1, histtype='step')
        P.setp(patches,'facecolor', 'b', 'alpha', 0.5)

        fig.savefig('RWC_' + name + '.png')
        print 'Plot RW Coverage Stats ... done'

    if len(randomwalks[1]) > 0 and len(randomwalks_super[1]) > 0:
        figC = P.figure()
        n, bins, patches = P.hist(randomwalks[1], 50, normed=1, histtype='step', label = 'RW')
        P.setp(patches,'facecolor', 'b', 'alpha', 0.5)
        n, bins, patches = P.hist(randomwalks_super[1], 50, normed=1, histtype='step', label = 'sRW')
        P.setp(patches,'facecolor', 'r', 'alpha', 0.5)
        P.xlabel('coverage steps')
        P.ylabel('frequency')
        P.legend(loc = 'upper right')

        figC.savefig('RWP_super_' + name + '.png')
        print 'Plot RW paths Stats ... done'

def plotRandomWalkStatsSuperOrder(randomwalks, randomwalks_super, randomwalks_order, name):

    if len(randomwalks[0]) > 0:
        fig = P.figure()
        n, bins, patches = P.hist(randomwalks[0], 50, normed=1, histtype='step')
        P.setp(patches,'facecolor', 'b', 'alpha', 0.5)

        fig.savefig('RWC_' + name + '.png')
        print 'Plot RW Coverage Stats ... done'

    if len(randomwalks[1]) > 0 and len(randomwalks_super[1]) > 0:
        figC = P.figure()
        n, bins, patches = P.hist(randomwalks_super[1], 50, normed=1, histtype='step', label = 'sRW_k')
        P.setp(patches,'facecolor', 'r', 'alpha', 0.5)
        n, bins, patches = P.hist(randomwalks_order[1], 50, normed=1, histtype='step', label = 'sRW_o')
        P.setp(patches,'facecolor', 'g', 'alpha', 0.5)
        n, bins, patches = P.hist(randomwalks[1], 50, normed=1, histtype='step', label = 'RW')
        P.setp(patches,'facecolor', 'b', 'alpha', 0.5)


        P.xlabel('coverage steps')
        P.ylabel('frequency')
        P.legend(loc = 'upper right')

        figC.savefig('RWP_super_' + name + '.png')
        print 'Plot RW paths Stats ... done'
