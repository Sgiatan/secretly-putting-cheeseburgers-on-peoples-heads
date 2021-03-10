import pygame
import random
import math

pygame.init()
window_x, window_y = 800, 600
screen = pygame.display.set_mode((window_x, window_y))

# Window
pygame.display.set_caption("Secretly Putting Cheeseburgers On People's Heads")
icon = pygame.image.load('files/pixel_borger.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('files/sprite.png')
playerX = -110
playerY = 200
playerY_change = 0
player_speed = 1

# Bullet
bulletImg = pygame.image.load('files/bullet.png')
bulletX = playerX
bulletY = playerY
bullet_speed = 2
bulletX_change = bullet_speed
bullet_isfired = False

# Enemy
enemyImg = pygame.image.load('files/pixel_victim1.png')
enemyX = window_x - 300
enemyY = random.randint(0, window_y - 150)
enemyX_change = -40
enemy_speed = 0.5
enemyY_change = enemy_speed

score = 0


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global bullet_isfired
    bullet_isfired = True
    screen.blit(bulletImg, (x, y))


def is_collision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt(((enemyX - bulletX) ** 2) + ((enemyY - bulletY) ** 2))
    return distance < 150


# game loop
running = True
while running:
    screen.fill((252, 185, 40))

    # events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -player_speed
            if event.key == pygame.K_DOWN:
                playerY_change = player_speed
            if event.key == pygame.K_SPACE:
                if not bullet_isfired:
                    bulletY = playerY
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0

    # moving the player
    playerY += playerY_change

    # player boundaries
    if playerY <= -5:
        playerY = -5
    elif playerY >= window_y - 150:
        playerY = window_y - 150

    # moving the enemy
    enemyY += enemyY_change

    # enemy boundaries
    if enemyY <= -50:
        enemyY_change = enemy_speed
        enemyX += enemyX_change
    elif enemyY >= window_y - 130:
        enemyY_change = -enemy_speed
        enemyX += enemyX_change

    # moving the bullet
    if bulletX == window_x - 250:
        bulletX = playerX
        bullet_isfired = False

    if bullet_isfired:
        fire_bullet(bulletX, bulletY)
        bulletX += bulletX_change

    # collision
    collision = is_collision(enemyX, enemyY, bulletX, bulletY)
    if collision:
        bulletX = playerX
        bullet_isfired = False
        score += 1
        print(score)
        enemyX = window_x - 300
        enemyY = random.randint(0, window_y - 150)

    player(playerX, playerY)
    enemy(enemyX, enemyY)
    pygame.display.update()
