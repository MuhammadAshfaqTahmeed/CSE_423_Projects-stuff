#task1
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

window_width, window_height = 800, 800

sky_darkness = 0 # Bright sky start
darkness_step = 0.5 # change of brightness

drop_num = 40
drop_xy = [] # setting it global for constant change
fall_speed = 10
wind_offset = 0 # 0 = straight fall +ve = right slant -ve = left slant  
wind_step = 1 # adjust slant after key press


def start_rain():
    global drop_xy
    for i in range(drop_num):
        x = random.randint(0, window_width)
        y  = random.randint(0, window_height)
        drop_xy.append([x,y])

def arrowpress(key, x, y):
    global wind_offset   
    if key == GLUT_KEY_LEFT:    
        wind_offset -= wind_step
    elif key == GLUT_KEY_RIGHT:
        wind_offset += wind_step

def drawRain():
    
    if sky_darkness < 0.5: #Change drop color to Blue at day
        glColor3f(0.1, 0.1, 0.8)
    else: #change drop color to white at night
        glColor3f(0.9, 0.9, 0.9)
    
    glBegin(GL_LINES)
    for drop in drop_xy:
        x = drop[0]
        y = drop[1] 
        glVertex2f(x,y)
        glVertex2f(x + wind_offset, y - 10)
    glEnd()

def update_rain():
    global drop_xy
    for drops in drop_xy:
        drops[0] += wind_offset *0.1 # changes x for wind effect.
        drops[1] -= fall_speed # changes y to make drops fall vertical.
        
        if drops[1] < 0: # y coordinate out of viewport vertical range(0--800)
            drops[0] = random.randint(0, window_width)
            drops[1] = window_height 
    
    glutPostRedisplay()  
        
def change_sky(key, x, y):    
    '''pressing w will increase sky brightness(day) and s will decrease sky brightness(night)''' 
    global sky_darkness
    if key == b'w':
        sky_darkness = max(0, sky_darkness - darkness_step)   # Blue sky
    elif key == b's':
        sky_darkness = min(1, sky_darkness + darkness_step)   # Black sky
    
    glutPostRedisplay()  # recall display() when any change  happen

def setup_projection():
    glViewport(0, 0, window_width, window_height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, window_width, 0, window_height, 0, 1)
    glMatrixMode(GL_MODELVIEW)

def drawSky():
    r = 0.68 * (1 - sky_darkness)
    g = 0.85 * (1 - sky_darkness)
    b = 0.90 * (1 - sky_darkness) 
    glColor3f(r, g, b)
    
    glBegin(GL_QUADS)
    glVertex2f(790, 550)
    glVertex2f(790, 800)
    glVertex2f(10, 800)
    glVertex2f(10, 550)
    glEnd()

def drawGrass():
    glColor3f(0.2, 0.6, 0.1)          
    glBegin(GL_TRIANGLES)

    #LEFT SIDE GRASS (from x=10 toward house)
    x = 10
    while x < 250: # stop before house left wall (x=250)
        # Bottom-left, bottom-right, top-center
        glVertex2f(x,     300)
        glVertex2f(x + 30, 300)
        glVertex2f(x + 15, 330)      
        x += 25                       

    # RIGHT SIDE GRASS (from x=790 toward house) 
    x = 790
    while x > 550:                    # Stop before house right wall (x=550)
        glVertex2f(x,     300)
        glVertex2f(x - 30, 300)
        glVertex2f(x - 15, 330)
        x -= 25

    glEnd()

def drawLand():
    glColor3f(0.55, 0.35, 0.15)
    glBegin(GL_QUADS)
    glVertex2f(790, 0)
    glVertex2f(790, 550)
    glVertex2f(10, 550)
    glVertex2f(10, 0)
    glEnd()



def drawHouse():
    # Roof drawing
    glColor3f(0.6, 0.2, 0.2)  # Dark red/brown color
    glBegin(GL_TRIANGLES)
    glVertex2f(200, 450)  # Left point
    glVertex2f(600, 450)  # Right point
    glVertex2f(400, 580)  # Top point (center)
    glEnd()
        
    # House body
    glColor3f(0.8, 0.6, 0.4)  # Light brown color
    glBegin(GL_QUADS)
    glVertex2f(250, 200)  # Bottom-left
    glVertex2f(550, 200)  # Bottom-right
    glVertex2f(550, 450)  # Top-right
    glVertex2f(250, 450)  # Top-left
    glEnd()

    # Door drawing
    glColor3f(0.4, 0.2, 0.1)  # Dark brown color
    glBegin(GL_QUADS)
    glVertex2f(350, 200)  # Bottom-left
    glVertex2f(450, 200)  # Bottom-right
    glVertex2f(450, 350)  # Top-right
    glVertex2f(350, 350)  # Top-left
    glEnd()
    
    # Door knob
    glColor3f(0.9, 0.8, 0.3)  # Golden color
    glPointSize(10)  
    glBegin(GL_POINTS)
    glVertex2f(430, 275)  # Position of the door knob
    glEnd()
    
    # Left window
    glColor3f(0.6, 0.8, 0.9)  # Light blue color
    glBegin(GL_QUADS)
    glVertex2f(270, 350)  # Bottom-left
    glVertex2f(330, 350)  # Bottom-right
    glVertex2f(330, 410)  # Top-right
    glVertex2f(270, 410)  # Top-left
    glEnd()
    
    # Left window frame 
    glColor3f(0.3, 0.3, 0.3)  # Dark gray
    glLineWidth(3)
    glBegin(GL_LINES)
    # Vertical line
    glVertex2f(300, 350)
    glVertex2f(300, 410)
    # Horizontal line
    glVertex2f(270, 380)
    glVertex2f(330, 380)
    glEnd()
    
    # Right window
    glColor3f(0.6, 0.8, 0.9)  # Light blue color
    glBegin(GL_QUADS)
    glVertex2f(470, 350)  # Bottom-left
    glVertex2f(530, 350)  # Bottom-right
    glVertex2f(530, 410)  # Top-right
    glVertex2f(470, 410)  # Top-left
    glEnd()
    
    # Right window frame 
    glColor3f(0.3, 0.3, 0.3)  # Dark gray
    glLineWidth(3)
    glBegin(GL_LINES)
    # Vertical line
    glVertex2f(500, 350)
    glVertex2f(500, 410)
    # Horizontal line
    glVertex2f(470, 380)
    glVertex2f(530, 380)
    glEnd()
    

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT) # Clears screen and depth buffer after each change.
    glLoadIdentity()
    setup_projection()

    drawSky()
    drawLand() 
    drawGrass()
    drawHouse() 
    drawRain()

    glutSwapBuffers()


