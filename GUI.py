# FishinFrenzy\GUI.py
# Sabina Maddila
# 01.20.2012

# *Classes:
# - color()
# - button()
# - Grid()
#    - Location()
# * squareGroup(LayeredUpdates)
#    - base_square()
#    - playing_square()
# * gridGroup(LayeredUpdates)
#    - weather_board()
#    - gridLines()
# - user_grid()
#    - user_square()
# - intro_screen()
# - main_screen()

# **Fuctions:
# - __main__()

import pygame, os, sys, random
from pygame.locals import *
from playerModule import AquaFish, Fish,Shark,JellyFish,load_image

points = 0
lives=3
isfrozen=False
freezeTime= 0
freezeDuration=5
fishcount = 0
sharkcount = 0
jellycount = 0
clock= pygame.time.Clock()
duration = 120
frame=0
time=0
###
class color:
    white = (255, 255, 255)
    black = (0, 0, 0)
    gray = (126, 139, 163)
    ocean = (72, 156, 224)
    
    green = (85, 242, 46)
    red = (245, 12, 12)
    very_light_gray = (220, 223, 227)
    rain = (11, 89, 153)
    
    def __init__(self):
        pass

###
class button():
    def __init__(self, title, font, surface, area, surfaceColor = color.gray, regTextColor = color.black):
        # Initializes class variables
        self.title = title
        self.font = font
        self.surface = surface
        self.area = area
        self.surfaceColor = surfaceColor
        self.regTextColor = regTextColor

        # Makes physical outline of widget
        self.widgetBody = pygame.draw.rect(surface, surfaceColor, area)

        # Adds Text
        self.widgetTitle = font.render(title, True, regTextColor)
        self.widgetTitleRect = self.widgetTitle.get_rect()
        self.widgetTitleRect.centerx = self.widgetBody.centerx
        self.widgetTitleRect.centery = self.widgetBody.centery

        self.surface.blit(self.widgetTitle, self.widgetTitleRect)

    def get_rect(self):
        return self.widgetBody
        
    def mouse_is_hovering(self):
        # Returns a Boolean that determines whether or not the mouse is /
        # hovering over the button
        mousePosition = pygame.mouse.get_pos()
        mouseX = mousePosition[0]
        mouseY = mousePosition[1]

        if mouseX > self.area[0] and mouseX < self.area[2] + self.area[0]:
            if mouseY > self.area[1] and mouseY < self.area[3] + self.area[1]:
                return True
            else: return False
        else: return False
        
    def hover(self,  hoverTextColor = color.white, hoverButtonColor = color.gray):
        # Changes button when user hovers over it
        
        # Redraws physical button
        button = pygame.draw.rect(self.surface, hoverButtonColor, self.area)

        # Adds Text, but with hoverTextColor
        buttonText = self.font.render(self.title, True, hoverTextColor)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.centerx = button.centerx
        buttonTextRect.centery = button.centery

        self.surface.blit(buttonText,buttonTextRect)

    def original_color (self):
        # Redraws physical button
        button = pygame.draw.rect(self.surface, self.surfaceColor, self.area)
        
        # Adds Text, but returns to original color
        buttonText = self.font.render(self.title, True, self.regTextColor)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.centerx = button.centerx
        buttonTextRect.centery = button.centery

        self.surface.blit(buttonText, buttonTextRect)
    #Updates the button to change the text
    def update(self, title):
        # Redraws physical button
        button = pygame.draw.rect(self.surface, self.surfaceColor, self.area)
        
        # Adds Text, but returns to original color
        buttonText = self.font.render(title, True, self.regTextColor)
        buttonTextRect = buttonText.get_rect()
        buttonTextRect.centerx = button.centerx
        buttonTextRect.centery = button.centery
        self.surface.blit(buttonText,buttonTextRect)

