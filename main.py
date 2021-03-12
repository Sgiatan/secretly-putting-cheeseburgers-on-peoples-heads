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

# Music
pygame.mixer.music.load('assets/soundtrack.wav')
pygame.mixer.music.play(-1)

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
spawn_rate = 1000
spawn_clock = 0
spawn_time = random.randint(0, spawn_rate)

# Score
total_score = 0
level_score = 0
level = 0
burgers_left = 50
game_over = False


def new_game():
    global enemy_speed, spawn_rate, spawn_clock, spawn_time
    global total_score, level_score, level, burgers_left, game_over

    pygame.mixer.music.unpause()

    # Reset enemies
    enemy_speed = 0.5
    spawn_rate = 1000
    spawn_clock = 0
    spawn_time = random.randint(0, spawn_rate)

    # Reset score
    total_score = 0
    level_score = 0
    level = 0
    burgers_left = 50
    game_over = False


score_x, score_y = 50, window_y - 100
font = pygame.font.Font('assets/insaniburger.regular.ttf', 32)
menu_font = pygame.font.Font('assets/insaniburger.regular.ttf', 72)


def show_score(x, y):
    score_text = font.render(f"Score: {total_score}", True, (0, 0, 0))
    level_text = font.render(f" Level: {level}", True, (0, 0, 0))
    burger_text = font.render(f"Burgers: {burgers_left}", True, (0, 0, 0))
    screen.blit(score_text, (x, y + 30))
    screen.blit(level_text, (x + 5, y))
    screen.blit(burger_text, (x - 31, y + 60))


def show_menu():
    while True:
        screen.fill((252, 185, 40))
        top_text = menu_font.render("Secretly Putting", True, (0, 0, 0))
        middle_text = menu_font.render("Cheeseburgers On", True, (0, 0, 0))
        bottom_text = menu_font.render("People's Heads", True, (0, 0, 0))
        press_space = font.render("Press Space", True, (0, 0, 0))
        screen.blit(top_text, (100, 100))
        screen.blit(middle_text, (85, 160))
        screen.blit(bottom_text, (149, 220))
        screen.blit(press_space, (310, 500))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True

        pygame.display.update()


def show_game_over():
    global game_over
    game_over = True
    pygame.mixer.music.pause()
    over_text = menu_font.render("You were spotted", True, (0, 0, 0))
    screen.blit(over_text, (85, 100))


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
enemies = []  # Enemy() for _ in range(6)]-stop


def is_collision(enemyX, enemyY, burgerX, burgerY):
    distance = math.sqrt(((enemyX - burgerX) ** 2) + ((enemyY - burgerY) ** 2))
    return distance < 75


# game loop
running = show_menu()
new_game()

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
                if game_over:
                    new_game()

                elif burgers_left != 0:
                    burger = Burger()
                    burgers.append(burger)
                    burger.fire()
                    burgers_left -= 1
            if event.key == pygame.K_ESCAPE:
                running = show_menu()

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

    if not game_over:
        # spawning new enemies
        spawn_clock += 1
        if spawn_clock == spawn_time:
            enemies.append(Enemy())
            spawn_clock = 0
            spawn_time = random.randint(100, 2000)

        # moving the enemies
        for enemy in enemies:
            enemy.y += enemy.y_change
            print(enemy.y_change)

            # death check
            if enemy.x <= 200:
                enemies.clear()
                show_game_over()
                i_tried = pygame.mixer.Sound('assets/i_tried.mp3')
                i_tried.play()
                break

            # enemy boundaries
            if enemy.y <= 0:
                enemy.y_change = enemy_speed
                enemy.x += enemy.x_change
            elif enemy.y >= window_y - 79:
                enemy.y_change = -enemy_speed
                enemy.x += enemy.x_change

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

        # change difficulty
        if level_score == level + 10:
            level += 1
            burgers_left += level + 20
            level_score = 0
            enemy_speed += 0.2
            spawn_rate -= min(spawn_rate, level - 50)
            # enemies = [Enemy() for _ in range(level + 6)]

    else:
        show_game_over()

    player(playerX, playerY)
    show_score(score_x, score_y)
    pygame.display.update()
