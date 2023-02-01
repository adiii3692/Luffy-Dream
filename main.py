#Author: Aditya Nair
#Date: 20th Jaunary,2023
#Name of program: Luffy_Dream_Game
#Purpose: Enable the user to play a 2D game in which the player needs to collect all the devil fruits by avoiding the enemies and ultimately reach the map at the end

"""
Variable Dictionary:
bgm  - a pygame variable to load the background music(bgm)
gameOutline - <class 'str'> - a list of strings for the game map
blockSize - <class 'int'>_- an int which stores the pixel size of the blocks(64)
screenWidth - <class 'int'> - the width of the screen
screenHeight - <class 'int'> - the height of the screen
pixelatedImages - <class 'pygame.Surface' - A list which stores pygame's version of pixelated images
self.font - <class 'pygame.Font'> -  An instance variable which stores the font type to use
self.healthFrame - <class 'pygame.Surface'> - An instance variable that stores the pixelated image of the health frame
self.healthFrameRect- <class 'int'> - A tuple which stores the position of the health frame's image
self.fruit - <class 'pygame.Surface'> - An instance variable that stores the pixelated image of the devil fruit
self.fruitRect - <class 'int'> - A tuple which stores the position of the devil fruit's image
currentHealth - <class 'pygame.Surface'> - Pygame's text version of the player's current health 
currentHealthRect - <class 'int'> - A tuple which stores the position of the text which display's the player's current health
currentAmount - <class 'pygame.Surface'> - Pygame's text version of the player's devil fruit count
currentAmountRect - <class 'int'> - A tuple which stores the position of the text which display's the player's devil fruit count
self.image - <class 'pygame.Surface'> - Stores the image that needs to be blitted onto the screen
self.imageIndex - <class 'int'> - Stores the index of the image (from the images list) being displayed on screen 
self.rect - <class 'pygame.Rect'> - Stores the postion of the rectangle created over an image
centerX - <class 'int'> - The x coordinate of the center of a block
centerY - <class 'int'> - The y coordinate of the center of a block
self.animationSpeed - <class 'int'> - The speed by which the images in a list are looped over to create an animation
self.speed - <class 'int'> - The speed with which the character moves around 
self.gravity - <class 'int'> - The downward pull applied on the player
self.jumpHeight - <class 'int'> - The height to which the player can jump
self.status - <class 'str'> - Status of the player(idle,jumping,running)
self.facingRight - <class 'bool'> - Checks if the player is facing right
self.onGround - <class 'bool'> - Checks if the player is on ground
self.onCeiling - <class 'bool'> - Checks if the player is touching a ceiling 
self.onLeft - <class 'bool'> - Checks if the user is on the left of a wall 
self.onRight - <class 'bool'> - Checks if the user is on the right of a wall
self.direction - <class 'pygame.math.Vector'> - A Vector used for obtaining the direction in which the player is moving
self.invincible - <class 'bool'> - Checks if the player is still invincible after coming in contact with an obstacle
self.invincibilityDuration - <class 'int'> - The duration in milliseconds for which the player ca be invincible
self.hurtTime - <class 'int'> - At what time after the code is run, has the player gotten hurt
self.fruitCount - <class 'int'> - How many fruits has the player collected
self.currentHealth - <class 'int'> - The current health of the player (keeps changing throughout the game)
self.worldShift - <class 'int'> - By how much the video should be moved to create a world shift along with the player
self.done - <class 'bool'> - Checks if the player has completed the game by collecting the map at the end
playerX - <class 'int'> - The x coordinate of the player
finalText - <class 'str'> - The final text which is displayed on the screen (You lose or You win)
finalTextRect - <class 'int'> - A tuple which stores the postion of the final text on the screen
clock - <class 'pygame.time.Clock' - Used to create a frames per second animaion
starting - <class 'pygame.Surface' - The image which is used for the starting screen
rules - <class 'pygame.Surface'> - The image which is used for the rules screen at the beginning
controls - <class 'pygame.Surface'> - The text for the movement controls
jump - <class 'pygame.Surface'> - The text for "press spacebar to jump"
objective - <class 'pygame.Surface'> - The text for the objective of the game
obstacles - <class 'pygame.Surface'> - The text for "avoid the obstacles in the game"
continueMethod - <class 'pygame.Surface'> - The text for "press the spacebar to continue"
creator - <class 'pygame.Surface'> - The text for me being the creator of the game
creatorFont - <class 'pygame.Surfac'> - Font for the creator text
"""

