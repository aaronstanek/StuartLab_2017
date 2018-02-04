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

def normalize_bins(bin_array):
    # takes a list of bins and sets their sum to 1
    # bin_array is a list of floats
    # returns list of floats of same length
    if len(bin_array)==0:
        return []
    s = 0.0
    for i in range(len(bin_array)):
        s += float(bin_array[i])
    ou = []
    for i in range(len(bin_array)):
        ou.append(bin_array[i] / s) # be careful, we could have issues here
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

def function_subtraction(full_data,background_data,bin_count):
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
    bin_delta = (data_max-data_min) / float(bin_count)
    full_bins = data_to_bins(full_data,data_min,bin_delta,bin_count)
    background_bins = data_to_bins(background_data,data_min,bin_delta,bin_count)
    # now we want to normalize our distributions, this allows for direct subtraction
    full_bins = normalize_bins(full_bins)
    background_bins = normalize_bins(background_bins)
    squeeze_factor = 1.0 # this is how much we need to shrink the background function to fit inside the full function
    for i in range(bin_count):
        if (full_bins[i]!=0) and (background_bins[i]!=0):
            y = float(background_bins[i]) / float(full_bins[i])
            if y > squeeze_factor:
                squeeze_factor = y
            del(y)
    # squeeze_factor is now determined
    alpha_bins = [] # this is where we are going to save the source only function (estimated)
    for i in range(bin_count):
        alpha_bins.append(full_bins[i] - (background_bins[i] / squeeze_factor))
        # this squeezes the background_data so it is always less than the full
        # then we subtract background from full to get an estimate of the source contribution
    # now normalize alpha
    alpha_bins = normalize_bins(alpha_bins)
    p = 1.0 - (1.0 / squeeze_factor) # this should give the source's contribution to the full
    diff_bins = dict()
    for i in range(bin_count):
        diff_bins[(float(i)+0.5)*bin_delta+data_min] = alpha_bins[i]
        # energy -> rate
    return [diff_bins,p]
