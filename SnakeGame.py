import pygame
import time
import random

pygame.init()

display_width = 680
display_height = 510
heighest_score = 0
snake_radius = 10

L=[] #(x,y,x_changed,y_changed)

black = (0,0,0) # RGB
white = (255,255,255)
red = (255,0,0)

gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption('Snake Game - Made by Banipreet Singh')
clock = pygame.time.Clock()

def snake(x,y,color,x_size,y_size):
	pygame.draw.rect(gameDisplay,color,[x,y,x_size,y_size]) 

def things(x,y,w,h,color):
	pygame.draw.rect(gameDisplay,color,[x,y,w,h])

def crash(score):
	message_display('You Crashed.', display_width/2, display_height*0.3,70)
	message_display('Your Score: '+str(score), display_width/2, display_height*0.4,40)
	global heighest_score
	if score > heighest_score: heighest_score = score
	print(heighest_score)
	message_display('Highest Score: '+str(heighest_score), display_width/2, display_height*0.47,30)

def textObjects(text, font):
	textSurface = font.render(text, True, black)
	return textSurface, textSurface.get_rect()


def message_display(text, locx, locy,size):
	largeText = pygame.font.Font('freesansbold.ttf', size) # Font(font name, font size)
	TextSurf, TextRec = textObjects(text, largeText)
	TextRec.center = (locx,locy)
	gameDisplay.blit(TextSurf, TextRec)
	pygame.display.update()


def gameLoop():
	x = (display_width * 0.45)
	y = (display_height * 0.8)
	started = False
	didcrash = False
	isPaused = False
	x_changed = 0
	y_changed = -5
	gameExit = False
	thing_width = snake_radius
	thing_height = snake_radius
	thing_startx = random.randrange(0, display_width-thing_width)
	thing_starty = random.randrange(0, display_height-thing_height)
	bonus_radius = 6
	
	score = 0
	L = [[x,y]]
	while not gameExit:

		gameDisplay.fill(white)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
	 			pygame.quit()
	 			quit()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_LEFT and not x_changed==5:
					x_changed = -5
					y_changed = 0
				elif event.key == pygame.K_RIGHT and not x_changed==-5:
					x_changed = 5
					y_changed = 0
				elif event.key == pygame.K_UP and not y_changed==5:
					y_changed = -5
					x_changed = 0
				elif event.key == pygame.K_DOWN and not y_changed==-5:
					y_changed = 5
					x_changed = 0
				elif event.key == pygame.K_RETURN and didcrash:
					print('reached')
					gameLoop()

				elif event.key == pygame.K_ESCAPE and not didcrash:
					if not isPaused: isPaused = True
					else: isPaused = False

			if event.type == pygame.KEYUP:
				if event.key == pygame.K_UP:
					started = True

		if isPaused: continue
		if didcrash: continue

		if not started:			
			message_display("Press UP Button to start the game ", display_width*0.5, display_height*0.5, 30)
			continue

		if (x+snake_radius>=thing_startx and x<=thing_startx+thing_width) and (y<=thing_starty+thing_height and y+snake_radius>=thing_starty):
			score+=1
			L = L+[[x,y]]
			thing_startx = random.randrange(0,display_width-thing_width)
			thing_starty = random.randrange(0,display_height-thing_height)
		else:
			tx = L[0][0]
			ty = L[0][1]
			i=4
			while i<len(L):
				if (tx+snake_radius>L[i][0] and tx<L[i][0]+snake_radius) and (ty<L[i][1]+snake_radius and ty+snake_radius>L[i][1]):
					print(tx)
					print(ty)
					print(L[i][0])
					print(L[i][1])
					didcrash = True 
				i+=1

		


		if not didcrash:
			things(thing_startx,thing_starty,thing_width,thing_height,red)
			i=len(L)-1
			while i>=0:
				if i==0:
					L[0][0]=x+x_changed
					L[0][1]=y+y_changed
					snake(L[0][0],L[0][1],black,snake_radius,snake_radius)
				elif i==1:
					snake(L[i][0],L[i][1],red,snake_radius,snake_radius)
					L[1][0]=x
					L[1][1]=y
				else:
					snake(L[i][0],L[i][1],red,snake_radius,snake_radius)
					L[i][0]=L[i-1][0]
					L[i][1]=L[i-1][1]
				i-=1
			x+=x_changed
			y+=y_changed
			
			if x>display_width: x-=display_width
			elif x<0: x+=display_width

			if y>display_height: y=0
			elif y<0: y=display_height 


			message_display("Score: "+str(score), display_width*0.9, display_height*0.05, 25)
			pygame.display.flip()
			fpslimit = 100
			fps = 30+score*2
			if fps<=fpslimit: clock.tick(fps)#+(5*(score))) #fps
			else: clock.tick(fpslimit)
		else:
			i=len(L)-1
			while i>=0:
				if i==0:
					snake(L[0][0],L[0][1],black,snake_radius,snake_radius)
				else:
					snake(L[i][0],L[i][1],red,snake_radius,snake_radius)
				i-=1
			crash(score)

gameLoop()
pygame.quit() #Anti init
quit()


#Edits:
#1. Has rectangular object that is eaten
#2. Snake can now increase its length, as the score increases and as the score increases, so does it's fps and it does so until the maximum fps limit is reached
#3. Snake can now follow the path of it's predecessor using lists which copies the value of x and y
#4. Snake can now eat a red object and as it does so it's tail become more and more longer in red color
#5. Pause system added without any text being displayed. If need be then the text can be displayed but left for now
#6. Now as you crash, the state of the text can be shown as where did it crash. If any bug will be there, it can be easily detected.