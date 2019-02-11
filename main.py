from direct.showbase.ShowBase import ShowBase;
from direct.actor.Actor import Actor;

class MyApp(ShowBase):

    def __init__(self):
        ShowBase.__init__(self);

        #Load and transform the panda Actor
        self.pandaActor = Actor("models/panda-model", {"walk": "models/panda-walk4"});
        self.pandaActor.setScale(0.005, 0.005, 0.005);
        self.pandaActor.setPos(0, 30, -5);
        self.pandaActor.setHpr(180, 0, 0);
        self.pandaActor.reparentTo(self.render);
        #Loop its animation
        self.pandaActor.loop("walk");

app = MyApp();
app.run();
