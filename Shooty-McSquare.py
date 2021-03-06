import pygame
import random
import sys

class Character:
    def __init__(self, x, y, height, width):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.lives = 3
        self.invulnerable = False
        self.invulnerableStartTime = False
        self.color = (255,255,255)
        self.blinkStart = True
        self.blinkTime = -3000
        self.blinkRate = 100
        self.hitbox = pygame.Rect(self.x, self.y, 75, 75)


    def display(self,surface):
        pygame.draw.rect(surface,self.color , pygame.Rect(self.x, self.y, self.height, self.width), 0)

    def blink(self,newColor):
        if self.blinkStart == True:
            if pygame.time.get_ticks() > self.blinkTime + self.blinkRate:
                self.color = newColor
                self.blinkStart = False
                self.blinkTime = pygame.time.get_ticks()
        elif self.blinkStart == False:
            if pygame.time.get_ticks() > self.blinkTime + self.blinkRate:
                self.color = (255, 255, 255)
                self.blinkStart = True
                self.blinkTime = pygame.time.get_ticks()

    def move(self, screenWidth, screenHeight):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_UP]:
            player.y -= 8
        if pressed[pygame.K_DOWN]:
            player.y += 8
        if pressed[pygame.K_LEFT]:
            player.x -= 8
        if pressed[pygame.K_RIGHT]:
            player.x += 8

        if self.x < 0:
            self.x = 1
        elif self.x > screenWidth - self.width:
            self.x = screenWidth - self.width - 1
        if self.y < 0:
            self.y = 1
        elif self.y > (screenHeight - 100) - self.height:
            self.y = screenHeight - self.height - 101

class Projectile:
    def __init__(self, x, y, direction, color):
        self.x = x
        self.y = y
        self.yVelocity = -30 * direction
        self.color = color
        self.hitbox = pygame.Rect(self.x, self.y, 20, 50)

    def go(self):
        self.y += self.yVelocity

    def display(self, surface):
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x, self.y, 20, 50), 0)

class EnemyShip:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xVelocity = 4
        self.yChange = 20
        self.timeShot = None
        self.hitbox = pygame.Rect(self.x, self.y, 50, 50)


    def display(self, surface):
        pygame.draw.rect(surface, (70, 50, 50), pygame.Rect(self.x, self.y, 50, 50), 0 )

    def move(self):
        self.x += self.xVelocity
        if self.x <= 0 or self.x >= screenWidth - 50:
            self.xVelocity = -(self.xVelocity)
            self.y += self.yChange

        if self.y >= 220:
            self.yChange = -20
        elif self.y <= 0:
            self.yChange = 20

    def shoot(self):
        shoot(self.x/2 + 5, self.y + 50, projectileList, -1)

class Shield:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hitbox = pygame.Rect(self.x, self.y, 85, 85)
        self.active = False
        self.hit = False

    def display(self, screen, player):
        if self.active == True:
            pygame.draw.rect(screen, (0, 150, 255), self.hitbox, 10)

    def defend(self,rect, rectList):
        if self.hitbox.colliderect(rect.hitbox) and self.active == True:
            rectList.remove(rect)
            self.hit = True
            return True
        else:
            self.hit = False
            return False

class Star:
    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.moveRate = None

    def display(self, screen):
        pygame.draw.circle(screen, (150,150,150), ((self.x), (self.y)), (self.radius))

def shoot(x, y, PList, direction, color):
    newProjectile = Projectile(x, y, direction, color)
    PList.append(newProjectile)

def starryBackground(surface):
    starList = []
    for star in range(26):
        star = Star(random.randint(0,790), random.randint(0,690), random.randint(5,11))
        starList.append(star)
        star.moveRate = random.randint(1, 4)
    return starList

def moveStars(surface,sList):
    for star in sList:
        star.display(surface)
        star.y += star.moveRate
        if star.y > screenHeight - 0:
            star.y = -5
            star.x = random.randint(0, 795)
            star.moveRate = random.randint(1, 4)

def createEnemy(x,y, eList):
    newEnemy = EnemyShip(x,y)
    directionChance = random.randint(1,2)
    if directionChance == 1:
        newEnemy.xVelocity = -4
    eList.append(newEnemy)

def displayText(displaySurface, text, x, y, textColor, screenColor, Font):
    text = text + "                                             "
    message = Font.render(text, True, textColor)
    displaySurface.blit(message, (x, y))

player = Character(400,400,75,75)
shield = Shield(player.x, player.y)


