from math import sqrt

def solve_quadratic(a, b, c):
    if a == 0: # not a quadratic
        if b != 0:
            return (-c/b,)
    
    elif (disc:= b**2 - 4*a*c) >= 0: # it doesnt have real roots
        return ((-b+sqrt(disc))/(2*a), 
                (-b-sqrt(disc))/(2*a))
    
    return tuple()



def lerp_1d(P0, P1, t):
    """linear interpolation"""
    return (1-t)*P0 + t*P1
    # (1-t)P₀ + tP₁

def lerp(P0, P1, t):
    return (lerp_1d(P0[0], P1[0], t), 
            lerp_1d(P0[1], P1[1], t))


def querp_1d(P0, P1, P2, t):
    """quadratic interpolation"""
    return (1-t)**2*P0 + 2*t*(1-t)*P1 + t**2*P2
    # (1-t)²P₀ + 2t(1-t)P₁ + t²P₂

def querp(P0, P1, P2, t):
    return (querp_1d(P0[0], P1[0], P2[0], t), 
            querp_1d(P0[1], P1[1], P2[1], t))


def cuberp_1d(P0, P1, P2, P3, t):
    """cubic interpolation"""
    A = (1-t)
    return A**3*P0 + 3*t*A**2*P1 + 3*t**2*A*P2 + t**3*P3
    # (1-t)³P₀ + 3t(1-t)²P₁ + 3t²(1-t)P₂ + t³P₃

def cuberp(P0, P1, P2, P3, t):   
    return (cuberp_1d(P0[0], P1[0], P2[0], P3[0], t), 
            cuberp_1d(P0[1], P1[1], P2[1], P3[1], t))



 
def querp_1d_dt(P0, P1, P2, t):
    return -2*P0*(1-t) + 2*P1*(1-2*t) + 2*P2*t
    # -2P₀(1-t) + 2P₁(1-2t) + 2P₂t

def querp_dt(P0, P1, P2, t):
    return (querp_1d_dt(P0[0], P1[0], P2[0], t), 
            querp_1d_dt(P0[1], P1[1], P2[1], t))

def querp_1d_dt2(P0, P1, P2, t):
    """this doesnt depend on t, its constant"""
    return 2*(P2 - 2*P1 + P0)

def querp_dt2(P0, P1, P2, t):
    return (querp_1d_dt2(P0[0], P1[0], P2[0], t), 
            querp_1d_dt2(P0[1], P1[1], P2[1], t))

def cuberp_1d_dt(P0, P1, P2, P3, t):
    return 3*(1-t)**2*(P1 - P0) + 6*(1-t)*t*(P2 - P1) + 3*t**2*(P3 - P2)
    # 3(1-t)²(P₁ - P₀) + 6t(1-t)(P₂ - P₁) + 3t²(P₃ - P₂)

def cuberp_dt(P0, P1, P2, P3, t):   
    return (cuberp_1d_dt(P0[0], P1[0], P2[0], P3[0], t), 
            cuberp_1d_dt(P0[1], P1[1], P2[1], P3[1], t))

def cuberp_1d_dt2(P0, P1, P2, P3, t):
    return 6*(1 - t)*(P2 - 2*P1 + P0) + 6*t*(P3 - 2*P2 + P1)

def cuberp_dt2(P0, P1, P2, P3, t):   
    return (cuberp_1d_dt2(P0[0], P1[0], P2[0], P3[0], t), 
            cuberp_1d_dt2(P0[1], P1[1], P2[1], P3[1], t))

def querp_curvature(P0, P1, P2, t, inCaseDivByZero=float('inf')):

    xp ,  yp = querp_dt(P0, P1, P2, t)
    xpp, ypp = querp_dt2(P0, P1, P2, t)
    
    num = xp*ypp - xpp*yp
    dem = sqrt(xp**2 + yp**2)**3
    
    if dem == 0:
        return inCaseDivByZero
    
    return num/dem

def cuberp_curvature(P0, P1, P2, P3, t, inCaseDivByZero=float('inf')):
    """
                 x'y'' - x''y'
        k(t) = ------------------
                  _________ 3
                 % x'² + y'²
    """
    xp ,  yp = cuberp_dt(P0, P1, P2, P3, t)
    xpp, ypp = cuberp_dt2(P0, P1, P2, P3, t)
    
    num = xp*ypp - xpp*yp
    dem = sqrt(xp**2 + yp**2)**3
    
    if dem == 0:
        return inCaseDivByZero
        
    return num/dem


def querp_offset(P0, P1, P2, t, dist):
    initx, inity = querp(P0, P1, P2, t) 
    dx, dy = querp_dt(P0, P1, P2, t)
    
    normx, normy = -dy, dx
    mag = sqrt(dx**2 + dy**2)
    if mag != 0:
        normx, normy = normx/mag, normy/mag
    
    return initx + dist*normx, inity + dist*normy

def quad_extrema(P0, P1, P2):
    # -2P₀(1-t) + 2P₁(1-2t) + 2P₂t = 0
    # (2P₀ - 4P₁ + 2P₂)t - 2P₀ + 2P₁ = 0
    # t = (2P₀ - 2P₁) / (-2P₀ + 4P₁ + 2P₂)
    
    coors = tuple()
    
    if (dem := 2*P0[0] - 4*P1[0] + 2*P2[0]) != 0:
        x_root = (2*P0[0] - 2*P1[0]) / dem
        if 1 >= x_root >= 0:
            coors += (querp(P0, P1, P2, x_root), )
    
    
    if (dem := 2*P0[1] - 4*P1[1] + 2*P2[1]) != 0:
        y_root = (2*P0[1] - 2*P1[1]) / dem
        
        if 1 >= y_root >= 0:
            coors += (querp(P0, P1, P2, y_root), )
    
    
    return coors

