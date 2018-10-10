import pygame
import random
import os
import time

#Prerequirements
#easier to change
#w=1366
#h=768
w=800
h=600
FPS=60
spriteW=72
spriteH=72

#Default way that it's looking
P1face=1
P2face=1

#Shooting face
SP1face=1
SP2face=1

#vector gives an x and y positional value, kind of like a graph
vector=pygame.math.Vector2
player_acc=0.5
player_friction=-0.12
gravity=0.5

#player health
p1health=25
p2health=25

#Bullet stuff
bulletdmg=1

#menu images functions
#state
state="menu"
#buttons (loading images)
btn1=pygame.image.load("startB.png")
btn2=pygame.image.load("instructionB.png")
btn3=pygame.image.load("exitB.png")
btn4=pygame.image.load("menuB.png")
backBt=pygame.image.load("backBt.png")
#colout changed images
btn1C=pygame.image.load("startC.png")
btn2C=pygame.image.load("instructionC.png")
btn3C=pygame.image.load("exitC.png")
backBtC=pygame.image.load("backBtC.png")

#start button
btn1_r = btn1.get_rect()
btn1_r.x, btn1_r.y = (w/2-65,h/2-100)
over_btn1=False
#instuctions button
btn2_r = btn2.get_rect()
btn2_r.x, btn2_r.y = (w/2-127,h/2-50)
over_btn2=False
#exit button
btn3_r = btn3.get_rect()
btn3_r.x, btn3_r.y = (w/2-45,h/2)
over_btn3=False
#menu button
btn4_r = btn4.get_rect()
btn4_r.x, btn4_r.y =(w/2-83,h/2+50)
#back button 
backBt_r= backBt.get_rect()
backBt_r.x, backBt_r.y =(0,0)
over_backBt=False

#colours
white=(255,255,255)
black=(0,0,0)
red=(255,0,0)
green=(26,230,0)
blue=(0,0,255)
yellow=(255,255,0)

#backgrounds
gameBg=pygame.image.load("background.png")
menuBg=pygame.image.load("menu.png")
player1Win=pygame.image.load("player1End.png")
player2Win=pygame.image.load("player2End.png")
instructBg=pygame.image.load("instructBg.png")

#Game requirements
pygame.init()
pygame.mixer.init()
screen=pygame.display.set_mode((w,h))
clock=pygame.time.Clock()
#music
pygame.mixer.music.load("Menu.mp3")
pygame.mixer.music.set_volume(0.05)
pygame.mixer.music.play(loops=-1)
#Player 1 Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        #Spawns and makes character
        #assigns values
        self.index=0
        self.imgNum = 1
        self.updateFrameCount = 0
        self.current_frame = 0
        self.walking = False
        self.jumping = False
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("pew1.png")
        self.standing_frames=[pygame.image.load("pew1.png"),pygame.image.load("pew2.png")]
        self.standing_framesL=[pygame.image.load("pew3.png"),pygame.image.load("pew4.png")]
        self.left_walk=[pygame.image.load("pewL1.png"),pygame.image.load("pewL2.png")]
        self.right_walk=[pygame.image.load("pewR1.png"),pygame.image.load("pewR2.png")]
        self.rect=self.image.get_rect()
        self.rect.centerx=w/2
        self.rect.bottom=h-10
        self.pos=vector(100,h/2)
        self.vel=vector(0,0)
        self.acc=(0,0)
        self.face=0

    def update(self):
        #run standby animation
        self.animate()
        #adds vector
        self.acc=vector(0,gravity)
        key=pygame.key.get_pressed()

        
        #Left animation (goes through the images so that it runs when key is pressed
        if key[pygame.K_a]:      
            self.acc.x=-player_acc

       #if right key is pressed and held down
        if key[pygame.K_d]:
            self.acc.x=player_acc
    
        #equation for friction  (physics)
        self.acc.x+=self.vel.x*player_friction
        
        #equation for motion
        self.vel+=self.acc
        if abs(self.vel.x) <0.1:
            self.vel.x=0
        self.pos+=self.vel+0.5*self.acc
        #borders(doesn't let the sprite go off the screen)
        if self.pos.x>w-spriteW/2:
            self.pos.x=w-spriteW/2
        if self.pos.x<spriteW/2:
            self.pos.x=spriteW/2
        if self.pos.y>h-spriteW+150:
            self.kill()

        self.rect.midbottom=self.pos
        #Health(if health is equal to or below 0 kill the sprite)
        if p1health<=0:
            self.kill()