def main():
    glutInit()                               # Initialize GLUT
    glutInitDisplayMode(GLUT_RGBA)           # Set display mode: RGBA color
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"task1")               
    start_rain() # initializes rain drawing
    
    glutDisplayFunc(display)
    glutIdleFunc(update_rain) # for the rain animation change after key press
    glutKeyboardFunc(change_sky)  # this listens w and s keys
    glutSpecialFunc(arrowpress) # this litstens to <---, ---> key
    
    glutMainLoop()                           

if __name__ == "__main__":
    main()

#task2
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random

window_width, window_height = 500, 500

points = []
inc_speed = 1.0
freez = False
blink_active = False
blink_frame_count = 0
blink_frames = 60

def makepoint(x,y):
    colr = (random.random(), random.random(), random.random())
    dx = random.choice([-1.0,1.0]) # change in x direction(-1 to 1)
    dy = random.choice([-1.0,1.0]) # change in y direction
    length =math.sqrt(dx*dx + dy*dy)
    speed = 2
    vx = (dx/length)*speed #speed change in x direction
    vy = (dy/length)*speed # speed change in y direction
    
    return {
        'x': x,'y': y,
        'r': colr[0], 'g': colr[1], 'b':colr[2],
        'vx': vx, 'vy': vy,
        'blink': 0
    }
def update_blink():
    global blink_frame_count
    blink_frame_count += 1
    if blink_frame_count >= blink_frames:
        blink_frame_count = 0
        for point in points:
            point['blink'] = 1 - point['blink']   
def move_points():
    for point in points:
        if blink_active and point['blink'] == 1:
             continue
        new_x = point['x'] + point['vx'] * inc_speed
        new_y = point['y'] + point["vy"] * inc_speed
        
        if new_x <= 0 or new_x >= window_width:
            point['vx'] = -point['vx']
            new_x = max(0, min(window_width, new_x))
        
        if new_y <= 0 or new_y >= window_height:
            point['vy'] = -point['vy']
            new_y = max(0, min(window_height, new_y))
        point['x'], point['y'] = new_x, new_y
def display():
   glClear(GL_COLOR_BUFFER_BIT)
   glMatrixMode(GL_PROJECTION)
   glLoadIdentity()
   glOrtho(0, window_width, 0, window_height, 0, 1)
   glMatrixMode(GL_MODELVIEW)
   glLoadIdentity()
   glPointSize(6)
   
   glBegin(GL_POINTS)
   for point in points:
        if blink_active and point['blink'] ==1:
                continue
        glColor3f(point['r'], point['g'], point['b'])
        glVertex2f(point['x'], point['y'])
   glEnd()
   glutSwapBuffers()

def animate():
    global freez
    if freez:
        glutPostRedisplay()
        return
    if blink_active:
        update_blink()
    move_points()
    glutPostRedisplay()

def special_key(key, x, y):
    global inc_speed
    if key == GLUT_KEY_UP:
        inc_speed = min(inc_speed*1.5, 50)
    elif key == GLUT_KEY_DOWN:
        inc_speed = max(inc_speed/1.5, 0.05)
    glutPostRedisplay()

def mouse_click(button, state, mx, my):
    global blink_active, blink_frame_count
    if state != GLUT_DOWN:
        return
    
    my =window_height - my
    
    if button == GLUT_RIGHT_BUTTON:
        points.append(makepoint(mx,my))
    
    elif button == GLUT_LEFT_BUTTON:
        blink_active = not blink_active
        if blink_active:
            blink_frame_count = 0
            for point in points:
                point['blink'] = 0
        else:
            for point in points:
                point['blink'] = 0
    glutPostRedisplay()

def Keybrd_space(key,x,y):
    global freez
    if key == b' ': 
        freez = not freez
    glutPostRedisplay()
        
def main():
    glutInit()
    glutInitDisplayMode(GLUT_RGBA)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(0,0)
    glutCreateWindow(b"Task2")
    
    glClearColor(0.0,0.0,0.0,1.0) # to keep the bacground black
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutMouseFunc(mouse_click)
    glutKeyboardFunc(Keybrd_space)
    glutSpecialFunc(special_key)
    
    glutMainLoop()

if __name__ == "__main__":
    main()