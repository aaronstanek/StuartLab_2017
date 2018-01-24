from get_files_in_folder import *
from read_json_ord_clump import *
from integrate_json_ord_clump import *
from generate_histogram import *

def histograms_from_folder(folder_path,what):
    # folderpath is a strings
    # what is a dict (integer->list(string))
    # it maps channel numbers to [title,x_label,y_label,bin_count,filename]
    # what dictates details of the plot to be generated for that channel
    # filename is the full path where the plot will be save (prefer ending in .png)
    # this function takes the data from a folder and plots it
    file_list = get_files_in_folder(folder_path)
    t = 0.0
    event_list = []
    for f in file_list:
        [ev,t] = read_json_ord_clump_basic(f) # you better hope that they all have the same delta t
        event_list = event_list + ev
    del(file_list) # just to be nice
    integrated = integrate_json_ord_clump(event_list,t)
    del(event_list)
    del(t)
    for plotnum in what:
        u = [] # take all the integration sums for a particular channel, and put them in this list
        for f in integrated:
            u.append(f[plotnum])
        # u now has all the integration sums for the channel plotnum
        # now plot it
        generate_histogram(what[plotnum][0],what[plotnum][1],what[plotnum][2],what[plotnum][3],u,what[plotnum][4])
        # title, x_label, y_label, bin_count, input_data, filename
