import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1080   
SCREEN_HEIGHT = 700
ENEMY_COUNT = 5
PLAYER_SPEED = 5
ENEMY_SPEED = 1
BULLET_SPEED = 2
FIRE_COOLDOWN = 300            # Cooldown in milliseconds (500ms = half a second)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BULLET_COLOR = (255, 0, 0,  ) 
SCORE_FONT = pygame.font.SysFont(None, 36)  # Font for displaying score
GAME_OVER_FONT = pygame.font.SysFont(None, 72)  # Font for displaying "Game Over"
RESTART_FONT = pygame.font.SysFont(None, 36)  # Font for displaying restart button text

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Impact")

# Load images
player_img = pygame.image.load('tin.png')
player_img = pygame.transform.scale(player_img, (60, 60))
enemy_img = pygame.image.load('eyy.png')
enemy_img = pygame.transform.scale(enemy_img, (80, 80))
bullet_img = pygame.image.load('tobol.png')
bullet_img = pygame.transform.scale(bullet_img, (60, 60))

# Define classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.last_shot = pygame.time.get_ticks()  # Time when the player last shot

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            self.rect.x += PLAYER_SPEED

        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Check if enough time has passed since the last shot
        now = pygame.time.get_ticks()
        if keys[pygame.K_SPACE] and now - self.last_shot > FIRE_COOLDOWN :
            bullet = Bullet(self.rect.centerx, self.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            self.last_shot = now  # Update the last shot time

class Enemy(pygame.sprite.Sprite): 
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = ENEMY_SPEED

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -BULLET_SPEED 

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Create sprite groups
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()

# Create player
player = Player()
all_sprites.add(player)

# Create enemies
for _ in range(ENEMY_COUNT):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Initialize score
score = 0

# Game over flag
game_over = False

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not game_over:
        all_sprites.update()

        # Check for bullet-enemy collisions
        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            # Remove the enemy
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            # Increase score
            score += 10

        # Check for player-enemy collisions
        hits = pygame.sprite.spritecollide(player, enemies, True)
        if hits:
            game_over = True

    # Draw / Render
    screen.fill(WHITE)
    all_sprites.draw(screen)
    
    if game_over:
        # Display "Game Over" text
        game_over_text = GAME_OVER_FONT.render("GAMAY KAG OTEN KAWAWA", True, RED)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2))

        # Display restart button text
        restart_text = RESTART_FONT.render("Press R to Restart", True, RED)
        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + game_over_text.get_height()))

        # Check for restart
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            # Reset game variables
            all_sprites.empty()
            enemies.empty()
            bullets.empty()
            player = Player()
            all_sprites.add(player)
            for _ in range(ENEMY_COUNT):
                enemy = Enemy()
                all_sprites.add(enemy)
                enemies.add(enemy)
            score = 0
            game_over = False

    # Display score
    score_text = SCORE_FONT.render("Score: " + str(score), True, RED)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
