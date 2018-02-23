import generate_heatmap as gh

def double_min_max(dataset1,dataset2):
    mm1 = gh.get_min_max(dataset1)
    mm2 = gh.get_min_max(dataset2)
    ou = dict()
    for v in ["xmin","ymin"]:
        if mm1[v]<mm2[v]:
            ou[v] = mm1[v]
        else:
            ou[v] = mm2[v]
    for v in ["xmax","ymax"]:
        if mm1[v]>mm2[v]:
            ou[v] = mm1[v]
        else:
            ou[v] = mm2[v]
    return ou

def make_grid(dataset1,dataset2,x_bin_count,y_bin_count):
    mm = double_min_max(dataset1,dataset2)
    ou = dict()
    ou["x"] = gh.make_axis(x_bin_count,mm["xmin"],mm["xmax"])
    ou["y"] = gh.make_axis(y_bin_count,mm["ymin"],mm["ymax"])
    ou["source"] = gh.put_points_in_bins(dataset1,x_bin_count,y_bin_count,mm)
    ou["back"] = gh.put_points_in_bins(dataset2,x_bin_count,y_bin_count,mm)
    return ou

def time_elimination_multiply(data_matrix,duration):
    for i in range(len(data_matrix)):
        for j in range(len(data_matrix[i])):
            data_matrix[i][j] = data_matrix[i][j]*(3600.0/duration)

def matrix_subtract(m1,m2):
    ou = []
    for i in range(len(m1)):
        k = []
        for j in range(len(m1[i])):
            k.append(m1[i][j]-m2[i][j])
        ou.append(k)
    return ou

def time_elimination(source_data,source_duration,background_data,background_duration,x_bin_count,y_bin_count):
    grid = make_grid(source_data,background_data,x_bin_count,y_bin_count)
    time_elimination_multiply(grid["source"],source_duration)
    time_elimination_multiply(grid["back"],background_duration)
    # both the source data and background data are now time normalized
    grid["sub"] = matrix_subtract(grid["source"],grid["back"])
    return grid

def function_subtraction_2D_normalize(matrix):
    total = 0.0
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            total += matrix[i][j]
    # now we apply this transformation
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = matrix[i][j] / total

def function_subtraction_2D_squeeze(source,back):
    squeeze_factor = 1.0
    for i in range(len(source)):
        for j in range(len(source[i])):
            if source[i][j]!=0 and back[i][j]!=0:
                y = back[i][j] / source[i][j]
                if y > squeeze_factor:
                    squeeze_factor = y
    return squeeze_factor

def function_subtraction_2D_subtract(source,back,squeeze_factor):
    ou = []
    for i in range(len(source)):
        k = []
        for j in range(len(source[i])):
            k.append(source[i][j] - (back[i][j] / squeeze_factor))
    return ou

def function_subtraction_2D(source_data,background_data,x_bin_count,y_bin_count):
    grid = make_grid(source_data,background_data,x_bin_count,y_bin_count)
    function_subtraction_2D_normalize(grid["source"])
    function_subtraction_2D_normalize(grid["back"])
    # data is normalized to 1
    squeeze_factor = function_subtraction_2D_squeeze(grid["source"],grid["back"])
    grid["sub"] = function_subtraction_2D_subtract(grid["source"],grid["back"],squeeze_factor)
    function_subtraction_2D_normalize(grid["sub"])
    return [grid,False] # eventually replace second return value with number thing