#import all the necessary modules
import pygame,os, sys,time

#initialise pygame
pygame.init()

#Requirement for codehs
os.environ['SDL_AUDIODRIVER'] = 'dsp'

#load the music and initialize mixer
bgm = pygame.mixer.Sound('./audio/bgm.wav')
bgm.set_volume(0.5)
bgm.play(loops=-1)

#The string version of the game map which I iterate through to create the actual map
gameOutline = [
'                               ',
'                               ',
'        F             F       M',
'XXX    XXX            XX     XX',
'XXX P                       XX ',
'XXXXX         XX           XXX ',
'XXX       F XX     F  T   ET   ',
'XXX    X  XXXX    XX  XXXXXX   ',
'XXTF  ET  XXXXF   XX  XXXXXX   ',
'XXXXXXXX  XXXXXX  XX  XXXXXX   ',
'XXXXXXXX  XXXXXX  XX  XXXXXX   ']

#The pixel size of each block 
blockSize = 64

#The screen's width
screenWidth = 1200

#The screen's height which depends on the blocksize and the game's outline map
screenHeight = len(gameOutline) * blockSize


#A helper function which will take a path to a file and convert the image to a better pixelated format and store it in a list
def load_images(path):
	"""
	Purpose: It takes a path to a file and using the os.walk method it gets list of all the file names in that path.
			 It then converts all the images to a better pixelated format for faster processing.
	Parameters: path - A string which contains the path to the folder containing all the image files
	Returns: pixelatedImages - A list which contains all the pixelated surface versions of the image files
	"""
	pixelatedImages = []

	for _,__,images in os.walk(path):
		for image in images:
			if image==".DS_Store":
				continue
			actualPath = path + '/' + image
			pixelated = pygame.image.load(actualPath).convert_alpha()
			pixelatedImages.append(pixelated)

	return pixelatedImages


#Class for displaying the health bar and the number of devil fruits collected
class Points:
	def __init__(self,screen):
		"""
		Purpose: Default constructor which loads all the images and the text to be displayed on the screen
		Parameters: screen - The pygame.display on which the image and font need to be rendered
		"""
		# setup 
		self.screen = screen 

		#font
		self.font = pygame.font.Font(pygame.font.get_default_font(),40)

		#health frame
		self.healthFrame = pygame.image.load('./graphics/points/health_frame.png')
		self.healthFrameRect = self.healthFrame.get_rect(topleft=(60,45))

		#devil fruit counts
		self.fruit = pygame.image.load('./graphics/fruits/1.png')
		self.fruitRect = self.fruit.get_rect(topleft=(60,125))

    #Function which keeps track of and displays the hitpoints(health) of the player out of 100
	def track_hp(self,current):
		"""
		Purpose: Blits the player's current health on the screen
		Parameters: current - An integer for the player's current health
		"""
		self.screen.blit(self.healthFrame,self.healthFrameRect)
		currentHealth = self.font.render(str(current),True,'white')
		currentHealthRect = currentHealth.get_rect(midleft = (self.healthFrameRect.right + 6, self.healthFrameRect.centery))
		self.screen.blit(currentHealth,currentHealthRect)

	#Function which keeps tracks of and displays the number of devil fruits collected by the player
	def track_fruits(self,number):
		"""
		Purpose: Blits the number of devil fruits collected by the user on screen
		Parameters: number - An integer for the number of devil fruits collected
		"""
		self.screen.blit(self.fruit,self.fruitRect)
		currentAmount = self.font.render(str(number),True,'white')
		currentAmountRect = currentAmount.get_rect(midleft=(self.fruitRect.right+6, self.fruitRect.centery))
		self.screen.blit(currentAmount,currentAmountRect)