def quad_boundbox(P0, P1, P2):
    """returns boundbox's topleft point, width, and height"""
    extrema = quad_extrema(P0, P1, P2)
    n = len(extrema)
    
    x_points = [P0[0], P2[0], *(extrema[i][0] for i in range(n))]
    y_points = [P0[1], P2[1], *(extrema[i][1] for i in range(n))]
    
    min_x, max_x = min(x_points), max(x_points)
    min_y, max_y = min(y_points), max(y_points) 

    return (max_x, max_y), (max_x-min_x, max_y-min_y)

def quad_boundbox_verts(P0, P1, P2):
    """returns boundbox vertecies in order"""
    extrema = quad_extrema(P0, P1, P2)
    n = len(extrema)
    
    x_points = [P0[0], P2[0], *(extrema[i][0] for i in range(n))]
    y_points = [P0[1], P2[1], *(extrema[i][1] for i in range(n))]
    
    min_x, max_x = min(x_points), max(x_points)
    min_y, max_y = min(y_points), max(y_points) 
    
    return ((min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y))    



def cuberp_offset(P0, P1, P2, P3, t, dist):
    initx, inity = cuberp(P0, P1, P2, P3, t) 
    dx, dy = cuberp_dt(P0, P1, P2, P3, t) # this is the tangent vector
    
    normx, normy = -dy, dx
    mag = sqrt(dx**2 + dy**2) 
    if mag != 0:
        normx, normy = normx/mag, normy/mag
    
    return initx + dist*normx, inity + dist*normy

def cubic_extrema(P0, P1, P2, P3):
    """find the points where the x or y derivative is 0, requires arguments to be tuples"""

    # solving for x derivative roots
    ax = 3*(P3[0] - 3*P2[0] + 3*P1[0] - P0[0])
    bx = 6*(P2[0] - 2*P1[0] + P0[0])
    cx = 3*(P1[0] - P0[0])
    dx_roots = filter(lambda t: 1 >= t >= 0, solve_quadratic(ax, bx, cx))
    
    # y derivative roots
    ay = 3*(P3[1] - 3*P2[1] + 3*P1[1] - P0[1])
    by = 6*(P2[1] - 2*P1[1] + P0[1])
    cy = 3*(P1[1] - P0[1])
    dy_roots = filter(lambda t: 1 >= t >= 0, solve_quadratic(ay, by, cy))
    
    return tuple(
        map(lambda t: cuberp(P0, P1, P2, P3, t), tuple(dx_roots) + tuple(dy_roots))
    )
    
    
    # dxdt_roots = tuple() 
    # if ax == 0: # not a quadratic
    #     if bx != 0 and 1 >= (algebra_sol:= -cx/bx) >= 0:
    #         dxdt_roots += (algebra_sol,)
    # 
    # elif (discx:= bx**2 - 4*ax*cx) >= 0: # it doesnt have real roots
    #     if 1 >= (e:= (-bx+sqrt(discx))/(2*ax)) >= 0:
    #         dxdt_roots += (e,)
    #     if 1 >= (e:= (-bx-sqrt(discx))/(2*ax)) >= 0:
    #         dxdt_roots += (e,)


def cubic_boundbox(P0, P1, P2, P3):
    """returns boundbox's topleft point, width, and height"""
    
    extrema = cubic_extrema(P0, P1, P2, P3)
    n = len(extrema)
    
    x_points = [P0[0], P3[0], *(extrema[i][0] for i in range(n))]
    y_points = [P0[1], P3[1], *(extrema[i][1] for i in range(n))]
    
    # x_points = [P0[0], P3[0], *cuberp1d_extrema(P0[0], P1[0], P2[0], P3[0])]
    # y_points = [P0[1], P3[1], *cuberp1d_extrema(P0[1], P1[1], P2[1], P3[1])]

    min_x, max_x = min(x_points), max(x_points)
    min_y, max_y = min(y_points), max(y_points) 

    return (min_x, min_y), (max_x-min_x, max_y-min_y)

def cubic_boundbox_verts(P0, P1, P2, P3):
    """returns boundbox vertecies in order"""
    extrema = cubic_extrema(P0, P1, P2, P3)
    n = len(extrema)
    
    x_points = [P0[0], P3[0], *(extrema[i][0] for i in range(n))]
    y_points = [P0[1], P3[1], *(extrema[i][1] for i in range(n))]
    
    # x_points = [P0[0], P3[0], *cuberp1d_extrema(P0[0], P1[0], P2[0], P3[0])]
    # y_points = [P0[1], P3[1], *cuberp1d_extrema(P0[1], P1[1], P2[1], P3[1])]

    min_x, max_x = min(x_points), max(x_points)
    min_y, max_y = min(y_points), max(y_points) 
    
    return (min_x, min_y), (min_x, max_y), (max_x, max_y), (max_x, min_y)


def _range(num):
    """yeilds a specified number of values between 0 and 1 with uniform spacing"""
    space = 1/num
    for i in range(num+1):
        yield i*space

def quadratic(P0, P1, P2, accuracy):
    l = []
    for i in _range(accuracy):
        l.append(querp(P0, P1, P2, i))
    return l


def cubic(P0, P1, P2, P3, accuracy):
    l = []
    for i in _range(accuracy):
        l.append(cuberp(P0, P1, P2, P3, i))
    return l

def quad_offset(P0, P1, P2, accuracy, offset):
    l = []
    for i in _range(accuracy):
        l.append(querp_offset(P0, P1, P2, i, offset))
    return l

def cubic_offset(P0, P1, P2, P3, accuracy, offset):
    l = []
    for i in _range(accuracy):
        l.append(cuberp_offset(P0, P1, P2, P3, i, offset))
    return l
    