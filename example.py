# this file is intended to show the usage of this software

# Section 1: Making Histograms

# to make a histogram from your data you will first want to get access to the plotting functions
# these are located in histograms_from_folder.py
# to do this, put the following line at the top of your file

from histograms_from_folder import histograms_from_folder

# this will give you access to the function which makes the plots
# to make a histogram you will want to use a line of the pattern:

plot_info = {
                1:[title,x_label,y_label,bin_count,filename],
                2:[title,x_label,y_label,bin_count,filename],
                3:[title,x_label,y_label,bin_count,filename],
                4:[title,x_label,y_label,bin_count,filename]
                }
histograms_from_folder(folder_path,plot_info)

# here title, x_label, y_label, filename, folder_path are all strings
# bin_count is an integer
# and plot_info is a dictionary, but that's not particularly important

# plot_info tells the function what plots to make and how to make them
# the keys refer to channels, and the list associated with that key is information about
# the plot that will be derived from that channel
# you only need to include those channels that you want to plot
# e.g. 3:[title,x_label,y_label,bin_count,filename]
#       The plot for channel three will have the title, x_label, y_label, and bin_count here
#       the plot will be saved at filename

# let's say that I just took some data on channels 2 and 3, I might want to write something like the following
# (where the data is in ~/Desktop/my_data_folder)
plot_info = {
                2:["Channel 2 Histogram","Channel 2 Energy","Hit Count",75,"~/Desktop/chan2.png"],
                3:["Channel 3 Histogram","Channel 3 Energy","Hit Count",75,"~/Desktop/chan3.png"]
                }
histograms_from_folder("~/Desktop/my_data_folder",plot_info)

# Section 2: Histogram Options

# The software tries to make best guess of what you want, but unfortunately it isn't psychic
# sometimes you will have to give it a bit more information

# histograms_from_folder has three options
#   remove_above
#   remove_below
#   energy_calibration

# they do what they sound like they do
# remove_above will remove any datapoints above a threshold from your plot
# remove_below will remove any datapoints below a threshold from your plot
# energy_calibration will multiply all of your data values by a particular value

# consider:
histograms_from_folder("~/Desktop/my_data_folder",plot_info,remove_below=0,energy_calibration=7.44)

# this will plot the data from ~/Desktop/my_data_folder according to plot_info
# AND it will remove all datapoints that fall below zero, and multiply the observed energy of the remaining datapoints by 7.44

# Section 3: Eliinating the Background

from histograms_from_folder import histograms_eliminating_background

plot_info = {
                1:[title,x_label,y_label,bin_count,filename],
                2:[title,x_label,y_label,bin_count,filename],
                3:[title,x_label,y_label,bin_count,filename],
                4:[title,x_label,y_label,bin_count,filename]
                }
histograms_eliminating_background(source_folder_path,background_folder_path,plot_info)

# source_folder is a directory path where the data for the run with the source is stored
# background_folder is a directory path where the data fir the run without the source is stored
# plot_info follows the same rules as in Section 1

# options

# all the options that are valid for histograms_from_folder are also valid for histograms_eliminating_background and have the same effects
# plus there are additional options for histograms_eliminating_background

# because the source of the data is uncertain, we must include multiple methods for removing the background
# if your detector can record events as fast as they occur, do not mess with this option
# the software will use the timestamps in the data to determine the hit rate, and use this to subtract the background, this is a very accurate method
# if your detector records events substantially slower than they occur, we cannot use default option here
# using the default option on data that came from a slow detector would cause the software to believe that the signal and noise have equal frequency
# the work around is to use linear algebra to get a good enough estimate of the background
# to use this option, elim_type="function"

# so, if your detector is slow compared to the hit rate, you should use:
histograms_eliminating_background(source_folder_path,background_folder_path,plot_info,elim_type="function")

# if you use the default option, the vertical axis of your plot will show hits per hour
# if you use elim_type="function", the vertical axis of your plot will show a probability density
# if you want a hit count instead of a probability density, use the option use_count=True
histograms_eliminating_background(source_folder_path,background_folder_path,plot_info,elim_type="function",use_count=True)

# beware, using the default background elimination method and use_count=True has undefined behavior
histograms_eliminating_background(source_folder_path,background_folder_path,plot_info,use_count=True) # DO NOT USE THIS LINE

# Section 4: Plotting in 2D

from heatmaps_from_folder import heatmaps_from_folder

plot_info = {
            1:{
                2:[title,x_label,y_label,x_bin_count,y_bin_count,filename],
                4:[title,x_label,y_label,x_bin_count,y_bin_count,filename]
                }
            3:{
                4:[title,x_label,y_label,x_bin_count,y_bin_count,filename]
                }
            }

heatmaps_from_folder(folder_path,plot_info)

# title, x_label, y_label, filename, and folder_path are strings and work identically to their counterparts in Section 1
# x_bin_count and y_bin_count are integers and set the number of bins to use on the x and y axes respectively
# you will notice the plot_info here has a different format than in the previous sections
# this is because we need to mark two channels to be plotted and the order in which to plot them
# earlier plot_info had the form dict(int->list)
# now it has the form dict(int->dict(int->list))
# the example above will make three plots
# the first has channel 1 data on the x axis and channel 2 data on the second axis
# the second has channel 1 data on the x axis and channel 4 data on the second axis
# the third has channel 3 data on the x axis and channel 4 data on the second axis

# an example might look like:

plot_info = {
            1:{
                2:["Channel 1 and Channel 2","Channel 1 Energy","Channel 2 Energy",75,75,"~/Desktop/1-2.png"],
                4:["Channel 1 and Channel 4","Channel 1 Energy","Channel 4 Energy",75,75,"~/Desktop/1-4.png"]
                }
            3:{
                4:["Channel 3 and Channel 4","Channel 3 Energy","Channel 4 Energy",75,75,"~/Desktop/3-4.png"]
                }
            }

heatmaps_from_folder("~/Desktop/my_data_folder",plot_info)

# Options

# remove_above_x
# remove_below_x
# remove_above_y
# remove_below_y
# energy_calibration_x
# energy_calibration_y

# see Section 2
# those that end with _x modify the first channel provided
# those that end with _y modify the second channel provided
