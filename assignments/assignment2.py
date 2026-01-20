from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import random
import time

# global variables:
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
CATCHER_WIDTH = 80
CATCHER_SPEED = 250.0
DIAMOND_SIZE = 30
FALL_SPEED_INITIAL = 80.0
SPEED_INCREASE_PER_CATCH = 5.0
SPEED_MULTIPLIER_RATE = 0.015
COLOR_CATCHER = (1.0, 1.0, 1.0)       
COLOR_GAME_OVER = (1.0, 0.0, 0.0)      

# game veriables
catcher_x = WINDOW_WIDTH // 2  # postioning of catcher at the center of the window
catcher_target_x = WINDOW_WIDTH // 2 # veriable to increase/decrease catcher postion pressing <-/->                                     
diamond_x = random.randint(50,WINDOW_WIDTH-50) # genarating diamond withing 50 to 550 range in X.
diamond_y= WINDOW_HEIGHT - 100 # Diamond will generate under the button postions.650(buttons at) start from 600
diamond_color = (1.0, 1.0, 0.0)  # Initial yellow

score = 0
game_over = False 
paused = False  
last_time = None # to store time stamp of previous frame
fall_speed = FALL_SPEED_INITIAL # fall increases with per catch
speed_multiplier = 1.0 # fall increses over time 
cheat_mode = False


def DrawMPL(x1, y1, x2, y2):
    '''draws lines using MPL'''

    zone = FindZone(x1, y1, x2, y2)

    # Converting points to zone 0
    x1_z0, y1_z0 = to_zone0(x1, y1, zone)
    x2_z0, y2_z0 = to_zone0(x2, y2, zone)

    # applying MPL algoithm
    dx = x2_z0 - x1_z0
    dy = y2_z0 - y1_z0
    d = 2 * dy - dx
    incE = 2 * dy
    incNE = 2 * (dy - dx)

    y = y1_z0
    x = x1_z0

    glBegin(GL_POINTS)
    while x <= x2_z0:
        # Converting x_0 and y_0 to original zone points and plotting

        orig_x, orig_y = from_zone0(x, y, zone)
        glVertex2i(orig_x, orig_y)

        if d > 0:
            y += 1
            d += incNE
        else:
            d += incE
        x += 1
    glEnd()


def FindZone(x1, y1, x2, y2):

    dx = x2-x1
    dy = y2-y1

    abs_dx = abs(dx)
    abs_dy = abs(dy)

    # slope <= 1 means zone 0,3,4,7
    # slope > 1 measns zone 1,2,5,6

    if abs_dx >= abs_dy:
        if dx >= 0 and dy >= 0:
            return 0
        elif dx >= 0 and dy < 0:
            return 7
        elif dx < 0 and dy >= 0:
            return 3
        else:
            return 4

    else:
        if dx >= 0 and dy >= 0:
            return 1
        elif dx < 0 and dy >= 0:
            return 2
        elif dx < 0 and dy < 0:
            return 5
        else:
            return 6


def to_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return -y, x
    elif zone == 7:
        return x, -y


