from direct.showbase.ShowBase import ShowBase;
from direct.actor.Actor import Actor;
from panda3d.bullet import BulletWorld
from panda3d.bullet import BulletRigidBodyNode
from panda3d.bullet import BulletBoxShape
from panda3d.bullet import BulletPlaneShape
from panda3d.bullet import BulletCylinderShape
from panda3d.bullet import BulletVehicle
from panda3d.core import Vec3

class RoadRally(ShowBase):

    def __init__(self):
        ShowBase.__init__(self);

        scene = BulletWorld();
        scene.setGravity(Vec3(0, 0, -9.81));
        base.setBackgroundColor(0.6,0.9,0.9);

        #The ground
        self.ground = BulletPlaneShape(Vec3(0, 0, 1,), 1)
        self.ground_node = BulletRigidBodyNode("The ground")
        self.ground_node.addShape(self.ground)
        self.ground_np = render.attachNewNode(self.ground_node)
        self.ground_np.setPos(0, 0, -2)
        scene.attachRigidBody(self.ground_node)

        #Load and transform the Car Actor
        self.car_model = loader.loadModel("Models/Car.egg");
        self.car_model.setPos(0, 20, -3);
        self.car_model.setHpr(180, 0, 0);
        self.car_model.reparentTo(self.render);

app = RoadRally();
app.run();
