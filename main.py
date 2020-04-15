import pygame
import random
import math
from pygame import mixer

# Initialization of pygame
pygame.init()

# create screen
screen = pygame.display.set_mode((800, 600))

# adding background to the screen
background = pygame.image.load('real_background.png')

#adding background sounds to the game
mixer.music.load("background.wav")
mixer.music.play(-1)


# title and icon
pygame.display.set_caption("Basic_Game")
icon = pygame.image.load('helicopter.png')
pygame.display.set_icon(icon)

# player image
player_image = pygame.image.load('space-invaders.png')
player_x = 370
player_y = 480
player_x_change = 0

# enemy image

enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_of_enemies = 6


for i in range (num_of_enemies):
    enemy_image.append(pygame.image.load('spaceship.png'))
    enemy_x.append(random.randint(0, 736))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(4)
    enemy_y_change.append(40)

# bullet
bullet_image = pygame.image.load('bullet.png')
bullet_x = 0
bullet_y = 480
bullet_x_change = 0
bullet_y_change = 10
bullet_state = "ready"  # you cant see the bullet on the screen

#score
score_value = 0
font = pygame.font.Font('freesansbold.ttf',20)
textX = 10
textY  =10

#Game Over Text
over_font = pygame.font.Font('freesansbold.ttf',200)

def game_over_text():
        over_font= font.render("GAME OVER", True, (255, 255, 255))
        screen.blit(over_font, (200, 250))

def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255,255,255))
    screen.blit(score, (x,y))


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y , i ):
    screen.blit(enemy_image[i], (x,y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_image, (x + 16, y + 10))


def iscollison(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.sqrt((math.pow(enemy_x - bullet_x, 2)) + (math.pow(enemy_y - bullet_y, 2)))
    if distance < 27:
        return True
    else:
        return False


# Game Loop
running = True
while running:
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check whether it is right or left

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_sound =mixer.Sound("Laser.wav")
                    bullet_sound.play()
                    bullet_x = player_x
                    fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0
    # Checking for the motion of the spaceship
    player_x += player_x_change

    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # creating the enemy movement
    for i in range(num_of_enemies):

        #Game over
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

        # Display Collision
        collision = iscollison(enemy_x[i], enemy_y[i], bullet_x, bullet_y)
        if collision:
                explosion_sound = mixer.Sound("explosion.wav")
                explosion_sound.play()
                bullet_y = 480
                bullet_state = "ready"
                score_value += 10

                enemy_x[i] = random.randint(0, 800)
                enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)



    # bullet movement
    if bullet_y <= 0:
        bullet_y = 480
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change



    player(player_x, player_y)
    show_score(textX,textY)
    pygame.display.update()