#Class for creating a block on which the player stands
class Blocks(pygame.sprite.Sprite):
    #initialising function
	def __init__(self,size,x,y):
		"""
		Purpose: Default constructor which loads the images for the blocks
		Parameters: size - An int which contains the size of the blocks - Mostly 64 pixels
					x - The x coordinate of the position
					y - The y coordinate of the position
		"""
		super().__init__()
		self.image = pygame.Surface((size,size))
		self.image.fill('grey')
		pos = (x,y)
		self.rect = self.image.get_rect(topleft = pos)

    #function which moves the screen along with the player
	def update(self,shift):
		"""
		Purpose: Moves the tiles along with the camera
		Parameter: shift - An int for the amount by which to move the camera
		"""
		self.rect.x += shift

#Fruit class - This class is used for the devil fruits and the walls
class Fruit(pygame.sprite.Sprite):
	def __init__(self,size,x,y,path):
		"""
		Purpose: Default constructor which loads the images for the devil fruits and creates their rects
		Parameters: size - An int which contains the size of the blocks - Mostly 64 pixels
					x - The x coordinate of the position
					y - The y coordinate of the position
					path - The path to the folder containing the devil fruit images
		"""
		super().__init__()
		self.images = load_images(path)
		self.imageIndex = 0
		self.image = self.images[self.imageIndex]
		centerX = x + int(size / 2)
		centerY = y + int(size / 2)
		self.rect = self.image.get_rect(center = (centerX,centerY))

	def animate(self):
		"""
		Purpose: Loops through all the fruit image files to create an animation
		"""
		self.imageIndex += 0.005
		if self.imageIndex >= len(self.images):
			self.imageIndex = 0
		self.image = self.images[int(self.imageIndex)]

	def update(self,worldShift):
		"""
		Purpose: Moves the devil fruits along with the camera
		Parameters: worldShift - An int for the amount by which to move the camera
		"""
		self.animate()
		self.rect.x += worldShift

#Class for the enemies
class Enemy(pygame.sprite.Sprite):
	def __init__(self,size,x,y,path):
		"""
		Purpose: Default constructor which loads the images for the enemies and creates their rects
		Parameters: size - An int which contains the size of the blocks - Mostly 64 pixels
					x - The x coordinate of the position
					y - The y coordinate of the position
					path - The path to the folder containing the enemy images
		"""
		super().__init__()
		pos = (x,y)
		self.images = load_images(path)
		self.imageIndex = 0
		self.image = self.images[self.imageIndex]
		self.rect = self.image.get_rect(topleft = pos)
		self.rect.y += size - self.image.get_size()[1]
		self.speed = 4

	def animate(self):
		"""
		Purpose: Loops through all the enemy image files to create an animation
		"""
		self.imageIndex += 0.15
		if self.imageIndex >= len(self.images):
			self.imageIndex = 0
		self.image = self.images[int(self.imageIndex)]

	#Function which makes the enemy run around
	def move(self):
		"""
		Purpose: Makes the enemy run around
		"""
		self.rect.x += self.speed

	#Function which reverses the image of the enemy if the enemy is running in the opposite direction
	def reverse_image(self):
		"""
		Purpose: If the enemy turns around, make flip the image 
		"""
		if self.speed > 0:
			self.image = pygame.transform.flip(self.image,True,False)

	#Function which reverses the direction in which the enemy is moving
	def reverse(self):
		"""
		Purpose: Reverses the direction of the enemy's movement
		"""
		self.speed *= -1

	#Function which animates the enemies
	def update(self,shift):
		"""
		Purpose: Makes the enemy move with the camera and creates an animation effect by calling upon the above mentioned functions
		Parameters: shift - An integer 
		"""
		self.rect.x += shift
		self.animate()
		self.move()
		self.reverse_image()

