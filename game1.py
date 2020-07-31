import pygame as pg
import random

pg.init()
screen=pg.display.set_mode((0,0),pg.FULLSCREEN)
win_x,win_y=screen.get_size()
done=False
clock=pg.time.Clock()

sesong = 'gametheme.mp3'
pg.mixer.music.load(sesong)

def disp(object):
	screen.blit(object.image,(object.x-int(object.image.get_size()[0]/2),
								object.y-int(object.image.get_size()[1]/2)))

def getImg(name):
	image=pg.image.load(name).convert_alpha()
	return image

class attackShip:

	def __init__(self):
		self.lives=5
		self.id="ship"
		self.maxspeed=15
		self.momentum=2
		self.x=int(win_x/2)
		self.y=win_y-100
		self.speed=0
		self.direction="none"
		self.image=None
		self.imageLeft=None
		self.imageRight=None
		self.imageIdle=None
		self.control="ship"
		self.bulletType=1
		self.invisible=False

	def shoot(self):
		pass

	def speedup(self):
		pass

	def slowdown(self):
		pass

	def left(self):

		if self.direction=="right":
			self.speed=0


		self.speed=self.speed+self.momentum
		self.direction="left"
		
		if(self.speed>15):
			self.speed=self.maxspeed
			self.image=self.imageLeft
		
		self.x=self.x-self.speed


	def right(self):

		if self.direction=="left":
			self.speed=0

		self.speed=self.speed+self.momentum
		self.direction="right"
		
		if(self.speed>15):
			self.speed=self.maxspeed
			self.image=self.imageRight
		
		self.x=self.x+self.speed

	def do(self):

		if(self.x<100):
			self.x=100
			self.image=self.imageIdle

		if(self.x>win_x-100):
			self.x=win_x-100
			self.image=self.imageIdle

		if(self.speed>0):
			self.speed=self.speed-1
		else:
			self.speed=0
			self.direction="none"

		if self.speed<int(self.maxspeed/2):
			self.image=self.imageIdle

		if(self.direction=="none"):
			return

		if(self.direction=="left"):
			self.x=self.x-self.speed

		if(self.direction=="right"):
			self.x=self.x+self.speed


def control(object):

	pressed=pg.key.get_pressed()

	if pressed[pg.K_RETURN]:
		restart()

	#if(object.y>250):
		#object.on_ground=1
		#object.y=250
	if pressed[pg.K_UP]:
		object.shoot()
		object.control = "bulletCreate"
	if pressed[pg.K_UP]:
		object.speedup()
	if pressed[pg.K_DOWN]:
		object.slowdown()
	if pressed[pg.K_LEFT]:
		object.left()
	if pressed[pg.K_RIGHT]:
		object.right()

	object.do()

def control2(object):

	pressed=pg.key.get_pressed()

	#if(object.y>250):
		#object.on_ground=1
		#object.y=250
	if pressed[pg.K_w]:
		object.shoot()
		object.control = "bulletCreate"
	if pressed[pg.K_UP]:
		object.speedup()
	if pressed[pg.K_s]:
		object.slowdown()
	if pressed[pg.K_a]:
		object.left()
	if pressed[pg.K_d]:
		object.right()

	object.do()


def restart():

	ship.x=int(win_x/2)
	ship2.x=int(win_x/2)
	ship.lives=5
	ship2.lives=5
	ship.bulletType=1
	ship2.bulletType=1
	ship.maxspeed=15
	ship2.maxspeed=15
	ship.invisible=False
	ship2.invisible=False

#define objects
ship=attackShip()
ship.imageIdle=getImg('ship.png')
ship.imageIdle=pg.transform.scale(ship.imageIdle,
	(int(ship.imageIdle.get_size()[0]*2),int(ship.imageIdle.get_size()[1]*2)))
ship.imageLeft=pg.transform.scale(ship.imageIdle,
	(int(ship.imageIdle.get_size()[0]/2),int(ship.imageIdle.get_size()[1])))
ship.imageRight=pg.transform.flip(ship.imageLeft,True,False)
ship.image=ship.imageIdle
ship.id="ship1"

