import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders Clone")

# Load assets
laser_sound = pygame.mixer.Sound(r"C:\Users\user\Desktop\karthik\laser-312360.mp3")
explosion_sound = pygame.mixer.Sound(r"C:\Users\user\Desktop\karthik\explosion-42132.mp3")

player_img = pygame.image.load(r"C:\Users\user\Desktop\karthik\spaceship.png")
bullet_img = pygame.image.load(r"C:\Users\user\Desktop\karthik\bullet.png")

player_x = 370
player_y = 480
player_x_change = 0

bullet_x = 0
bullet_y = 480
bullet_y_change = 10
bullet_state = "ready"

enemy_img = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
num_enemies = 6

for _ in range(num_enemies):
    enemy_img.append(pygame.image.load(r"C:\Users\user\Desktop\karthik\enemy.png"))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(random.randint(50, 150))
    enemy_x_change.append(2)
    enemy_y_change.append(20)

# Fire button setup
fire_button_rect = pygame.Rect(WIDTH - 120, HEIGHT - 70, 100, 50)
fire_button_color = (50, 200, 50)

# Fonts
score_value = 0
font = pygame.font.Font(None, 36)
game_over_font = pygame.font.Font(None, 64)

def show_score(x, y):
    score = font.render("Score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(player_img, (x, y))

def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))
    laser_sound.play()

def is_collision(enemy_x, enemy_y, bullet_x, bullet_y):
    distance = math.hypot(enemy_x - bullet_x, enemy_y - bullet_y)
    return distance < 27

def draw_fire_button():
    pygame.draw.rect(screen, fire_button_color, fire_button_rect)
    label = font.render("FIRE", True, (0, 0, 0))
    screen.blit(label, (fire_button_rect.x + 20, fire_button_rect.y + 10))

# Main loop
running = True
while running:
    screen.fill((0, 0, 30))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard input
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -5
            if event.key == pygame.K_RIGHT:
                player_x_change = 5
            if event.key == pygame.K_SPACE and bullet_state == "ready":
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)

        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player_x_change = 0

        # Mouse input for fire button
        if event.type == pygame.MOUSEBUTTONDOWN:
            if fire_button_rect.collidepoint(event.pos) and bullet_state == "ready":
                bullet_x = player_x
                fire_bullet(bullet_x, bullet_y)

    # Update player position
    player_x += player_x_change
    player_x = max(0, min(player_x, WIDTH - 64))

    # Update enemies
    for i in range(num_enemies):
        if enemy_y[i] > 440:
            for j in range(num_enemies):
                enemy_y[j] = 2000
            game_over_text()
            break

        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0 or enemy_x[i] >= WIDTH - 64:
            enemy_x_change[i] *= -1
            enemy_y[i] += enemy_y_change[i]

        if is_collision(enemy_x[i], enemy_y[i], bullet_x, bullet_y):
            explosion_sound.play()
            bullet_y = 480
            bullet_state = "ready"
            score_value += 1
            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = random.randint(50, 150)

        enemy(enemy_x[i], enemy_y[i], i)

    # Bullet movement
    if bullet_state == "fire":
        fire_bullet(bullet_x, bullet_y)
        bullet_y -= bullet_y_change
        if bullet_y <= 0:
            bullet_y = 480
            bullet_state = "ready"

    # Draw everything
    player(player_x, player_y)
    show_score(10, 10)
    draw_fire_button()
    pygame.display.update()