#Player Class for creating the player
class Player(pygame.sprite.Sprite):
	def __init__(self,pos,update_health,update_fruits):
		"""
		Purpose: Default constructor which loads all the player's images and sets all the player's attributes 
				 such as the gravity and the jump height 
		Parameters: pos - A tuple for the intial position of the player
					update_health - A function which updates the player's health
					update_fruits - A function which updates the player's devil fruit count
		"""
		super().__init__()
		self.load_player_images()
		self.frameIndex = 0
		self.animationSpeed = 0.15
		self.image = self.animations['idle'][self.frameIndex]
		self.rect = self.image.get_rect(topleft = pos)

		# player movement
		self.direction = pygame.math.Vector2(0,0)
		self.speed = 8
		self.gravity = 0.7
		self.jumpHeight = -14

		# player status
		self.status = 'idle'
		self.facingRight = True
		self.onGround = False
		self.onCeiling = False
		self.onLeft = False
		self.onRight = False

		# health management'
		self.invincible = False
		self.invincibilityDuration = 1000
		self.hurtTime = 0
		
        #function for updating the player's health if the player touched an enemy
		self.update_health = update_health

		#fruit management function which increments the fruit count if the player collects a fruit
		self.update_fruits = update_fruits

		#the player's x coordinate
		self.playerX = self.rect.centerx

    #Function for loading the images for the player's animations
	def load_player_images(self):
		"""
		Purpose: Load the images for the player's animation and store them on a list
		"""
		path = './graphics/player/'
		self.animations = {'idle':[],'run':[],'jump':[],'fall':[],'win':[]}

		for animation in self.animations.keys():
			fullPath = path + animation
			self.animations[animation] = load_images(fullPath)

    #Function which loops over all the images to create an animation
	def animate(self,status):
		"""
		Purpose: Loops over all the images in the self.animations list to creat the effect of an animation
		Parameters: status - A string which indicates the status of the player (idle,running,jumping...)
		"""
		animation = self.animations[status]

		# loop over frame index 
		self.frameIndex += self.animationSpeed
		if self.frameIndex >= len(animation):
			self.frameIndex = 0

		image = animation[int(self.frameIndex)]
		if self.facingRight:
			self.image = image
		else:
			mirrorImage = pygame.transform.flip(image,True,False)
			self.image = mirrorImage

		#update the rect of the player
		if self.onGround and self.onRight:
			self.rect = self.image.get_rect(bottomright = self.rect.bottomright)
		elif self.onGround and self.onLeft:
			self.rect = self.image.get_rect(bottomleft = self.rect.bottomleft)
		elif self.onGround:
			self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
		elif self.onCeiling and self.onRight:
			self.rect = self.image.get_rect(topright = self.rect.topright)
		elif self.onCeiling and self.onLeft:
			self.rect = self.image.get_rect(topleft = self.rect.topleft)
		elif self.onCeiling:
			self.rect = self.image.get_rect(midtop = self.rect.midtop)

    #Function which checks for key presses from the user
	def key_inputs(self):
		"""
		Purpose: Function which checks if the user has pressed any of the keys for movement
		"""
		keys = pygame.key.get_pressed()

		if keys[pygame.K_RIGHT]:
			self.direction.x = 1
			self.facingRight = True
		elif keys[pygame.K_LEFT]:
			self.direction.x = -1
			self.facingRight = False
		else:
			self.direction.x = 0

		if keys[pygame.K_SPACE] and self.onGround:
			self.jump()

	def get_position(self):
		"""
		Purpose: Function which calculates the player's x coordinate - For the meteor's trajectory
		"""
		self.playerX = self.rect.centerx

    #Function which checks if the player is running, jumping, idle or falling 
	def check_status(self):
		"""
		Purpose: A function which identifies the status of the player (idle,jump,run...)
		"""
		if self.direction.y < 0:
			self.status = 'jump'
		elif self.direction.y > 1:
			self.status = 'fall'
		else:
			if self.direction.x != 0:
				self.status = 'run'
			else:
				self.status = 'idle'

    #Function which applies gravity on the player
	def apply_gravity(self):
		"""
		Purpose: Applies gravity to the player and makes the player fall down while in air
		"""
		self.direction.y += self.gravity
		self.rect.y += self.direction.y

    #Function which allows the player to jump
	def jump(self):
		"""
		Purpose: Lets the user jump when the player presses the spacebar
		"""
		self.direction.y = self.jumpHeight

    #Function which updates the player's health if he comes in contact with the enemy or bomb
	def hurt(self,amt):
		"""
		Purpose: Updates the player's health if the player comes in contact with the enemy or bomb or fireball
		Parameters: amt - An integer for the amount by which to reduce the player's health
		"""
		if not self.invincible:
			self.update_health(amt)
			self.invincible = True
			self.hurtTime = pygame.time.get_ticks()
	
    #Function which increments the devil fruit count if the player collects one
	def collect_fruit(self):
		"""
		Purpose: Increments the devil fruit count
		"""
		self.update_fruits(1)

    #Function which makes the player invincible for a short duration
	def invincibility_timer(self):
		"""
		Purpose: Makes the player invincible for 0.5 seconds to ensure that the player doesn't continuously lose health
		"""
		if self.invincible:
			currentTime = pygame.time.get_ticks()
			if currentTime - self.hurtTime >= self.invincibilityDuration:
				self.invincible = False

    #Function which calls upon the above functions to create a working player
	def update(self,done=False):
		"""
		Purpose: Function which calls the above function to create a working player
		Parameters: done - A boolean which checks if the player has won and if so, doesn't let the player move
		"""
        #If the player has won the game, it plays the winning animation
		if done:
			self.animate('win')
			self.direction.x = 0
			self.direction.y = 0
        #Else it continues normally
		else:
			self.get_position()
			self.key_inputs()
			self.check_status()
			self.animate(self.status)
			self.invincibility_timer()