def from_zone0(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_diamond(cx, cy, size):
    """Draw diamond clockwise"""
    half = size // 2   
    DrawMPL(cx, cy - half, cx + half, cy)   # bottom → right
    DrawMPL(cx + half, cy, cx, cy + half)   # right → top
    DrawMPL(cx, cy + half, cx - half, cy)   # top → left
    DrawMPL(cx - half, cy, cx, cy - half)   # left → bottom

def draw_catcher(cx, length):
    """Draw catcher bowl using 4 lines"""
    half = length // 2
    y = 50
    # Top horizontal line (wide opening)
    DrawMPL(cx - half, y + 20, cx + half, y + 20)
    # Left slant (slants inward going down)
    DrawMPL(cx - half, y + 20, cx - half//2, y)
    # Right slant (slants inward going down)
    DrawMPL(cx + half, y + 20, cx + half//2, y)
    # Bottom line (narrow base)
    DrawMPL(cx - half//2, y, cx + half//2, y)
    
def draw_button_left_arrow():
    cx, cy = 60, WINDOW_HEIGHT - 50
    # Arrow body
    DrawMPL(cx - 20, cy, cx + 10, cy)
    # Arrow head (pointing left)
    DrawMPL(cx - 20, cy, cx - 12, cy - 8)
    DrawMPL(cx - 20, cy, cx - 12, cy + 8)

def draw_pause_play_button():   
    cx, cy = WINDOW_WIDTH // 2, WINDOW_HEIGHT - 50
    if paused or game_over:
        # Play triangle
        DrawMPL(cx - 10, cy - 15, cx - 10, cy + 15)
        DrawMPL(cx - 10, cy - 15, cx + 15, cy)
        DrawMPL(cx - 10, cy + 15, cx + 15, cy)
    else:
        # Two thick bars (pause)
        DrawMPL(cx - 10, cy - 15, cx - 10, cy + 15)
        DrawMPL(cx - 8, cy - 15, cx - 8, cy + 15)
        DrawMPL(cx - 6, cy - 15, cx - 6, cy + 15)
        
        DrawMPL(cx + 6, cy - 15, cx + 6, cy + 15)
        DrawMPL(cx + 8, cy - 15, cx + 8, cy + 15)
        DrawMPL(cx + 10, cy - 15, cx + 10, cy + 15)

def draw_exit_button():   
    cx, cy = WINDOW_WIDTH - 60, WINDOW_HEIGHT - 50
    # X shape
    DrawMPL(cx - 15, cy - 15, cx + 15, cy + 15)
    DrawMPL(cx - 15, cy + 15, cx + 15, cy - 15)

def is_caught():
    catcher_left = catcher_x - CATCHER_WIDTH // 2
    catcher_right = catcher_x + CATCHER_WIDTH // 2
    catcher_top = 70
    catcher_bottom = 50
    
    diamond_left = diamond_x - DIAMOND_SIZE // 2
    diamond_right = diamond_x + DIAMOND_SIZE // 2
    diamond_top = diamond_y + DIAMOND_SIZE // 2
    diamond_bottom = diamond_y - DIAMOND_SIZE // 2
    
    # AABB collision detection
    return (diamond_left < catcher_right and
            diamond_right > catcher_left and
            diamond_bottom < catcher_top and
            diamond_top > catcher_bottom)

def reset_diamond():
    global diamond_x, diamond_y, diamond_color, fall_speed
    diamond_x = random.randint(50, WINDOW_WIDTH - 50)
    diamond_y = WINDOW_HEIGHT - 100

    diamond_color = (random.uniform(0.6, 1.0),
                     random.uniform(0.6, 1.0),
                     random.uniform(0.6, 1.0))
    
    fall_speed += SPEED_INCREASE_PER_CATCH

def restart_game():    
    global score, game_over, paused, fall_speed, speed_multiplier, last_time
    global catcher_x, catcher_target_x, cheat_mode
    score = 0
    game_over = False
    paused = False
    fall_speed = FALL_SPEED_INITIAL
    speed_multiplier = 1.0
    catcher_x = WINDOW_WIDTH // 2
    catcher_target_x = WINDOW_WIDTH // 2
    cheat_mode = False
    last_time = None
    reset_diamond()
    print("Starting Over")

def special_key(key, x, y):  
    global catcher_target_x
    if game_over or paused:
        return
    if cheat_mode:
        return  # No manual control in cheat mode
    
    step = 15
    if key == GLUT_KEY_LEFT:
        catcher_target_x = catcher_x - step
    elif key == GLUT_KEY_RIGHT:
        catcher_target_x = catcher_x + step
    
    # Keep target inside screen
    catcher_target_x = max(CATCHER_WIDTH // 2, 
                          min(WINDOW_WIDTH - CATCHER_WIDTH // 2, catcher_target_x))

def keyboard(key, x, y):  
    global cheat_mode, paused
    if key == b'c' or key == b'C':
        cheat_mode = not cheat_mode
        print("Cheat Mode:", "ON" if cheat_mode else "OFF")
    elif key == b' ':
        # Space bar toggles pause
        if not game_over:
            paused = not paused
            print("Paused" if paused else "Resumed")

def mouse_click(button, state, x, y):    
    global paused, game_over
    if button != GLUT_LEFT_BUTTON or state != GLUT_DOWN:
        return    
    y = WINDOW_HEIGHT - y
    if 30 < x < 90 and WINDOW_HEIGHT - 80 < y < WINDOW_HEIGHT - 20:
        restart_game()

    # Pause/Play button (center)
    elif abs(x - WINDOW_WIDTH // 2) < 40 and WINDOW_HEIGHT - 80 < y < WINDOW_HEIGHT - 20:
        if not game_over:
            paused = not paused
            print("Paused" if paused else "Resumed")
    
    # Exit button (right)
    elif WINDOW_WIDTH - 90 < x < WINDOW_WIDTH - 30 and WINDOW_HEIGHT - 80 < y < WINDOW_HEIGHT - 20:
        print(f"Goodbye {score}")
        glutLeaveMainLoop()

def animate():
    
    global last_time, diamond_y, game_over, score, paused
    global speed_multiplier, catcher_x, catcher_target_x
    
    current_time = time.time()  
    # Initialize on first frame
    if last_time is None:
        last_time = current_time
        glutPostRedisplay()
        return    
    # Calculate delta time
    dt = current_time - last_time    
    # Clamp dt to prevent huge jumps (if window dragged, etc.)
    if dt > 0.05:
        dt = 0.05
    
    last_time = current_time
    
    # Don't update game state if paused or game over
    if game_over or paused:
        glutPostRedisplay()
        return
    
    speed_multiplier += SPEED_MULTIPLIER_RATE * dt
    diamond_y -= fall_speed * speed_multiplier * dt
    
    # Catcher movement
    if cheat_mode:
        catcher_target_x = diamond_x
        
        # catcher stays within boundry and diamond fall position
        catcher_target_x = max(CATCHER_WIDTH // 2,
                              min(WINDOW_WIDTH - CATCHER_WIDTH // 2, catcher_target_x)) 
    
    # Smooth movement toward target
    dx = catcher_target_x - catcher_x
    if abs(dx) > 0.1:
        max_move = CATCHER_SPEED * dt
        if dx > 0:
            move = min(dx, max_move)
        else:
            move = max(dx, -max_move)
        catcher_x += move
    
    # Keep catcher inside screen
    catcher_x = max(CATCHER_WIDTH // 2,
                   min(WINDOW_WIDTH - CATCHER_WIDTH // 2, catcher_x))
    
    # Check collision
    if is_caught():
        score += 1
        print(f"Score: {score}")
        reset_diamond()
    elif diamond_y + DIAMOND_SIZE // 2 < 0:
        # Diamond hit ground - Game Over!
        game_over = True
        print(f"Game Over {score}")
    
    glutPostRedisplay()

def display():

    glClear(GL_COLOR_BUFFER_BIT)
    

    glColor3f(0.0, 0.65, 0.65)  # Teal for restart
    draw_button_left_arrow()
    
    glColor3f(1.0, 0.6, 0.0)  # Amber for pause/play
    draw_pause_play_button()
    
    glColor3f(1.0, 0.2, 0.2)  # Red for exit
    draw_exit_button()
    
    # Draw catcher (changes color when game over)
    if game_over:
        glColor3f(*COLOR_GAME_OVER) # catcher to become red
    else:
        glColor3f(*COLOR_CATCHER)
    draw_catcher(int(catcher_x), CATCHER_WIDTH)
    
    # Draw diamond (vanishes when game over)
    if not game_over:
        glColor3f(*diamond_color)
        draw_diamond(int(diamond_x), int(diamond_y), DIAMOND_SIZE)
    
    glutSwapBuffers()

def main():
    global last_time
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b'Assignment2')

    glClearColor(0.0, 0.0, 0.0, 1.0)  # to keep the backgroung black always.
    glPointSize(1.0)
    
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, 0, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    
    # Register callbacks
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutSpecialFunc(special_key)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse_click)
    
    # Initialize time
    last_time = None
    
    print("Game Started!")
    print("Controls:")
    print("  ← → arrows: Move catcher")
    print("  C: Toggle cheat mode")
    print("  Space: Pause/Resume")
    print("  Click buttons at top for actions")
    
    # Start main loop
    glutMainLoop()

if __name__ == "__main__":
    main()
