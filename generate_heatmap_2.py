# see https://gist.github.com/teechap/9c066a9ab054cc322877

import matplotlib.pyplot as plt
import numpy as np

def get_min_max(datapoints):
    ou = dict()
    ou["xmin"] = datapoints[0][1]
    ou["xmax"] = datapoints[0][1]
    ou["ymin"] = datapoints[0][0]
    ou["ymax"] = datapoints[0][0]
    for p in datapoints:
        if p[1]<ou["xmin"]:
            ou["xmin"] = p[1]
        elif p[1]>ou["xmax"]:
            ou["xmax"] = p[1]
        if p[0]<ou["ymin"]:
            ou["ymin"] = p[0]
        elif p[0]>ou["ymax"]:
            ou["ymax"] = p[0]
    return ou

def get_bin_width(bin_count,d_min,d_max):
    return (d_max-d_min) / float(bin_count)

def make_axis(bin_count,d_min,d_max):
    dd = get_bin_width(bin_count,d_min,d_max)
    ou = []
    for i in range(bin_count+1):
        spot = float(i)+0.5
        ou.append(d_min+spot*dd)
    return ou

def put_points_in_bins(datapoints,x_bin_count,y_bin_count,mm):
    dx = get_bin_width(x_bin_count,mm["xmin"],mm["xmax"])
    dy = get_bin_width(y_bin_count,mm["ymin"],mm["ymax"])
    ou = []
    for fx in range(x_bin_count+1):
        k = []
        for fy in range(y_bin_count+1):
            k.append(0)
        ou.append(k)
        del(k)
    # ou  now has the correct dimensions
    for p in datapoints:
        sx = (p[1]-mm["xmin"]) / dx
        sx = int(sx)
        if sx>=x_bin_count:
            sx = x_bin_count-1
        sy = (p[0]-mm["ymin"]) / dy
        sy = int(sy)
        if sy>=y_bin_count:
            sy = y_bin_count-1
        ou[sx][sy] = ou[sx][sy] + 1
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
    #  set axis
    mm = get_min_max(datapoints)
    x = make_axis(x_bin_count,mm["xmin"],mm["xmax"])
    y = make_axis(y_bin_count,mm["ymin"],mm["ymax"])
    intensity = put_points_in_bins(datapoints,x_bin_count,y_bin_count,mm)
    #setup the 2D grid with Numpy
    x, y = np.meshgrid(x, y)
    #convert intensity (list of lists) to a numpy array for plotting
    intensity = np.array(intensity)
    #now just plug the data into pcolormesh, it's that easy!
    plt.pcolormesh(x, y, intensity)
    plt.colorbar() #need a colorbar to show the intensity scale
    plt.savefig(filename)