#Class for the fireball
class Ball(pygame.sprite.Sprite):
	def __init__(self, size,x,y,path):
		"""
		Purpose: Deafault constructor which loads the images for the fireball and sets some attributes
		Parameters: size - Size of the fireball image (mostly 64 pixels)
					x - X coordinate of the fireball (depends on the player's position)
					y - Y coordinate of the fireball (Initally 0)
					path - Path to the image files
		"""
		super().__init__()
		self.pos = (x,y)
		self.image = load_images(path)[0]
		self.rect = self.image.get_rect(topleft=self.pos)
		self.rect.y += size - self.image.get_size()[1]
		self.speed = 6

	#Function which makes the meteor fall
	def fall(self):
		"""
		Purpose: Makes the fireball fall down
		"""
		self.rect.y += self.speed
	
	#Function which makes the fireball go back to the top after falling down completely
	def go_back(self):
		"""
		Purpose: Returns the fireball to the top of the screen if it falls down completely
		"""
		if self.rect.y > screenHeight:
			self.rect = self.image.get_rect(topleft=self.pos)
	
	#Function which moves the camera and creates the meteor by calling upon the above mentioned functions
	def update(self,worldShift):
		"""
		Purpose: Calls the above mentioned functions to create a functioning fireball
		Parameters: worldShift - The amount by which to move the camera
		"""
		self.rect.x += worldShift
		self.fall()
		self.go_back()

