import pygame, sys, random

#Game functions
#Floor movement
def floor_mov():
    screen.blit(floor, (floor_x, floor_y))
    screen.blit(floor, (floor_x + screen_width, floor_y))

#Top and bottom pipe creation
def pipe_create():
    rand_height = random.choice(pipe_height)
    bottom_pipe = pipe_s.get_rect(midtop = (screen_width + 50, rand_height + pipe_gap))
    top_pipe = pipe_s.get_rect(midbottom = (screen_width + 50, rand_height))
    return top_pipe, bottom_pipe

#Pipes movements 
def pipe_mov(pipes):
    for p in pipes:
        p.centerx -= pipe_speed
    return pipes

#Loading and flipping pipes
def pipe_screen(pipes):
    for p in pipes:
        if p.bottom >= screen_height:
            screen.blit(pipe_s, p)
        else: 
            reversed_pipe = pygame.transform.flip(pipe_s, False, True)
            screen.blit(reversed_pipe, p)

#Remove passed pipes
def pipe_remove(pipes):
    for p in pipes:
        if p.x + 101 <= 0:
            pipes.pop(0)
    return pipes

#Rectangle collision check
def collision_check(pipes):
    for p in pipes:
        #Collision with pipes
        if bird_r.colliderect(p):
            return False
    #Collision with floor and sky
    if bird_r.bottom >= floor_y or bird_r.top <= -50:
        return False
    return True

#Bird rotation
def rotate_b(bird):
    rotated_b = pygame.transform.rotate(bird, - bird_speed * 3)
    return rotated_b

#Display and update score while game is active
def score_screen_active(game_cond):
    if game_cond == True:
        score_s = font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_s.get_rect(center = (screen_width/2, 100))
        screen.blit(score_s, score_rect)

#Display current session score and high score when game ends
def score_screen_inactive():
    score_s = font.render(f'Score: {int(score)}', True, (255, 255, 255))
    score_rect = score_s.get_rect(center = (screen_width/2, 100))
    screen.blit(score_s, score_rect)
    tip = font.render(f'Press space to play', True, (255, 255, 255))
    tip_rect = tip.get_rect(center = (screen_width/2, 245))
    screen.blit(tip, tip_rect)
    high_score_s = font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
    high_score_rect = high_score_s.get_rect(center = (screen_width/2, 410))
    screen.blit(high_score_s, high_score_rect)

#Update highscore
def score_upd(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

#General settings 
pygame.init()

#Game variables
screen_width = 288
screen_height = 512
run = True
floor_y = 440
fps = 100
floor_x = 0
gravity = 0.3  
bird_speed = 0
bird_jump = 8
pipe_refresh_rate = 1400
pipe_gap = 150
pipe_speed = 2
font = pygame.font.Font('font/font.TTF', 25)
score = 0
high_score = 0

#Establish screen size, clock tick rate and game caption
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Flappy bird')
clock = pygame.time.Clock()

#Uploading surfaces
#Loading background
background = pygame.image.load('img/background.png').convert()
#Loading floor
floor = pygame.image.load('img/base.png').convert()
#Loading bird
bird = pygame.image.load('img/bird_up.png').convert()
#Loading pipe
pipe_s = pygame.image.load('img/pipe.png').convert()

#Lists for pipes 
pipe_list = []
pipe_height = [50, 140, 255]

#Event for pipe spawn
pipe_spawn = pygame.USEREVENT
pygame.time.set_timer(pipe_spawn, pipe_refresh_rate)

#Creating rectangles around objects 
bird_r = bird.get_rect(center = (100, screen_height/2))
floor_r = floor.get_rect()

#Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            False
            sys.exit()
        #Bird control
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird_speed = 0
                bird_speed -= bird_jump
        #Restart game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and run == False:
                pipe_list.clear()
                run = True
                score = 0 
                bird_r = bird.get_rect(center = (100, screen_height/2))
        #Adding pipes on screen
        if event.type == pipe_spawn:
            pipe_list.extend(pipe_create())

    #Setting up a FPS
    clock.tick(fps)

    #Setting background on screen 
    screen.blit(background, (0, 0))
    
    if run:
        #Bird
        bird_speed += gravity
        bird_r.centery += bird_speed
        bird_rotate = rotate_b(bird)
        screen.blit(bird_rotate, bird_r)
        #Pipe
        pipe_screen(pipe_list)
        pipe_list = pipe_mov(pipe_list)
        pipe_list = pipe_remove(pipe_list)
        #Score
        score += 0.01
        score_screen_active(run)
        if collision_check(pipe_list) == False:
            run = False
    
    #Score after game is over
    if run == False:
        high_score = score_upd(score, high_score)
        score_screen_inactive()

    #Floor
    #When the second floor surface reaches the left corner, first surface is placed after it, so it creates image of an infinite floor
    floor_mov()
    if floor_x == -screen_width:
        floor_x = 0
    floor_x -= 2   #Changing x position of the floor to make it move

    pygame.display.update()