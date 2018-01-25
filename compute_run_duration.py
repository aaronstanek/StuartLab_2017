import time

def parse_time_string(s):
    t = time.strptime(s,"%Y %m %d %H %M %S") # format is fixed and dictated by encoding .ord.json encoding
    return t

def compute_run_duration(event_list):
    first = parse_time_string(event_list[0]["EV_META"]["TIME"]) # assumes at least one event
    last = parse_time_string(event_list[-1]["EV_META"]["TIME"])
    delta = time.mktime(last) - time.mktime(first) # this converts datatype and then subtracts
    return delta