#animation instance
    def animate(self):
        currentTime = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        #show walking animation
        if self.walking:
            #180 is millisecond
            if currentTime - self.updateFrameCount > 180:
                self.updateFrameCount = currentTime 
                self.current_frame = (self.current_frame + 1) % len(self.left_walk)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.right_walk[self.current_frame]
                else:
                    self.image = self.left_walk[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                
        #Shows the standby animation
        if P1face==1:
            if not self.jumping and not self.walking:
                if currentTime - self.updateFrameCount > 350:
                    self.updateFrameCount = currentTime
                    self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                    bottom = self.rect.bottom
                    self.image = self.standing_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
        if P1face==-1:
            if not self.jumping and not self.walking:
                if currentTime - self.updateFrameCount > 350:
                    self.updateFrameCount = currentTime
                    self.current_frame = (self.current_frame + 1) % len(self.standing_framesL)
                    bottom = self.rect.bottom
                    self.image = self.standing_framesL[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
    def jump(self):
        #goes down 1 to check if the platform is below
        self.rect.x+=1
        #checks if it hits the platform
        pHit=pygame.sprite.spritecollide(self,platforms,False)
        #goes back by 1 to original state
        self.rect.x-=1
        #Can only jump again after you hit the ground/platform
        if pHit:
            self.vel.y=-12.5
            
    def shoot(self):
        global bullets1,bullet1
        #creates group for collision checks
        bullet1=Bullet(self.rect.centerx,self.rect.top)
        all_sprites.add(bullet1)
        bullets1.add(bullet1)

    def healthbar(self):
        #adding the health bar to game
        width=200*p1health/25
        healthbar=pygame.Rect(0,0,width,25)
        basebar=pygame.Rect(0,0,200,25)
        if p1health<=25:
            pygame.draw.rect(screen,red,basebar)
            pygame.draw.rect(screen,green,healthbar)
            
# Player 2 Class
class Player2(pygame.sprite.Sprite):
    def __init__(self):
        #Spawns and makes character
        #assigns values
        self.index=0
        self.imgNum = 1
        self.updateFrameCount = 0
        self.current_frame = 0
        self.walking = False
        self.jumping = False
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load("cat0.png")
        self.standing_frames=[pygame.image.load("cat0.png"),pygame.image.load("cat1.png")]
        self.standing_framesL=[pygame.image.load("cat2.png"),pygame.image.load("cat3.png")]
        self.left_walk=[pygame.image.load("catRunL0.png"),pygame.image.load("catRunL1.png")]
        self.right_walk=[pygame.image.load("catRun0.png"),pygame.image.load("catRun1.png")]
        self.rect=self.image.get_rect()
        self.rect.centerx=w/2
        self.rect.bottom=h-10
        self.pos=vector(w-100,h/2)
        self.vel=vector(0,0)
        self.acc=(0,0)
        
     
    def update(self):
        #run standby animation
        self.animate()
        #adds vector
        self.acc=vector(0,gravity)
        key=pygame.key.get_pressed()
        
        
        #Left animation (goes through the images so that it runs when key is pressed
        if key[pygame.K_LEFT]:      
            self.acc.x=-player_acc

       #if right key is pressed and held down
        if key[pygame.K_RIGHT]:
            self.acc.x=player_acc
    
        #equation for friction  (physics)
        self.acc.x+=self.vel.x*player_friction
        
        #equation for motion
        self.vel+=self.acc
        if abs(self.vel.x) <0.1:
            self.vel.x=0
        self.pos+=self.vel+0.5*self.acc
        #borders(doesn't let the sprite go off the screen)
        if self.pos.x>w-spriteW/2:
            self.pos.x=w-spriteW/2
        if self.pos.x<spriteW/2:
            self.pos.x=spriteW/2
        if self.pos.y>h-spriteW+150:
            self.kill()
            
        self.rect.midbottom=self.pos
        #Health(if health is equal to or below 0 kill the sprite)
        if p2health<=0:
            self.kill()


#animation instance
    def animate(self):
        currentTime = pygame.time.get_ticks()
        if self.vel.x != 0:
            self.walking = True
        else:
            self.walking = False
        #show walking animation
        if self.walking:
            #180 is millisecond
            if currentTime - self.updateFrameCount > 180:
                self.updateFrameCount = currentTime 
                self.current_frame = (self.current_frame + 1) % len(self.left_walk)
                bottom = self.rect.bottom
                if self.vel.x > 0:
                    self.image = self.right_walk[self.current_frame]
                else:
                    self.image = self.left_walk[self.current_frame]
                self.rect = self.image.get_rect()
                self.rect.bottom = bottom
                
        #Shows the standby animation When facing Right
        if P2face==1:
            if not self.jumping and not self.walking:
                if currentTime - self.updateFrameCount > 350:
                    self.updateFrameCount = currentTime
                    self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
                    bottom = self.rect.bottom
                    self.image = self.standing_frames[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
        if P2face==-1:
             if not self.jumping and not self.walking:
                if currentTime - self.updateFrameCount > 350:
                    self.updateFrameCount = currentTime
                    self.current_frame = (self.current_frame + 1) % len(self.standing_framesL)
                    bottom = self.rect.bottom
                    self.image = self.standing_framesL[self.current_frame]
                    self.rect = self.image.get_rect()
                    self.rect.bottom = bottom
    def jump(self):
        #goes down 1 to check if the platform is below
        self.rect.x+=1
        #checks if it hits the platform
        pHit=pygame.sprite.spritecollide(self,platforms,False)
        #goes back by 1 to original state
        self.rect.x-=1
        #Can only jump again after you hit the ground/platform
        if pHit:
            self.vel.y=-12.5

    def shoot(self):
        global bullets2,bullet2
        #creates group for collision checks
        bullet2=Bullet2(self.rect.centerx,self.rect.top+5)
        all_sprites.add(bullet2)
        bullets2.add(bullet2)
        
    def healthbar(self):
        width=200*p2health/25
        healthbar=pygame.Rect(w-200,0,width,25)
        basebar=pygame.Rect(w-200,0,200,25)
        #outlinebar=pygame.Rect(w-202.5,0,202.5,37.5)
        if p2health<=25:
            #pygame.draw.rect(screen,black,outlinebar)
            pygame.draw.rect(screen,red,basebar)
            pygame.draw.rect(screen,green,healthbar)
        
#Player 1 Bullet class
class Bullet(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((20,5))
        self.image.fill(black)
        self.rect=self.image.get_rect()
        self.rect.bottom=y+spriteH/2+1
        #Checks which way you're facing and shoots that way
        self.rect.centerx=x+35*SP1face
        
        self.speedx= SP1face*10
    def update(self):
        self.rect.x+=self.speedx
        if self.rect.x>w or self.rect.x<0:
            self.kill()
#Player 2 bullet class
class Bullet2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((20,5))
        self.image.fill(black)
        self.rect=self.image.get_rect()
        self.rect.bottom=y+spriteH/2+1
        #Checks which way you're facing and shoots that way
        self.rect.centerx=x+35*SP2face
        
        self.speedx= SP2face*10
    def update(self):
        self.rect.x+=self.speedx
        if self.rect.x>w or self.rect.x<0:
            self.kill()    
    
#platform class
class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #ELEVATED PLATFORMS                                     
        self.image=pygame.image.load("platform.png")
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
class Platform2(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        #GROUND PLATFORM                                   
        self.image=pygame.image.load("bplatform.png")
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        
keeprunning=True

#new sprites added
all_sprites=pygame.sprite.Group()
#Player sprite
player1_sprite=pygame.sprite.Group()
player2_sprite=pygame.sprite.Group()

#platform group for collision check
platforms=pygame.sprite.Group()

#Bullet Groups
bullets1=pygame.sprite.Group()
bullets2=pygame.sprite.Group()

#adding the player sprites into the sprite group
player=Player()
all_sprites.add(player)
player1_sprite.add(player)
player2=Player2()
all_sprites.add(player2)
player2_sprite.add(player2)

#adding platforms
p1=Platform(-176,h-200)
all_sprites.add(p1)
platforms.add(p1)

p2=Platform(w-177,h-200)
all_sprites.add(p2)
platforms.add(p2)

p3=Platform(w/2-175,h-335)
all_sprites.add(p3)
platforms.add(p3)

p4=Platform2(0,h-75)
all_sprites.add(p4)
platforms.add(p4)
while keeprunning:
    clock.tick(FPS)
    #print menu
    #Update
    all_sprites.update()
    #Player and Platform hit collision detector
    if player.vel.y>0:
        hits=pygame.sprite.spritecollide(player,platforms,False)
        if hits:
            player.pos.y=hits[0].rect.top+1
            player.vel.y=0
    
    if player2.vel.y>0:
        hits2=pygame.sprite.spritecollide(player2,platforms,False)
        if hits2:
            player2.pos.y=hits2[0].rect.top+1
            player2.vel.y=0
            
    #Bullet Collision Detectors
    #If player 1 gets hit by player 2
    B1hits=pygame.sprite.groupcollide(player1_sprite,bullets2,False,True)
    for hit in B1hits:
        p1health-=bulletdmg
    
    #If player 2 gets hit by player 1
    B2hits=pygame.sprite.groupcollide(player2_sprite,bullets1,False,True)
    for hit in B2hits:
        p2health-=bulletdmg
        
    #menu state
    if state=="menu":
        screen.blit(menuBg,(0,0))
        #BUTTON 1 (START)-----------------------------------
        if btn1_r.collidepoint(pygame.mouse.get_pos()):
            over_btn1=True
        else:
            over_btn1=False
        time.sleep(0.0000000000000000001)
        if over_btn1:
            screen.blit(btn1C,(w/2-65,h/2-100))
        else:
            screen.blit(btn1,(w/2-65,h/2-100))
        #BUTTON 2 (INSTRUCTIONS)-----------------------------
        if btn2_r.collidepoint(pygame.mouse.get_pos()):
            over_btn2=True
        else:
            over_btn2=False
        time.sleep(0.0000000000000000001)

        if over_btn2:
            screen.blit(btn2C,(w/2-127,h/2-50))
        else:
            screen.blit(btn2,(w/2-127,h/2-50))
        
        #BUTTON 3 (EXIT)--------------------------------------
        if btn3_r.collidepoint(pygame.mouse.get_pos()):
            over_btn3=True
        else:
            over_btn3=False
        time.sleep(0.0000000000000000001)

        if over_btn3:
            screen.blit(btn3C,(w/2-45,h/2))
        else:
            screen.blit(btn3,(w/2-45,h/2))
        
     #instructions state
    elif state == "instructions":
        screen.blit(instructBg,(0,0))
        
        #back button colour change
        if backBt_r.collidepoint(pygame.mouse.get_pos()):
            over_backBt=True
        else:
            over_backBt=False
        time.sleep(0.0000000000000000001)

        if over_backBt:
            screen.blit(backBtC,(0,0))
        else:
            screen.blit(backBt,(0,0))
        
        #game state
    elif state=="game":
        screen.blit(gameBg,(0,0))
        all_sprites.draw(screen)
        for sprite in player1_sprite:
            sprite.healthbar()
        for sprite in player2_sprite:
            sprite.healthbar()
        
    #Score Screens (who wins)
        if p2health==0 and p1health>0:
            screen.blit(player1Win,(0,0))
            screen.blit(btn4,(w/2-83,h/2+50))
        if p1health==0 and p2health>0:
            screen.blit(player2Win,(0,0))
            screen.blit(btn4,(w/2-83,h/2+50))

    pygame.display.flip()
                   
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keeprunning=False        
        if event.type==pygame.KEYDOWN:
           #jumping event
            if event.key==pygame.K_w:
                player.jump()
            #shooting event
            if event.key==pygame.K_k:
                if p1health>0:
                    player.shoot()
            if event.key==pygame.K_a:   
                #when pressed it facing is to the left
                P1face=-1
                SP1face=-1
            if event.key==pygame.K_d: 
                #when pressed it facing is to the right
                P1face=1
                SP1face=1
            #jump for player 2
            if event.key==pygame.K_UP:
                player2.jump()
            #shooting for player 2
            if event.key==pygame.K_KP2:
                if p2health>0:
                    player2.shoot()
            if event.key==pygame.K_LEFT:
                P2face=-1
                SP2face=-1
            if event.key==pygame.K_RIGHT:
                P2face=1
                SP2face=1
                
        #if mouse hits game button(menu)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if btn1_r.collidepoint(pygame.mouse.get_pos()):
                state="game"
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Game.mp3")
                pygame.mixer.music.set_volume(0.05)
                pygame.mixer.music.play(loops=-1)
                
            if btn2_r.collidepoint(pygame.mouse.get_pos()):
                state="instructions"
            if btn3_r.collidepoint(pygame.mouse.get_pos()):
                keeprunning=False
            if btn4_r.collidepoint(pygame.mouse.get_pos()):
                state="menu"
                pygame.mixer.music.stop()
                game_restart=True
                pygame.mixer.music.load("Menu.mp3")
                pygame.mixer.music.set_volume(0.05)
                pygame.mixer.music.play(loops=-1)
                if game_restart:
                    p1health=25
                    p2health=25
                    all_sprites=pygame.sprite.Group()
                    player1_sprite=pygame.sprite.Group()
                    player2_sprite=pygame.sprite.Group()

                    #platform group for collision check
                    platforms=pygame.sprite.Group()

                    #Bullet Groups
                    bullets1=pygame.sprite.Group()
                    bullets2=pygame.sprite.Group()

                    #adding the player sprites into the sprite group
                    player=Player()
                    all_sprites.add(player)
                    player1_sprite.add(player)
                    player2=Player2()
                    all_sprites.add(player2)
                    player2_sprite.add(player2)
                    p1=Platform(-176,h-200)
                    all_sprites.add(p1)
                    platforms.add(p1)

                    p2=Platform(w-177,h-200)
                    all_sprites.add(p2)
                    platforms.add(p2)

                    p3=Platform(w/2-175,h-335)
                    all_sprites.add(p3)
                    platforms.add(p3)

                    p4=Platform2(0,h-75)
                    all_sprites.add(p4)
                    platforms.add(p4)
                    game_restart=False
            if backBt_r.collidepoint(pygame.mouse.get_pos()):
                state="menu"
                
pygame.quit()
            
            
    

           
              
            
        
