import matplotlib.pyplot as plt
import numpy as np

def makeSingleAxisBins(dmin,dmax,dCount):
    dd = float(dmax-dmin) / float(dCount)
    points = []
    for i in range(dCount+1):
        points.append(dmin+(dd*i))
    ou = []
    for i in range(len(points)-1):
        small = points[i]
        big = points[i+1]
        middle = float(big+small) / float(2)
        ou.append([small,middle,big])
    return dd,ou

def makeGrid(xCount,yCount):
    ou = []
    k = []
    for i in range(xCount):
        for j in range(yCount):
            k.append(int(0))
        ou.append(k)
        k = []
    return ou

def TwoAxisSort(data,xmin,dx,xCount,ymin,dy,yCount):
    z = makeGrid(xCount,yCount)
    for dataPoint in data:
        xNum = float(dataPoint[0]-xmin) / float(dx)
        if xNum<0:
            continue
        if xNum>(xCount-1):
            continue
        yNum = float(dataPoint[1]-ymin) / float(dy)
        if yNum<0:
            continue
        if yNum>(yCount-1):
            continue
        xNum = int(xNum)
        yNum = int(yNum)
        z[xNum][yNum] = z[xNum][yNum]+1
    return z

def stripChop(chop):
    ou = []
    for x in chop:
        ou.append(x[1])
    return ou

def generate_heatmap(title,x_label,y_label,x_bin_count,y_bin_count,datapoints,filename):
    # title, x_label, y_label are strings
    # x_bin_count and y_bin_count are integers
    # datapoints is a list of lists of size 2
    # each sublist contains two floats, (and x value and a y value)
    # filename is a string
    plt.close("all")
    plt.figure(1)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # parse datapoints
    x_data = []
    y_data = []
    for p in datapoints:
        x_data.append(p[0])
        y_data.append(p[1])
    # code from earlier version
    dx,xChop = makeSingleAxisBins(min(x_data),max(x_data),x_bin_count)
    dy,yChop = makeSingleAxisBins(min(y_data),max(y_data),y_bin_count)
    z = TwoAxisSort(datapoints,min(x_data),dx,x_bin_count,min(y_data),dy,y_bin_count)
    cmap = plt.get_cmap("plasma")
    xChop = stripChop(xChop)
    yChop = stripChop(yChop)
    plt.contourf(xChop,yChop,z,100)
    plt.savefig(filename)
