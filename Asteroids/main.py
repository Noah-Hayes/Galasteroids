import pygame
import math
import random
pygame.init()

sw = 1920
sh = 1080

bg = pygame.image.load('asteroids.pics/starbg.png')
alien = pygame.image.load('asteroids.pics/alienShip.png')
user = pygame.image.load('asteroids.pics/spaceRocket75.png')
star = pygame.image.load('asteroids.pics/star.png')
asteroid50 = pygame.image.load('asteroids.pics/asteroid50.png')
asteroid100 = pygame.image.load('asteroids.pics/asteroid100.png')
asteroid150 = pygame.image.load('asteroids.pics/asteroid150.png')

pygame.display.set_caption('Asteroids')
win = pygame.display.set_mode((sw, sh))

clock = pygame.time.Clock()

gameover = False
lives = 3
score = 0


class Player(object):
    def __init__(self):
        self.img = user
        self.w = self.img.get_width()
        self.h = self.img.get_height()
        self.x = sw // 2
        self.y = sh // 2
        self.angle = 0
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)  # set center of player model to the center of screen on spawn
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.nose = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)


    def draw(self, win):
        # win.blit(self.img, [self.x, self.y, self.w, self.h])
        win.blit(self.rotatedSurf, self.rotatedRect)

    def turnLeft(self):
        self.angle += 2.5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.nose = (self.x + self.cosine * self.w//2, self.y - self.sine * self.h//2)

    def turnRight(self):
        self.angle -= 2.5
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.nose = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def moveForward(self):
        self.x += self.cosine * 3
        self.y -= self.sine * 3
        self.rotatedSurf = pygame.transform.rotate(self.img, self.angle)
        self.rotatedRect = self.rotatedSurf.get_rect()
        self.rotatedRect.center = (self.x, self.y)
        self.cosine = math.cos(math.radians(self.angle + 90))
        self.sine = math.sin(math.radians(self.angle + 90))
        self.nose = (self.x + self.cosine * self.w // 2, self.y - self.sine * self.h // 2)

    def updateLocation(self): # if player goes off screen, bring back onto the opposite side
        if self.x > sw + 50:
            self.x = 0
        elif self.x < 0 - self.w:
            self.x = sw
        elif self.y < -50:
            self.y = sh
        elif self.y > sh + 50:
            self.y = 0

class Bullet(object):
    def __init__(self):
        self.point = player.nose
        self.x, self.y = self.point
        self.w = 8
        self.h = 8
        self.c = player.cosine
        self.s = player.sine
        self.xv = self.c * 10
        self.yv = self.s * 10

    def move(self):
        self.x += self.xv
        self.y -= self.yv

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 200), [self.x, self.y, self.w, self.h])

    def checkOffScreen(self): # save RAM instead of letting objects exist off screen
        if self.x < -50 or self.x > sw or self.y < -50 or self.y> sh:
            return True

class Asteroid(object):
    def __init__(self, rank):
        self.rank = rank
        if self.rank == 1:
            self.image = asteroid50
        elif self.rank == 2:
            self.image = asteroid100
        elif self.rank == 3:
            self.image = asteroid150
        self.w = 50 * rank
        self.h = 50 * rank
        self.ranPoint = random.choice([(random.randrange(0, sw - self.w), random.choice([-1 * self.h - 5, sh + 5])), (random.choice([-1 * self.w - 5, sw + 5]), random.randrange(0, sh- self.h))])
        self.x, self.y = self.ranPoint
        if self.x < sw // 2:
            self.xdir = 1
        else:
            self.xdir = -1
        if self.y < sh // 2:
            self.ydir = 1
        else:
            self.ydir = -1
        self.xv = self.xdir * random.randrange(1, 3)
        self.yv = self.ydir * random.randrange(1, 3)

    def draw(self, win):
        win.blit(self.image, (self.x, self.y))

def redrawGameWindow():
    win.blit(bg, (0, 0))
    font = pygame.font.SysFont('arial',25)
    livesText = font.render('LIVES: ' + str(lives), 1, (255, 255, 255))
    playAgainText = font.render('PRESS SPACE TO PLAY AGAIN', 1, (255, 255, 255))
    scoreText = font.render('SCORE: ' + str(score), 1, (255, 255, 255))

    player.draw(win)
    for a in asteroids:
        a.draw(win)
    for b in playerBullets:
        b.draw(win)

    if gameover:
        win.blit(playAgainText, (sw//2 - playAgainText.get_width()//2, sh//2 - playAgainText.get_height()//2))
    win.blit(scoreText, (25, 75))
    win.blit(livesText, (25, 25))
    pygame.display.update()


player = Player()
playerBullets = []
asteroids = []
count = 0
run = True
while run:
    clock.tick(144)
    count += 1
    if not gameover:
        if count % 50 == 0:
            ran = random.choice([1, 1, 1, 2, 2, 3])
            asteroids.append(Asteroid(ran))
        player.updateLocation()
        for b in playerBullets:
            b.move()
            if b.checkOffScreen():
                playerBullets.pop(playerBullets.index(b)) # to save memory

        for a in asteroids:
            a.x += a.xv
            a.y += a.yv

            # check for player collision with asteroid, removing a life
            if (player.x >= a.x and player.x <= a.x + a.w) or (player.x + player.w >= a.x and player.x + player.w <= a.x + a.w):
                if (player.y >= a.y and player.y <= a.y + a.h) or (player.y + player.h >= a.y and player.y + player.h <= a.y + a.h):
                    lives -= 1
                    asteroids.pop(asteroids.index(a))
                    break

            # check for bullet collision, removing the asteroid when it gets shot
            for b in playerBullets:
                if (b.x >= a.x and b.x <= a.x + a.w) or (b.x + b.w >= a.x and b.x + b.w <= a.x + a.w):
                    if (b.y >= a.y and b.y <= a.y + a.h) or (b.y + b.h >= a.y and b.y + b.h <= a.y + a.h):
                        if a.rank == 3: # spawn two smaller asteroids when an asteroid gets shot
                            score += 10
                            na1 = Asteroid(2) # so new asteroids spawn where the old one got shot
                            na2 = Asteroid(2)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        elif a.rank == 2:
                            score += 20
                            na1 = Asteroid(1)
                            na2 = Asteroid(1)
                            na1.x = a.x
                            na2.x = a.x
                            na1.y = a.y
                            na2.y = a.y
                            asteroids.append(na1)
                            asteroids.append(na2)
                        else:
                            score += 30
                        asteroids.pop(asteroids.index(a))
                        playerBullets.pop(playerBullets.index(b))

        if lives <= 0:
            gameover = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.turnLeft()
        if keys[pygame.K_d]:
            player.turnRight()
        if keys[pygame.K_w]:
            player.moveForward()
        if keys[pygame.K_LEFT]:
            player.turnLeft()
        if keys[pygame.K_RIGHT]:
            player.turnRight()
        if keys[pygame.K_UP]:
            player.moveForward()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN: # instead of key detection in the while loop, so user can't hold down space to shoot
            if event.key == pygame.K_SPACE:
                if not gameover:
                    playerBullets.append(Bullet())
                else:
                    gameover = False
                    lives = 3
                    asteroids.clear()

    redrawGameWindow()
pygame.quit()