ship2=attackShip()
ship2.imageIdle=getImg('ship2.png')
ship2.imageIdle=pg.transform.scale(ship2.imageIdle,
	(int(ship2.imageIdle.get_size()[0]*2),int(ship2.imageIdle.get_size()[1]*2)))
ship2.imageIdle=pg.transform.rotate(ship2.imageIdle,180)
ship2.imageLeft=pg.transform.scale(ship2.imageIdle,
	(int(ship.imageIdle.get_size()[0]/2),int(ship.imageIdle.get_size()[1])))
ship2.imageRight=pg.transform.flip(ship2.imageLeft,True,False)
ship2.image=ship2.imageIdle
ship2.id="ship2"

ship2.y=100

background=getImg('space.png')
background=pg.transform.scale(background,(win_x,win_y))

font = pg.font.Font('freesansbold.ttf',32)
text=font.render('lives',True,(0,255,0),)

#functions and classes

class bullet:

	def __init__(self):
		self.image=getImg('missile.png')
		self.image=pg.transform.scale(self.image,(15,50))
		self.destroyImg=getImg('explosion.png')
		self.speedy=25
		self.speedx=30
		self.x=0
		self.y=0
		self.time=3
		self.state="bullet"
		self.ship=1
		self.type=1

	def destroy(self):
		self.image=self.destroyImg
		self.state="destroyed"
		disp(self)

	def do(self):

		if(self.time<=0):
			self.state="destroyed"
			self.image=None

		if(self.state=="destroy"):
			self.time-=1

class bullet2(bullet):

	def __init__(self):

		super(bullet2,self).__init__()

		self.image=getImg('dirt.png')
		self.image=pg.transform.scale(self.image,(15,50))
		self.speedx=0
		self.speedy=50
		self.type=2

class weapon:

	def __init__(self,x1,y1,imname,type1):

		self.image=getImg(imname)
		self.xsize=50
		self.ysize=80
		self.image=pg.transform.scale(self.image,(self.xsize,self.ysize))
		self.type=type1
		self.x=x1
		self.y=y1
		self.speed=5
		self.direction=1
		self.state="inactive"

	def getWeapon(self,someship):

		someship.bulletType=self.type

	def move(self):

		self.x=self.x+self.speed*self.direction

		if(self.x>win_x or self.x<0):
			self.state="inactive"

	def isHit(self,bullet):

		if self.state=="active" and bullet.x>self.x-self.xsize/2-10 and bullet.x<self.x+self.xsize/2+10 and bullet.y>self.y-self.ysize/2 and bullet.y<self.y+self.ysize/2:

			if(bullet.ship=="ship1"):
				print(ship.bulletType," : bullet type ship1")
				self.getWeapon(ship)
				bullet.destroy()
				self.state="inactive"
				return

			if(bullet.ship=="ship2"):
				print(ship2.bulletType," : bullet type ship2")
				self.getWeapon(ship2)
				bullet.destroy()
				self.state="inactive"
				return

	def highlight(self):
		pg.draw.rect(screen,(200,100,150),(self.x-int(self.xsize/2)-4,self.y-int(self.ysize/2)-4,self.xsize+8,self.ysize+8),2)


class Health(weapon):

	def __init__(self,x1,y1,imname,type1):

		super(Health,self).__init__(x1,y1,imname,type1)

	def isHit(self,bullet):

		if self.state=="active" and bullet.x>self.x-self.xsize/2 and bullet.x<self.x+self.xsize/2 and bullet.y>self.y-self.ysize/2 and bullet.y<self.y+self.ysize/2:

			if(bullet.ship=="ship1"):
				ship.lives+=1
				bullet.destroy()
				self.state="inactive"
				return

			if(bullet.ship=="ship2"):
				ship2.lives+=1
				bullet.destroy()
				self.state="inactive"
				return

class Boost(weapon):

	def __init__(self,x1,y1,imname,type1):

		super(Boost,self).__init__(x1,y1,imname,type1)

	def isHit(self,bullet):

		if self.state=="active" and bullet.x>self.x-self.xsize/2 and bullet.x<self.x+self.xsize/2 and bullet.y>self.y-self.ysize/2 and bullet.y<self.y+self.ysize/2:

			if(bullet.ship=="ship1"):
				ship.maxspeed+=10
				bullet.destroy()
				self.state="inactive"
				return

			if(bullet.ship=="ship2"):
				ship.maxspeed+=10
				bullet.destroy()
				self.state="inactive"
				return

