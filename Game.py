import pygame
from pygame import mixer
import sys
import random
import os


pygame.init()

screen = pygame.display.set_mode((700, 980))
background_image = pygame.image.load('background.jpg')
pygame.display.set_caption("Sailor")
mixer.music.load('sails.wav')
mixer.music.play(-1)
font = pygame.font.Font('freesansbold.ttf', 36)
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 980

def load_and_scale_image(file_path, size):
    image = pygame.image.load(file_path)
    return pygame.transform.scale(image, size)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_and_scale_image('obstacle.png', (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height  # Start above the screen
        self.speed = 5  # Constant speed

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)

class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = load_and_scale_image('collection.png', (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height  # Start above the screen
        self.speed = 3  # Constant speed
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.y = -self.rect.height
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)



class BaseSprite(pygame.sprite.Sprite):
    def __init__(self, image_path, size, speed):
        super().__init__()
        self.image = load_and_scale_image(image_path, size)
        self.rect = self.image.get_rect()
        self.speed = speed

    def update(self):
        keys = pygame.key.get_pressed()
        self.rect.x = max(0, min(SCREEN_WIDTH - self.rect.width, self.rect.x - self.speed * keys[pygame.K_LEFT] + self.speed * keys[pygame.K_RIGHT]))
        self.rect.y = max(0, min(SCREEN_HEIGHT - self.rect.height, self.rect.y - self.speed * keys[pygame.K_UP] + self.speed * keys[pygame.K_DOWN]))

class Boat(BaseSprite):
    def __init__(self):
        super().__init__('boat.png', (75, 75), 2.5)

class Sprite1(BaseSprite):
    def __init__(self):
        super().__init__('sprite1.png', (75, 75), 1.5)

class Sprite2(BaseSprite):
    def __init__(self):
        super().__init__('sprite2.png', (100, 100), 3.5)

# Create boat sprite
boat_sprite = Boat()
all_sprites = pygame.sprite.Group()
all_sprites.add(boat_sprite)

selected_sprites_boat = pygame.sprite.Group()
selected_sprites_sprite1 = pygame.sprite.Group()
selected_sprites_sprite2 = pygame.sprite.Group()

def Background(image):
    size = pygame.transform.scale(image, (700, 980))
    screen.blit(size, (0, 0))

def is_overlapping(sprite, group):
    return pygame.sprite.spritecollide(sprite, group, False)

def load_high_score():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            try:
                high_score = int(file.read())
            except ValueError:
                return 0
        return high_score
    else:
        return 0

def save_high_score(high_score):
    with open("highscore.txt", "w") as file:
        file.write(str(high_score))

 
def main_menu(screen):
    font_title = pygame.font.Font(None, 72)
    font_options = pygame.font.Font(None, 36)
    menu_options = ["Play", "Settings", "Customization", "Exit"]
    selected_option = 0

    sailor_text = font_title.render("Sailor", True, (50, 50, 255))
    sailor_rect = sailor_text.get_rect(center=(screen.get_width() // 2, 100))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                elif event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == len(menu_options) - 1:
                        pygame.quit()
                        sys.exit()
                    else:
                        return selected_option

        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))

        screen.blit(sailor_text, sailor_rect)

        for i, option in enumerate(menu_options):
            color = (0, 0, 0) if i == selected_option else (50, 50, 255)
            text = font_options.render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 300 + i * 50))
            screen.blit(text, text_rect)

        pygame.display.flip()

def settings_menu(screen):
    font = pygame.font.Font(None, 36)
    font2 = pygame.font.Font(None, 46)
    volume = 50
    volume_slider_rect = pygame.Rect(250, 300, 200, 20)
    volume_slider_color = (255, 255, 255)
    slider_circle_color = (0, 0, 0)
    slider_color = (50, 50, 255)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                elif event.key == pygame.K_b:
                    return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if volume_slider_rect.collidepoint(event.pos):
                        volume = max(0, min(100, (event.pos[0] - volume_slider_rect.x) / volume_slider_rect.width * 100))
                        mixer.music.set_volume(volume / 100)

        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))

        title_text = font2.render("Settings", True, (50, 50, 255))
        screen.blit(title_text, (250, 200))

        volume_text = font.render(f"Volume: {int(volume)}", True, (50, 50, 255))
        screen.blit(volume_text, (250, 250))

        pygame.draw.rect(screen, volume_slider_color, volume_slider_rect)
        slider_position = (volume / 100) * volume_slider_rect.width + volume_slider_rect.x
        pygame.draw.circle(screen, slider_color, (int(slider_position), volume_slider_rect.centery), 10)

        back_text = font.render("Back (B)", True, (50, 50, 255))
        screen.blit(back_text, (20, 20))

        pygame.display.flip()