###
class Location():
   def __init__(self, grid, row, col, isFull = False, isAbyss = False):
        self.grid = grid

        self.row = row
        self.col = col
        self.isFull = isFull
        self.isAbyss = isAbyss
        
        self.content = None

   # Returns the Location in string format
   def __str__(self):
       return str((self.row, self.col))

   def return_position(self):
       return (self.row, self.col)

   # Fills an Location object with actor
   def add(self, obj):
       self.content = obj
       self.isFull = True
       return self.content

   # Removes actor in location
   def remove_object(self):
       obj = self.content
       self.isFull = False
       self.content = None
       return obj

   # Returns actor in location
   def get(self):
       return self.content

   # Returns important values
   def get_row(self):
       return self.row

   def get_col(self):
       return self.col

   def get_grid(self):
       return self.grid

   def is_full(self):
       return self.isFull

   def is_Abyss(self):
       return self.isAbyss

   def make_Abyss(self):
       self.isAbyss = True
       return self.isAbyss

   def remove_Abyss(self):
       self.isAbyss = False
       return self.isAbyss

   # Compares two Location objects in terms of coordinates
   def equals(self, locationObject):
       if self.grid == locationObject.get_grid():
           if self.row == locationObject.get_row() and self.col == locationObject.get_col():
               return True
           else: return False
       else: return False
   
class Grid():
   # Creates an Grid full of empty Location objects
   def __init__(self, numRows = 15, numCols = 15):
       self.totalRows = numRows
       self.totalCols = numCols

       self.fog = False
       self.rain = False
        
       self.tab = {}

       # Creates list that stores Location objects
       self.grid = []
       for row in range(self.totalRows):
           for col in range (self.totalCols):
               interim_location = Location(self, row, col)
               self.tab[interim_location.return_position()] = interim_location.is_full()
               self.grid.append(interim_location)

   def __str__(self):
       return str(self.tab)

   # returns Location object in self.grid
   def get_location(self, row, col):
       return self.grid[row*self.totalRows + col]

   # Checks to see if the Location object is full
   def locationFull(self, row, col):
       return self.get_location(row, col).is_full()
    
   # Checks to see if an location object is in an abyss
   def isAbyss(self, row, col):
       return self.get_location(row, col).is_Abyss()

   # Both changes weather (rain or fog) and returns True or False whether or not rain or fog present
   def make_it_fog(self):
       self.fog = True
       return self.fog

   def lose_the_fog(self):
       self.fog = False
       return self.fog

   def isFogging(self):
       return self.fog

   def make_it_rain(self):
       self.rain = True
       return self.rain

   def lose_the_rain(self):
       self.rain = False
       return self.rain

   def isRaining(self):
       return self.rain

   # Get dimensions of the Grid object
   def get_totalRows(self):
       return self.totalRows

   def get_totalCols(self):
       return self.totalCols

   # Adds an object to the Grid at a certain Location
   def addObjectToGrid(self, obj, row, col):
       self.get_location(row, col).add(obj)
       self.tab[(row, col)]=self.get_location(row, col).is_full()

   # Removes a object at a certain Location
   def removeObjectFromGrid(self, obj, row, col):
       self.get_location(row, col).remove_object()
       self.tab[(row,col)]=self.get_location(row,col).is_full()

   # Get the contents of a Location object
   def getObject(self, row, col):
       return self.get_location(row, col).content

                  
###       
class base_square(pygame.sprite.Sprite):
    def __init__(self, surface, LocationClassObject, side = 40):
        # Calls Sprite constructor
        pygame.sprite.Sprite.__init__(self)

        # Initialize key variables
        # Assumes a LocationClassObject such that the functions get_row() and get_col() exist
        self.grid = LocationClassObject.get_grid()
        self.row = LocationClassObject.get_row()
        self.col = LocationClassObject.get_col()

        self.loc = LocationClassObject

        self.side = int(side)
        self.surface = surface
        self.isAbyss = LocationClassObject.is_Abyss()
        self.rect = pygame.Rect(self.col*self.side, self.row*self.side, self.side, self.side)

        # Draws either an openOcean(color.ocean) or Abyss square(color.black)
        if self.isAbyss: Abyss = pygame.draw.rect(self.surface, color.black, self.rect)
        else: openOcean = pygame.draw.rect(self.surface, color.ocean, self.rect)

    def make_Abyss(self):
        self.isAbyss = self.loc.make_Abyss()
        return self.isAbyss

    def undo_Abyss(self):
        self.isAbyss = self.loc.remove_Abyss()
        return self.isAbyss

    def get_rect(self):
        # Returns rectangle
        return self.rect
            
    def update(self):
        # Redraws either and openOcean or Abyss square
        if self.isAbyss: return pygame.draw.rect(self.surface, color.black, self.rect)
        else: return pygame.draw.rect(self.surface, color.ocean, self.rect)

