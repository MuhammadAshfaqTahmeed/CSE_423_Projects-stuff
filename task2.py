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
    glutInitWindowSize(window_width, window_height) # setting the width and height of the window
    glutInitWindowPosition(0,0) # window is created from the top-left of the screen
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