def customization_menu(screen):
    font = pygame.font.Font(None, 36)
    font2 = pygame.font.Font(None, 46)
    sprite_options = ["Boat", "Pirate Ship", "Row Boat"]
    selected_sprites = {'Boat': Boat, 'Pirate Ship': Sprite1, 'Row Boat': Sprite2}
    selected_sprite_index = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
                elif event.key == pygame.K_UP:
                    selected_sprite_index = (selected_sprite_index - 1) % len(sprite_options)
                elif event.key == pygame.K_DOWN:
                    selected_sprite_index = (selected_sprite_index + 1) % len(sprite_options)
                elif event.key == pygame.K_RETURN:
                    selected_sprite_class = selected_sprites[sprite_options[selected_sprite_index]]
                    return selected_sprite_class

        screen.fill((0, 0, 0))
        screen.blit(background_image, (0, 0))

        title_text = font2.render("Customization", True, (50, 50, 255))
        screen.blit(title_text, (250, 200))

        for i, option in enumerate(sprite_options):
            color = (0, 0, 0) if i == selected_sprite_index else (50, 50, 255)
            text = font.render(option, True, color)
            text_rect = text.get_rect(center=(screen.get_width() // 2, 300 + i * 50))
            screen.blit(text, text_rect)

        pygame.display.flip()

def play_game(screen, player_sprite_class):
    clock = pygame.time.Clock()

    # Initialize scores and difficulty parameters
    score = 0
    high_score = load_high_score() 
    difficulty_level = 1
    obstacle_spawn_timer = 0
    max_obstacles_on_screen = 7
    collectible_spawn_timer = 0
    max_collectibles_on_screen = 2

    font = pygame.font.Font(None, 36)

    # Create player sprite at the middle of the bottom
    player_sprite = player_sprite_class()
    player_sprite.rect.x = (SCREEN_WIDTH - player_sprite.rect.width) // 2
    player_sprite.rect.y = SCREEN_HEIGHT - player_sprite.rect.height

    # Create sprite groups
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    collectibles = pygame.sprite.Group()

    # Add player sprite to the group
    all_sprites.add(player_sprite)

    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return  # Return to the main menu

        keys = pygame.key.get_pressed()
        player_sprite.rect.x = max(0, min(SCREEN_WIDTH - player_sprite.rect.width, player_sprite.rect.x - player_sprite.speed * keys[pygame.K_LEFT] + player_sprite.speed * keys[pygame.K_RIGHT]))
        player_sprite.rect.y = max(0, min(SCREEN_HEIGHT - player_sprite.rect.height, player_sprite.rect.y - player_sprite.speed * keys[pygame.K_UP] + player_sprite.speed * keys[pygame.K_DOWN]))

        if not game_over:
            # Update difficulty parameters based on score
            difficulty_level = min(score // 10 + 1, 10)  # Increase difficulty every 10 points

            # Update obstacle spawn interval based on difficulty
            obstacle_spawn_interval = max(120 - 10 * difficulty_level, 60)  # Decrease spawn interval as difficulty increases

            # Update collectible spawn interval based on difficulty
            collectible_spawn_interval = max(200 - 20 * difficulty_level, 100)  # Decrease spawn interval as difficulty increases

            # Add new obstacles
            obstacle_spawn_timer += 1
            if obstacle_spawn_timer >= obstacle_spawn_interval:
                if len(obstacles) < max_obstacles_on_screen:
                    obstacle = Obstacle()
                    while is_overlapping(obstacle, obstacles) or is_overlapping(obstacle, collectibles):
                        obstacle.rect.x = random.randint(0, SCREEN_WIDTH - obstacle.rect.width)
                        obstacle.rect.y = -obstacle.rect.height
                    obstacles.add(obstacle)
                    obstacle_spawn_timer = 0

            # Add new collectibles
            collectible_spawn_timer += 1
            if collectible_spawn_timer >= collectible_spawn_interval:
                if len(collectibles) < max_collectibles_on_screen:
                    collectible = Collectible()
                    while is_overlapping(collectible, obstacles) or is_overlapping(collectible, collectibles):
                        collectible.rect.x = random.randint(0, SCREEN_WIDTH - collectible.rect.width)
                        collectible.rect.y = -collectible.rect.height
                    collectibles.add(collectible)
                    collectible_spawn_timer = 0

            # Update sprites
            all_sprites.update()
            obstacles.update()
            collectibles.update()

            # Check for collisions with obstacles
            collisions = pygame.sprite.spritecollide(player_sprite, obstacles, False)
            if collisions:
                # Game over
                game_over = True

            # Check for collisions with collectibles
            collectible_collisions = pygame.sprite.spritecollide(player_sprite, collectibles, True)
            if collectible_collisions:
                # Increase the score when player collects a collectible
                score += 1

        screen.fill((255, 255, 255))
        screen.blit(background_image, (0, 0))

        # Draw all sprites
        all_sprites.draw(screen)
        obstacles.draw(screen)
        collectibles.draw(screen)

        # Draw the score and high score
        score_text = font.render(f"Score: {score}", True, (50, 50, 255))
        screen.blit(score_text, (10, 10))

        high_score_text = font.render(f"High Score: {high_score}", True, (50, 50, 255))
        screen.blit(high_score_text, (10, 50))

        if game_over:
            # Check and update high score
            if score > high_score:
                high_score = score
                # Save the high score to file
                save_high_score(high_score)

            # Draw the game over message in the middle of the screen
            game_over_text1 = font.render("Game Over", True, (255, 0, 0))
            game_over_rect1 = game_over_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
            screen.blit(game_over_text1, game_over_rect1)

            game_over_text2 = font.render(f"Score: {score}", True, (255, 0, 0))
            game_over_rect2 = game_over_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            screen.blit(game_over_text2, game_over_rect2)

            game_over_text3 = font.render(f"High Score: {high_score}", True, (255, 0, 0))
            game_over_rect3 = game_over_text3.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
            screen.blit(game_over_text3, game_over_rect3)

        pygame.display.flip()

        clock.tick(60)
        
def main():
    clock = pygame.time.Clock()

    selected_sprite = None

    while True:
        menu_option = main_menu(screen)

        if menu_option == 0:
            # "Play" option selected
            if selected_sprite is not None:
                play_game(screen, selected_sprite)
        elif menu_option == 1:
            settings_menu(screen)
        elif menu_option == 2:
            # "Customization" option selected
            selected_sprite = customization_menu(screen)

if __name__ == "__main__":
    main()