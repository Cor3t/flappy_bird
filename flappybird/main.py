import pygame
import random

pygame.init()
pygame.font.init()
WIDTH, HEIGHT = 450, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

game_font = pygame.font.Font("04B_19.TTF", 40)

BG1 = pygame.transform.scale(pygame.image.load("assets/sprites/background-day.png").convert(), (WIDTH, HEIGHT))
BG2 = pygame.transform.scale(pygame.image.load("assets/sprites/background-night.png").convert(), (WIDTH, HEIGHT))

floor = pygame.image.load("assets/sprites/base.png").convert()
floor = pygame.transform.scale(floor, (WIDTH, floor.get_height()))

bird_downflap = pygame.transform.scale2x(pygame.image.load("assets/sprites/bluebird-downflap.png").convert_alpha())
bird_midflap = pygame.transform.scale2x(pygame.image.load("assets/sprites/bluebird-midflap.png").convert_alpha())
bird_upflap = pygame.transform.scale2x(pygame.image.load("assets/sprites/bluebird-upflap.png").convert_alpha())
bird_frame = [bird_downflap,bird_midflap, bird_upflap]
BIRDINDEX = 0
bird = bird_frame[BIRDINDEX]
bird_rect = bird.get_rect(center =(200,350))

# bird = pygame.image.load("assets/sprites/bluebird-midflap.png").convert_alpha()
# bird = pygame.transform.scale2x(bird)
# bird_rect = bird.get_rect(center =(100,350))

pipe_surface = pygame.image.load("assets/sprites/pipe-green.png")
pipe_surface = pygame.transform.scale2x(pipe_surface)

def create_pipe(pipe_length):
	random_pipe_pos = random.choice(pipe_length)
	bottom_pipe = pipe_surface.get_rect(midtop = (700, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (700, random_pipe_pos - 170))
	return bottom_pipe, top_pipe
	
def move_pipes(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= HEIGHT - floor.get_height():
 			WIN.blit(pipe_surface, pipe)
		else:
 			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
 			WIN.blit(flip_pipe, pipe)

def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			return False

	if bird_rect.top <= 0 or bird_rect.bottom >= HEIGHT - floor.get_height():
		return False

	return True

def rotate_bird(bird, bird_movement):
	new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
	return new_bird

def score_display(score):
	score_surface = game_font.render(f"{int(score)}", 1, (255,255,255))
	score_rect = score_surface.get_rect(center = (225, 100))
	WIN.blit(score_surface, score_rect)


def main():
	global BIRDINDEX
	score = 0
	hihg_score = 0
	game_active = True
	run = True
	FPS = 60
	floor_x_pos = 0
	gravity = 0.25
	bird_movement = 0
	SPAWMPIPE = pygame.USEREVENT
	BIRDFLAP = pygame.USEREVENT + 1
	pygame.time.set_timer(BIRDFLAP, 200)
	pygame.time.set_timer(SPAWMPIPE, 1200)
	pipe_list = []
	pipe_height =[400, 350, 300]
	game_font

	def floor_animation():
		WIN.blit(floor, (floor_x_pos, (HEIGHT - floor.get_height())))
		WIN.blit(floor, (floor_x_pos + WIDTH, (HEIGHT - floor.get_height())))

	def update():
		WIN.blit(BG1, (0,0))
		if game_active:
			rotated_bird = rotate_bird(bird, bird_movement)
			WIN.blit(rotated_bird, bird_rect)
			draw_pipes(pipe_list)
			score_display(score)

		floor_animation()


		pygame.display.update()

	def bird_animation():
		global bird_rect, bird
		bird = bird_frame[BIRDINDEX]
		bird_rect = bird.get_rect(center = (200, bird_rect.centery))
		

	while run:
		clock.tick(FPS)
		update()

		if floor_x_pos <= -WIDTH:
			floor_x_pos = 0

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE and game_active:
					bird_movement = 0
					bird_movement -= 5
				if event.key == pygame.K_SPACE and game_active == False:
					score = 0
					game_active = True
					pipe_list.clear()
					bird_movement = 0
					bird_rect.center = (200,350)
			if event.type == SPAWMPIPE:
				pipe_list.extend(create_pipe(pipe_height))
			if event.type == BIRDFLAP:
				if BIRDINDEX < 2:
					BIRDINDEX += 1
				else:
					BIRDINDEX = 0
				bird_animation()


		if game_active:
			pipe_list = move_pipes(pipe_list)
			score += 0.01


			floor_x_pos -= 5
			bird_movement += gravity
			bird_rect.centery += bird_movement

			game_active = check_collision(pipe_list)




main()	