add_library('minim') #sound effects
import os
import random 


path = os.getcwd() # Get current working directory
RESOLUTION1 = 750 #width of mainpage
RESOLUTION2 = 550 #height of mainpage
GROUND = 550
fireboy_score = 0
watergirl_score = 0
winner = ""
player = Minim(this) 

class Platform:
    
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
    
    def display(self):
        fill(150)
        stroke(150)
        rect(self.x,self.y,self.w,self.h)




#PLAYER CLASS    
class Character:
    
    def __init__(self, x, y, r,  img, img_w, img_h, num_slices, type):
        self.x = x
        self.y = y
        self.r = r
        self.type = type
        self.g = GROUND
        self.vx = 0
        self.vy = 0
        self.img = loadImage(path + "/cs/" + img)
        self.img_w = img_w
        self.img_h = img_h
        self.num_slices = num_slices
        self.slice = 0
        self.dir = RIGHT
        self.key_handler = {LEFT:False, RIGHT:False, UP:False}
        self.score = 0
        self.diamond = player.loadFile(path + "/sound/Saf.mp3") #diamond collecting sound
        self.die = player.loadFile(path + "/sound/Death.mp3") #sound when death due to puddle
        self.mybo = player.loadFile(path + "/sound/mybo.mp3") #mysterybox collecting sound

        
    def gravity(self): #gravity of the players
        if self.y + self.r <= self.g:
            self.vy += 0.4
            if self.y + self.r + self.vy > self.g:
                self.vy = self.g - (self.y + self.r)
        else:
            self.vy = 0
            
    
        for platform in game.platforms: #landing on platform after collision
            if self.y +self.r <= platform.y and self.y + self.r <= platform.y + platform.h and self.x  >= platform.x and self.x <= platform.x + platform.w:
                self.g = platform.y
                break
            else:
                self.g = GROUND
    
    def update(self):

        self.gravity()
        #limit the player within the dimensions of the game page
        if self.key_handler[LEFT] == True:
            if self.x == 0 or self.y >= RESOLUTION2 or self.y == 0 : #restrict movement of players when reaching left of game page
                self.vx = 0
                self.x += self.vx
            self.vx = -3
            self.dir = LEFT
            #restrict movement of players when reaching right of game page
        elif self.key_handler[RIGHT] == True:
            if self.x + 32> (RESOLUTION1):
                self.x = RESOLUTION1-self.img_w
            else:
                self.vx = 3
                self.x += self.vx
            self.vx = 3
            self.dir = RIGHT
        else:
            self.vx = 0
            #restrict movement of players when reaching top of game page
        if self.key_handler[UP] == True and self.y + self.r == self.g:
            self.vy = -15
        elif self.key_handler[UP] == True and self.y <= 0:
            self.vy = 0
            
            
            
        if frameCount % 5 == 0:        
            self.slice = (self.slice + 1) % self.num_slices
            
        self.x += self.vx
        self.y += self.vy
        
        if self.x - self.r < 0:
            self.x = self.r
        self.gravity()
        
    def display(self): #to display items
        self.update()
        for i in red_diamond:
            self.collect_item(i)
            
        for j in blue_diamond:
            self.collect_item(j) 
            
        for k in mystery_box:
            self.collect_item(k)   
            
        for v in gates:
            self.victory(v)            
                                  
            
            
        if self.dir == RIGHT:
            image(self.img, self.x - self.img_w//2, self.y - self.img_h//2, self.img_w, self.img_h, self.slice*self.img_w, 0, (self.slice + 1) * self.img_w, self.img_h)
        elif self.dir == LEFT:
            image(self.img, self.x - self.img_w//2,  self.y - self.img_h//2, self.img_w, self.img_h, (self.slice + 1)*self.img_w, 0, self.slice * self.img_w, self.img_h)
 
 
     #collect diamonds and mysterybox with score increment       
    def collect_item(self, Item): 
        if Item.type == "box":
            print(self.distance1(Item),self.r + (Item.w)//2) 
            
        if self.distance1(Item) <= self.r + (Item.w)//2:
            if Item.type == "red" and self.type == "red":
                self.diamond.rewind()
                self.diamond.play()
                global red_diamond
                red_diamond.remove(Item)
                self.score += 1
                global fireboy_score
                fireboy_score += 1
            elif Item.type == "box":
                print(self.distance1(Item),self.r + (Item.w)//2)
                self.mybo.rewind()
                self.mybo.play()
                global mystery_box
                mystery_box.remove(Item)
                self.score += random.randint(1,10) #mystery box containing random scores
                if self.type == "red":
                    global fireboy_score
                    fireboy_score +=  self.score
                elif self.type == "blue":
                    global watergirl_score
                    watergirl_score +=  self.score
                
            elif Item.type == "blue" and self.type == "blue":
                self.diamond.rewind()
                self.diamond.play()
                global blue_diamond
                blue_diamond.remove(Item)
                self.score += 1
                global watergirl_score
                watergirl_score += 1
                

    #check if both players at the gate           
    def victory(self):
        global fireboy_score
        global watergirl_score
        for v in game.gates:
            if self.distance1(v) <= v.w/2:
                if v.col == self.type:
                    return True 
                
    #death due to touching the wrong puddle            
    def death(self):
         for p in game.puddles:
            if self.distance1(p) <= p.w/2:
                if p.col != self.type and p.col != "green":
                    self.die.rewind()
                    self.die.play()
                    return True 
                    
    #calculate distance between player and different items (gate, diamond,mystery box)        
    def distance1(self,v): 
        return ((self.x - (v.x + v.w/2))**2 + (self.y - (v.y + v.h - self.r))**2)**0.5    
                

         

class Item:
    def __init__(self,x,y,w,h, type):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.type = type
        self.img_red = loadImage(path+"/cs/diamond_red.png") #image of red diamond
        self.img_blue = loadImage(path+"/cs/diamond_blue.png") #image of blue diamond
        self.img_box = loadImage(path + "/cs/mb.png") #image of mysterybox diamond

        
    def display_r(self):
        image(self.img_red, self.x-20, self.y)
        
    def display_b(self):
        image(self.img_blue, self.x-40, self.y)
        
    def display_box(self):
        image(self.img_box, self.x, self.y, self.w, self.h)
        

 #attributes of red diamonds       
dr_1 = Item(460, 40, 42, 38, "red")
dr_2 = Item(175, 345, 42, 38, "red")
dr_3 = Item(570, 250, 42, 38, "red")
#attributes of blue diamonds
db_1 = Item(340, 45, 38, 31, "blue")
db_2 = Item(585, 350, 38, 31, "blue")
db_3 = Item(350, 250, 38, 31, "blue")
#attributes of mystery box
mb = Item(340,425,71,71, "box")
mb1 = Item(660,65,71,71, "box")



blue_diamond = [db_1, db_2, db_3] #list of blue diamonds
red_diamond = [dr_1, dr_2, dr_3]  #list of red diamonds
mystery_box = [mb, mb1] #list of mysteryboxes
gates = [] #list of gates

            

class Gate:
    def __init__(self,x,y,col,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = col
        
    
    def display(self): #display gates
        if self.col == "red":
            fill(255,50,50)
            stroke(255,50,50)
            rect(self.x,self.y,40,60)
        elif self.col == "blue":
            fill(0,0,255)
            stroke(0,0,255)
            rect(self.x,self.y,40,60)
            
        
 
class Puddle:
    def __init__(self,x, y, w, h, col):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.col = col
        
    def display(self): #diaplay puddles
        if self.col == "red":
            fill(255,0,0)
            stroke(255,0,0)
            rect(self.x,self.y,self.w,self.h)
        if self.col == "green":
            fill(0,255,0)
            stroke(0,255,0)
            rect(self.x,self.y,self.w,self.h)
        elif self.col == "blue":
            fill(0,0,255)
            stroke(0,0,255)
            rect(self.x,self.y,self.w,self.h)
            
    
class Game:
    def __init__(self):
        self.w = RESOLUTION1 #set the width of game screen
        self.h = RESOLUTION2 #set the height of game screen
        self.g = GROUND 
        self.bg_image = loadImage(path + "/cs/brick.jpg") #image background of the game
        self.fireboy = Character(80,80,20,"fb.png",32,45,6,"red") #image of fireboy and attributes
        self.watergirl= Character(40,40,20,"wg.png",40,45,5, "blue") #image of watergirl and attributes
        self.img1 = loadImage(path + "/cs/" + "begin.png") #image of begin page of the game
        self.game_over = loadImage(path + "/cs/" + "gameover.jpg") #image of game over page of the game
        self.begin = True
        self.platforms = []#list of platforms
        self.puddles = [] #list of puddles
        self.gates = [] #list of gates
        self.gameover = False
        self.bg = player.loadFile(path + "/sound/mominarox.mp3") #background sound in game
        self.bg.loop() #to keep the sound playing 
        
        #placing of puddles in the game
        self.puddles.append(Puddle(0, 380, 100, 10, "blue")) 
        self.puddles.append(Puddle(650, 380, 100, 10, "red"))
        self.puddles.append(Puddle(500, 75, 100, 10, "blue"))
        self.puddles.append(Puddle(165, 75, 100, 10, "red"))
        self.puddles.append(Puddle(340, 180, 70, 10, "green"))
        #placing of platforms in the game
        self.platforms.append(Platform(200,75,50,225)) 
        self.platforms.append(Platform(500,75,50,225))
        self.platforms.append(Platform(430,75,200,40))
        self.platforms.append(Platform(140,75,200,40))
        self.platforms.append(Platform(0,140,150,40))
        self.platforms.append(Platform(750-150,140,150,40))
        self.platforms.append(Platform(310,180,130,40))
        self.platforms.append(Platform(150,280,450,40))
        self.platforms.append(Platform(0,380,250,40))
        self.platforms.append(Platform(750-250,380,250,40))
        self.platforms.append(Platform(240,500,250,40))
        self.gates.append(Gate(255,220,"red",40,60))
        self.gates.append(Gate(455,220, "blue",40,60))
      

    def display_frontpage(self): #xisplay front page of the game
        image(self.img1, 0, 0,RESOLUTION1,RESOLUTION2)
        fill(237, 188, 44)
        rect(330, 55, 100, 47)
        strokeWeight(2)
        fill(0, 0, 0)
        textSize(18)
        text("Play", 360, 80)
        fill(237, 188, 44)
        rect(550, 400, 150, 110)
        strokeWeight(2)
        fill(0, 0, 0)
        textSize(12)
        text("Instructions: \n Fireboy : l,j,i \n Watergirl : d,a,w \n for right,left,up \n respectively", 575, 418) #display instructions of the game
        fill(237, 188, 44)
        rect(30, 330, 200, 200)
        strokeWeight(2)
        fill(0, 0, 0)
        textSize(12)
        #display rules of the game
        text("Rules: \n Fireboy: collect red diamonds \n blue puddle kills \n reach red gate",40, 350) 
        text("Watergirl: collect blue diamonds \n red puddle kills \n reach blue gate", 40, 425)
        text("Both: collect mysterybox(bonus) \n green puddle is safe", 40, 485)
        
            
        if mouseX>=330 and mouseX<=430 and mouseY>=54 and mouseY<=105: #where to click to start the game
            if mousePressed:
                self.begin = False
    
    def display_gamepage(self): #display the game for play
        image(self.bg_image, 0, 0,RESOLUTION1,RESOLUTION2)
        
    
        
        
        
    def victory(self): #who wins the game
        global winner
        all_red_collected = len(red_diamond) == 0
        all_blue_collected = len(blue_diamond) == 0
        all_mystery_collected = len(mystery_box) == 0
        if (self.fireboy.victory() and self.watergirl.victory() and all_red_collected and all_blue_collected and all_mystery_collected):
            self.gameover = True
            image(self.game_over, 0, 0,RESOLUTION1,RESOLUTION2)
            winner = "Both win together as a team!"
        if self.fireboy.death() == True:
            self.gameover = True
            image(self.game_over, 0, 0,RESOLUTION1,RESOLUTION2)
            winner = "Watergirl wins!"
        elif self.watergirl.death() == True:
            self.gameover = True
            image(self.game_over, 0, 0,RESOLUTION1,RESOLUTION2)
            winner = "Fireboy wins!"
            
            

        
    def display(self):
        for platform in self.platforms: #draw the platforms
            platform.display()
        for gate in self.gates: #draw the gates
            gate.display()
            
        for Puddle in self.puddles: #draw the puddles
            Puddle.display()
        
        self.victory() #check if a player wins
            
        for Item in red_diamond: #draw red diamond
            Item.display_r()
        for Item in blue_diamond: #draw blue diamond
            Item.display_b()
        for Item in mystery_box: #draw mystery box
            Item.display_box()
        
        
    
       
         
def setup():
    size(RESOLUTION1, RESOLUTION2)
    background(255,255,255)
         

game = Game()
        
        
def draw():
    global winner
    if  game.begin == True:
        game.display_frontpage() #display the front page of game
    elif game.begin == False and game.gameover == False:
        game.display_gamepage() #display the game screen
        game.bg.play() #play background music
        game.display()
        game.watergirl.display() #display watergirl
        game.fireboy.display() #display firegirl
        text("Fireboy score: " + str(fireboy_score), 10, 20) #display fireboy score
        text("Watergirl score: " + str(watergirl_score), 10, 40) #display watergirl score
    elif game.gameover == True: #display game over screen and scores
        fill(0)
        background(0)
        image(game.game_over, 0, 0,RESOLUTION1,RESOLUTION2)
        if winner == "":
            if fireboy_score > watergirl_score: #check who wins the game based on scores
                winner = "Fireboy wins!"
            elif watergirl_score > fireboy_score:
                winner = "Watergirl wins!"    
            elif watergirl_score == fireboy_score:
                winner = "It's a tie!"
        textSize(18)
        text("Fireboy score: " + str(fireboy_score),290, 275)
        text("Watergirl score: " + str(watergirl_score),290 ,300)
        text(winner, 290,330) #display the winner of the game
      
        
#assigning keys to move the players
def keyPressed(): 
    if key == 'a':
        game.watergirl.key_handler[LEFT] = True
    elif key == 'd':
        game.watergirl.key_handler[RIGHT] = True
    elif key == 'w':
        game.watergirl.key_handler[UP] = True

    if key == 'j':
        game.fireboy.key_handler[LEFT] = True
    elif key == 'l':
        game.fireboy.key_handler[RIGHT] = True
    elif key == 'i':
        game.fireboy.key_handler[UP] = True        
        
def keyReleased():
    if key == 'a':
        game.watergirl.key_handler[LEFT] = False
    elif key == 'd':
        game.watergirl.key_handler[RIGHT] = False
    elif key == 'w':
        game.watergirl.key_handler[UP] = False    
        
            
    if key == 'j':
        game.fireboy.key_handler[LEFT] = False
    elif key == 'l':
        game.fireboy.key_handler[RIGHT] = False
    elif key == 'i':
        game.fireboy.key_handler[UP] = False      
        
        
        



        
        