class playing_square(base_square):
    def __init__(self, surface, location, side = 40):
        # Calls base_square constructor
        base_square.__init__(self, surface, location, side = 40)
        self.loc=location
        # First determines if there is a player object at location, then returns the object
        # Assumes LocationClassObject has both a playerExists() Boolean method and a get_player() method
        if self.loc.is_full():
            self.AquaFish = self.loc.get()
    
    def draw_AquaFish(self,aquaFish):
        # Get and align AquaFishImage and AquaFishImageRect
        if isinstance(aquaFish,AquaFish):
            AquaFishImage = aquaFish.getImage()
            AquaFishImageRect = aquaFish.getRect()
            AquaFishImageRect.centerx = self.rect.centerx
            AquaFishImageRect.centery = self.rect.centery

            # Draw sprite
            return self.surface.blit(AquaFishImage, AquaFishImageRect)
        else:
            return 
 
    def update(self):
        # First determine if there is a player object at location, then draws the object (or abyss)
        if self.loc.is_full():
            self.AquaFish = self.loc.get()
            self.draw_AquaFish(self.AquaFish)
        elif self.loc.is_Abyss():
            row= self.loc.get_row()
            col= self.loc.get_col()
            rect= (col*self.side,row*self.side, self.side,self.side)
            return self.surface.fill((0,0,0),rect)
        else:
            return

###
class weather_board(pygame.sprite.Sprite):
    def __init__(self, surface, gridObject, sideLength = 40):
        # Calls Sprite constructor
        pygame.sprite.Sprite.__init__(self)

        # Initialize key varables
        self.surface = surface
        self.numRows = gridObject.get_totalRows()
        self.numColumns = gridObject.get_totalCols()
        self.side = sideLength
        self.isRain = gridObject.isRaining()
        self.isFog = gridObject.isFogging()

        self.weatherSurface = pygame.Surface((self.numColumns*self.side, self.numRows*self.side))
        self.weatherSurface.set_colorkey()
             
    def clear_weather(self):
        # 'Draws' clear weather
        pass

    def rain(self):
        # Randomly generate raindrops on weatherSurface
        for num in range(500):
            xPos = random.randint(0, self.numColumns*self.side)
            yPos = random.randint(0, self.numRows*self.side)
            pygame.draw.circle(self.surface, color.rain, (xPos, yPos), 3)
            
    def fog(self):
        pygame.draw.rect(self.surface, color.very_light_gray, (0, 0, self.numColumns*self.side, self.numRows*self.side))

    def makeRain(self):
        self.isRain = True
        return self.isRain

    def removeRain(self):
        self.isRain = False
        return self.isRain

    def makeFog(self):
        self.isFog = True
        return self.isFog

    def removeFog(self):
        self.isFog = False
        return self.isFog

    def update(self):
        if self.isFog:
            self.fog()
        elif self.isRain:
            self.rain()
        else: self.clear_weather()

class gridLines(pygame.sprite.Sprite):
    def __init__(self, surface, gridObject, side = 40):
        # Calls Sprite constructor
        pygame.sprite.Sprite.__init__(self)

        # Initialize key variables
        self.surface = surface
        self.numRows = gridObject.get_totalRows()
        self.numColumns = gridObject.get_totalCols()
        self.side = side

        self.playScreenWidth = self.numColumns*side
        self.playScreenHeight = self.numRows*side
        
    def draw(self):
        for x in range(self.numColumns + 1):
            pygame.draw.line(self.surface, color.black, (x*self.side, 0), (x*self.side, self.playScreenHeight))

        for y in range(self.numRows + 1):
            pygame.draw.line(self.surface, color.black, (0, y*self.side), (self.playScreenWidth, y*self.side))

    def update(self):
        self.draw()

