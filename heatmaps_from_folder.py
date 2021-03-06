from get_files_in_folder import *
from read_json_ord_clump import *
from integrate_json_ord_clump import *
from generate_heatmap_2 import *
from slice_data import *
from compute_run_duration import *
from background_elimination_2D import *

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
            if "energy_calibration_x" in options:
                for i in range(len(u)):
                    u[i][0] = u[i][0]*options["energy_calibration_x"]
            if "energy_calibration_y" in options:
                for i in range(len(u)):
                    u[i][1] = u[i][1]*options["energy_calibration_y"]
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

def heatmaps_eliminating_background(data_folder_path,background_folder_path,what,**options):
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
    for plotnum1 in what:
        for plotnum2 in what[plotnum1]:
            u = [] # source data
            v = [] # background data
            for i in range(len(j[0])):
                u.append([j[0][i][plotnum1],j[0][i][plotnum2]])
            for i in range(len(j[1])):
                v.append([j[1][i][plotnum1],j[1][i][plotnum2]])
            if "energy_calibration_x" in options:
                for i in range(len(u)):
                    u[i][0] = u[i][0]*options["energy_calibration_x"]
                for i in range(len(v)):
                    v[i][0] = v[i][0]*options["energy_calibration_x"]
            if "energy_calibration_y" in options:
                for i in range(len(u)):
                    u[i][1] = u[i][1]*options["energy_calibration_y"]
                for i in range(len(v)):
                    v[i][1] = v[i][1]*options["energy_calibration_y"]
            if "remove_below_x" in options:
                u = remove_below_MD(u,options["remove_below_x"],0)
                v = remove_below_MD(v,options["remove_below_x"],0)
            if "remove_above_x" in options:
                u = remove_above_MD(u,options["remove_above_x"],0)
                v = remove_above_MD(v,options["remove_above_x"],0)
            if "remove_below_y" in options:
                u = remove_below_MD(u,options["remove_below_y"],1)
                v = remove_below_MD(v,options["remove_below_y"],1)
            if "remove_above_y" in options:
                u = remove_above_MD(u,options["remove_above_y"],1)
                v = remove_above_MD(v,options["remove_above_y"],1)
            # now we start the fun stuff
            if elim_type=="time":
                be = time_elimination(u,dur[0],v,dur[1],what[plotnum1][plotnum2][3],what[plotnum1][plotnum2][4])
            elif elim_type=="function":
                [be,nope] = function_subtraction_2D(u,v,x_bin_count,y_bin_count)
            else:
                raise "Unknown elim_type"
            if "use_count" in options:
                if options["use_count"]==True:
                    for i in range(len(be["sub"])):
                        for j in range(len(be["sub"][i])):
                            be["sub"][i][j] = be["sub"][i][j] * event_counts[0]
            pli = what[plotnum1][plotnum2]
            generate_heatmap_auto(pli[0],pli[1],pli[2],be,pli[5])
