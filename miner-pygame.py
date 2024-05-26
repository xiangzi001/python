import pygame, math
from pygame.locals import*
from sys import exit
from random import*
from time import*
from pickle import *
#---------------------------------------------------------------------------------------------------------------
pygame.init()
#---------------------------------------------------------------------------------------------------------------
world = 0
block_width = 4
block_height = 4
world_deep = 91
world_long = 50
block_pos_list = []
block_list = []
block_blood_list=[]
player_x = 0
player_y = 0
mouse_pos=[0,0]
speed = 1
g = 0
money=0
pickaxe=1
shop = False
#---------------------------------------------------------------------------------------------------------------
down = False
up = False
left = False
right = False
mouse_click = False
#---------------------------------------------------------------------------------------------------------------
pygame.display.set_caption(" .Miner")
icon = pygame.image.load("./icon.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((600, 400),pygame.RESIZABLE)
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def block_pos_create():
    global block_pos_list, block_width, block_height

    block_pos_list = []
    for i in range (world_deep):
        for n in range(world_long):
            block_pos_list.append([ 15.9*block_width*n + (player_x+4.3) * block_width * 16, 15.9*block_height*i + (player_y+3.1) * block_height * 16 ])
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def block_create():
    global block_list, block_blood_list
    for  i in range (world_deep*world_long):
        if i == 0 :
            n = 999
        elif i < world_long:
            n = 1
        elif i <3*world_long :
            n = 2
        elif i < 11*world_long :
            n = randint(3,8)
        elif i < 20*world_long :
            n = randint(10,14)
        elif i < 30*world_long :
            n = randint(15,19)
        elif i < 40*world_long :
            n = randint(20,24)
        elif i < 50*world_long :
            n = randint(25,29)
        elif i < 60*world_long :
            n = randint(30,34)
        elif i < 70*world_long :
            n = randint(35,39)
        elif i < 80*world_long :
            n = randint(40,44)
        elif i < 90*world_long :
            n = randint(45,49)
        else:
            n = 999
        block_list.append(str(n))
        block_blood_list.append(int(n))
#----------------------------------------------------------------------------------------------------------------
def fill(pic, color):
    w, h = pic.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = pic.get_at((x, y))[3]
            pic.set_at((x, y), pygame.Color(r, g, b, a))
    return pic
def load_file():
    global block_list, block_blood_list
    global player_x, player_y, g, money, pickaxe
    try:
        with open ("./world/"+str(world)+"block_list.pickle","rb") as f:
            block_list = load(f)
        with open ("./world/"+str(world)+"block_blood_list.pickle","rb") as f:
            block_blood_list = load(f)
        with open("./world/"+str(world)+"save.pickle",'rb') as f:
            save_file=load(f)
            player_x=save_file["player_x"]
            player_y=save_file["player_y"]
            g = save_file["g"]
            money = save_file["money"]
            pickaxe = save_file["pickaxe"]
    except:
        block_create()
def word(words, size, pos, color):
    global block_width, block_height, screen
    size_x, size_y=size
    pos_x, pos_y=pos
    i=0
    for n in words:
        if n != " ":
            num_img = pygame.image.load( "./images/letter-"+n+".png" )
            fill(num_img, color)
            num_img = pygame.transform.scale(num_img, ( size_x , size_y))
            screen.blit(num_img , ((4/3*i*size_x+pos_x),pos_y))
        i=i+1
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
def world_draw():
    global block_pos_list, block_list, surface_width, surface_height, block_width, block_height, g
    global block_blood_list, mouse_pos
    global up, down, left, right, player_x, player_y, speed, money
    global shop
    #----player-1----------------------------------------------------------------------------------------------------
    player_img = pygame.image.load("./images/player.png")
    player_img = pygame.transform.scale(player_img, ( 16*block_width , 16*block_height))
    screen.blit(player_img , (surface_width/2 - 8 *block_width , surface_height/2 -  16*block_height) )
    tip=""
    down = True
    g = g+0.004
    player_rect = pygame.Rect(surface_width/2-8*block_width , surface_height/2-16*block_height, 15*block_width , 15.5*block_height)
    #pygame.draw.rect(screen, [0, 0, 0],player_rect )
    player_up_rect = pygame.Rect(surface_width/2-6*block_width , surface_height/2-16*block_height, 12*block_width , 1*block_height)
    #pygame.draw.rect(screen, [0, 0, 0],player_up_rect )
    player_down_rect = pygame.Rect(surface_width/2-6*block_width , surface_height/2-0.5*block_height, 12*block_width , 1*block_height)
    #pygame.draw.rect(screen, [255, 0, 0],player_down_rect )
    player_left_rect = pygame.Rect(surface_width/2-8*block_width , surface_height/2-15*block_height, 1*block_width , 13.5*block_height)
    #pygame.draw.rect(screen, [0, 255, 0],player_left_rect )
    player_right_rect = pygame.Rect(surface_width/2+7*block_width , surface_height/2-15*block_height, 1*block_width , 13.5*block_height)
    #pygame.draw.rect(screen, [0, 0, 255],player_right_rect )
    
    #----block-------------------------------------------------------------------------------------------------------
    block_rect = []
    block_rect_pos=[]
    block_rect_number=[]
    for i in range (world_deep*world_long) :
        #draw
        if -16*block_width < block_pos_list[i][0] < surface_width and -16*block_height < block_pos_list[i][1] < surface_height :
            if block_blood_list[i] > 0:
                block_img = pygame.image.load( "./images/block"+block_list[i]+".png" )
                block_img = pygame.transform.scale(block_img, ( 16*block_width , 16*block_height))
                screen.blit(block_img , block_pos_list[i])
                #damage
                if block_blood_list[i] != int(block_list[i]) and int(block_list[i]) != 999 :
                    block_damage_img = pygame.image.load("./images/Health"+str((10*block_blood_list[i])//int(block_list[i])/10)+".png")
                    block_damage_size_x, block_damage_size_y = block_damage_img.get_rect().size
                    block_damage_img = pygame.transform.scale(block_damage_img, ( block_width*block_damage_size_x , block_height* block_damage_size_y ))
                    screen.blit(block_damage_img , [block_pos_list[i][0] + 8*block_width - block_width*block_damage_size_x/2 ,  block_pos_list[i][1]+8*block_height-block_height* block_damage_size_y /2])
                 #dig
                if surface_width/6*5 > block_pos_list[i][0] > surface_width/6:
                    block_rect = pygame.Rect( block_pos_list[i][0] , block_pos_list[i][1] , 16*block_width , 16*block_height )
                    if block_rect.colliderect(player_down_rect):
                        down = False
                        if up and g <= 0.004 :
                            pass
                        else:
                            up = False
                        g=0
                    if block_rect.colliderect(player_up_rect):
                        player_y = player_y - 0.2
                    if block_rect.colliderect(player_left_rect):
                        left = False
                    if block_rect.colliderect(player_right_rect):
                        right = False
                    if block_rect.collidepoint(mouse_pos):
                        select_img = pygame.image.load("./images/select.png")
                        select_img = pygame.transform.scale(select_img, ( 16*block_width , 16*block_height))
                        screen.blit(select_img , block_pos_list[i])
                        if mouse_click == True :
                            if int(block_list[i]) == 999:
                                tip="you can not dig this block"
                            else:
                                block_blood_list[i]=block_blood_list[i]-0.05*pickaxe
                                if block_blood_list[i] <= 0:
                                    money = money + int(block_list[i])
    #---------player-2----------------------------------------------------------------------------------------------
    if down == True :
        player_y = player_y - 0.1 - g
    if up == True :
        player_y = player_y + 0.19
    if left == True :
        player_x = player_x + 0.1*speed
    if right == True :
        player_x = player_x - 0.1*speed
    pickaxe_img = pygame.image.load("./images/pickaxe"+str(pickaxe)+".png")
    pickaxe_img = pygame.transform.scale(pickaxe_img, ( 12*block_width , 12*block_height))
    screen.blit(pickaxe_img , (surface_width/2+4*block_width , surface_height/2-14*block_height))
    #----------words----------------------------------------------------------------------------------------------
    word("money",( 3*block_width , 4*block_height),(6*block_width,6*block_height),(255,255,255))
    word(str(money),( 3*block_width , 4*block_height),(30*block_width,6*block_height),(255,255,255))
    word(tip, ( 3*block_width,4*block_height),(6*block_width,92*block_height),(255,255,255))
    #----------shop------------------------------------------------------------------------------------------------
    if shop:
        pass
    else:
        shop_img = pygame.image.load("./images/Shop.png")
        shop_img = pygame.transform.scale(shop_img, ( 20*block_width , 8*block_height))
        screen.blit(shop_img , (surface_width/2 , surface_height/2) )
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

clock = pygame.time.Clock()
loading=False
number=[K_0,K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]
while True:
    clock.tick(60)
    surface_width, surface_height = pygame.display.get_surface().get_size()
    block_width = surface_width / 150
    block_height = surface_height / 100
    screen.fill((50, 100, 250))
    Key_pressed = pygame.key.get_pressed()
    event_get = pygame.event.get()

    if loading :
        right  = Key_pressed[K_d]
        left    = Key_pressed[K_a]
        if Key_pressed[K_w]:
            up = True
        if Key_pressed[K_LCTRL]:
            speed=1.5
        else:
            speed=1
        block_pos_create()
        world_draw()
    else:
        i=1
        word("loadworld", ( 12*block_width , 16*block_height),(7*block_width,25*block_height),(255,255,255))
        word(str(world),( 12*block_width , 16*block_height),(7*block_width,55*block_height),(255,255,255))
        word("press enter to start", ( 3*block_width,4*block_height),(6*block_width,92*block_height),(255,255,255))

    for event in event_get:
        if event.type==pygame.MOUSEBUTTONDOWN:
            mouse_click = True
        elif event.type==pygame.MOUSEBUTTONUP:
            mouse_click = False
        if event.type==pygame.MOUSEMOTION:
            mouse_pos = event.pos
        if event.type==pygame.KEYDOWN:
            if loading == False:
                for i in range(10):
                    if event.key == number[i]:
                        world = world*10+i
                if event.key == K_BACKSPACE:
                    world = world//10
                if event.key == K_RETURN:
                    load_file()
                    loading = True
        if event.type==pygame.QUIT:
            if loading:
                with open("./world/"+str(world)+"block_list.pickle",'wb') as f:
                    dump(block_list,f)
                with open("./world/"+str(world)+"block_blood_list.pickle",'wb') as f:
                    dump(block_blood_list,f)
                with open("./world/"+str(world)+"save.pickle",'wb') as f:
                    save_list={"player_x":player_x,"player_y":player_y,"g":g, "money":money, "pickaxe":pickaxe}
                    dump(save_list,f)
            exit()

    pygame.display.update()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