###    
class user_square(pygame.sprite.Sprite):
    def __init__(self, surface, LocationClassObject, side = 40):
        # Calls base_square constructor
        pygame.sprite.Sprite.__init__(self)

        # Initialize key variables
        # Assumes a LocationClassObject such that the functions get_row() and get_col() exist
        self.row = LocationClassObject.get_row()
        self.col = LocationClassObject.get_col()
        self.grid = LocationClassObject.get_grid()
        self.side = int(side)
        self.surface = surface
        self.rect = pygame.Rect(self.col*self.side, self.row*self.side, self.side, self.side)

    
    def mouse_is_hovering(self):
        # Returns True if hovering
        mousePosition = pygame.mouse.get_pos()
        mouseX = mousePosition[0]
        mouseY = mousePosition[1]

        if mouseX > self.col*self.side and mouseX < self.col*self.side + self.side:
            if mouseY > self.row*self.side and mouseY < self.row*self.side + self.side:
                return True
            else: return False
        else: return False

    def hover(self):
        # Redraws user_square layer
        cursorRect = pygame.Rect(self.col*self.side, self.row*self.side, self.side, self.side)
        return pygame.draw.rect(self.surface, color.red, cursorRect, 4)

    def return_cursorRect(self):
        return pygame.Rect(self.col*self.side, self.row*self.side, self.side, self.side)

    def returnLocation(self):
        return Location(self.grid, self.row, self.col)

    def get_rect():
        return self.rect

class user_grid():
    def __init__(self, surface, gridObject, side = 40):
        # Initalize key variables
        self.surface = surface
        self.totalRows = gridObject.get_totalRows()
        self.totalCols = gridObject.get_totalCols()
        self.side = side

        self.playingFieldWidth = self.totalCols*side
        self.playingFieldHeight = self.totalRows*side

        self.userGrid = []

        # Assumes a LocationClassObject
        # Fills playing space with user_square objects
        for row in range(self.totalRows):
            for col in range(self.totalCols):
                location = gridObject.get_location(row, col)
                self.userGrid.append(user_square(self.surface, location, self.side))

    def get_square(self, Location):
        row = Location.get_row()
        col = Location.get_col()

        return self.userGrid[row*15 + col]

    def get_square(self, row, col):
        return self.userGrid[row*15 + col]

    def mouse_on_board(self):
        mousePosition = pygame.mouse.get_pos()
        mouseX = mousePosition[0]
        mouseY = mousePosition[1]
        
        row = 0
        col = 0

        for numX in range(0, self.playingFieldWidth, self.side):
            for numY in range(0, self.playingFieldHeight, self.side):
                if numY <= mouseY:
                    row = numY/self.side
                else: break
            if numX <= mouseX:
                col = numX/self.side
            else: break
        if row < self.totalRows and col < self.totalCols:
            return True
        else: return False

    def mouse_move(self):
        mousePosition = pygame.mouse.get_pos()
        mouseX = mousePosition[0]
        mouseY = mousePosition[1]
        
        row = 0
        col = 0

        for numX in range(0, self.playingFieldWidth, self.side):
            for numY in range(0, self.playingFieldHeight, self.side):
                if numY <= mouseY:
                    row = numY/self.side
                else: break
            if numX <= mouseX:
                col = numX/self.side
            else: break

        return self.get_square(row, col)

    def mouse_hover(self):
        return self.mouse_move().hover()

    def mouse_click(self):
        if self.mouse_on_board():
            observed_square = self.mouse_move()
            return observed_square.returnLocation()
        else:
            return
###
class screen():
    # Initialize screen
    def __init__(self,fontFileName,fontSize):
        self.fontFileName = fontFileName
        self.fontSize = fontSize

    # Draw screen
    def draw(self): pass

    #Handle events
    def event(self): pass

