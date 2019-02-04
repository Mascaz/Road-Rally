from math import pi, sin, cos;

from direct.showbase.ShowBase import ShowBase;
from direct.task import Task

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self);

        #Load the environment model
        self.scene = self.loader.loadModel("models/environment");
        #Reparent the model to render
        self.scene.reparentTo(self.render);
        #Apply scale and position transforms on the model
        self.scene.setScale(0.25, 0.25, 0.25);
        self.scene.setPos(-8, 42, 0);

        #Add the spinCameraTask procedure to the task manager
        self.taskMgr.add(self.spinCameraTask, "SpinCameraTask");

    #Define a procedure to move the camera
    def spinCameraTask(self, task):
        angleDegrees = task.time * 6.0; #Rotates camera every 6 seconds
        angleRadians = angleDegrees * (pi / 180.0); # Radians needed to calculate position
        self.camera.setPos(20 * sin(angleRadians), -20.0 * cos(angleRadians), 3); # Sets the position in a circular motion
        self.camera.setHpr(angleDegrees, 0, 0); # Rotates the camera at the same rate as the angle in radians but in degrees
        return Task.cont; #Task is returned for the task manager to handle

app = MyApp();
app.run();