#Class which creates the game
class Create:
	def __init__(self,gameOutline,screen,update_health,update_fruits):
		"""
		Purpose: Default constructor for setting the attributes
		Parameters: gameOutline - A string list which contains the layout for the game map
					screen - the screen (pygame.display.set_mode((screenWidth,screenHeight)))
					update_health - A helper function which updates the player's health
					update_fruits - A helper function which updates the devil fruit count
		"""

		# game setup
		self.screen = screen 
		self.create_game(gameOutline,update_health,update_fruits)
		self.worldShift = 0
		self.currentX = 0

		#fruit count
		self.fruitCount = 0

		#check if the map has been collected
		self.done = False

		#font
		self.font = pygame.font.SysFont(pygame.font.get_default_font(),100)

	#Function which creates the level by creating the sprites
	def create_game(self,gameOutline,update_health,update_fruits):
		"""
		Purpose: Function which setus up the game by looping over the layout to place the player, enemies, blocks and other elements
		Parameters: gameOutline - A string list which contains the layout for the game map
					update_health - Helper function which updates the player's health
					update_fruits - Helper function which updates the devil fruit count
		"""
		self.blocks = pygame.sprite.Group()
		self.player = pygame.sprite.GroupSingle()
		self.fruits = pygame.sprite.Group()
		self.enemies = pygame.sprite.Group()
		self.walls = pygame.sprite.Group()
		self.map = pygame.sprite.GroupSingle()
		self.ball = pygame.sprite.GroupSingle()

		#Loops over the gameOutline and creates the sprites
		for rowIndex,row in enumerate(gameOutline):
			for colIndex,cell in enumerate(row):
				x = colIndex * blockSize
				y = rowIndex * blockSize
				
				if cell == 'X':
					tile = Blocks(blockSize,x,y)
					self.blocks.add(tile)
				if cell == 'P':
					playerSprite = Player((x,y),update_health,update_fruits)
					self.player.add(playerSprite)
				if cell == 'F':
					fruitSprite = Fruit(blockSize,x,y,'./graphics/fruits')
					self.fruits.add(fruitSprite)
				if cell == 'T':
					wall = Blocks(blockSize,x,y)
					self.walls.add(wall)
				if cell == 'E':
					enemySprite = Enemy(blockSize,x,y,'./graphics/enemy')
					self.enemies.add(enemySprite)
				if cell == 'M':
					mapSprite = Fruit(blockSize,x,y,'./graphics/map')
					self.map.add(mapSprite)
				
				player = self.player.sprite
				if player != None:
					playerX = player.rect.centerx
					ball = Ball(blockSize,(playerX+100),0,'./graphics/ball')
					self.ball.add(ball)

	#Function which moves the screen along with the player
	def move_video(self):
		"""
		Purpose: Moves the screen along with the player
		"""
		player = self.player.sprite
		playerX = player.rect.centerx
		directionX = player.direction.x

		if playerX < screenWidth / 4 and directionX < 0:
			self.worldShift = 8
			player.speed = 0
		elif playerX > screenWidth - (screenWidth / 4) and directionX > 0:
			self.worldShift = -8
			player.speed = 0
		else:
			self.worldShift = 0
			player.speed = 8

	#Function which checks if the player is horizontally colliding with any of the walls or tiles
	def horizontal_movement_collision(self):
		"""
		Purpose: Function which handles the horizontal movement collision with the walls
		"""
		player = self.player.sprite
		player.rect.x += player.direction.x * player.speed
		collidableSprites = self.blocks.sprites() + self.walls.sprites()
		for sprite in collidableSprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.x < 0: 
					player.rect.left = sprite.rect.right
					player.onLeft = True
					self.currentX = player.rect.left
				elif player.direction.x > 0:
					player.rect.right = sprite.rect.left
					player.onRight = True
					self.currentX = player.rect.right

		if player.onLeft and (player.rect.left < self.currentX or player.direction.x >= 0):
			player.onLeft = False
		if player.onRight and (player.rect.right > self.currentX or player.direction.x <= 0):
			player.onRight = False

	#Function which checks if the user is vertically colliding with any of the tiles or walls
	def vertical_movement_collision(self):
		"""
		Purpose: Function which handles the vertical movement collision with the walls
		"""
		player = self.player.sprite
		player.apply_gravity()
		collidableSprites = self.blocks.sprites() + self.walls.sprites()

		for sprite in collidableSprites:
			if sprite.rect.colliderect(player.rect):
				if player.direction.y > 0: 
					player.rect.bottom = sprite.rect.top
					player.direction.y = 0
					player.onGround = True
				elif player.direction.y < 0:
					player.rect.top = sprite.rect.bottom
					player.direction.y = 0
					player.onCeiling = True

		if player.onGround and player.direction.y < 0 or player.direction.y > 1:
			player.onGround = False
		if player.onCeiling and player.direction.y > 0.1:
			player.onCeiling = False

	#Function which reverses the direction of the enemy if the enemy collides with a wall
	def reverse_enemy_direction(self):
		"""
		Purpose: Reverses the enemies' direction if they collide with a wall
		"""
		for enemy in self.enemies.sprites():
			if pygame.sprite.spritecollide(enemy,self.walls,False):
				enemy.reverse()
	
	#Function which checks if the player is touching the enemy
	def check_enemy_collisions(self):
		"""
		Purpose: Function which checks if the player is in contact with an enemy
		"""
		enemyCollisions = pygame.sprite.spritecollide(self.player.sprite,self.enemies,False)

		if enemyCollisions:
			self.player.sprite.hurt(-10)

	#Function which checks if the user is touching a devil fruit
	def check_fruit_collision(self):
		"""
		Purpose: Function which checks if the user is in contact with a devil fruit
		"""
		collidedFruits = pygame.sprite.spritecollide(self.player.sprite,self.fruits,True)
		if collidedFruits:
			self.fruitCount += 1
			self.player.sprite.collect_fruit()
	
	#Function which checks if the user is touching the map 
	def check_map_collision(self):
		"""
		Purpose: Function which checks if the user is in contact with the map at the end
		"""
		mapCollision = pygame.sprite.spritecollide(self.player.sprite,self.map,True)
		if mapCollision:
			self.done = True
	
	#Function which checks if the fireball is touching the player
	def check_ball_collision(self):
		"""
		Purpose: Function which checks if the player is in contact with a fireball
		"""
		ballCollision = pygame.sprite.spritecollide(self.player.sprite,self.ball,False)
		if ballCollision:
			self.player.sprite.hurt(-30)
	
	#Function which checks if the player collides with a bomb
	def check_bomb_collision(self):
		"""
		Purpose: Function which checks if the player is in contact with a bomb
		"""
		wrongCollision = pygame.sprite.spritecollide(self.player.sprite,self.fruits,False)
		if wrongCollision:
			self.player.sprite.hurt(-15)

	#Function which checks if the player has collected all 6 devil fruits
	def check_done(self):
		"""
		Purpose: Function which checks if the player has collected all 6 devil fruits
		"""
		if self.fruitCount == 6:
			return True
		else:
			return False
	
	#Function which checks if the player has fallen down
	def check_defeat(self):
		"""
		Purpose: Function which checks if the player has fallen down
		"""
		if self.player.sprite.rect.top >= screenHeight:
			return True
		else:
			return False
	
	#change the fireball's postion if the player is moving
	def change_pos(self):
		"""
		Purpose: Function which increments or decrements the fireball's x coordinate depending on if the player is moving to the left, right or is idle
		"""
		playerX = self.player.sprite.playerX
		if self.player.sprite.status == 'idle':
			playerX = playerX
		elif self.player.sprite.facingRight == True:
			playerX += 100
		elif self.player.sprite.facingRight == False:
			playerX -= 100
		pos = (playerX,0)
		self.ball.sprite.pos = pos

	#Function which properly creates the game 
	def run(self):
		"""
		Purpose: Function which calls upon the above functions to create the game properly 
		"""

		#If the game is over, the characters stop moing and the screen displays "You win"
		if self.done:
			self.blocks.draw(self.screen)
			self.walls.draw(self.screen)
			self.enemies.draw(self.screen)
			self.player.update(True)
			self.player.draw(self.screen)
			finalText = self.font.render("YOU WIN!",False,'cyan')
			finalTextRect = finalText.get_rect(midleft=(400,screenHeight//2))
			self.screen.blit(finalText,finalTextRect)

		#If the player has lost, the game displays "You lost"
		elif self.check_defeat():
			finalText = self.font.render("YOU LOST!",False,'cyan')
			finalTextRect = finalText.get_rect(midleft=(400,screenHeight//2))
			self.screen.blit(finalText,finalTextRect)

		#Else, it creates the game normally
		else:
			# blocks
			self.blocks.update(self.worldShift)
			self.blocks.draw(self.screen)
			self.move_video()

			#walls
			self.walls.update(self.worldShift)
			self.walls.draw(self.screen)
			self.move_video()

			#enemies
			self.enemies.update(self.worldShift)
			self.reverse_enemy_direction()
			self.enemies.draw(self.screen)

			#fruits
			self.fruits.update(self.worldShift)
			self.fruits.draw(self.screen)

			# player
			self.player.update()
			self.horizontal_movement_collision()
			self.vertical_movement_collision()
			self.player.draw(self.screen)

			#map
			self.map.update(self.worldShift)
			self.map.draw(self.screen)

			#fireball
			self.ball.update(self.worldShift)
			self.ball.draw(self.screen)
			self.check_ball_collision()
			self.change_pos()

			#update health
			self.check_enemy_collisions()

			#update fruit count or check if bomb collision
			for i in self.fruits.sprites():
				if i.imageIndex <=1:
					self.check_bomb_collision()
				else:
					self.check_fruit_collision()

			#check for map collision if collected all fruits
			if self.check_done():
				self.check_map_collision()

#Class which runs the game
class Run:
	def __init__(self,screen):
		"""
		Purpose: Default constructor which sets the game attributes
		Parameters: screen - the screen 
		"""
		# game attributes
		self.currentHealth = 100
		self.fruits = 0

		# health and fruit count
		self.points = Points(screen)
		
		#display surface
		self.screen = screen
		
		#create the game
		self.created = Create(gameOutline,self.screen,self.update_health,self.update_fruits)

		#font
		self.font = pygame.font.SysFont('comicsansms',100)

	#Function which updates the player's hitpoints
	def update_health(self,amount):
		"""
		Purpose: Function which updates the player's health
		Parameters: amount - The amount by which to reduce the player's health
		"""
		self.currentHealth += amount
	
	#Function which updates the devil fruit count
	def update_fruits(self,amount):
		"""
		Purpose: Funtion which updates the devil fruit count
		Parameters: amount - The amount by which to increase the devil fruit count
		"""
		self.fruits += amount
	
	#Function which checks if the player's hitpoints has reached 0 
	def check_lost(self):
		"""
		Purpose: Function which checks if the player's health has fallen below 0 
		"""
		if self.currentHealth <= 0:
			return True
		else:
			return False

	#Function which runs the game
	def run(self):
		"""
		Purpose: Function which calls the above mentioned functions and the created game to run it smoothly
		"""
		#Checks if the player has lost and if so, it displays "You lost on screen"
		if self.check_lost():
			finalText = self.font.render("YOU LOST!",False,'cyan')
			finalTextRect = finalText.get_rect(midleft=(400,screenHeight//2))
			self.screen.blit(finalText,finalTextRect)
			
		#Else it calls on the above mentioned functions to create a smoothly running game
		else:
			self.created.run()
			self.points.track_hp(self.currentHealth)
			self.points.track_fruits(self.fruits)
		
#Function which checks if the user has pressed the spacebar
def key_input():
	"""
	Purpose: Function which checks if the user has pressed the spacebar
	"""
	keys = pygame.key.get_pressed()

	if keys[pygame.K_SPACE]:
		return True
	else:
		return False
		
#The screen on which to display
screen = pygame.display.set_mode((screenWidth,screenHeight))

#clock for the frame rate
clock = pygame.time.Clock()

#Creates the game which can be run
game = Run(screen)

#The background image for the starting screen
starting = pygame.image.load("./graphics/bg.png")

#The background image for the rules screen
rules = pygame.image.load("./graphics/rules.png")

#The font to be used
font = pygame.font.SysFont(pygame.font.get_default_font(),50)

#Font for creator of the game
creatorFont = pygame.font.SysFont(pygame.font.get_default_font(),20)

#Text that needs to be displayed on the screen for the rules and the starting screen
controls = font.render('1. Use the left and right arrow keys to move',True,'white')
jump = font.render("2. Use the spacebar to jump",True,'white')
objective = font.render("3. Collect all the devil fruits and the map to win!",True,'white')
obstacles = font.render("4. Beware of the obstacles!",True,'white')
continueMethod = font.render("5. Press the spacebar to continue!", True, 'white')
creator = font.render("A game by Aditya Nair",True,'black')
controlsRect = controls.get_rect(midleft = (100,(1/7*screenHeight)))
jumpRect = jump.get_rect(midleft = (100,(2/7*screenHeight)))
objectiveRect = objective.get_rect(midleft = (100,(3/7*screenHeight)))
obstaclesRect = obstacles.get_rect(midleft = (100,(4/7*screenHeight)))
continueRect = continueMethod.get_rect(midleft=(100,(5/7*screenHeight)))
creatorRect = creator.get_rect(midleft=(600,(5/7*screenHeight)))

#A dictionary for the text and their respective position
displayRules = {controls:controlsRect,jump:jumpRect,objective:objectiveRect,obstacles:obstaclesRect,continueMethod:continueRect}

#while loop which blits the rules on the screen and continues if the player presses the spacebar
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	screen.fill('black')
	screen.blit(rules,(0,0))
	for i in displayRules.keys():
		screen.blit(i,displayRules[i])
	if key_input():
		break
	pygame.display.update()
	clock.tick(60)

time.sleep(0.15)

#While loop which prints the starting screen and continues if the player presses the spacebar
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
	screen.fill('black')
	screen.blit(starting,(0,0))
	screen.blit(creator,creatorRect)
	if key_input():
		break
	pygame.display.update()
	clock.tick(60)

#time.sleep() for a fraction of a second so that the player doesn't jump at the start of the game
time.sleep(0.1)

#while loop which runs the game
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			bgm.stop()
			pygame.quit()
			sys.exit()
	
	screen.fill('black')
	game.run()
	pygame.display.update()
	clock.tick(60)