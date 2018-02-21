from get_files_in_folder import *
from read_json_ord_clump import *
from integrate_json_ord_clump import *
from generate_histogram import *
from slice_data import *
from compute_run_duration import *
from background_elimination import *

def histograms_from_folder(folder_path,what,**options):
    # folderpath is a strings
    # what is a dict (integer->list(string))
    # it maps channel numbers to [title,x_label,y_label,bin_count,filename]
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
    for plotnum in what:
        u = [] # take all the integration sums for a particular channel, and put them in this list
        for f in integrated:
            u.append(f[plotnum])
        # u now has all the integration sums for the channel plotnum
        # we might need to do some cuts
        if "remove_below" in options:
            u = remove_below(u,options["remove_below"])
        if "remove_above" in options:
            u = remove_above(u,options["remove_above"])
        if "nonneg" in options:
            if options["nonneg"]==True:
                u = remove_below(u,0.0) # this remove all negative datapoints
        if "energy_calibration" in options:
            for i in range(len(u)):
                u[i] = u[i]*options["energy_calibration"]
        # now plot it
        generate_histogram(what[plotnum][0],what[plotnum][1],what[plotnum][2],what[plotnum][3],u,what[plotnum][4])
        # title, x_label, y_label, bin_count, input_data, filename

def histograms_eliminating_background(data_folder_path,background_folder_path,what,**options):
    # see above for argument information
    # determine elimination type
    elim_type = "time"
    if options["elim_type"] == "function":
        elim_type = "function"
    j = [] # j will be a list of lists of events
    dur = [] # this will hold run durations, floats
    event_counts = []
    for x in [data_folder_path,background_folder_path]:
        file_list = get_files_in_folder(x)
        t = 0.0
        event_list = []
        for f in file_list:
            [ev,t] = read_json_ord_clump_basic(f)
            event_list = event_list + ev
            del(ev)
        dur.append(compute_run_duration(event_list))
        j.append(integrate_json_ord_clump(event_list,t))
        event_counts.append(len(event_list))
    del(file_list)
    del(event_list)
    del(t)
    for plotnum in what:
        u = [] # integration sums for data
        v = [] # integration sums for background
        if "remove_below" in options:
            u = remove_below(u,options["remove_below"])
            v = remove_below(v,options["remove_below"])
        if "remove_above" in options:
            u = remove_above(u,options["remove_above"])
            v = remove_above(v,options["remove_above"])
        for x in j[0]:
            u.append(x[plotnum])
        for x in j[1]:
            v.append(x[plotnum])
        if elim_type=="time":
            be = background_elimination(u,dur[0],v,dur[1],what[plotnum][3]) # that last argument is the number of bins
        elif elim_type=="function":
            [be,nope] = function_subtraction(u,v,what[plotnum][3])
        else:
            raise "Unknown elim_type"
        if "use_count" in options:
            if options["use_count"]==True:
                be_temp = be.items()
                be = dict()
                for x in be_temp:
                    be[x[0]] = x[1]*event_counts[0] # multiply the portion by the number of events in the data run
                del(be_temp)
        if "energy_calibration" in options:
            be_temp = be.items()
            be = dict()
            for x in be_temp:
                be[x[0]*options["energy_calibration"]] = x[1] # we change the key by some constant factor, can be used to calibrate energy levels
            del(be_temp)
        generate_bargraph(what[plotnum][0],what[plotnum][1],what[plotnum][2],be,what[plotnum][4])
