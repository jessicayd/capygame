import pygame
import random
import math
from pygame import mixer

# initialize
pygame.init()

# create screen w width, height
screen = pygame.display.set_mode((800, 600))

# title
pygame.display.set_caption("capybara")

# add icons but doesn't work on mac?!
icon = pygame.image.load('data/player.png')
pygame.display.set_icon(icon)

# background
background = pygame.image.load('data/background.png')

# background sound
mixer.music.load('data/happymusic.wav')
mixer.music.play(-1)
mixer.music.set_volume(0.5)

# loading player
playerImg = pygame.image.load('data/player.png')
playerImg = pygame.transform.smoothscale(playerImg, (64, 64)) 
playerX = 370
playerY = 480
playerX_change = 0

# loading enemy 
num_enemies = 6
enemyImgRight = []
enemyImgLeft = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = 60
right = []

for i in range(num_enemies):
	enemyImgRight.append(pygame.transform.smoothscale(pygame.image.load('data/enemyRight.png'), (64, 64)))
	enemyImgLeft.append(pygame.transform.smoothscale(pygame.image.load('data/enemyLeft.png'), (64, 64)))
	enemyX.append(random.randint(0, 736))
	enemyY.append(random.randint(50, 150))
	enemyX_change.append(3)
	right.append(True)



# loading bullet
bulletImg = pygame.image.load('data/bullet.png')
bulletImg = pygame.transform.smoothscale(bulletImg, (32, 32)) 
bulletY = 480
bulletX = 0
bulletY_change = 8
bullet_ready = True # ready is can't see, false is moving

def isCollision(enemyX, enemyY, bulletX, bulletY):
	if bulletX + 30 >= enemyX and bulletX <= enemyX + 60:
		if bulletY + 20 >= enemyY and bulletY <= enemyY + 20:
			return True
	return False

# displaying player onto surface
def player(x, y):
	screen.blit(playerImg, (x, y))

# displaying enemy onto surface
def enemy(x, y, i):
	if right[i] == True:
		screen.blit(enemyImgRight[i], (x, y))
	if right[i] == False:
		screen.blit(enemyImgLeft[i], (x, y))

# displaying bullet onto surface
def fire_bullet(x, y):
	global bullet_ready
	bullet_ready = False
	screen.blit(bulletImg, (x + 16, y + 10))

#score
score_value = 0
font = pygame.font.Font('data/TequillaSunrise.ttf', 32)
gamefont = pygame.font.Font('data/TequillaSunrise.ttf', 48)
textX = 10
textY = 10

def show_score(x,y):
	score = font.render("Score: " + str(score_value), True, (0,0,0))
	screen.blit(score, (x,y))

def game_over_text():
	rect = pygame.Surface((800, 135))
	rect.set_alpha(180)
	rect.fill((255,255,255))
	screen.blit(rect, (0,230))
	gameover = gamefont.render("GAME OVER", True, (0, 0, 0))
	screen.blit(gameover, (150, 250))


# game loop
running = True
while running:
	# change background
	screen.fill((50,80,20))
	screen.blit(background,(0,0))

	# check for quit
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

		# if keystroke is pressed, check if right/left
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_LEFT:
				playerX_change = -4
			if event.key == pygame.K_RIGHT:
				playerX_change = 4
			if event.key == pygame.K_SPACE:
				if bullet_ready:
					bulletX = playerX
					fire_bullet(bulletX, bulletY)
		if event.type == pygame.KEYUP:
			if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
				playerX_change = 0


	playerX += playerX_change

	if playerX < 0: playerX = 0
	elif playerX > 736: playerX = 736

	# enemy movement
	for i in range(num_enemies):
		# game over
		if enemyY[i] > 400 and enemyX[i] + 55 >= playerX and enemyX[i] < playerX + 55:
			for j in range(num_enemies):
				enemyY[j] = 2000
			game_over_text()
			break
		enemyX[i] += enemyX_change[i]
		if enemyX[i] < 0: 
			enemyX_change[i] = 3
			enemyY[i] += enemyY_change
			right[i] = True
		elif enemyX[i] > 736: 
			enemyX_change[i] = -3
			enemyY[i] += enemyY_change
			right[i] = False 

		# collision
		collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)
		if collision:
			coll_sound = mixer.Sound('data/boom.wav')
			coll_sound.play()
			coll_sound.set_volume(0.5)
			bulletY = 480
			bullet_ready = True
			score_value += 1
			enemyX[i] = random.randint(0, 736)
			enemyY[i] = random.randint(50, 150)
		enemy(enemyX[i], enemyY[i], i)

	# bullet movement
	if bulletY <= 0:
		bulletY = 480
		bullet_ready = True
	if not bullet_ready:
		fire_bullet(bulletX, bulletY)
		bulletY -= bulletY_change

	show_score(textX, textY)
	# show player
	player(playerX, playerY)

	pygame.display.update()