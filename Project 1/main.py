import pygame
import random

# Game constants
WIDTH = 800
HEIGHT = 400
FPS = 30
GRAVITY = 0.75

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("T-Rex Game")
clock = pygame.time.Clock()

# Load game assets
font_name = pygame.font.match_font("arial")
img_dir = "assets"

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join(img_dir, "trex.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 4
        self.rect.bottom = HEIGHT - 10
        self.y_speed = 0

    def update(self):
        self.y_speed += GRAVITY
        self.rect.y += self.y_speed
        if self.rect.bottom > HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10
            self.y_speed = 0

    def jump(self):
        self.y_speed = -15

# Cactus class
class Cactus(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            os.path.join(img_dir, "cactus.png")).convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(100, 400)
        self.rect.y = HEIGHT - 70

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.rect.x = WIDTH + random.randint(100, 400)
            self.rect.y = HEIGHT - 70

# Initialize sprites
all_sprites = pygame.sprite.Group()
cacti = pygame.sprite.Group()
player = Player()
all_sprites.add(player)

for _ in range(5):
    cactus = Cactus()
    all_sprites.add(cactus)
    cacti.add(cactus)

# Game loop
running = True
while running:
    clock.tick(FPS)

    # Process events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                player.jump()

    # Update
    all_sprites.update()

    # Check collision
    hits = pygame.sprite.spritecollide(player, cacti, False)
    if hits:
        running = False

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Update display
    pygame.display.flip()

# Game over screen
game_over_font = pygame.font.Font(font_name, 40)
game_over_text = game_over_font.render("Game Over", True, WHITE)
game_over_rect = game_over_text.get_rect()
game_over_rect.center = (WIDTH // 2, HEIGHT // 2)
screen.blit(game_over_text, game_over_rect)
pygame.display.flip()

pygame.time.wait(2000)

pygame.quit()
