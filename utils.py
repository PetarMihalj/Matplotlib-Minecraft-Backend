"""
Adapted for python from https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
"""

def plotLineLow(x0,y0, x1,y1,f):
    dx = x1 - x0
    dy = y1 - y0
    yi = 1
    if dy < 0:
        yi = -1
        dy = -dy
    D = 2*dy - dx
    y = y0

    for x in range(x0,x1+1):
        f(x, y)
        if D > 0:
            y = y + yi
            D = D - 2*dx
        D = D + 2*dy

def plotLineHigh(x0,y0, x1,y1,f):
    dx = x1 - x0
    dy = y1 - y0
    xi = 1
    if dx < 0:
        xi = -1
        dx = -dx
    D = 2*dx - dy
    x = x0

    for y in range(y0,y1+1):
        f(x, y)
        if D > 0:
            x = x + xi
            D = D - 2*dy
        D = D + 2*dx

def plotLine(x0,y0, x1,y1, f):
    if abs(y1 - y0) < abs(x1 - x0):
        if x0 > x1:
            plotLineLow(x1, y1, x0, y0, f)
        else:
            plotLineLow(x0, y0, x1, y1, f)
    else:
        if y0 > y1:
            plotLineHigh(x1, y1, x0, y0, f)
        else:
            plotLineHigh(x0, y0, x1, y1, f)