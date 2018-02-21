def remove_above(raw,limit):
    ou = []
    for x in raw:
        if x<=limit:
            ou.append(x)
    return ou

def remove_below(raw,limit):
    ou = []
    for x in raw:
        if x>=limit:
            ou.append(x)
    return ou

# the next two functions implement cuts for the case that we have data in more than one dimension

def remove_above_MD(raw,limit,index):
    ou = []
    for x in raw:
        if x[index]<=limit:
            ou.append(x)
    return ou

def remove_below_MD(raw,limit,index):
    ou = []
    for x in raw:
        if x[index]>=limit:
            ou.append(x)
    return ou
