import direct.directbase.DirectStart 
from panda3d.core import Fog
from direct.showbase.DirectObject import DirectObject
from direct.interval.MetaInterval import Sequence
from direct.interval.LerpInterval import LerpFunc
from direct.interval.FunctionInterval import Func
import sys

TUNNEL_SEGMENT_LENGTH = 50           
TUNNEL_TIME = 2

class World(DirectObject):

  def __init__(self):

  	self.plane = loader.loadModel('./models/plane/boeing707')
  	self.plane.reparentTo(render)
  	self.plane.setScale(0.04, 0.04, 0.04)
  	
  	self.xPos = 0
  	self.plane.setPosHpr(self.xPos,-0.7,0,0,270,0)

  	base.disableMouse()
   	camera.setPosHpr(0,0.5,10, 0, -100, 0) #Vary this
   	base.setBackgroundColor(0,0.5,1)
    
   	self.fog = Fog('distanceFog')

   	self.fog.setColor(0, 0.5, 1)

   	self.fog.setExpDensity(.08)

   	render.setFog(self.fog)

   	self.initTunnel()
   	self.contTunnel()

   	self.accept('escape', sys.exit)
   	self.accept('d', self.moveRight)
   	self.accept('a', self.moveLeft)
    
  def moveRight(self):
  	self.xPos = self.xPos + 0.1
  	self.plane.setPosHpr(self.xPos, -0.7, 0, 0, 270, 0)


  def moveLeft(self):
  	self.xPos = self.xPos - 0.1
  	self.plane.setPosHpr(self.xPos, -0.7, 0, 0, 270, 0)
  
  def initTunnel(self):
    self.tunnel = [None for i in range(4)]
    
    for x in range(4):
      self.tunnel[x] = loader.loadModel('models/terrain/tunnel')

      if x == 0: self.tunnel[x].reparentTo(render)

      else:      self.tunnel[x].reparentTo(self.tunnel[x-1])

      self.tunnel[x].setPos(0, 0, -TUNNEL_SEGMENT_LENGTH)

  def contTunnel(self):
    self.tunnel = self.tunnel[1:]+ self.tunnel[0:1]

    self.tunnel[0].setZ(0)

    self.tunnel[0].reparentTo(render)

    self.tunnel[0].setScale(.155, .155, .305)

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

w = World()
run()

