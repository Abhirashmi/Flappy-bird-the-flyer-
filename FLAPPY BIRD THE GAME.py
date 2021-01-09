import random  #for generting random numbers
import sys #we will use sys.exit to exit the program
import pygame
from pygame.locals import * #basic pygame imports

#global variabls for game
score=0
FPS=32
SCREEN_WIDTH=289
SCREEN_HEIGHT=511
SCREEN = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
GROUND_Y=SCREEN_HEIGHT * 0.8
GAME_SPRITES={}
GAME_SOUNDS={}
PLAYER='gallary/sprites/flappy.jpeg'
BACKGROUND='gallary/sprites/background.jpeg'
PIPE='gallary/sprites/pipe.png'
player_x = int((SCREEN_WIDTH/5))
player_y = int((SCREEN_HEIGHT - GAME_SPRITES['player'].get_height())/2)
message_x = int((SCREEN_WIDTH - GAME_SPRITES['message'].get_width())/2)
message_y = int(SCREEN_HEIGHT * 0.13)
basex = 0

def main_game():
    playerx=int(SCREEN_WIDTH/5)
    playery=int(SCREEN_WIDTH/2)
    basex=0

def welcome_screen():
   # player_x=(int(SCREEN_WIDTH/5))
   # player_y=(int(SCREEN_HEIGHT - GAME_SPRITES['player'].get_height())/2)
   # message_x=(int(SCREEN_WIDTH - GAME_SPRITES['message'].get_width())/2)
   # message_y=(int(SCREEN_HEIGHT*0.13))
   # basex=0
   while(True):
       for event in pygame.event.get():
           if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE ) :
               pygame.quit()
               sys.exit()

           elif event.type == KEYDOWN and (event.type == K_SPACE or event.type == K_UP):
               return

           else:
               SCREEN.blit(GAME_SPRITES['background'],(0 ,0 ))
               SCREEN.blit(GAME_SPRITES['player'],(player_x,player_y))
               SCREEN.blit(GAME_SPRITES['message'],( message_x,message_y ))
               SCREEN.blit(GAME_SPRITES['base'],(basex ,GROUND_Y))
               pygame.display.update()
               fps_clock.tick(FPS)

def iscollide(player_x,player_y,upper_pipes,lower_pipes):
    if (player_y> GROUND_Y or player_y<0):
        GAME_SOUNDS['hit'].play()
        return True
    for pipe in upper_pipes:
        pipe_height=GAME_SPRITES['pipe'][0]
        if (player_y <pipe_height +pipe['y'] and abs(player_x - pipe['x']) <GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
        return True

    for pipe in lower_pipes:
       if (player_y+GAME_SPRITES['player'].get_height() >pipe['y']) and abs(player_x - pipe['x']) < GAME_SPRITES['pipe'][0].get_width():
           GAME_SOUNDS['hit'].play()
        return True

    # return False

#create 2 pipes for blitting on the screen


def get_random_pipes():
    pipe_height=GAME_SPRITES['pipe'][0].get_height()
    offset=SCREEN_HEIGHT/3
    y2=offset +random.randrange(0,int(SCREEN_HEIGHT- GAME_SPRITES['base'].get_height() - 1.2 * offset))
    pipe_x=SCREEN_WIDTH+10
    y1=pipe_height - y2+offset
    pipe=[
        {'x':pipe_x, 'y':-y1}, #upper_pipe thats why -y1
        {'x':pipe_x, 'y':y1} #upper_pipe thats why -y1
    ]
    return pipe


new_pipe1= get_random_pipes()
new_pipe2= get_random_pipes()
# my_list of upper pipes
upper_pipes=[
    {'x':SCREEN_WIDTH+200, 'y':new_pipe1[0]['y']},
    {'x':SCREEN_WIDTH+200+(SCREEN_WIDTH/2), 'y':new_pipe2[0]['y']}
]
 # my_list of  lower pipes

lower_pipes=[
    {'x':SCREEN_WIDTH+200, 'y':new_pipe1[1]['y']},
    {'x':SCREEN_WIDTH+200+(SCREEN_WIDTH/2), 'y':new_pipe2[1]['y']}
]

pipe_velocity_x= -4

playar_velocity_y= -9
playar_max_velocity_y= 10
playar_min_velocity_y= -8
player_acc_y= 1

player_flap_Acc_v= -8 #velocity while flapping

player_flapperd=False #it is true only when player the bird is flapping

while(True):
    for event in pygame.event.get():
        if event.type == QUIT or (event.type == KEYDOWN and event.type == K_ESCAPE):
            pygame.quit()
            sys.exit()

        if event.type == KEYDOWN and (event.type == K_SPACE or event.key == K_UP):
            if player_y > 0:
                player_velocity_y = player_acc_y
                player_flapperd = True
                GAME_SOUNDS['wing'].play

    crashTest = iscollide(player_x,player_y,upper_pipes,lower_pipes) #this function will return true if the player is crashed
    if crashTest:
        exit()

    #check scode
    player_mid_pos=player_x+GAME_SPRITES['player'].get_width()/2
    for pipe in upper_pipes:
        pipe_mid_position= pipe['x'] +GAME_SPRITES['pipe'][0].get_width()/2
        if pipe_mid_position <= player_mid_pos < pipe_mid_position+4:
            score=score+1
            print(f"Your score is {score}")
            GAME_SOUNDS['point'].play()


    if playar_velocity_y <playar_max_velocity_y and not player_flapperd:
        playar_velocity_y= playar_velocity_y+player_acc_y

    if player_flapperd:
        player_flapperd = False
    player_height=GAME_SPRITES['player'].get_height()
    player_y = player_y+ min(playar_velocity_y,GROUND_Y - player_y - player_height)

    #moves_pipe_to_the_left

    for upper_pipes ,lower_pipes in zip(upper_pipes,lower_pipes):
        upper_pipes['x'] = upper_pipes['x']+pipe_velocity_x
        lower_pipes['x'] = lower_pipes['x']+pipe_velocity_x
#Add a new pipe when the first pipe is about to go to thw left most part of the screen of the game
    if 0<upper_pipes[0]['x'] < 5:
        new_Pipe= get_random_pipes()
        upper_pipes.append(new_Pipe[0])
        lower_pipes.append(new_Pipe[1])
    #if the pipe is out of the screen remove it
    if upper_pipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
        upper_pipes.pop(0)
        lower_pipes.pop(0)

#lets blit our sprites now
    SCREEN.blit(GAME_SPRITES['background'], 0,0)
    for upper_pipes ,lower_pipes in zip(upper_pipes,lower_pipes):
        SCREEN.blit(GAME_SPRITES['pipe'][0], upper_pipes['x'],upper_pipes['y'])
        SCREEN.blit(GAME_SPRITES['pipe'][1], lower_pipes['x'], lower_pipes['y'])

    SCREEN.blit(GAME_SPRITES['base'],basex,GROUND_Y)
    SCREEN.blit(GAME_SPRITES['player'],player_x,player_y)
    mydigits=[int(x) for x in list(str(score))]
    width=0
    for digit in mydigits:
        width = width+GAME_SPRITES['numbers'][digit].get_width()
        xOffset= (SCREEN_WIDTH - width)/2

        for digit in mydigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(xOffset, SCREEN_HEIGHT *0.12))
            xOffset += GAME_SPRITES['numbers'].get_width()
        pygame.display.update()
        FPS.tick(FPS)
    SCREEN.blit(GAME_SPRITES['base'],basex,GROUND_Y)

