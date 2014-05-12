import math

def is_numeric(x):
    try:
        for i in x:
            float(i)
        return True
    except:
        return False

def mean(x):
    if is_numeric(x):
        return sum(x) * 1.0 / len(x)

def variance(alist):
    if is_numeric(alist):
        m = mean(alist)
        return map(lambda x: (x - m)**2, alist)

def stdev(alist):
    if is_numeric(alist):
        return math.sqrt(mean(variance(alist)))
