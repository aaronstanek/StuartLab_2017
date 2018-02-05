import math

def nice_float_string(n,s):
    # n is a float, input number
    # s is an int, significant digits
    # this function takes a floating point number, and returns a nicely formatted string
    # of that number, with the desired number of significant digits
    # note: this method truncates, it does not round
    m = int(math.log10(n)) # this gives the order of the most significant digit
    y = [] # y is an array of chars, it holds the number we are going to output
    for i in range(s):
        div = float(10**(m-i))
        v = int(n / div) % 10
        y.append(v)
    ou = ""
    for i in range(len(y)):
        ou = ou + str(y[i])
        if i==0:
            ou = ou + "."
    ou = ou + "e" + str(m)
    return ou
