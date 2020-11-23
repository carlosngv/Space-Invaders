import pygame, sys, math
import random
from pygame import mixer

# Initialize the pygame
pygame.init()

# Creating window (width x height)
window = pygame.display.set_mode((600, 500))

# Setting background
background = pygame.image.load('public/background.jpg')

# Changing caption and icon
pygame.display.set_caption('Space Invader')
icon = pygame.image.load('public/logo.png')
pygame.display.set_icon(icon)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 27)
text_x = 10
text_y = 10

# Game Over text
over_font = pygame.font.Font('freesansbold.ttf', 64)
over_x = 10
over_y = 10

class Player(object):
    def __init__(self):
        self.player_img = pygame.image.load('public/spaceship.png')
        self.player_x = 265
        self.playerX_change = 0
        self.player_y = 400
        pass

    def draw_player(self, x, y):
        window.blit(self.player_img, (x, y))


class Alien(object):
    def __init__(self):
        # Alien image
        self.alien_img = []
        self.alien_x = []
        self.alienX_change = []
        self.alien_y = []
        self.alienY_change = []
        self.alien_number = 6
        self.generate_aliens()

    def generate_aliens(self):
        # creates 6 aliens
        for i in range(self.alien_number):
            self.alien_img.append(pygame.image.load('public/alien.png'))
            self.alien_x.append(random.randint(0, 535))
            self.alienX_change.append(0.3)
            self.alien_y.append(random.randint(0, 50))
            self.alienY_change.append(30)

    def draw_alien(self, x, y, i):
        window.blit(self.alien_img[i], (x, y))

class Bullet(object):
    def __init__(self):
        self.bullet_img = pygame.image.load('public/bullet.png')
        self.bullet_x = 0
        self.bulletX_change = 0
        self.bullet_y = 400
        self.bulletY_change = 0.5
        self.bullet_state = "ready"

    def fire_bullet(self, x, y):
        self.bullet_state = "fire"
        window.blit(self.bullet_img, (x + 16, y + 10))

    def isCollision(self, alien_x, alien_y, bullet_x, bullet_y):
        # Distance between two points equation
        distance = math.sqrt(math.pow(alien_x - bullet_x, 2) + math.pow(alien_y - bullet_y, 2))
        if (distance < 27):
            return True
        return False

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    window.blit(score, (x, y))


def game_over_text():
    over_text = font.render("GAME OVER", True, (255, 255, 255))
    window.blit(over_text, (220, 220))

def draw_screen():
    # RGB (Red, Green, Blue)
    window.fill((255, 150, 0))
    # background image
    window.blit(background, (0, 0))

if __name__ == '__main__':
    player = Player()
    alien = Alien()
    bullet = Bullet()
    running = True

    while running:
        draw_screen()
        for event in pygame.event.get(): # Iterating all events pygame has on its API
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                sys.exit()
            # if keystroke is pressed check whether is right or left
            if event.type == pygame.KEYDOWN: # KEYDOWN refers to any key is pressed down
                if event.key == pygame.K_LEFT:
                    player.playerX_change = -0.3
                if event.key == pygame.K_RIGHT:
                    player.playerX_change = 0.3
                if event.key == pygame.K_SPACE:
                    if bullet.bullet_state == 'ready':
                        bullet.bullet_sound = mixer.Sound('public/laser.wav')
                        bullet.bullet_sound.play()
                        bullet.bullet_x = player.player_x
                        bullet.fire_bullet(bullet.bullet_x, bullet.bullet_y)
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player.playerX_change = 0

        # Player movement
        player.player_x += player.playerX_change
        # Player boundaries
        if player.player_x <= 0:
            player.player_x = 0
        elif player.player_x >= 535:
            player.player_x = 535

        # Alien movement
        for i in range(alien.alien_number):
            # Game over
            if alien.alien_y[i] > 350:
                for j in range(alien.alien_number):
                    alien.alien_y[j] = 2000
                game_over_text()
                break

            alien.alien_x[i] += alien.alienX_change[i]
            # Alien boundaries
            if alien.alien_x[i] <= 0:
                alien.alienX_change[i] = 0.3
                alien.alien_y[i] += alien.alienY_change[i]
            elif alien.alien_x[i] >= 535:
                alien.alienX_change[i] = -0.3
                alien.alien_y[i] += alien.alienY_change[i]
            # Collision
            collision = bullet.isCollision(alien.alien_x[i], alien.alien_y[i], bullet.bullet_x, bullet.bullet_y)
            if collision:
                print('buuuum')
                explosion_sound = mixer.Sound('public/explosion.wav')
                explosion_sound.play()
                bullet_y = 400
                bullet_state = "ready"
                score_value += 1
                alien.alien_x[i] = random.randint(0, 535)
                alien.alien_y[i] = random.randint(0, 50)
            alien.draw_alien(alien.alien_x[i], alien.alien_y[i], i)

        # Bullet movement
        if bullet.bullet_y <= 0:
            bullet.bullet_y = 400
            bullet.bullet_state = "ready"
        if bullet.bullet_state == 'fire':
            bullet.fire_bullet(bullet.bullet_x, bullet.bullet_y)
            bullet.bullet_y -= bullet.bulletY_change

        # Displaying objects on window
        player.draw_player(player.player_x, player.player_y)
        show_score(text_x, text_y)
        # Updating window every loop
        pygame.display.update()