pygame.init()
clock = pygame.time.Clock()
screenHeight = 800
screenWidth = 800
screen = pygame.display.set_mode((screenWidth,screenHeight))
done = False
projectileList = []
enemyList = []
timeDestroyed = None
specialActivated = None
specialDeactivated = None
points = 0
lastHit = 0
pygame.display.set_caption("Shooty McSquare")
quit = False
beamFired = False
finished = False
starList = starryBackground(screen)
cooldown = 1000
color = (150,150,150)


font = pygame.font.SysFont('times new roman', 75)
subFont = pygame.font.SysFont('times new roman', 45)
subSubFont = pygame.font.SysFont('times new roman', 35)



while not quit:
    enemyList = []
    createEnemy(random.randint(0, 730), random.randint(0, 200), enemyList)
    createEnemy(random.randint(0, 730), random.randint(0, 200), enemyList)
    createEnemy(random.randint(0, 730), random.randint(0, 200), enemyList)

    while not finished:

        screen.fill((0, 0, 0))
        moveStars(screen, starList)
        displayText(screen, "Shooty McSquare", 120, screenHeight - 550, (0, 255, 255), (0, 0, 0), font)
        displayText(screen, "Press space to start", 210, screenHeight - 450, (255, 255, 255), (0, 0, 0), subFont)
        displayText(screen, "Press 't' for the tutorial", 180, screenHeight - 380, (255, 255, 255), (0, 0, 0), subFont)

        pygame.display.flip()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    finished = True

                elif event.key == pygame.K_t:
                    enemyList = []
                    createEnemy(100,100,enemyList)
                    complete = False
                    called = pygame.time.get_ticks()
                    print("im working")
                    canShoot = False
                    instructionProjectileList = []
                    lastAction = 1000000000000
                    moveOn = False
                    canMove = False
                    showCharacter = False
                    canSpecial = False
                    showLives = False

                    while not complete:

                        screen.fill((0, 0, 0))
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                complete = True
                                sys.exit()
                            if event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_SPACE and canShoot:
                                    if shield.active:
                                        shield.active = False
                                        specialDeactivated = pygame.time.get_ticks()
                                    shoot(player.x + player.width / 2 - 10, player.y - 25,
                                          instructionProjectileList, 1, (255, 0, 0))
                                    if moveOn == False:
                                        lastAction = pygame.time.get_ticks()
                                        moveOn = True

                        moveStars(screen, starList)
                        if showCharacter:
                            player.display(screen)
                        if called + 3000 > pygame.time.get_ticks() > called + 1000:
                            displayText(screen, "The Game Is Simple", 200, 300, (255, 255, 255), (0, 0, 0),
                                        subFont)
                        elif called + 10000 > pygame.time.get_ticks() > called + 3000:
                            displayText(screen, " You, the white square", 175, 300, (255, 255, 255), (0, 0, 0),
                                        subFont)
                        if called + 10000 > pygame.time.get_ticks() > called + 6500:
                            displayText(screen, " must defeat the enemy square ships.", 50, 350,
                                        (255, 255, 255), (0, 0, 0), subFont)
                        if called + 6000 > pygame.time.get_ticks() > called + 5000:
                            player.x = 325
                            player.y = 600
                            showCharacter = True
                        for enemy in enemyList:
                            if pygame.time.get_ticks() > called + 8000:
                                enemy.x = 330
                                enemy.y = 100
                                enemy.hitbox = pygame.Rect(enemy.x, enemy.y, 50, 50)
                                enemy.display(screen)
                        if not moveOn and pygame.time.get_ticks() > called + 11000:
                            displayText(screen, "Press space to fire!", 220, 350, (255, 255, 255), (0, 0, 0),
                                        subFont)
                            canShoot = True
                        for proj in instructionProjectileList:
                            proj.display(screen)
                            proj.go()
                            proj.hitbox = pygame.Rect(proj.x, proj.y, 20, 50)
                            for enemy in enemyList:
                                if proj.hitbox.colliderect(enemy.hitbox):
                                    enemyList.remove(enemy)
                                    instructionProjectileList.remove(proj)

                        if lastAction + 2500 > pygame.time.get_ticks() > lastAction + 1000 and moveOn:
                            displayText(screen, "You got him!", 250, 350, (255, 255, 255), (0, 0, 0), subFont)
                            canMove = True

                        if lastAction + 5000 > pygame.time.get_ticks() > lastAction + 3000 and canMove:
                            displayText(screen, "Use the arrow keys to move.", 150, 350, (255, 255, 255),
                                        (0, 0, 0), subFont)

                        if lastAction +8000 > pygame.time.get_ticks() > lastAction + 5500:
                            displayText(screen, "You can also use Special abilities.", 100, 350, (255, 255, 255), (0, 0, 0), subFont)
                            canSpecial = True

                        if lastAction + 12000 > pygame.time.get_ticks() > lastAction + 8500:
                            displayText(screen, "Press 'w' for a beam,", 225, 300, (255, 255, 255), (0, 0, 0), subFont)
                            displayText(screen, "Press 's' for a shield.", 225, 350, (255, 255, 255), (0, 0, 0), subFont)

                        if lastAction + 15500 > pygame.time.get_ticks() > lastAction + 12500:
                            displayText(screen, "The shield blocks lasers,", 200, 300, (255, 255, 255), (0, 0, 0), subFont)
                            displayText(screen, "but doesn't work against collisions.", 100, 350, (255, 255, 255), (0, 0, 0),
                                        subFont)

                        if lastAction + 19500 > pygame.time.get_ticks() > lastAction + 16000:
                            displayText(screen, "Every time you get hit, you lose a life.", 75, 300, (255, 255, 255), (0, 0, 0), subFont)
                            displayText(screen, "You have three lives.", 220, 350, (255, 255, 255),
                                        (0, 0, 0), subFont)
                            showLives = True

                        if lastAction + 23000 > pygame.time.get_ticks() > lastAction + 20000:
                            displayText(screen, "Every time you hit an enemy,", 125, 300, (255, 255, 255), (0, 0, 0), subFont)
                            displayText(screen, "you gain a point.", 225, 350, (255, 255, 255), (0, 0, 0),
                                        subFont)

                        if lastAction + 26000 > pygame.time.get_ticks() > lastAction + 23000:
                            displayText(screen, "Get the most points you can!", 125, 300, (255, 255, 255), (0, 0, 0), subFont)

                        if canSpecial:
                            pygame.draw.rect(screen, color, pygame.Rect(0, screenHeight - 100, screenWidth, 100))
                            pressed = pygame.key.get_pressed()
                            if ((pressed[
                                     pygame.K_w] and specialDeactivated is None) or beamFired) and not shield.active:
                                beamFired = True
                                if specialActivated == None:
                                    specialActivated = pygame.time.get_ticks()
                                elif pygame.time.get_ticks() <= specialActivated + 500:
                                    shoot(player.x + player.width / 2 - 10, player.y - 30, instructionProjectileList, 1,
                                          (0, 20, 225))
                                elif pygame.time.get_ticks() > specialActivated + 500:
                                    specialDeactivated = pygame.time.get_ticks()
                                    beamFired = False
                            if (pressed[pygame.K_s] and specialDeactivated is None) or shield.active:
                                if specialActivated is None:
                                    specialActivated = pygame.time.get_ticks()
                                    shield.active = True
                                    shield.hit = False
                                if shield.hit:
                                    shield.active = False
                                    specialDeactivated = pygame.time.get_ticks()
                                shield.hitbox = pygame.Rect(player.x - 8, player.y - 8, 90, 90)
                                shield.display(screen, player)

                            if specialDeactivated is not None:
                                if pygame.time.get_ticks() >= specialDeactivated + 3000:
                                    specialActivated = None
                                    specialDeactivated = None
                                    beamFired = False
                                    shield.active = False

                            if specialDeactivated == None:
                                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 40, 75, 25), 0)
                            elif specialDeactivated + 1000 > pygame.time.get_ticks() >= specialDeactivated + 500:
                                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 40, 12, 25), 0)
                            elif specialDeactivated + 1500 > pygame.time.get_ticks() >= specialDeactivated + 1000:
                                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 40, 25, 25), 0)
                            elif specialDeactivated + 2000 > pygame.time.get_ticks() >= specialDeactivated + 1500:
                                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 40, 37, 25), 0)
                            elif specialDeactivated + 2500 > pygame.time.get_ticks() >= specialDeactivated + 2000:
                                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 40, 50, 25), 0)
                            elif specialDeactivated + 3000 > pygame.time.get_ticks() >= specialDeactivated + 2500:
                                pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 40, 62, 25), 0)

                            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(350, screenHeight - 40, 75, 25), 2)
                            displayText(screen, "Energy", 340, screenHeight - 90, (0, 0, 0), (0, 0, 0), subSubFont)
                        if showLives:
                            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(500, screenHeight - 75, 50, 50))
                            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(600, screenHeight - 75, 50, 50))
                            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(700, screenHeight - 75, 50, 50))

                        if showCharacter:
                            player.display(screen)
                        if canMove:
                            player.move(screenWidth, screenHeight)

                        pygame.display.update()
                        clock.tick(60)

                        if lastAction + 1000000 > pygame.time.get_ticks() > lastAction + 26000:
                            complete = True
                            finished = True
                            enemyList = []
                            createEnemy(random.randint(0, 730), random.randint(0, 200), enemyList)
                            createEnemy(random.randint(0, 730), random.randint(0, 200), enemyList)
                            createEnemy(random.randint(0, 730), random.randint(0, 200), enemyList)
                #    print("im working")



    while not done:
        player.hitbox = pygame.Rect(player.x, player.y, 75, 75)

        if len(enemyList) > 3:
            enemyList.remove(enemyList[2])

        screen.fill((0, 0, 0))

        moveStars(screen,starList)


        if player.invulnerable:
            player.blink((0,0,0))
            if pygame.time.get_ticks() > player.invulnerableStartTime + 2000:
                player.invulnerable = False
                player.color = (255,255,255)
                player.blinkStart = True
                player.blinkTime = -3000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit = True
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    shoot(player.x + player.width / 2 - 10, player.y - 25, projectileList, 1, (255,0,0))
                    if shield.active:
                        shield.active = False
                        specialDeactivated = pygame.time.get_ticks()
                if event.key == pygame.K_1:
                    done = True

        for enemy in enemyList:
            enemy.display(screen)
            enemy.move()
            shootCooldown = 2000
            enemy.hitbox = pygame.Rect(enemy.x, enemy.y, 50, 50)


            if enemy.timeShot is None:
                enemy.timeShot = pygame.time.get_ticks()
                #shoot(enemy.x + 25, enemy.y + 50, projectileList, -1, (255,100,0))
                #enemy.timeShot = pygame.time.get_ticks()
            elif pygame.time.get_ticks() > enemy.timeShot + shootCooldown:
                shoot(enemy.x + 25, enemy.y + 50, projectileList, -1, (255,0,0))
                enemy.timeShot = pygame.time.get_ticks()
            if enemy.hitbox.colliderect(player.hitbox) and not player.invulnerable and enemy in enemyList: #I gotta fix this mess
                player.lives -= 1
                shield.active = False
                specialDeactivated = pygame.time.get_ticks()
                player.invulnerableStartTime = pygame.time.get_ticks()
                player.blinkTime = pygame.time.get_ticks()
                player.invulnerable = True
                points += 1
                timeDestroyed = pygame.time.get_ticks()
                enemyList.remove(enemy)

        for projectile in projectileList:
            projectile.go()
            projectile.display(screen)
            projectile.hitbox = pygame.Rect(projectile.x, projectile.y, 20, 50)
            shield.defend(projectile, projectileList)
            if projectile.y < -50 or projectile.y > screenHeight - 100:
                projectileList.remove(projectile)
            for enemy in enemyList:
                if projectile.hitbox.colliderect(enemy.hitbox) and projectile in projectileList:
                    enemyList.remove(enemy)
                    projectileList.remove(projectile)
                    timeDestroyed = pygame.time.get_ticks()
                    points += 1
                if projectile.hitbox.colliderect(player.hitbox) and not player.invulnerable and projectile in projectileList:
                    if pygame.time.get_ticks() > lastHit + cooldown:
                        player.lives -= 1
                        lastHit = pygame.time.get_ticks()
                        projectileList.remove(projectile)
                        player.invulnerable = True
                        player.invulnerableStartTime = pygame.time.get_ticks()
                        player.blinkTime = pygame.time.get_ticks()
        if len(enemyList) < 2:
            timeStamp = pygame.time.get_ticks()
            createEnemy(random.randint(0, 730), random.randint(0, 200), enemyList)



        if timeDestroyed != None and pygame.time.get_ticks() > timeDestroyed + cooldown :
            createEnemy(random.randint(0, 730), random.randint(0, 200), enemyList)
            timeDestroyed = None
            timeShot = None

        player.move(screenWidth, screenHeight)

        pressed = pygame.key.get_pressed()
        if ((pressed[pygame.K_w] and specialDeactivated is None) or beamFired) and not shield.active:
            beamFired = True
            if specialActivated == None:
                specialActivated = pygame.time.get_ticks()
            elif pygame.time.get_ticks() <= specialActivated + 500:
                shoot(player.x + player.width / 2 - 10, player.y - 30, projectileList, 1, (0,20,225))
            elif pygame.time.get_ticks() > specialActivated + 500:
                specialDeactivated = pygame.time.get_ticks()
                beamFired = False
        if (pressed[pygame.K_s] and specialDeactivated is None) or shield.active:
            if specialActivated is None:
                specialActivated = pygame.time.get_ticks()
                shield.active = True
                shield.hit = False
            if shield.hit:
                shield.active = False
                specialDeactivated = pygame.time.get_ticks()
            shield.hitbox = pygame.Rect(player.x - 8, player.y - 8, 90, 90)
            shield.display(screen, player)

        if specialDeactivated is not None:
            if pygame.time.get_ticks() >= specialDeactivated + 3000:
                specialActivated = None
                specialDeactivated = None
                beamFired = False
                shield.active = False

        player.display(screen)
        message = "Points: " + str(points)
        pygame.draw.rect(screen, color, pygame.Rect(0, screenHeight - 100, screenWidth, 100))
        displayText(screen, message, 0, screenHeight - 100, (0, 0, 255), color,font)

        if player.lives == 3:
            pygame.draw.rect(screen, (255,255,255),pygame.Rect(500, screenHeight - 75, 50,50))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(600, screenHeight - 75, 50, 50))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(700, screenHeight - 75, 50, 50))
        elif player.lives == 2:
            pygame.draw.rect(screen, (255,255,255),pygame.Rect(500, screenHeight - 75, 50,50))
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(600, screenHeight - 75, 50, 50))
        elif player.lives == 1:
            pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(500, screenHeight - 75, 50, 50))
        elif player.lives == 0 and pygame.time.get_ticks() < player.invulnerableStartTime + 3500:
            displayText(screen, "One more hit and", 240, screenHeight - 550, (255, 255, 255), (0, 0, 0), subFont)
            displayText(screen, "you're toast!", 280, screenHeight - 475, (255, 255, 255), (0, 0, 0), subFont)

        if specialDeactivated == None:
            pygame.draw.rect(screen, (0,0,255), pygame.Rect(350, screenHeight - 40, 75, 25), 0)
        elif specialDeactivated + 1000 > pygame.time.get_ticks() >= specialDeactivated + 500:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 40, 12, 25), 0)
        elif specialDeactivated + 1500 > pygame.time.get_ticks() >= specialDeactivated + 1000:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 40, 25, 25), 0)
        elif specialDeactivated + 2000 > pygame.time.get_ticks() >= specialDeactivated + 1500:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 40, 37, 25), 0)
        elif specialDeactivated + 2500 > pygame.time.get_ticks() >= specialDeactivated + 2000:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 40, 50, 25), 0)
        elif specialDeactivated + 3000 > pygame.time.get_ticks() >= specialDeactivated + 2500:
            pygame.draw.rect(screen, (0, 0, 255), pygame.Rect(350, screenHeight - 40, 62, 25), 0)

        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(350, screenHeight - 40, 75, 25), 2)
        displayText(screen, "Energy", 340, screenHeight - 90, (0, 0, 0), (0, 0, 0), subSubFont)

        if player.lives == -1:
            for blinks in range(3):
                pygame.draw.rect(screen, (0, 0, 0), pygame.Rect(player.x, player.y, player.height, player.width), 0)
                pygame.display.flip()
                pygame.time.delay(500)
                player.display(screen)
                pygame.display.flip()
                pygame.time.delay(500)
            enemyList = []
            done = True

        pygame.display.flip()
        clock.tick(60)

    screen.fill((0, 0, 0))
    reallyDone = False
    '''
    filename = "ShootyMcSquare.git/blah.txt"
    file = open(filename, "r")
    scoreThing = file.readline().split(" ")
    oldHighScore = (scoreThing[1])
    if points > int(oldHighScore):
        highScore = str(points).rstrip()
    else:
        highScore = str(oldHighScore).rstrip()'''

    while not reallyDone:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                quit = True
                reallyDone = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    reallyDone = True
                    done = False
                    finished = False
                    points = 0
                    player.x = 350
                    player.y = 550
                    projectileList = []
                    player.lives = 3
                    player.invulnerable = True
                    player.invulnerableStartTime = pygame.time.get_ticks()

        screen.fill((0,0,0))
        moveStars(screen, starList)
        displayText(screen, "Game Over", 225, screenHeight - 550, (255, 120, 12), (0, 0, 0), font)
        displayText(screen, "Press 'r' to restart", 250, screenHeight - 450, (255, 255, 255), (0, 0, 0),subFont)


        pygame.display.flip()
        clock.tick(60)