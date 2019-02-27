from direct.showbase.ShowBase import ShowBase;
from direct.actor.Actor import Actor;
from panda3d.bullet import BulletWorld;
from panda3d.bullet import BulletRigidBodyNode;
from panda3d.bullet import BulletBoxShape;
from panda3d.bullet import BulletPlaneShape;
from panda3d.bullet import BulletCylinderShape;
from panda3d.bullet import BulletVehicle;
from panda3d.core import Vec3;
from panda3d.bullet import ZUp;

class RoadRally(ShowBase):

    def __init__(self):
        ShowBase.__init__(self);

        scene = BulletWorld();
        scene.setGravity(Vec3(0, 0, -9.81));
        base.setBackgroundColor(0.6,0.9,0.9);

        #The ground
        self.ground = BulletPlaneShape(Vec3(0, 0, 1,), 1);
        self.ground_node = BulletRigidBodyNode("The ground");
        self.ground_node.addShape(self.ground);
        self.ground_np = render.attachNewNode(self.ground_node);
        self.ground_np.setPos(0, 0, -2);
        scene.attachRigidBody(self.ground_node);

        self.track_model = loader.loadModel("Models/Track.egg");
        self.track_model.reparentTo(self.render);
        self.track_model.setPos(0, 0, -7);
        self.track_tex = loader.loadTexture("Textures/Road.jpg");
        self.track_model.setTexture(self.track_tex, 1);

        #The car
        Car_shape = BulletBoxShape(Vec3(1, 2.0, 1.0))
        Car_node = BulletRigidBodyNode("The Car")
        Car_node.setMass(1200.0)
        Car_node.addShape(Car_shape)
        Car_np = render.attachNewNode(Car_node)
        Car_np.setPos(0,0,0)
        Car_np.setHpr(0,0,0)
        Car_np.node().setDeactivationEnabled(False)
        scene.attachRigidBody(Car_node)

        self.Car_sim = BulletVehicle(scene, Car_np.node())
        self.Car_sim.setCoordinateSystem(ZUp)
        scene.attachVehicle(self.Car_sim)

        #Load and transform the Car Actor
        self.car_model = loader.loadModel("Models/Car.egg");
        self.car_model.setPos(0, 20, -3);
        self.car_model.setHpr(180, 0, 0);
        self.car_model.reparentTo(self.render);
        self.car_model.reparentTo(Car_np);

        def Update(task):
            dt = globalClock.getDt();
            scene.doPhysics(dt, 5, 1.0/180.0);
            return task.cont;

app = RoadRally();
app.run();
