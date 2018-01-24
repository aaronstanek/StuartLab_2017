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
