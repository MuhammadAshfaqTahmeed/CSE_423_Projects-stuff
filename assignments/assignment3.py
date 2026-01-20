from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import math

game_over = 0  # 0 = playing, 1 = game over
player_life = 5 
score = 0
bullet_miss = 0
player_x = 0
player_z = 0
angle  = 0     # direction player facing
step = 20      # player move steps after pressing W/S        
rotate_step = 10  # degree to rotate after pressing A/D

enemy_data = {}
bullet_data = {}
bullet_id = 1
bullet_speed = 5
enemy_scale = 1    # scaling factor for enemy grow/shrink
cheat_mode = 0
camera_angle = 45  # third person camera angle
camera_height = 600
camera_dist = 600
fps = 0
cheatmode_fps = 0
cheatmode_angle = 0  # angle stored when cheatmodefps toggles


def draw_text(x, y, text, font=GLUT_BITMAP_HELVETICA_18):
    glColor3f(1, 1, 1)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    gluOrtho2D(0, 1000, 0, 800)  # left, right, bottom, top

    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glRasterPos2f(x, y)
    for ch in text:
        glutBitmapCharacter(font, ord(ch))

    glPopMatrix()
    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)


def tile(row, col, color):
    glColor3f(color[0], color[1], color[2])
    glBegin(GL_QUADS)
    glVertex3f((row - 6.5) * 80, 0, (col - 6.5) * 80)
    glVertex3f((row - 6.5) * 80 + 80, 0, (col - 6.5) * 80)
    glVertex3f((row - 6.5) * 80 + 80, 0, (col - 6.5) * 80 + 80)
    glVertex3f((row - 6.5) * 80, 0, (col - 6.5) * 80 + 80)
    glEnd()


def Grid():
    counter = 0
    for i in range(13):
        for j in range(13):
            if counter % 2 == 0:
                color = (1.0, 1.0, 1.0)
            else:
                color = (0.5, 0.0, 0.5)
            counter += 1
            tile(i, j, color)

    # left wall
    glPushMatrix()
    glColor3f(1, 0, 1)
    glTranslatef(-520, 25, 0)
    glScalef(2, 50, 260)
    glutSolidCube(4)
    glPopMatrix()

    # right wall
    glPushMatrix()
    glColor3f(0, 1, 0)
    glTranslatef(520, 25, 0)
    glScalef(2, 50, 260)
    glutSolidCube(4)
    glPopMatrix()

    # back wall
    glPushMatrix()
    glColor3f(0, 0, 1)
    glTranslatef(0, 25, -520)
    glScalef(260, 50, 2)
    glutSolidCube(4)
    glPopMatrix()

    # front wall
    glPushMatrix()
    glColor3f(1, 1, 0)
    glTranslatef(0, 25, 520)
    glScalef(260, 50, 2)
    glutSolidCube(4)
    glPopMatrix()


def draw_player():
    global player_x, player_z, angle, game_over

    if game_over == 1:
        glPushMatrix()
        glTranslatef(player_x, 30, player_z)
        glRotatef(-270, 1, 0, 0)

        # body
        glPushMatrix()
        glColor3f(0.0, 0.3, 0.0)
        glScalef(15, 12, 15)
        glutSolidCube(4)
        glPopMatrix()

        # head
        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)
        glTranslatef(0, 45, 0)
        glutSolidSphere(20, 32, 32)
        glPopMatrix()

        # hand1
        glPushMatrix()
        glColor3f(1.0, 0.80, 0.60)
        glTranslatef(-30, 20, 0)
        glRotatef(180, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)
        glPopMatrix()

        # hand2
        glPushMatrix()
        glColor3f(1.0, 0.80, 0.60)
        glTranslatef(30, 20, 0)
        glRotatef(180, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)
        glPopMatrix()

        # gun
        glPushMatrix()
        glColor3f(0.5, 0.5, 0.5)
        glTranslatef(0, 10, 0)
        glRotatef(180, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 15, 0, 80, 10, 10)
        glPopMatrix()

        # leg1
        glPushMatrix()
        glColor3f(0.0, 0.0, 1.0)
        glTranslatef(-15, -15, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 15, 5, 80, 10, 10)
        glPopMatrix()

        # leg2
        glPushMatrix()
        glColor3f(0.0, 0.0, 1.0)
        glTranslatef(15, -15, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 15, 5, 80, 10, 10)
        glPopMatrix()

        glPopMatrix()

    else:
        glPushMatrix()
        glTranslatef(player_x, 100, player_z)
        glRotatef(angle, 0, 1, 0)

        # body
        glPushMatrix()
        glColor3f(0.0, 0.3, 0.0)
        glScalef(15, 12, 15)
        glutSolidCube(4)
        glPopMatrix()

        # head
        glPushMatrix()
        glColor3f(0.0, 0.0, 0.0)
        glTranslatef(0, 45, 0)
        glutSolidSphere(20, 32, 32)
        glPopMatrix()

        # hand1
        glPushMatrix()
        glColor3f(1.0, 0.80, 0.60)
        glTranslatef(-30, 20, 0)
        glRotatef(180, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)
        glPopMatrix()

        # hand2
        glPushMatrix()
        glColor3f(1.0, 0.80, 0.60)
        glTranslatef(30, 20, 0)
        glRotatef(180, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 10, 5, 50, 10, 10)
        glPopMatrix()

        # gun
        glPushMatrix()
        glColor3f(0.5, 0.5, 0.5)
        glTranslatef(0, 10, 0)
        glRotatef(180, 0, 1, 0)
        gluCylinder(gluNewQuadric(), 15, 0, 100, 10, 10)
        glPopMatrix()

        # leg1
        glPushMatrix()
        glColor3f(0.0, 0.0, 1.0)
        glTranslatef(-15, -15, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 15, 5, 80, 10, 10)
        glPopMatrix()

        # leg2
        glPushMatrix()
        glColor3f(0.0, 0.0, 1.0)
        glTranslatef(15, -15, 0)
        glRotatef(90, 1, 0, 0)
        gluCylinder(gluNewQuadric(), 15, 5, 80, 10, 10)
        glPopMatrix()

        glPopMatrix()