class Invisiblity(weapon):

	def __init__(self,x1,y1,imname,type1):

		super(Invisiblity,self).__init__(x1,y1,imname,type1)

	def isHit(self,bullet):

		if self.state=="active" and bullet.x>self.x-self.xsize/2 and bullet.x<self.x+self.xsize/2 and bullet.y>self.y-self.ysize/2 and bullet.y<self.y+self.ysize/2:

			if(bullet.ship=="ship1"):
				ship.invisible=True
				bullet.destroy()
				self.state="inactive"
				return

			if(bullet.ship=="ship2"):
				ship2.invisible=True
				bullet.destroy()
				self.state="inactive"
				return

def controlbullet(bullet1):

	if bullet1.type==2:
		control(ship)

	if bullet1.x>ship2.x-50 and bullet1.x<ship2.x+50 and bullet1.y>ship2.y-50 and bullet1.y<ship2.y+50:
			ship2.lives=ship2.lives-1
			ship2.invisible=False
			print("ship2 destroyed")
			bullet1.destroy()

	if bullet1.y<-100:
		bullet1.destroy()

	pressed=pg.key.get_pressed()
	bullet1.y=bullet1.y-bullet1.speedy

	if pressed[pg.K_SPACE]:
		pass
	if pressed[pg.K_UP]:
		pass
	if pressed[pg.K_DOWN]:
		if bullet1.x>ship2.x-100 and bullet1.x<ship2.x+100 and bullet1.y>ship2.y-100 and bullet1.y<ship2.y+100:
			ship2.lives=ship2.lives-1
			ship2.invisible=False
			print("ship2 destroyed")
		bullet1.destroy()
	if pressed[pg.K_LEFT]:
		bullet1.x=bullet1.x-bullet1.speedx
	if pressed[pg.K_RIGHT]:
		bullet1.x=bullet1.x+bullet1.speedx

def controlbullet2(bullet1):

	if bullet1.type==2:
		control2(ship2)

	if bullet1.x>ship.x-50 and bullet1.x<ship.x+50 and bullet1.y>ship.y-50 and bullet1.y<ship.y+50:
			ship.lives=ship.lives-1
			ship.invisible=False
			print("ship1 destroyed")
			bullet1.destroy()

	if bullet1.y>win_y+100:
		bullet1.destroy()

	pressed=pg.key.get_pressed()
	bullet1.y=bullet1.y+bullet1.speedy

	if pressed[pg.K_SPACE]:
		pass
	if pressed[pg.K_UP]:
		pass
	if pressed[pg.K_s]:
		if bullet1.x>ship.x-100 and bullet1.x<ship.x+100 and bullet1.y>ship.y-100 and bullet1.y<ship.y+100:
			ship.lives=ship.lives-1
			ship.invisible=False
			print("ship1 destroyed")
		bullet1.destroy()
	if pressed[pg.K_a]:
		bullet1.x=bullet1.x-bullet1.speedx
	if pressed[pg.K_d]:
		bullet1.x=bullet1.x+bullet1.speedx

	if pressed[pg.K_s]:
		pass

def createbullet(ship):

	if ship.bulletType==1:

		Bullet=bullet()
		Bullet.x=ship.x
		Bullet.y=ship.y
		Bullet.ship=ship.id
		return Bullet

	if ship.bulletType==2:
		
		Bullet=bullet2()
		Bullet.x=ship.x
		Bullet.y=ship.y
		Bullet.ship=ship.id
		return Bullet


def manageBullets():
	pass


def drawMenus():
	num1=font.render(str(ship.lives),True,(100,255,0),).convert_alpha()
	num2=font.render(str(ship2.lives),True,(100,255,0),).convert_alpha()

	screen.blit(text,(10,10))
	screen.blit(num2,(35,50))

	screen.blit(text,(10,win_y-100))
	screen.blit(num1,(35,win_y-60))

