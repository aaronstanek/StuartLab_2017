from get_files_in_folder import *
from read_json_ord_clump import *
from integrate_json_ord_clump import *
from generate_heatmap_2 import *
from slice_data import *
from compute_run_duration import *
from background_elimination import *

def heatmaps_from_folder(folder_path,what,**options):
    # folderpath is a strings
    # what is a dict integer -> dict(integer->list(string))
    # the first interger is the first channel, the second integer is the second channel
    # it maps channel numbers to [title,x_label,y_label,x_bin_count,y_bin_count,filename]
    # what dictates details of the plot to be generated for that channel
    # filename is the full path where the plot will be save (prefer ending in .png)
    # this function takes the data from a folder and plots it
    # present options nonneg = True, cuts all negative data points
    file_list = get_files_in_folder(folder_path)
    t = 0.0
    event_list = []
    for f in file_list:
        [ev,t] = read_json_ord_clump_basic(f) # you better hope that they all have the same delta t
        event_list = event_list + ev
        del(ev)
    del(file_list) # just to be nice
    integrated = integrate_json_ord_clump(event_list,t)
    del(event_list)
    del(t)
    for plotnum1 in what:
        for plotnum2 in what[plotnum1]:
            u = []
            for f in integrated:
                u.append([f[plotnum1],f[plotnum2]])
            # u is now a list of all the datapoints that we care about
            # we might want to do some cuts on this
            if "remove_below_x" in options:
                u = remove_below_MD(u,options["remove_below_x"],0)
            if "remove_above_x" in options:
                u = remove_above_MD(u,options["remove_above_x"],0)
            if "remove_below_y" in options:
                u = remove_below_MD(u,options["remove_below_y"],1)
            if "remove_above_y" in options:
                u = remove_above_MD(u,options["remove_above_y"],1)
            k = what[plotnum1][plotnum2]
            generate_heatmap(k[0],k[1],k[2],k[3],k[4],u,k[5])
            del(k)
