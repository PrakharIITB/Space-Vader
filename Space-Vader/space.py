import pygame
import random
import time
import os
pygame.init()
window = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invader")
icon = pygame.image.load('astronomy.png')
pygame.display.set_icon(icon)
player_image = pygame.image.load('firing.png')
player_image = pygame.transform.scale(player_image, (50, 50))
clock = pygame.time.Clock()
fps = 60
monster = pygame.image.load('monster.png')
monster = pygame.transform.scale(monster, (50, 50))
font = pygame.font.SysFont(None, 50)
bullet = pygame.image.load('bullet1.png')
bullet = pygame.transform.scale(bullet, (70, 90))
#back_image = pygame.image.load('backimage.jpg')
#back_image = pygame.transform.scale(back_image, (800, 600))
if 'highscore.txt' in os.listdir():
    pass
else:
    with open("highscore.txt", "w") as f:
        f.write(str(0))

def image(file, length, width, posx, posy):
    a = pygame.image.load(file)
    a = pygame.transform.scale(a, (length, width))
    window.blit(a, (posx, posy))
def screen_draw(file, x, y):
    window.blit(file, (x, y))


def screen_write(text, colour, x, y):
    screen = font.render(text, True, colour)
    window.blit(screen, [x, y])

def play_sound(file):
    pygame.mixer.init()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play()
def welcome():
    game_over = True
    while game_over:
        image('backimage.jpg', 800, 600, -5, 5)
        #screen_write("Welcome to Space Invader", (255, 0, 0), 190, 250)
        #screen_write("Press Enter to Start", (255, 0, 0), 250, 300)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    gameloop(4, 0.1)
                    game_over =False
                elif event.key == pygame.K_e:
                    gameloop(2.5, 0.5)
                    game_over =False
                elif event.key == pygame.K_m:
                    gameloop(3, 0.3)
                    game_over = False
        pygame.display.update()

def gameloop(speed1, frequency):
    game_over = True
    game_end = True
    with open("highscore.txt") as f:
        hscore = int(f.read())
    score = 0
    playerX = 370
    playerY = 480
    speed = 0
    bullet_list = []
    bullet_speed = 0
    monsterX = 0
    monsterY = 50
    initial = time.time()
    monster_list = []

    while game_over:
        if game_end == False:
            screen_write("Game Over", (255, 0, 0), 300, 200)
            screen_write("Press Backspace to play again", (255, 0, 0), 170, 250)
            screen_write("Press R to return to the main menu", (255, 0, 0), 150, 300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        gameloop(speed1, frequency)
                    if event.key == pygame.K_r:
                        welcome()

            pygame.display.update()
        else:
            a = time.time()
            image('back2.jpg', 800, 600, 0, 0)
            #window.fill((190, 190, 190))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        if speed1 == 5:
                            speed = 8
                        else:
                            speed = 6
                    if event.key == pygame.K_LEFT:
                        if speed1 == 5:
                            speed = -8
                        else:
                            speed = -6
                    if event.key == pygame.K_SPACE:
                        bullet_list.append([playerX-24, playerY-70, playerX+6, playerY-70])
                        bullet_speed = 5
                        play_sound('laser.mp3')

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                        speed = 0

            if playerX > 750 :
                playerX = 750
            elif playerX < 0:
                playerX = 0

            if int(a) - int(initial) > frequency:
                screen_draw(monster, monsterX, 0)
                initial = time.time()
                monsterX = random.randint(150, 600)
                monster_list.append([monsterX, monsterY])
            else:
                f=0
                for i, j in monster_list:
                    screen_draw(monster, i, j)
                    monster_list[f][1] = j+speed1
                    f += 1

            for i, j in monster_list:
                if j > 430:
                    game_end = False
            m = 0
            for i, j, k, l in bullet_list:
                screen_draw(bullet, i, j)
                bullet_list[m][1] = j-2
                screen_draw(bullet, k, l)
                bullet_list[m][3] = l - 2
                r = 0
                for f, g in monster_list:
                    if abs(g-j) < 20 or abs(g-l) < 20:
                        if abs(f-i) < 20 or abs(f-k) < 20:
                            del bullet_list[m]
                            del monster_list[r]
                            score += 1
                    r += 1
                m += 1
                if hscore < score:
                    hscore = score
                    with open("highscore.txt", "r+") as p:
                        p.write(str(hscore))

            screen_write(f"Score : {score}", (255, 0, 0), 0, 0)
            screen_write(f"High Score: {hscore}", (255, 0, 0), 0, 50)
            screen_draw(player_image, playerX, playerY)

            playerX += speed
            pygame.display.update()
            clock.tick(90)
welcome()