import matplotlib.pyplot as plt

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
