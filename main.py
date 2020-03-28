import pygame
import random
import math
from pygame import mixer

# initialize py_game
pygame.init()

# setup or run the screen
screen = pygame.display.set_mode((800, 600))
running = True

# background
background = pygame.image.load('background.png')

# title and icon
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('iconimage.png')
pygame.display.set_icon(icon)

# player
player_img = pygame.image.load('spaceship.png')
player_x = 370
player_y = 480
player_x_change = 0

# enemy
enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load('enemy.png'))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

# bullet
bullet_img = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"

# score
score_value = 0
font = pygame.font.Font("freesansbold.ttf", 32)
text_x = 10
text_y = 10

# game over text
over_font = pygame.font.Font("freesansbold.ttf", 64)


# function of score
def show_score(x, y):
    score = font.render("score :" + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))


# game over function
def game_over_text():
    over_text_1 = over_font.render("GAME OVER !!", True, (225, 0, 0))
    over_text_2 = over_font.render("YOUR SCORE : " + str(score_value), True, (0, 255, 0))
    screen.blit(over_text_1, (200, 250))
    screen.blit(over_text_2, (160, 320))


# function of player
def player(x, y):
    screen.blit(player_img, (x, y))


# function of enemy
def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# function of bullet
def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


# function of collision
def collision(enemyx, enemyy, bulletx, bullety):
    distance = math.sqrt((math.pow(enemyx - bulletx, 2)) + (math.pow(enemyy - bullety, 2)))
    if distance < 27:
        return True
    else:
        return False


# game loop
while running:

    # RBG color
    screen.fill((0, 0, 0))

    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():

        # when game is closed
        if event.type == pygame.QUIT:
            running = False

        # for left and right moment
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        # for stopping left or right moment
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # creating conditions for boundary of player
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # for moving enemy
    for i in range(num_of_enemies):
        if enemy_y[i] > 440:
            for j in range(num_of_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_x_change[i] = 4
            enemy_y[i] += enemy_y_change[i]
        elif enemy_x[i] >= 736:
            enemy_x_change[i] = -4
            enemy_y[i] += enemy_y_change[i]

        # collision
        is_collision = collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if is_collision:
            collision_sound = mixer.Sound('explosion.wav')
            collision_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"

    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change

    # this runs the output screen and updates the screen continuously
    player(player_x, player_y)
    show_score(text_x, text_y)
    pygame.display.update()