if __name__ == '__main__':
    #this will be the main point our game will start
    pygame.init() #initialise all pygames module
    fps_clock=pygame.time.Clock()
    pygame.display.set_caption('FLAPPY_BIRD_by_Abhirashmi')
    GAME_SPRITES['numbers']=(
        pygame.image.load('gallary/sprites/0.jpeg').convert_alpha(),
        pygame.image.load('gallary/sprites/1.jpeg').convert_alpha(),
        pygame.image.load('gallary/sprites/2.jpeg').convert_alpha(),
        pygame.image.load('gallary/sprites/3.jpeg').convert_alpha(),
        pygame.image.load('gallary/sprites/4.jpeg').convert_alpha(),
        pygame.image.load('gallary/sprites/5.jpeg').convert_alpha(),
        pygame.image.load('gallary/sprites/6.jpeg').convert_alpha(),
        pygame.image.load('gallary/sprites/7.jpeg').convert_alpha(),
        pygame.image.load('gallary/sprites/8.jpeg').convert_alpha(),
        pygame.image.load('gallary/sprites/9.jpeg').convert_alpha(),
    )
    GAME_SPRITES['message'] = pygame.image.load('gallary/sprites/message.jpeg').convert_alpha()

    GAME_SPRITES['base'] =pygame.image.load('gallary/sprites/base.jpeg')

    GAME_SPRITES['pipe'] =(pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(), 180),
        pygame.image.load(PIPE).convert_alpha()
    )

    #game_sounds

    GAME_SOUNDS['die']= pygame.mixer.Sound('gallary/audio/die.mp3')
    GAME_SOUNDS['hit']= pygame.mixer.Sound('gallary/audio/hit.mp3')
    GAME_SOUNDS['point']= pygame.mixer.Sound('gallary/audio/point.mp3')
    GAME_SOUNDS['swoosh']= pygame.mixer.Sound('gallary/audio/swoosh.mp3')
    GAME_SOUNDS['wing']= pygame.mixer.Sound('gallary/audio/wing.mp3')

    GAME_SPRITES['background']=pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player']=pygame.image.load(PLAYER).convert_alpha()


    while(True):
        welcome_screen() #shows welcome screen to the user untill a button is pressed
        main_game() #main part of the game
