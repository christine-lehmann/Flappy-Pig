import pygame, sys, random

def draw_floor():
    screen.blit(floor_surface,(floor_x_pos, 600)) # 900
    screen.blit(floor_surface,(floor_x_pos + 384, 600)) # 576, 900

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos)) # 192, 341.5
    top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 250)) # 300 original 250
    return  bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 683:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    global can_score
    for pipe in pipes:
        if pig_rect.colliderect(pipe):
            death_sound.play()
            can_score = True
            return False

    if pig_rect.top <= -100 or pig_rect.bottom >= 600:
        can_score = True
        return False

    return True

def rotate_pig(pig):
    new_pig = pygame.transform.rotozoom(pig, -pig_movement*2, 1)
    return new_pig

def pig_animation():
    new_pig = pig_frames[pig_index]
    new_pig_rect = new_pig.get_rect(center = (100, pig_rect.centery))
    return new_pig, new_pig_rect

def score_display(game_state):
    if game_state == 'main_game':
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center=(192, 80)) # 100
        screen.blit(score_surface, score_rect)
    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(192, 80))  # 100
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)}', True, (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(192, 580))  # 100
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

def pipe_score_check():
    global score, can_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and can_score:
                score += 1
                score_sound.play()
                can_score = False
            if pipe.centerx < 0:
                can_score = True

# pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 580) #512
pygame.init()
pygame.display.set_caption("Flappy Pig")
icon = pygame.image.load("pig512.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((384, 684)) # (576,1024)
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.TTF', 40)

# Game Variables
gravity = 0.25
pig_movement = 0
game_active = True
score = 0
high_score = 0


bg_surface = pygame.image.load('assets/sprites/background-night2.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/sprites/base2.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 1

pig_downflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/wings1.png').convert_alpha())
pig_midflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/wings2.png').convert_alpha())
pig_upflap = pygame.transform.scale2x(pygame.image.load('assets/sprites/wings3.png').convert_alpha())
pig_frames = [pig_downflap, pig_midflap, pig_upflap]
pig_index = 0
pig_surface = pig_frames[pig_index]
pig_rect = pig_surface.get_rect(center = (100, 341.5))

PIGFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(PIGFLAP, 200)

# pig_surface = pygame.image.load('assets/sprites/wings2.png').convert_alpha()
# pig_surface = pygame.transform.scale2x(pig_surface)
# pig_rect = pig_surface.get_rect(center = (100, 341.5))

pipe_surface = pygame.image.load('assets/sprites/pipe-green2.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_height = [280, 350, 450] # 250, 350, 450 / 300, 450, 500 original 280 350 450
              #400, 600, 800

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/sprites/mes3.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(194, 350)) #100, 341.5

flap_sound = pygame.mixer.Sound('assets/audio/wing.wav')
death_sound = pygame.mixer.Sound('assets/audio/hit.wav')
score_sound = pygame.mixer.Sound('assets/audio/point.wav')
score_sound_countdown = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT,100)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                pig_movement = 0
                pig_movement -= 6 # 12
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                pig_rect.center = (100, 341.5)
                pig_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == PIGFLAP:
            if pig_index < 2:
                pig_index += 1
            else:
                pig_index = 0

            pig_surface, pig_rect = pig_animation()

    screen.blit(bg_surface, (0, 0))

    if game_active:
        # Pig
        pig_movement += gravity
        rotated_pig = rotate_pig(pig_surface)
        pig_rect.centery += pig_movement
        screen.blit(rotated_pig, pig_rect)
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        pipe_score_check()
        score_display('main_game')
    else:
        screen.blit(game_over_surface, game_over_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -384:
        floor_x_pos = 0
    screen.blit(floor_surface, (floor_x_pos, 600))

    pygame.display.update()
    clock.tick(100) #110 / 120

