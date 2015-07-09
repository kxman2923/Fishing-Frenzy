###################################################
#          Player class for Fishin' Frenzy
#                 by Willy Vasquez
#


import random, math, pygame, os, sys
from pygame.locals import *

points = 0
fishcount = 0
sharkcount = 0
jellycount = 0
white=[255,255,255]
black=[0,0,0]

#########load_image function (from Chimp example)####################     
def load_image(name, colorkey=None):
    try:
        image = pygame.image.load(name)
    except pygame.error, message:
        print 'Cannot load image:', name
        raise SystemExit, message
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(image.get_at((0,0)), RLEACCEL)
    return image, image.get_rect()

###############AquaFish#######################

class AquaFish(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.setLocation()
        self.setDirection()
        self.fish_red = pygame.image.load("redfish.bmp").convert()
        self.fish_blue = pygame.image.load("bluefish.bmp").convert()
        self.fish_green = pygame.image.load("greenfish.bmp").convert()
        self.sharkimage = pygame.image.load("sharksprite.bmp").convert()
        self.jellyimage = pygame.image.load("jellyfishsprite.bmp").convert()        
        self.fish_red.set_colorkey(self.fish_red.get_at((0,0)), RLEACCEL)
        self.fish_blue.set_colorkey(self.fish_blue.get_at((0,0)), RLEACCEL)
        self.fish_green.set_colorkey(self.fish_green.get_at((0,0)), RLEACCEL)
        self.sharkimage.set_colorkey(self.sharkimage.get_at((0,0)), RLEACCEL)
        self.jellyimage.set_colorkey(self.jellyimage.get_at((0,0)), RLEACCEL)

    def getLocation(self):
        return self.location

    def setLocation(self):
        #depending on the range of grid
        self.x = random.randint(0,560)
        self.y = random.randint(0,560)
        self.location = self.x, self.y
        
    def getDirection(self):
        return self.direction

    def setDirection(self, degrees = (random.randint(0,8)*45)):
        x = random.randint(1,2)
        if degrees % 90 == 0:
            degrees = (degrees + 180)%360
            if x %2==0:
                self.direction = degrees +45
            else:
                self.direction = degrees
        else:
            self.direction =  (degrees+90)%360
            if x %2==0:
                self.direction = degrees + 45
            else:
                self.direction = degrees
        
    def move(self):
        if (self.y <= 0) or (self.y >= 560) or (self.x >= 560) or (self.x <= 0):
            self.setDirection(self.direction)
            #print("x: " + str(self.x) + " y: " + str(self.y))
        if self.direction == 0:
            self.y += 5
        if self.direction == 45:
            self.x += 5
            self.y += 5
        if self.direction == 90:
            self.x += 5
        if self.direction == 135:
            self.x += 5
            self.y -= 5
        if self.direction == 180:
            self.y -= 5
        if self.direction == 225:
            self.y -= 5
            self.x -= 5
        if self.direction == 270:
            self.x -= 5
        if self.direction == 315:
            self.x -= 5
            self.y += 5

    def create(self,screen,tipo,x,y,color = "none"):
        #draw a sprite depending on what the type is on a certain part of the screen
        #show the sprite
        """if tipo == redFish:
            screen.blit(fish_red, [x, y])
        if tipo == blueFish:
            screen.blit(fish_blue, [x,y])
        if tipo == greenFish:
            screen.blit(fish_green, [x,y])"""        
        if tipo == Fish:
            if color == "red":
                screen.blit(self.fish_red, [x, y])
                pass
            if color == "blue":
                screen.blit(self.fish_blue, [x,y])
                pass
            if color == "green":
                screen.blit(self.fish_green, [x,y])
                pass
        if tipo == JellyFish:
            #draw JellyFish sprite:
            print "Jelly created"
            pass
        if tipo == Shark:
            #screen.blit(sharkimage, [x,y])
            print "shark created"
            pass
        
        self.setLocation()
        self.setDirection()
        pass

    def destroy(self,tipo):
        global sharkcount
        global jellycount
        global fishcount
        #stops showing sprite on game screen and removes entity from game grid
        #will be overloaded by subclasses
        if isinstance(tipo,Shark):
            sharkcount = 0
            #code to remove shark instance
        if isinstance(tipo,JellyFish):
            #code to remove jelly instance
            jellycount -= 1 #if we get negatives we may end up getting more than one jelly
        if isinstance(tipo,Fish):
            fishcount -= 1
            #code to remove fish instance

############Fish#################3    
class Fish(AquaFish):
    
    def __init__(self):
        x = random.randint(0,20)
        if x <= 10:
            self.color = "blue"
            self.point = 1
            self.image, self.rect = load_image('bluefish.bmp',-1)
        if x > 10 and x <= 17:
            self.color = "green"
            self.point = 2
            self.image, self.rect = load_image('greenfish.bmp',-1)
        if x > 17:
            self.color = "red"
            self.point = 3
            self.image, self.rect = load_image('redfish.bmp',-1)
        self.fish_red = pygame.image.load("redfish.bmp").convert()
        self.fish_blue = pygame.image.load("bluefish.bmp").convert()
        self.fish_green = pygame.image.load("greenfish.bmp").convert()       
        self.fish_red.set_colorkey(self.fish_red.get_at((0,0)), RLEACCEL)
        self.fish_blue.set_colorkey(self.fish_blue.get_at((0,0)), RLEACCEL)
        self.fish_green.set_colorkey(self.fish_green.get_at((0,0)), RLEACCEL)

        self.setLocation()

    def eaten(self, obj):
        global points
        if isinstance(obj, Shark):
            self.destroy(self)
        else:
            points += self.point
            self.destroy(self)
        """if isinstance(obj, Player):
            points += self.point
            self.destroy(self)"""

    def create(self,screen,x,y,color,tipo="Fish"): 
        if color == "red":
            screen.blit(self.fish_red, [x, y])
            pass
        if color == "blue":
            screen.blit(self.fish_blue, [x,y])
            pass
        if color == "green":
            screen.blit(self.fish_green, [x,y])
            pass
    def getImage(self):
        return self.image
    def getRect(self):
        return self.rect

##############Shark###############
class Shark(AquaFish):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.sharkimage = pygame.image.load("sharksprite.bmp").convert()
        self.sharkimage.set_colorkey(self.sharkimage.get_at((0,0)), RLEACCEL)
        AquaFish.__init__(self)
        self.image, self.rect = load_image('sharksprite.bmp',-1)

    def create(self,screen,x,y,color="none",tipo="Shark"):
        screen.blit(self.sharkimage,[x,y])

    def eat(self,target):
        hit = self.rect.inflate(-5,-5)
        return hit.colliderect(target.rect)

    def sharkAttack(self):
        global sharkcount
        if sharkcount == 0:
            return False
        else:
            return True
        #if there already exists an instance of a shark then do nothing this
        #will return a boolean if there already is one or not
    
    def clickShark(self):
        pos = pygame.mouse.get_pos()
        if self.x < pos[0] and pos[0] < self.x+40 and self.y <= pos[1] and self.y+40 >= pos[1]:
            return True
        else:
            return False

    def timetodie(self):
        #timer runs out so it's time to die
        self.destroy(self)

    def getImage(self):
        return self.sharkimage
    def getRect(self):
        return self.rect
        
##############JellyFish##################
        
class JellyFish(AquaFish):
    def __init__(self):
        global jellycount
        self.jellyimage = pygame.image.load("jellyfishsprite.bmp").convert()
        self.jellyimage.set_colorkey(self.jellyimage.get_at((0,0)), RLEACCEL)
        AquaFish.__init__(self)
        self.image, self.rect = load_image('jellyfishsprite.bmp',-1)
        self.followPlayer()
            
    def create(self,screen,x,y,color="none",tipo="JellyFish"):
        screen.blit(self.jellyimage,[x,y])
        
    def lockPlayer(self):
        #Once it locks the player it should go ahead and die
        self.destroy(self)
        x = 0
        while x < 4000:
            pygame.mouse.set_visible(0) # this will make the mouse not visible for awhile
            x += 1
        pygame.mouse.set_visible(1)
        pass
    def followPlayer(self):
        #gets information from the player.cursor and will continuesly follow it
        self.move()
        
    def clickJelly(self):
        pos = pygame.mouse.get_pos()
        if self.x <= pos[0] and pos[0] <= self.x+40 and self.y <= pos[1] and self.y+40 >= pos[1]:
            return True
        else:
            return False
    def getImage(self):
        return self.image
    def getRect(self):
        return self.rect

def __main__():
    pygame.init()

    screen = pygame.display.set_mode([800,600])

    pygame.display.set_caption("Fishin' Frenzy")

    background = pygame.Surface(screen.get_size())
    background.fill(white)
    screen.blit(background, [0,0])

    sharkimage = pygame.image.load("sharksprite.bmp").convert()
    jellyimage = pygame.image.load("jellyfishsprite.bmp").convert()
    sharkimage.set_colorkey(sharkimage.get_at((0,0)), RLEACCEL)
    jellyimage.set_colorkey(jellyimage.get_at((0,0)), RLEACCEL)

    background_position=[0,0]
    #This is to make the outer part of each image transperant
    done = False
    clock = pygame.time.Clock()
    n = 0
    seconds = 0
    shark = Shark()
    jelly = JellyFish()
    #allsprites = pygame.sprite.RenderPlain((shark, jelly))
    x = random.randint(1,100)
    fishy = []
    for i in range(x):
        fish=Fish()
        fishy.append(fish)
        fish.create(screen,fish.x,fish.y,fish.color)

    while done == False:
        clock.tick(30)
        n += 1
        if n%30 == 0:
            seconds += 1
            
        if seconds == 60:
            done = True
                
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if shark.clickShark():
                    done = True
                if jelly.clickJelly():
                    jelly.lockPlayer()
                    
            if shark.eat(fishy[x-1]):
                fishy[x-1].eaten(shark)
            
                
                    

        if fishcount > 20 and seconds > 20:
            shark.create(screen,shark.x,shark.y)
            shark.move()
        if n > 50:
            jelly.create(screen, jelly.x,jelly.y)
            jelly.followPlayer()

        #allsprites.update()
        #screen.blit(background, (0, 0))
        #allsprites.draw(screen)
        #pygame.display.flip()
        pygame.display.update()

    pygame.quit()


