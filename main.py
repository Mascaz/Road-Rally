from direct.showbase.ShowBase import ShowBase;
from direct.actor.Actor import Actor;
from panda3d.bullet import BulletWorld;
from panda3d.bullet import BulletRigidBodyNode;
from panda3d.bullet import BulletBoxShape;
from panda3d.bullet import BulletPlaneShape;
from panda3d.bullet import BulletCylinderShape;
from panda3d.bullet import BulletVehicle;
from panda3d.core import Vec3;
from panda3d.core import Point3;
from panda3d.bullet import ZUp;
from direct.showbase.InputStateGlobal import inputState;

class RoadRally(ShowBase):

    def __init__(self):
        ShowBase.__init__(self);

        scene = BulletWorld();
        scene.setGravity(Vec3(0, 0, -9.81));
        base.setBackgroundColor(0.6,0.9,0.9);

        #Variables
        self.steering = 0;

        #Controls
        inputState.watchWithModifiers("F", "arrow_up")
        inputState.watchWithModifiers("B", "arrow_down")
        inputState.watchWithModifiers("L", "arrow_left")
        inputState.watchWithModifiers("R", "arrow_right")

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

        #Load and transform the Car Actor
        self.car_model = loader.loadModel("Models/Car.egg");
        self.car_model.setPos(0, 20, -3);
        self.car_model.setHpr(180, 0, 0);
        self.car_model.reparentTo(Car_np);

        self.Car_sim = BulletVehicle(scene, Car_np.node());
        self.Car_sim.setCoordinateSystem(ZUp);
        scene.attachVehicle(self.Car_sim);

        #Camera
        #base.disableMouse()
        camera.reparentTo(Car_np);
        camera.setPos(0, 0, 0);
        camera.setHpr(0, 0, 0);

        def Wheel(pos, r, f):
            w = self.Car_sim.createWheel();
            w.setChassisConnectionPointCs(pos);
            w.setFrontWheel(f);
            w.setWheelDirectionCs(Vec3(0, 0, -1));
            w.setWheelAxleCs(Vec3(1, 0, 0));
            w.setWheelRadius(r);
            w.setMaxSuspensionTravelCm(40);
            w.setSuspensionStiffness(120);
            w.setWheelsDampingRelaxation(2.3);
            w.setWheelsDampingCompression(4.4);
            w.setFrictionSlip(50);
            w.setRollInfluence(0.1);

        #Wheels
        Wheel(Point3(-1,1,-0.6), 0.4, False);
        Wheel(Point3(-1.1,-1.2,-0.6), 0.4, True);
        Wheel(Point3(1.1,-1,-0.6), 0.4, True);
        Wheel(Point3(1,1,-0.6), 0.4, False);

        def ProcessInput(dt):

            engineForce = 0.0;
            self.steeringClamp = 35.0;
            self.steeringIncrement = 70;

            #Get the vehicle's current speed
            self.carspeed = self.Car_sim.getCurrentSpeedKmHour();

            #Reset the steering
            if not inputState.isSet("L") and not inputState.isSet("R"):

                if self.steering < 0.00:
                    self.steering = self.steering + 0.6;
                    if self.steering > 0.00:
                        self.steering = self.steering - 0.6;

                    if self.steering < 1.0 and self.steering > -1.0:
                        self.steering = 0;

            if inputState.isSet("F"):
                engineForce = 35;

            if inputState.isSet("B"):
                engineForce = -35;

            #Left
            if inputState.isSet("L"):
                if self.steering < 0.0:
                    #This makes the steering reset at the correct speed when turning from right to left
                    self.steering += dt * self.steeringIncrement + 0.6;
                    self.steering = min(self.steering, self.steeringClamp);
                else:
                    #Normal steering
                    self.steering += dt * self.steeringIncrement;
                    self.steering = min(self.steering, self.steeringClamp);

			#Right
            if inputState.isSet("R"):
                if self.steering > 0.0:
                    #This makes the steering reset at the correct speed when turning from left to right
                    self.steering -= dt * self.steeringIncrement + 0.6;
                    self.steering = max(self.steering, -self.steeringClamp);
                else:
                    #Normal steering
                    self.steering -= dt * self.steeringIncrement;
                    self.steering = max(self.steering, -self.steeringClamp);

            #Apply forces to wheels
            self.Car_sim.applyEngineForce(engineForce, 0);
            self.Car_sim.applyEngineForce(engineForce, 3);

        def Update(task):
            dt = globalClock.getDt();
            ProcessInput(dt);
            scene.doPhysics(dt, 5, 1.0/180.0);
            return task.cont;

        taskMgr.add(Update, "Update");

app = RoadRally();
app.run();
