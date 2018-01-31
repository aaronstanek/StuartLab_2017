def data_to_bins(raw,data_min,bin_delta,bin_count):
    # raw is a list of floats
    # data_min is a float
    # bin_delta is a float
    # bin_count is an integer
    # this function puts data into the correct bins
    ou = []
    for i in range(bin_count):
        ou.append(0)
    for r in raw:
        b = int((r - data_min) / bin_delta)
        if b>=bin_count: # the largest data point will be in a bin larger than what we can handle, so we move it one down
            b = bin_count-1
        ou[b] = ou[b] + 1 # this increments that bin
    return ou

def background_elimination(full_data,full_duration,background_data,background_duration,bin_count):
    # fulldata and background_data are lists of floats
    # bin_count is a integer
    # fulldata and background_data should be lists of integral sums for the same channel
    # first is to decide the bounds and size of the bins
    # full_duration and background_duration are floats representing seconds
    # returns a dict(float->float), that maps energies to rates (hits per hour, accounting for background)
    f_max = max(full_data)
    b_max = max(background_data)
    f_min = min(full_data)
    b_min = min(background_data)
    if f_max>b_max:
        data_max = f_max
    else:
        data_max = b_max
    if f_min<b_min:
        data_min = f_min
    else:
        data_min = b_min
    del(f_max)
    del(b_max)
    del(f_min)
    del(b_min)
    # now data_max and data_min give us the bounds on the data
    bin_delta = (data_max-data_min) / float(bin_count)
    # bin_delta is now the width of each bin
    full_bins = data_to_bins(full_data,data_min,bin_delta,bin_count)
    background_bins = data_to_bins(background_data,data_min,bin_delta,bin_count)
    # now we need to correct for time
    # determine rate per hour
    for i in range(bin_count):
        full_bins[i] = full_bins[i]*(3600.0/full_duration)
        background_bins[i] = background_bins[i]*(3600.0/background_duration)
    # now deterine difference in rates to find how many true events per hour happened
    diff_bins = dict()
    for i in range(bin_count):
        diff_bins[(float(i)+0.5)*bin_delta+data_min] = full_bins[i]-background_bins[i]
        # energy -> rate
    return diff_bins
