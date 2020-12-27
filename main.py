import pygame
from pygame import mixer
import random
import numpy as np
#initializing the pygame library
pygame.init()
#create the screen
screen = pygame.display.set_mode((600,600))
#Title and icon
pygame.display.set_caption("Caterpillar invaders")
icon = pygame.image.load("imgs/caterpillar-worm-shape.png")
pygame.display.set_icon(icon)
#values
NUM_OF_ENEMIES = 10
PLAYER_X_MOVE_CHANGE = 0.15
LETTUCE_Y_MOVE_CHANGE = 15
LETTUCE_X_MOVE_CHANGE = [0.35]*NUM_OF_ENEMIES
BULLET_Y_MOVE_CHANGE = 1

#player and enemies
caterpillar_img = pygame.image.load("imgs/caterpillar.png")
bullet_img = pygame.image.load("imgs/drop.png")

cat_x, cat_y = 270, 480
but_x, but_y = cat_x, cat_y
bullet_state = 'ready'

lettuce_img = []
let_x, let_y = [], []
for i in range(NUM_OF_ENEMIES):
    lettuce_img.append(pygame.image.load("imgs/lettuce.png"))
    let_x.append(random.randint(0,600))
    let_y.append(random.randint(20,50))

def player(x,y):
    screen.blit(caterpillar_img, (x, y))

def enemy1(x,y,i):
    screen.blit(lettuce_img[i], (x, y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bullet_img, (x+6, y+6))

def isCollision(bulletX, bulletY, enemyX, enemyY):
    if np.linalg.norm(np.array([bulletX-enemyX, bulletY-enemyY])) <=25:
        return True
    else:
        return False

#score
score_value = 0
font = pygame.font.Font('KIdDOS-Regular.ttf', 32)
textX, textY = 10, 550

#game_over_text:
def game_over_text():
    font2 = pygame.font.Font('KIdDOS-Regular.ttf', 70)
    end = font2.render(f"Game Over! Score: {int(score_value)}", True, (255,0,0))
    screen.blit(end, (40, 250))


def showScore(x,y):
    score = font.render(f"Score: {int(score_value)}", True, (255,0,0))
    screen.blit(score, (x, y))

#game loop
total_x_change = 0
running = True
while running:
    game_over = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                total_x_change =-PLAYER_X_MOVE_CHANGE
            if event.key == pygame.K_RIGHT:
                total_x_change =PLAYER_X_MOVE_CHANGE
            if event.key == pygame.K_SPACE and bullet_state=='ready':
                shoot = mixer.Sound('sounds/laser.wav')
                shoot.play()
                but_x = cat_x
                fire_bullet(but_x, but_y)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                total_x_change = 0
    cat_x+=total_x_change
    

    if cat_x<-50:
        cat_x=650
    elif cat_x>650:
        cat_x=-50
    #game window
    screen.fill((138, 228, 101))
    #enemy movment
    for i in range(NUM_OF_ENEMIES):
        #check if game is over
        if let_y[i]>420:
            for j in range(NUM_OF_ENEMIES):
                let_y[j] = 2000
                game_over = True
                break
        let_x[i]+=LETTUCE_X_MOVE_CHANGE[i]
        if let_x[i]<0:
            let_x[i]=0
            LETTUCE_X_MOVE_CHANGE[i] *=-1
            let_y[i]+=LETTUCE_Y_MOVE_CHANGE
        elif let_x[i]>590:
            let_x[i]=590
            LETTUCE_X_MOVE_CHANGE[i] *=-1
            let_y[i]+=LETTUCE_Y_MOVE_CHANGE

        #Collision
        collision = isCollision(but_x, but_y, let_x[i], let_y[i])
        if collision:
            explosion = mixer.Sound('sounds/explosion.wav')
            explosion.play()
            but_y = cat_y
            bullet_state = 'ready'
            score_value+=1
            let_x[i], let_y[i] = random.randint(0,600), random.randint(20,50)
        #printing in screen
        enemy1(let_x[i],let_y[i],i)

    
    if but_y <=0:
        bullet_state = 'ready'
        but_y = cat_y
    if bullet_state == 'fire':
        fire_bullet(but_x, but_y)
        but_y-= BULLET_Y_MOVE_CHANGE

    

    player(cat_x, cat_y)
    showScore(textX,textY)
    if game_over:
        screen.fill((138, 228, 101))
        game_over_text()
    pygame.display.update()
