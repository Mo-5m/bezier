import pygame as pg 
import bezier
from math import sqrt
from random import randint

pg.init()
WIN_SIZE = WIN_W, WIN_H = 700, 700
screen = pg.display.set_mode(WIN_SIZE)
# WIN_W, WIN_H = pg.display.get_window_size()

font = pg.font.SysFont('Arial', 20)

# point circle collision to detect if the mouse is above a point
def point_circle(point, center, radius):
    distx = point[0]-center[0]
    disty = point[1]-center[1]
    dist = sqrt(distx**2 + disty**2)
    if dist <= radius: 
        return True
    return False

# initial 
accuracy = 100
Points = [(randint(0, WIN_W), randint(0, WIN_H)) for _ in range(4)]
mode = "cubic"


controls = {
    # Is the mouse moving a point
    'mos moving': False,
    # Index of that point
    'mos point': 0,
    
    # Press a and input a number then press enter to change accuracy
    'a pressed': False,
    'new acc': ""
}

fps = 0
dt_list = [] # to find average fps

clock = pg.time.Clock()
running = True
while running: 
    # ---*--- Events ---*--- 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
                
            if controls['a pressed']: 
                n = ''.join(
                    filter(str.isdigit, pg.key.name(event.key))
                )
                controls['new acc'] += n
                
            if event.key == pg.K_a:
                controls['a pressed'] = True
                controls['new acc'] = ""
            if event.key == pg.K_RETURN: # RETURN is ENTER
                int_acc = int(controls['new acc'])
                accuracy = int_acc if controls['new acc'] and int_acc else 10
                controls['a pressed'] = False
            
            if event.key == pg.K_q:
                if mode != "quad":
                    Points.pop(2)
                    mode = 'quad'
            if event.key == pg.K_c:
                if mode != "cubic":
                    Points.append((randint(0, WIN_W), randint(0, WIN_H)))
                    mode = "cubic"
                
                
        # moving control points of curve
        if event.type == pg.MOUSEBUTTONDOWN:
            for i in range(len(Points)):
                if point_circle(pg.mouse.get_pos(), Points[i], 20):
                    controls['mos moving'] = True
                    controls['mos point'] = i
        if event.type == pg.MOUSEBUTTONUP:
            controls['mos moving'] = False
        # ---
        
    if controls['mos moving']: 
        mos_pos = pg.mouse.get_pos()
        
        # makee sure the new point place is within the screen
        if mos_pos[0] > WIN_SIZE[0]:
            mos_pos = WIN_SIZE[0], mos_pos[1]
        
        if mos_pos[1] > WIN_SIZE[1]:
            mos_pos = mos_pos[0], WIN_SIZE[1]
        
        Points[controls['mos point']] = mos_pos
    
    
    # Drawing ---*--- ---*---
    
    screen.fill((255,255,255))
    
    if mode == 'cubic':
        curve = bezier.cubic(*Points, accuracy)
        offset = bezier.cubic_offset(*Points, accuracy, -20)
    else: # mode == 'quad'
        curve = bezier.quadratic(*Points, accuracy)
        
        offset = bezier.quad_offset(*Points, accuracy, -20)

    
    # Curve
    pg.draw.lines(screen, (0,0,0), 0, curve, 3)
    
    # lines between control points
    if mode == "cubic":
        pg.draw.line(screen, (0,0,0), Points[0], Points[1])
        pg.draw.line(screen, (0,0,0), Points[2], Points[3])
        
    # offset 
    pg.draw.lines(screen, (0,0,255), 0, offset)
    # Bounding Box 
    if mode == "cubic":
        pg.draw.lines(screen, (255,0,0), 1, bezier.cubic_boundbox_verts(*Points))
    else: # mode == "quad"
        pg.draw.lines(screen, (255,0,0), 1, bezier.quad_boundbox_verts(*Points))
    
    # Points
    for point in Points:
        pg.draw.circle(screen, (0,255,0), point, 8) # radius = 5
        
    # extrema 
    if mode == "cubic":
        for point in bezier.cubic_extrema(*Points):
            pg.draw.circle(screen, (255,0,0), point, 5) # radius = 5
    else: # mode == "quad"
        for point in bezier.quad_extrema(*Points):
            pg.draw.circle(screen, (255,0,0), point, 5)
            
  
    # curvuture in the middle
    if mode == "cubic":
        midp = midx, midy = bezier.cuberp(*Points, 0.5)
        dx, dy = bezier.cuberp_dt(*Points, 0.5)
        curvature = bezier.cuberp_curvature(*Points, 0.5)
    
    else: # mode == "quad"
        midp = midx, midy = bezier.querp(*Points, 0.5)
        dx, dy = bezier.querp_dt(*Points, 0.5)
        curvature = bezier.querp_curvature(*Points, 0.5)
    

    normx, normy = -dy, dx
    mag = sqrt(dx**2 + dy**2)
    
    if mag != 0:
        normx, normy = normx/mag, normy/mag
    
    if curvature != 0:
        radius = 1/curvature
    else: radius = float('inf')
    
    offx, offy = normx*radius, normy*radius
    center = midx + offx, midy + offy
    
    pg.draw.circle(screen, (80,80,0), midp, 4) 
    pg.draw.circle(screen, (0,80,80), center, abs(radius), 2)
        
    # info
    screen.blit(font.render(f'accuracy: {accuracy}', 1, (0,0,0)), (50, 50))
    screen.blit(font.render(f'fps: {fps:.1f}', 1, (0,0,0)), (50, 70))
    
    
    pg.display.update()
    
    # average fps calculation
    dt_list.append(clock.tick())
    if len(dt_list) == 10:
        fps = 10_000/sum(dt_list) # values are in ms so x1000 and x10 to get average 
        dt_list = []