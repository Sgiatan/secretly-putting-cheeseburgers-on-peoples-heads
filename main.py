import pygame
import random
import math
import os

pygame.init()
window_x, window_y = 800, 600
screen = pygame.display.set_mode((window_x, window_y))

# Window
pygame.display.set_caption("Secretly Putting Cheeseburgers On People's Heads")
icon = pygame.image.load('assets/icon.png')
pygame.display.set_icon(icon)

# Player
playerImg = pygame.image.load('assets/sprites/player.png')
playerX = -110
playerY = 200
playerY_change = 0
player_speed = 1

# Burger initialisation
playerX_to_burgerX = 230
burger_speed = 1

# Enemy initialisation
enemy_images = [x.path for x in list(os.scandir('assets\\victims'))]
enemy_speed = 0.5
spawn_rate = 2000
spawn_clock = 0
spawn_time = random.randint(0, spawn_rate)

# Score
total_score = 0
level_score = 0
level = 0

score_x, score_y = 50, window_y - 100
font = pygame.font.Font('assets/insaniburger.regular.ttf', 32)


def show_score(x, y):
    score_text = font.render(f"Score: {total_score}", True, (0, 0, 0))
    level_text = font.render(f" Level: {level}", True, (0, 0, 0))
    screen.blit(score_text, (x, y))
    screen.blit(level_text, (x + 5, y + 30))


def player(x, y):
    screen.blit(playerImg, (x, y))


class Burger:
    def __init__(self):
        self.img = pygame.image.load('assets/sprites/burger.png')
        self.x = playerX + playerX_to_burgerX
        self.y = playerY + 76
        self.x_change = burger_speed
        self.is_fired = False

    def fire(self):
        self.is_fired = True
        screen.blit(self.img, (self.x, self.y))


class Enemy:
    def __init__(self):
        self.img = pygame.image.load(random.choice(enemy_images))
        self.x = window_x - 100
        self.y = random.randint(0, window_y - 150)
        self.x_change = -80
        self.y_change = random.choice((enemy_speed, -enemy_speed))
        screen.blit(self.img, (self.x, self.y))


burgers = []
enemies = [Enemy() for _ in range(6)]


def is_collision(enemyX, enemyY, burgerX, burgerY):
    distance = math.sqrt(((enemyX - burgerX) ** 2) + ((enemyY - burgerY) ** 2))
    return distance < 75


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
                burger = Burger()
                burgers.append(burger)
                burger.fire()

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

    for burger in burgers:
        # moving the burger
        if burger.x == window_x:
            burger.x = playerX + playerX_to_burgerX
            burgers.remove(burger)
            burger.is_fired = False

        if burger.is_fired:
            burger.fire()
            burger.x += burger.x_change

    # spawning new enemies
    spawn_clock += 1
    if spawn_clock == spawn_time:
        enemies.append(Enemy())
        spawn_clock = 0
        spawn_time = random.randint(100, 2000)

    # moving the enemies
    for enemy in enemies:
        enemy.y += enemy.y_change

        # enemy boundaries
        if enemy.y <= 0:
            enemy.y_change = enemy_speed
            enemy.x += enemy.x_change
        elif enemy.y >= window_y - 79:
            enemy.y_change = -enemy_speed
            enemy.x += enemy.x_change

        # death check
        if enemy.x <= playerX + playerX_to_burgerX:
            running = False

        # collision
        for burger in burgers:
            collision = is_collision(enemy.x, enemy.y, burger.x, burger.y)
            if collision:
                burger.x = playerX + playerX_to_burgerX
                burger.is_fired = False
                burgers.remove(burger)
                enemies.remove(enemy)
                level_score += 1
                total_score += 1

        screen.blit(enemy.img, (enemy.x, enemy.y))

    if level_score == level + 10:
        level += 1
        level_score = 0
        enemy_speed += 0.2
        spawn_rate -= spawn_rate * 0.1
        enemies = [Enemy() for _ in range(level + 6)]

    player(playerX, playerY)
    show_score(score_x, score_y)
    pygame.display.update()