def draw_enemy(x, y):
    global enemy_scale

    # enemy head (small sphere black)
    glPushMatrix()
    glColor3f(0, 0, 0)
    glTranslatef(x, 90, y)
    glScalef(enemy_scale, enemy_scale, enemy_scale)
    glutSolidSphere(15, 100, 100)
    glPopMatrix()

    # enemy body (big red sphere)
    glPushMatrix()
    glColor3f(1.0, 0.0, 0.0)
    glTranslatef(x, 40, y)
    glScalef(enemy_scale, enemy_scale, enemy_scale)
    glutSolidSphere(40, 100, 100)
    glPopMatrix()


def draw_bullet(x=0, y=0):
    glPushMatrix()
    glColor3f(1, 0, 0)
    glTranslatef(x, 105, y)
    glutSolidCube(12)
    glPopMatrix()


def keyboard(key, x, y):
    global player_x, player_z, angle, cheat_mode, player_life, bullet_miss, score
    global enemy_data, bullet_data, bullet_id, game_over, cheatmode_fps, cheatmode_angle
    global rotate_step, fps

    rad = math.radians(angle)
    dirForward = (math.sin(rad), 0, -math.cos(rad))

    if key == b'a':      # rotate left
        angle = angle + rotate_step
        if angle >= 360:
            angle -= 360
        elif angle < 0:
            angle += 360

    elif key == b'd':    # rotate right
        angle = angle - rotate_step
        if angle >= 360:
            angle -= 360
        elif angle < 0:
            angle += 360

    elif key == b'w':
        if game_over != 1:
            if -500 <= (player_x - dirForward[0] * step) <= 500 and -500 <= (player_z + dirForward[2] * step) <= 500:
                player_x -= dirForward[0] * step
                player_z += dirForward[2] * step

    elif key == b's':
        if game_over != 1:
            if -500 <= (player_x + dirForward[0] * step) <= 500 and -500 <= (player_z - dirForward[2] * step) <= 500:
                player_x += dirForward[0] * step
                player_z -= dirForward[2] * step

    elif key == b'c':
        if game_over != 1:
            cheat_mode = 1 - cheat_mode
            if cheat_mode == 1:
                bullet_miss = 0

    elif key == b'r':
        # reset game
        game_over = 0
        score = 0
        player_life = 5
        bullet_miss = 0
        enemy_data = {}
        bullet_data = {}
        bullet_id = 1
        player_x = 0
        player_z = 0
        angle = 0.0
        fps = 0
        cheatmode_fps = 0
        cheatmode_angle = 0
        print("Game Restarted")

    if cheat_mode == 1 and key == b'v':
        cheatmode_fps = 1 - cheatmode_fps
        cheatmode_angle = angle

    glutPostRedisplay()


def mouse(button, state, x, y):
    global player_x, player_z, angle, bullet_id, fps

    rad = math.radians(angle)
    dirForward = (math.sin(rad), 0, -math.cos(rad))

    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        bullet_data[bullet_id] = (player_x, player_z, dirForward[0], dirForward[2])
        print("Player Bullet Fired!")
        bullet_id += 1
        glutPostRedisplay()

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        fps = 1 - fps


