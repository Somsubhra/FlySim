# Import all libraries
import direct.directbase.DirectStart 
from panda3d.core import Fog
from direct.showbase.DirectObject import DirectObject
from direct.interval.MetaInterval import Sequence
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func
from direct.task import Task
import sys
import serial

# Define constants 
TUNNEL_SEGMENT_LENGTH = 50           
TUNNEL_TIME = 15

# The World class
class World(DirectObject):

# Initialize the world class
	def __init__(self):

# Load the Boeing707
		self.scale = 0.04
		self.xPos = 0.0
		self.yPos = 0.0
		self.tilt = 0.0
		
		self.plane = loader.loadModel('./models/plane/boeing707')
		self.plane.reparentTo(render)
		self.plane.setScale(self.scale, self.scale, self.scale)  	
		self.xPos = 0
		self.tilt = 0.0
		self.plane.setPosHpr(self.xPos, -0.7, 0, 0, 270, self.tilt)


		base.disableMouse()
		camera.setPosHpr(0, 0.5, 10, 0, -100, 0) #Vary this
		base.setBackgroundColor(0, 0.5, 1)
    
# Load fog into the view
		self.fog = Fog('distanceFog')
		self.fog.setColor(0, 0.5, 1)
		self.fog.setExpDensity(.08)
		render.setFog(self.fog)

# Load the tunnel and keep it running infinitely
		self.initTunnel()
		self.contTunnel()

# Key mappings
		self.accept('escape', sys.exit)
		self.accept('d', self.moveRight)
		self.accept('a', self.moveLeft)
		self.accept('+', self.scaleUp)
		self.accept('-', self.scaleDown)

		try:
			self.ser = serial.Serial('/dev/ttyUSB0', 9600)
			taskMgr.add(self.serialTask, "serialTask")
		except:
			print("Could not open Serial port")

# The serial task
	def serialTask(self, task):
		reading = self.ser.readline()

		if(reading != ""):
			try:
				if(reading[0] == 'y'):
					x = float(reading[1:])
				
				if(reading[1] == 'x'):
					y = float(reading[1:])

				devX = (320.0 - x)
		
				if(devX < -25):
					self.moveLeft()
				elif(devX > 25):
					self.moveRight()
				else:
					self.stabilizePlane()
			except:
				pass

		return Task.cont

# Make the Boeing stable
	def stabilizePlane(self):
		if(self.tilt > 0):
			if(self.tilt != 0.0):
				self.tilt = self.tilt - 0.25
		else:
			if(self.tilt != 0.0):
				self.tilt = self.tilt + 0.25
		self.plane.setPosHpr(self.xPos, -0.7, 0, 0, 270, self.tilt)

# Zoom into the plane
	def scaleUp(self):
		self.scale = self.scale + 0.005
		self.plane.setScale(self.scale, self.scale, self.scale)

# Zoom out of the plane
	def scaleDown(self):
		self.scale = self.scale - 0.005
		self.plane.setScale(self.scale, self.scale, self.scale)
  	
# Move the plane right
	def moveRight(self):
		if(self.tilt >= 30):
			self.tilt = 30
		self.xPos = self.xPos + 0.01
		self.tilt = self.tilt + 0.25
		self.plane.setPosHpr(self.xPos, -0.7, 0, 0, 270, self.tilt)

# Move the plane left
	def moveLeft(self):
		if(self.tilt <= -30):
			self.tilt = -30
		self.tilt = self.tilt - 0.25
		self.xPos = self.xPos - 0.01
		self.plane.setPosHpr(self.xPos, -0.7, 0, 0, 270, self.tilt)
  
# The tunnel initialization function
	def initTunnel(self):
		self.tunnel = [None for i in range(4)]
    
		for x in range(4):
			self.tunnel[x] = loader.loadModel('models/terrain/tunnel')

			if x == 0:
				self.tunnel[x].reparentTo(render)

			else:
				self.tunnel[x].reparentTo(self.tunnel[x-1])

			self.tunnel[x].setPos(0, 0, -TUNNEL_SEGMENT_LENGTH)

# Function to keep the tunnel running infinite
	def contTunnel(self):
		self.tunnel = self.tunnel[1:]+ self.tunnel[0:1]

		self.tunnel[0].setZ(0)

		self.tunnel[0].reparentTo(render)

		self.tunnel[0].setScale(.355, .355, .505)

		self.tunnel[3].reparentTo(self.tunnel[2])
		self.tunnel[3].setZ(-TUNNEL_SEGMENT_LENGTH)
		self.tunnel[3].setScale(1)

		self.tunnelMove = Sequence(
			LerpFunc(self.tunnel[0].setZ,
					duration = TUNNEL_TIME,
					fromData = 0,
					toData = TUNNEL_SEGMENT_LENGTH*.305),
			Func(self.contTunnel)
		)
		self.tunnelMove.start()

# Load the world
w = World()
run()