###
class intro_screen(screen):
    def draw(self):
        # Sets size and displays introductory screen
        introSize = (350, 350)
        introScreen = pygame.display.set_mode(introSize)
        pygame.display.set_caption ("Welcome to Fishin' Frenzy")

        basicFont = pygame.font.Font(self.fontFileName, self.fontSize)

        # Draw background and background Elements
        introScreen.fill(color.gray)

        introLayerSize = (320, 320)
        introLayerDestination = (15, 15)

        introLayer = pygame.Surface(introLayerSize)
        introLayer.fill(color.white)

        introLayer = introScreen.blit(introLayer, introLayerDestination)

        # Draws play and cancel buttons
        self.playButtonArea = (30, 275, 130, 50) 
        self.playButton = button('PLAY', basicFont, introScreen, self.playButtonArea, color.green)

        self.cancelButtonArea = (190, 275, 130, 50)
        self.cancelButton = button('CANCEL', basicFont, introScreen, self.cancelButtonArea, color.ocean)

        # Loads logo image
        logo = pygame.image.load("FishinFrenzyLOGO.png")
        logo = logo.convert()
        logoRect = logo.get_rect()
        logoRect.centerx = introLayer.centerx
        logoRect.centery = 140
        introScreen.blit(logo, logoRect)

        pygame.display.update()

    def event(self):
        try:
            while True:
                for event in pygame.event.get():
                    # If user exits the screen
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    # If user presses/uses playButton
                    if self.playButton.mouse_is_hovering():
                        self.playButton.hover()
                        pygame.display.update([self.playButton.get_rect()])
                        if True in pygame.mouse.get_pressed():
                            pygame.display.quit()
                            return True
                    else:
                        self.playButton.original_color()
                        pygame.display.update([self.playButton.get_rect()])

                    # If user presses/uses cancelButton
                    if self.cancelButton.mouse_is_hovering():
                        self.cancelButton.hover()
                        pygame.display.update([self.cancelButton.get_rect()])
                        if True in pygame.mouse.get_pressed():
                            pygame.quit()
                            sys.exit()
                    else:
                        self.cancelButton.original_color()
                        pygame.display.update ([self.cancelButton.get_rect()])

        except SystemExit:
            pygame.quit()

