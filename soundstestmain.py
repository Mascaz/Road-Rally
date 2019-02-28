from panda3d.core import loadPrcFileData

loadPrcFileData("", "win-size 1200 600")
loadPrcFileData("", "audio-libary-name p3openal-audio")
from direct.showbase.ShowBase import ShowBase
from panda3d.core import NodePath, TextNode
from direct.gui.OnscreenText import OnscreenText
from direct.showbase.DirectObject import DirectObject
from direct.interval.SoundInterval import SoundInterval
from direct.interval.LerpInterval import LerpHprInterval
from direct.showbase.InputStateGlobal import inputState
import sys

base = ShowBase()

class SoundManager(ShowBase):

    def __init__(self):
        
        # Our standard title and instructions text
        # probably not neccessary for main project
        self.title = OnscreenText(text="Sounds Test, Hold 'X' to start engine, Up Arrow to accelerate\n""Space bar for horn",
                                  parent=base.a2dBottomCenter,
                                  pos=(0, 0.08), scale=0.08,
                                  fg=(1, 1, 1, 1), shadow=(0, 0, 0, .5))
        self.escapeText = OnscreenText(text="ESC: Quit", parent=base.a2dTopLeft,
                                       fg=(1, 1, 1, 1), pos=(0.06, -0.1),
                                       align=TextNode.ALeft, scale=.05)

        # Set up the key input
        self.accept('escape', sys.exit)

        # variables
        self.start = 0
        self.volume = 0

        # Functions tocall sounds
        # engine start idle sound
        def startcar():
            self.start = 1
            self.start_sound.play()
            self.start_sound.setTime(0.5)
            self.engine_idle_sound.setVolume(0.60)
            self.engine_idle_sound.play()
        # engine stops idle sound
        def stopcar():
            self.start = 0
            self.engine_idle_sound.stop()
        # honk horn
        def horn():
            self.horn_sound.play()

        #Controls 
        inputState.watchWithModifiers("F", "arrow_up")

        do = DirectObject()

        do.accept("x-repeat", startcar) # hold x to call function start car
        do.accept("x", stopcar)     # if x is pressed after car has started
        do.accept("space", horn)    # space bar for horn

        # background music
        self.musicBoxSound = loader.loadMusic('Sounds/bensound-dance.ogg')
        self.musicBoxSound.setVolume(0.60) # set volume/ Set from 0 - 1
        self.musicBoxSound.setLoop(True) # Set background music to loop
        self.musicBoxSound.play()
        

        # Sounds
        self.horn_sound = loader.loadSfx("Sounds/car+horn+x.wav")
        self.start_sound = loader.loadSfx("Sounds/StartCar.wav")
        self.engine_idle_sound = loader.loadSfx("Sounds/engineidle.ogg")
        self.engine_idle_sound.setLoop(True)
        self.accelerate_sound = loader.loadSfx("Sounds/enginethrottle.ogg")
        

        # accepts input to initiate sounds
        def inputTests(dt):
            if inputState.isSet("F"):
                self.accelerate_sound.play()

        # Update the program
        def update(task):
            dt = globalClock.getDt() 
            inputTests(dt)
            return task.cont

        taskMgr.add(update, "Update")

#Run the program
app = SoundManager()
base.run()