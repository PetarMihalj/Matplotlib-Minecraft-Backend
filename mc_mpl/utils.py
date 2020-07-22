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

import mcpi.block

def rgb_to_wool_data(rgbface):
    if rgbface==None:
        r,g,b=(0,0,0)
    else:
        r,g,b,_=rgbface
    r*=256
    g*=256
    b*=256

    data=[(233,236,236,0),
    (240,118,19,1),
    (189,68,179,2),
    (58,175,217,3),
    (248,198,39,4),
    (112,185,25,5),
    (237,141,172,6),
    (62,68,71,7),
    (142,142,134,8),
    (21,137,145,9),
    (121,42,172,10),
    (53,57,157,11),
    (114,71,40,12),
    (84,109,27,13),
    (161,39,34,14),
    (20,21,25,15),
    ]
    closest = min(data,key=lambda x:abs(x[0]-r)+abs(x[1]-g)+abs(x[2]-b))
    return closest[3]