###
class main_screen(screen):
    def draw(self):
        size = (850, 600)
        background = pygame.display.set_mode(size)
        pygame.display.set_caption ("Fishin' Frenzy")
        background.fill(color.gray)

        # Initializing playing surface
        self.playScreenSize = (600, 600)
        self.playScreen = pygame.Surface(self.playScreenSize)
        self.playScreen.fill(color.ocean)
        self.playScreenRect = background.blit(self.playScreen, (0, 0))

        # Drawing initial playing surface
        totalRows = 15
        totalColumns = 15
        sideLength = 40
        
        self.grid = Grid(totalRows, totalColumns)
        
        # Types of sprites included in squareGroup(LayeredUpdates): base_square, playing_square
        self.playingFieldWidth = totalColumns*sideLength
        self.playingFieldHeight = totalRows*sideLength

        self.baseGrid = []
        self.playingGrid = []
        self.layeredGrid = []

        for row in range(totalRows):
            for col in range(totalColumns):
                location = self.grid.get_location(row, col)
                
                base = base_square(background, location, sideLength)
                self.baseGrid.append(base)
                
                actor = playing_square(background, location, sideLength)
                self.playingGrid.append(actor)
                
                self.layeredGrid.append(pygame.sprite.LayeredUpdates(base, actor))
                self.layeredGrid[row*15 + col].update()

        # gridGroup(LayeredUpdates): base_square, playing_square)
        self.weather = weather_board(background, self.grid, sideLength)
        #randWeather(self.weather) , Uncomment to randomly set weather (optional)
        self.gridline = gridLines(background, self.grid, sideLength)

        self.gridGroupSprites = pygame.sprite.LayeredUpdates((self.weather, self.gridline))
        self.gridGroupSprites.update()

        self.user_input = user_grid(background, self.grid, sideLength)

        basicFont = pygame.font.Font(self.fontFileName, self.fontSize)
        smallerFont = pygame.font.Font(self.fontFileName, self.fontSize - 5)

        # Draws play and cancel buttons
        self.restartButtonArea = (635, 470, 130, 50) 
        self.restartButton = button('RESTART', basicFont, background, self.restartButtonArea, color.green)

        self.quitButtonArea = (635, 535, 130, 50)
        self.quitButton = button('QUIT', basicFont, background, self.quitButtonArea, color.red)

        #Draw timer, freeze timer, lives, and points buttons
        global points
        self.pointArea= (635, 200,160,60)
        self.pointButton=button('Points:'+ str(points),basicFont,background,self.pointArea, color.gray)

        global time
        global duration
        self.timerArea= (635, 60, 160, 60)
        self.timerButton=button(str(duration-time)+" seconds", basicFont,background,self.timerArea, color.gray)

        global lives
        self.lifeArea= (635, 270, 160, 60)
        self.lifeButton=button("Lives:"+str(lives),basicFont,background,self.lifeArea,color.gray)

        global freezeTime
        global freezeDuration

        self.freezeArea= (645, 130, 160,60)
        self.freezeButton=button("Frozen:"+str(freezeDuration-freezeTime)+ " seconds", basicFont, background,self.freezeArea,color.gray)
       
        pygame.display.update()

    #Updates the rectangles by drawing the AquaFish objects and/or the abyss objects (automatically draws abyss everywhere)
    def refreshRect(self, location, sideLength = 40):
        if location.get_col() > 0:
            col = location.get_col()
        else: col = 0

        if location.get_row()> 0:
            row = location.get_row()
        else: row = 0

        self.playingGrid[row*15 + col].update()
        self.gridGroupSprites.update()


    # Handles events for main_screen
    def event(self):
        global points
        global time
        global clock
        global frame
        global time
        global lives
        global isfrozen
        global freezeTime
        global freezeDuration
        frame=0
        time=0
        points=0
        lives=3
        pygame.time.wait(1000)
        fillGrid_Fish(self.grid,100)
        fillGrid_Shark(self.grid,4)
        fillGrid_Jelly(self.grid,6)
        try:
            while True:
                clock.tick(30)
                frame+=1
                if frame%30 == 0:
                    time += 1
                    if isfrozen==True:
                        freezeTime+=1
                        if freezeTime==freezeDuration:
                            isfrozen=False
                    else:
                        freezeTime=0
                pygame.display.update([self.timerButton.get_rect(), self.freezeButton.get_rect()])
                self.timerButton.update(str(duration-time)+" seconds")
                self.freezeButton.update("Frozen:"+str(freezeDuration-freezeTime)+ " seconds")
                for event in pygame.event.get():
                    # If user quits the screen
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type==MOUSEBUTTONDOWN:
                        if isfrozen==False:
                            self.user_input.mouse_hover()
                            loc = self.user_input.mouse_click()
                            self.refreshRect(loc)
                            pygame.display.update([self.playScreenRect])
                            clickGrid(self.user_input,self.grid)
                        else:
                            pass

                    # If user presses/uses restartButton
                    if self.restartButton.mouse_is_hovering():
                        self.restartButton.hover(color.green, color.white)
                        pygame.display.update([self.restartButton.get_rect()])

                        if True in pygame.mouse.get_pressed():
                            pygame.display.quit()
                            return True
                    else:
                        self.restartButton.original_color()
                        pygame.display.update([self.restartButton.get_rect()])

                    # If user presses/uses quitButton
                    if self.quitButton.mouse_is_hovering():
                        self.quitButton.hover(color.red, color.white)
                        pygame.display.update([self.quitButton.get_rect()])

                        if True in pygame.mouse.get_pressed():
                            pygame.quit()
                            sys.exit()
                    else:
                        self.quitButton.original_color()
                        pygame.display.update ([self.quitButton.get_rect()])
                #Updates the timer and points buttons
                pygame.display.update([self.pointButton.get_rect(), self.lifeButton.get_rect()])
                self.pointButton.update('Points:'+ str(points))
                self.lifeButton.update('Lives:'+str(lives))
                if lives==0 or duration-time==0:
                    pygame.quit()
                    return False
        except SystemExit:
            pygame.quit()

