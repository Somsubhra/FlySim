from math import pi, sin, cos
from direct.showbase.ShowBase import ShowBase
from direct.task import Task
class FliSim(ShowBase):

	def __init__(self):
		ShowBase.__init__(self)
		self.setBackgroundColor(0, 0, 0)
		self.environ = self.loader.loadModel("./models/forestsky")

		self.environ.reparentTo(self.render)

		self.environ.setScale(0.50, 0.50, 0.50)
		self.environ.setPos(-15 , -15, 20)

		self.taskMgr.add(self.spinCameraTask, "spinCameraTask")

	def spinCameraTask(self, task):
		angleDegrees = task.time * 30.0
		angleRadians = angleDegrees * (pi / 180.0)
		self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3)
		self.camera.setHpr(angleDegrees, 0, 0)
		return Task.cont

sim = FliSim()
sim.run()