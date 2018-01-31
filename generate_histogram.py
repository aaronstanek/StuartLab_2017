import matplotlib.pyplot as plt
import numpy as np

def generate_histogram(title,x_label,y_label,bin_count,input_data,filename):
    # string, string, string, int, list of floats, string
    # filename is where to save the plot
    # start plotting
    plt.close("all")
    plt.figure(1)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # now the plot is set up
    plt.hist(input_data,bins=bin_count)
    plt.savefig(filename)

def generate_bargraph(title,x_label,y_label,input_data,filename):
    # string, string, string, list of dict(float->float), filename
    # input_data maps x value to a y value
    plt.close("all")
    plt.figure(1)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # now the plot is set up
    objects = list(input_data)
    objects.sort() # we want the stuff in order, otherwise it's hard to read
    align = np.arange(len(objects)) # the horizontal positions of the bars
    y_vals = []
    for x in objects:
        y_vals.append(input_data[x])
    # y_vals now has the heights of the bars, in order
    plt.bar(align, y_vals, align='center', width=1.0) # make the bars
    st_objects = []
    for i in range(len(objects)):
        if i==0:
            st_objects.append(str(objects[0]))
        elif i==len(objects)-1:
            st_objects.append(str(objects[-1]))
        else:
            st_objects.append("")
    plt.xticks(align, st_objects)
    plt.savefig(filename)