######
class end_screen(screen):
    def draw(self):
        # Sets size and displays introductory screen
        endSize = (400, 450)
        endScreen = pygame.display.set_mode(endSize)
        pygame.display.set_caption ("Play Again?")

        basicFont = pygame.font.Font(self.fontFileName, self.fontSize)

        # Draw background and background Elements
        endScreen.fill(color.gray)

        endLayerSize = (370, 420)
        endLayerDestination = (15, 15)

        endLayer = pygame.Surface(endLayerSize)
        endLayer.fill(color.white)

        endLayer = endScreen.blit(endLayer, endLayerDestination)

        # Draws play and cancel buttons
        self.playButtonArea = (30, 375, 130, 50) 
        self.playButton = button('PLAY', basicFont, endScreen, self.playButtonArea, color.green)

        self.cancelButtonArea = (190, 375, 130, 50)
        self.cancelButton = button('QUIT', basicFont, endScreen, self.cancelButtonArea, color.ocean)
        
        global points
        self.pointArea= (110, 275,200,60)
        self.pointButton=button('Final Score:'+ str(points),basicFont,endScreen,self.pointArea, color.white)

        # Loads logo image
        logo = pygame.image.load("FishinFrenzyLOGO.png")
        logo = logo.convert()
        logoRect = logo.get_rect()
        logoRect.centerx = endLayer.centerx
        logoRect.centery = 120
        endScreen.blit(logo, logoRect)

        pygame.display.update()

    def event(self):
        try:
            global points
            while True:
                pygame.display.update([self.pointButton.get_rect()])
                self.pointButton.update('Final Score:'+ str(points))
                for event in pygame.event.get():
                    # If user exits the screen
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()

                    # If user presses/uses playButton
                    if self.playButton.mouse_is_hovering():
                        self.playButton.hover()
                        pygame.display.update([self.playButton.get_rect()])
                        if True in pygame.mouse.get_pressed():
                            pygame.display.quit()
                            return True
                    else:
                        self.playButton.original_color()
                        pygame.display.update([self.playButton.get_rect()])

                    # If user presses/uses cancelButton
                    if self.cancelButton.mouse_is_hovering():
                        self.cancelButton.hover()
                        pygame.display.update([self.cancelButton.get_rect()])
                        if True in pygame.mouse.get_pressed():
                            pygame.quit()
                            sys.exit()
                    else:
                        self.cancelButton.original_color()
                        pygame.display.update ([self.cancelButton.get_rect()])

        except SystemExit:
            pygame.quit()
####

            
#The following function fills a grid with Fish, Shark, or JellyFish objects (check included)
#If the spot is already fill with an object, the fill functions will place the object in the first
# empty spot if finds in Grid.
def fillGrid_Fish(grid,numberFish,sideLength=40):
    global fishcount
    fishcount=0
    for x in range(numberFish):
        fish=Fish()
        row= fish.y/sideLength
        col= fish.x/sideLength
        isPlaced=False
        if grid.locationFull(row,col)==False:
            grid.addObjectToGrid(fish,row,col)
            fishcount+=1
        else:
            while isPlaced==False:
                rows= range(grid.get_totalRows())
                cols= range(grid.get_totalCols())
                r= random.choice(rows)
                c= random.choice(cols)
                if grid.locationFull(r,c)==False:
                    grid.addObjectToGrid(fish,r,c)
                    fishcount+=1
                    isPlaced=True
                    break