def special_keys(key, x, y):
    global camera_angle, camera_height

    if key == GLUT_KEY_LEFT:
        camera_angle += 5
    elif key == GLUT_KEY_RIGHT:
        camera_angle -= 5
    elif key == GLUT_KEY_UP:
        camera_height += 20
    elif key == GLUT_KEY_DOWN:
        camera_height -= 20

    glutPostRedisplay()


def ShowScreen():
    global enemy_data, angle, player_x, player_z, bullet_data, bullet_id, bullet_speed
    global bullet_miss, score, player_life, cheat_mode, game_over
    global camera_angle, camera_height, camera_dist, cheatmode_fps, cheatmode_angle
    global fps

    rad = math.radians(angle)
    dirForward = (math.sin(rad), 0, -math.cos(rad))

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # camera setup
    if fps == 0:
        gluLookAt(camera_dist * math.cos(math.radians(camera_angle)),
                  camera_height,
                  camera_dist * math.sin(math.radians(camera_angle)),
                  0, 0, 0,
                  0, 1, 0)
    elif fps == 1:
        if cheatmode_fps == 0:
            gluLookAt(player_x - 50, 190, player_z + 40,
                      player_x - 50 - dirForward[0], 190, player_z + 40 + dirForward[2],
                      0, 1, 0)
        else:
            # use stored angle cheatmode_angle
            look_dx = -math.sin(math.radians(cheatmode_angle))
            look_dz = math.cos(math.radians(cheatmode_angle))
            gluLookAt(player_x - 50, 190, player_z + 40,
                      player_x - 50 + look_dx, 190, player_z + 40 + look_dz,
                      0, 1, 0)

    # update game_over
    if player_life == 0 or bullet_miss > 50:
        game_over = 1

    if game_over == 1:
        Grid()
        draw_player()
        draw_text(20, 770, f"Game is Over! Your Score is {score}")
        draw_text(20, 740, 'PRESS "R" to Restart The Game!')

    else:
        Grid()
        draw_player()

        # cheat mode: auto rotate + auto fire
        if cheat_mode == 1:
            angle = (angle - 1) % 360
            bullet_data[bullet_id] = (player_x, player_z, dirForward[0], dirForward[2])
            bullet_id += 1

        # ensure 5 enemies
        for id in range(1, 6):
            if id not in enemy_data:
                enemy_data[id] = {
                    "x": random.randint(-500, 500),
                    "z": random.randint(-500, 500),
                    "health": 1,
                    "speed": 0.2
                }

        # move enemies & handle player collision
        for i in list(enemy_data.keys()):
            e = enemy_data[i]
            dx = player_x - e["x"]
            dz = player_z - e["z"]
            length = math.sqrt(dx * dx + dz * dz)

            if length < 50:
                player_life -= 1
                print("Remaining Player Life: ", player_life)
                del enemy_data[i]
                continue

            dx /= length
            dz /= length
            e["x"] += dx * e["speed"]
            e["z"] += dz * e["speed"]
            draw_enemy(e["x"], e["z"])

        # bullet-enemy collisions
        for eid in list(enemy_data.keys()):
            e = enemy_data[eid]
            ex, ez = e["x"], e["z"]
            for bidk in list(bullet_data.keys()):
                bx, bz, fx, fz = bullet_data[bidk]
                if (ex - 60 <= bx <= ex + 60) and (ez - 60 <= bz <= ez + 60):
                    del enemy_data[eid]
                    del bullet_data[bidk]
                    score += 1
                    break

        # update bullets
        for i in list(bullet_data.keys()):
            bx, bz, fx, fz = bullet_data[i]
            bx -= fx * bullet_speed
            bz += fz * bullet_speed

            if -500 <= bx <= 500 and -500 <= bz <= 500:
                bullet_data[i] = (bx, bz, fx, fz)
                draw_bullet(bx, bz)
            else:
                if cheat_mode != 1:
                    bullet_miss += 1
                    print("Bullet Missed: ", bullet_miss)
                del bullet_data[i]

        draw_text(10, 770, f"Game Score: {score}")
        draw_text(10, 740, f"Player life remaining: {player_life}")
        draw_text(10, 710, f"Player bullet Missed: {bullet_miss}")

    glutSwapBuffers()


def idle():
    global enemy_scale, game_over
    if enemy_scale < 1.5:
        if game_over == 0:
            enemy_scale += 0.009
    else:
        enemy_scale = 1
    glutPostRedisplay()


def init():
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glViewport(0, 0, 800, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 800 / 600, 0.5, 1500)
    glMatrixMode(GL_MODELVIEW)


def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"Shooting")
    init()
    glutDisplayFunc(ShowScreen)
    glutSpecialFunc(special_keys)
    glutKeyboardFunc(keyboard)
    glutMouseFunc(mouse)
    glutIdleFunc(idle)
    glutMainLoop()

if __name__ == "__main__":
    main()