def drawmap():

	screen.blit(background,(0,0))
	drawMenus()
	manageBullets()

def write(string,x,y,rgb,size):
	font=pg.font.Font('freesansbold.ttf',size)
	stre = font.render(string,True,rgb,).convert_alpha()
	screen.blit(stre,(x-int(stre.get_size()[0]/2),y-int(stre.get_size()[1]/2)))

def checkwin():

	if ship.lives<=0:
		write("SHIP 2 WINS",int(win_x/2),int(win_y/2),(200,100,100),40)
		write("press enter for rematch",int(win_x/2),int(win_y/2)+50,(200,100,100),20)
		ship2.lives=5
		newweapon.state="inactive"

	if ship2.lives<=0:
		write("SHIP 1 WINS",int(win_x/2),int(win_y/2),(100,100,200),40)
		write("press enter for rematch",int(win_x/2),int(win_y/2)+50,(100,100,200),20)
		ship.lives=5
		newweapon.state="inactive"

def manageWeapon(weapon):

	if weapon.state=="active":
		disp(weapon)

	weapon.move()

#main

pg.mixer.music.play(-1)

ship.bulletType=1
ship2.bulletType=1

weapon1=weapon(win_x/2-100,win_y/2,'dirt.png',2)
weapon2=weapon(win_x/2+100,win_y/2,'missile.png',1)
health=Health(win_x/2+100,win_y/2,'sky.png',3)
boost=Boost(win_x/2+100,win_y/2,'ship.png',4)
invisiblity=Invisiblity(win_x/2+100,win_y/2,'space.png',5)

#menu
quit=False
while not done:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			done=True
			quit=True

	pressed=pg.key.get_pressed()

	if pressed[pg.K_RETURN]:
		done=True

	if pressed[pg.K_ESCAPE]:
		screen=pg.display.set_mode((win_x,win_y))

	screen.blit(background,(0,0))
	write("<<< DOGFIGHT >>>",int(win_x/2),int(win_y/2),(255,0,0),60)
	write("press enter to continue",int(win_x/2),int(win_y/2)+50,(250,0,0),20)

	disp(ship)
	disp(ship2)

	pg.display.flip()
	clock.tick(60)

done=False

count=0
newweapon=weapon1

#game
while not done and not quit:
	for event in pg.event.get():
		if event.type == pg.QUIT:
			done=True

	pressed=pg.key.get_pressed()

	if pressed[pg.K_ESCAPE]:
		screen=pg.display.set_mode((win_x,win_y))	

	drawmap()

	if count%60==0:

		if(random.choice(range(0,1000))<200 and newweapon.state=="inactive"):
			newweapon=random.choice([weapon1,weapon2,health,boost,invisiblity])
			newweapon.y=win_y/2
			newweapon.x=random.choice([0,win_x])

			if newweapon.x==win_x:
				newweapon.direction=-1
			if newweapon.x==0:
				newweapon.direction=1

			newweapon.state="active"

	if ship.control=="ship":
		control(ship)

	if ship2.control=="ship":
		control2(ship2)

	if ship.control=="bulletCreate":
		ship.do()
		Bullet=createbullet(ship)
		ship.control="bullet"

	if ship2.control=="bulletCreate":
		ship2.do()
		Bullet2=createbullet(ship2)
		Bullet2.image=pg.transform.rotate(Bullet2.image,180)
		ship2.control="bullet"

	if ship.control=="bullet":
		ship.do()
		controlbullet(Bullet)
		newweapon.isHit(Bullet)
		disp(Bullet)
		if Bullet.state=="destroyed":
			ship.control="ship"

	if ship2.control=="bullet":
		ship2.do()
		controlbullet2(Bullet2)
		newweapon.isHit(Bullet2)
		disp(Bullet2)
		if Bullet2.state=="destroyed":
			ship2.control="ship"

	if ship.invisible==False:
		disp(ship)

	if ship2.invisible==False:
		disp(ship2)
	
	manageWeapon(newweapon)

	checkwin()
	count+=1

	pg.display.flip()
	clock.tick(60)