def fillGrid_Shark(grid,numberShark,sideLength=40):
    global sharkcount
    sharkcount=0
    for x in range(numberShark):
        shark=Shark()
        row= shark.y/sideLength
        col= shark.x/sideLength
        isPlaced=False
        if grid.locationFull(row,col)==False:
            grid.addObjectToGrid(shark,row,col)
            sharkcount+=1
        else:
            while isPlaced==False:
                rows= range(grid.get_totalRows())
                cols= range(grid.get_totalCols())
                r= random.choice(rows)
                c= random.choice(cols)
                if grid.locationFull(r,c)==False:
                    grid.addObjectToGrid(shark,r,c)
                    sharkcount+=1
                    isPlaced=True
                    break
def fillGrid_Jelly(grid,numberJelly,sideLength=40):
    global jellycount
    jellycount=0
    for x in range(numberJelly):
        jelly=JellyFish()
        row= jelly.y/sideLength
        col= jelly.x/sideLength
        isPlaced=False
        if grid.locationFull(row,col)==False:
            grid.addObjectToGrid(jelly,row,col)
            jellycount+=1
        else:
            while isPlaced==False:
                rows= range(grid.get_totalRows())
                cols= range(grid.get_totalCols())
                r= random.choice(rows)
                c= random.choice(cols)
                if grid.locationFull(r,c)==False:
                    grid.addObjectToGrid(jelly,r,c)
                    jellycount+=1
                    isPlaced=True
                    break
        
        
#Random weather
def randWeather(weatherBoard):
    weatherChoice=['clear','rain','fog']
    weatherBoard.removeFog()
    weatherBoard.removeRain()
    weatherBoard.clear_weather()
    if random.choice(weatherChoice)=='clear':
        weatherBoard.clear_weather()
    elif random.choice(weatherChoice)=='rain':        
        weatherBoard.makeRain()
    elif random.choice(weatherChoice)=='fog':
        weatherBoard.makeFog()

#When the player clicks the grid, it will catch what is in the square (usergrid and grid must match)
#Assume the object is already drawn
#Increment the player's points (to be determined)
#Removes the object that was clicked on from the grid(image still shows)
def clickGrid(usergrid,grid):
    #Stores the position of the mouse
    loc=usergrid.mouse_click()
    row= loc.get_row()
    col= loc.get_col()
    #Stores the object in the location the mouse clicked on
    obj= grid.getObject(row,col)
    global points
    global lives
    global isfrozen
    #When a fish object is clicked on, the player gets points
    if isinstance(obj,Fish):
        if obj.color=="blue":
            points+=10
        elif obj.color=="green":
            points+=20
        elif obj.color=="red":
            points+=30
        grid.removeObjectFromGrid(obj,row,col)
    #When a shark object is clicked on, the player loses points, loses a life, and a set of abyss forms around it
    elif isinstance(obj,Shark):
        points-=100
        lives-=1
        grid.removeObjectFromGrid(obj,row,col)
        for r in range(row-1,row+2,1):
            for c in range(col-1,col+2,1):
                if r>=0 and c>=0 and r<grid.get_totalRows() and c<grid.get_totalCols():
                    if r==row and c==col:
                        pass
                    else:
                        grid.get_location(r,c).make_Abyss()
                        if grid.locationFull(r,c)==True:
                            grid.removeObjectFromGrid(grid.getObject(r,c),r,c)
    #When a jellyfish object is clicked on, the player is frozen for 5 seconds and loses points
    elif isinstance(obj,JellyFish):
        points-=50
        isfrozen=True
        grid.removeObjectFromGrid(obj,row,col)
    else:
        return
    

# MAIN CODE
def __main__():
    pygame.init()
    continueLoop = True
    intro = intro_screen('C:\\Windows\\Fonts\\Action Man.ttf', 30)
    mainPlay = main_screen(intro.fontFileName, intro.fontSize)
    end= end_screen('C:\\Windows\\Fonts\\Action Man.ttf', 30)
    

    intro.draw()
    if intro.event():
        while continueLoop:
            mainPlay.draw()
            if mainPlay.event():
                continue
            else:                
                pygame.font.init()
                end.draw()
                if end.event():
                    continueLoop=True
                else:
                    continueLoop=False
