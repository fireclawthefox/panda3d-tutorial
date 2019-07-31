#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

# Python imports
import os

# Panda3D imoprts
from direct.showbase.ShowBase import ShowBase
from direct.fsm.FSM import FSM
from direct.gui.DirectGui import DGG
from panda3d.core import (
    CollisionTraverser,
    CollisionHandlerPusher,
    AntialiasAttrib,
    ConfigPageManager,
    ConfigVariableInt,
    ConfigVariableBool,
    ConfigVariableString,
    OFileStream,
    WindowProperties,
    loadPrcFileData,
    loadPrcFile,
    Filename,
    AudioSound)
from direct.showbase.Audio3DManager import Audio3DManager

# Game imports
from player import Player
from arena import Arena
from menu import Menu
from credits import Credits
from characterselection import CharacterSelection
from levelselection import LevelSelection
from koscreen import KoScreen
from hud import Hud
from helper import hide_cursor, show_cursor

#
# PATHS AND CONFIGS
#
# set company and application details
companyName = "Grimfang Studio"
appName = "Tatakai no ikimono"
versionstring = "19.07"

# build the path from the details we have
home = os.path.expanduser("~")
basedir = os.path.join(
    home,
    companyName,
    appName)
if not os.path.exists(basedir):
    os.makedirs(basedir)

# look for a config file
prcFile = os.path.join(basedir, "{}.prc".format(appName))
if os.path.exists(prcFile):
    mainConfig = loadPrcFile(Filename.fromOsSpecific(prcFile))

# set configurations that should not be changed from a config file
loadPrcFileData("",
"""
    #
    # Model loading
    #
    model-path $MAIN_DIR/assets/

    #
    # Window and graphics
    #
    window-title {}
    #show-frame-rate-meter 1

    #
    # Logging
    #
    #notify-level info
    notify-timestamp 1
""".format(appName))

#
# MAIN GAME CLASS
#
class Main(ShowBase, FSM):
    """Main function of the application
    initialise the engine (ShowBase)"""

    def __init__(self):
        """initialise the engine"""
        ShowBase.__init__(self)
        base.notify.info("Version {}".format(versionstring))
        FSM.__init__(self, "FSM-Game")

        #
        # BASIC APPLICATION CONFIGURATIONS
        #
        # disable pandas default camera driver
        self.disableMouse()
        # set antialias for the complete sceen to automatic
        self.render.setAntialias(AntialiasAttrib.MAuto)
        # shader generator
        render.setShaderAuto()
        # Enhance font readability
        DGG.getDefaultFont().setPixelsPerUnit(100)
        # get the displays width and height for later usage
        self.dispWidth = self.pipe.getDisplayWidth()
        self.dispHeight = self.pipe.getDisplayHeight()

        #
        # CONFIGURATION LOADING
        #
        # load given variables or set defaults
        # check if particles should be enabled
        # NOTE: If you use the internal physics engine, this always has
        #       to be enabled!
        particles = ConfigVariableBool("particles-enabled", True).getValue()
        if particles:
            self.enableParticles()

        def setFullscreen():
            """Helper function to set the window fullscreen
            with width and height set to the screens size"""
            # set window properties
            # clear all properties not previously set
            base.win.clearRejectedProperties()
            # setup new window properties
            props = WindowProperties()
            # Fullscreen
            props.setFullscreen(True)
            # set the window size to the screen resolution
            props.setSize(self.dispWidth, self.dispHeight)
            # request the new properties
            base.win.requestProperties(props)
            # Set the config variables so we correctly store the
            # new size and fullscreen setting later
            winSize = ConfigVariableString("win-size")
            winSize.setValue("{} {}".format(self.dispWidth, self.dispHeight))
            fullscreen = ConfigVariableBool("fullscreen")
            fullscreen.setValue(True)
            # Render a frame to make sure the fullscreen is applied
            # before we do anything else
            self.taskMgr.step()
            # make sure to propagate the new aspect ratio properly so
            # the GUI and other things will be scaled appropriately
            aspectRatio = self.dispWidth / self.dispHeight
            self.adjustWindowAspectRatio(aspectRatio)


        # check if the config file hasn't been created
        if not os.path.exists(prcFile):
            setFullscreen()
        # automatically safe configuration at application exit
        #base.exitFunc = self.__writeConfig

        #
        # INITIALIZE GAME CONTENT
        #
        base.cTrav = CollisionTraverser("base collision traverser")
        base.pusher = CollisionHandlerPusher()
        self.menu = Menu()
        self.credits = Credits()
        self.charSelection = CharacterSelection()
        self.levelSelection = LevelSelection()
        self.koScreen = KoScreen()
        self.hud = Hud()
        self.menuMusic = loader.loadMusic("assets/audio/menuMusic.ogg")
        self.menuMusic.setLoop(True)
        self.fightMusic = loader.loadMusic("assets/audio/fightMusic.ogg")
        self.fightMusic.setLoop(True)
        base.audio3d = Audio3DManager(base.sfxManagerList[0], camera)

        #
        # EVENT HANDLING
        #
        # By default we accept the escape key
        self.accept("escape", self.__escape)

        #
        # ENTER GAMES INITIAL FSM STATE
        #
        self.request("Menu")

    #
    # FSM PART
    #
    def enterMenu(self):
        show_cursor()
        self.accept("Menu-Start", self.request, ["CharSelection"])
        self.accept("Menu-Credits", self.request, ["Credits"])
        self.accept("Menu-Quit", self.userExit)
        self.ignore("KoScreen-Back")
        self.koScreen.hide()
        self.menu.show()
        if self.menuMusic.status() != AudioSound.PLAYING:
            self.menuMusic.play()
        if self.fightMusic.status() == AudioSound.PLAYING:
            self.fightMusic.stop()

    def exitMenu(self):
        self.ignore("Menu-Start")
        self.ignore("Menu-Credits")
        self.ignore("Menu-Quit")
        self.menu.hide()

    def enterCredits(self):
        self.accept("Credits-Back", self.request, ["Menu"])
        self.koScreen.hide()
        self.credits.show()

    def exitCredits(self):
        self.ignore("Credits-Back")
        self.credits.hide()

    def enterCharSelection(self):
        self.accept("CharSelection-Back", self.request, ["Menu"])
        self.accept("CharSelection-Start", self.request, ["LevelSelection"])
        self.charSelection.show()

    def exitCharSelection(self):
        self.ignore("CharSelection-Start")
        self.ignore("CharSelection-Back")
        self.charSelection.hide()
        self.selectedChar1 = self.charSelection.selectedCharacter1
        self.selectedChar2 = self.charSelection.selectedCharacter2

    def enterLevelSelection(self):
        self.accept("LevelSelection-Back", self.request, ["CharSelection"])
        self.accept("LevelSelection-Start", self.request, ["Game"])
        self.levelSelection.show()

    def exitLevelSelection(self):
        self.ignore("LevelSelection-Start")
        self.ignore("LevelSelection-Back")
        self.levelSelection.hide()

    def enterGame(self):
        # main game code should be called here
        self.arena = Arena(self.levelSelection.selectedLevel)
        self.arena.start()
        self.camera.setPos(0, -5, 1.25)
        self.player = Player(0, self.selectedChar1, "p1")
        self.player2 = Player(1, self.selectedChar2, "p2")
        self.player.setEnemy(self.player2.collisionNodeName)
        self.player2.setEnemy(self.player.collisionNodeName)
        self.player.start(self.arena.getStartPos(1))
        self.player2.start(self.arena.getStartPos(2))
        self.taskMgr.add(self.updateWorldCam, "world camera update task")
        self.accept("gameOver", self.gameOver)
        self.hud.show()
        def lifeChanged(charId, health):
            base.messenger.send(
                "hud_setLifeBarValue",
                [charId, health])
        self.accept("lifeChanged", lifeChanged)
        hide_cursor()
        if self.fightMusic.status() != AudioSound.PLAYING:
            self.fightMusic.play()
        if self.menuMusic.status() == AudioSound.PLAYING:
            self.menuMusic.stop()

    def exitGame(self):
        # cleanup for game code
        self.taskMgr.remove("world camera update task")
        self.player.stop()
        self.player2.stop()
        del self.player
        del self.player2
        self.arena.stop()
        self.ignore("gameOver")
        self.ignore("lifeChanged")
        self.hud.hide()

    #
    # FSM PART END
    #

    #
    # BASIC FUNCTIONS
    #
    def gameOver(self, LoosingCharId):
        show_cursor()
        winningChar = 1
        if LoosingCharId == 0:
            winningChar = 2
        self.accept("KoScreen-Back", self.request, ["Credits"])
        self.koScreen.show(winningChar)

    def updateWorldCam(self, task):
        playerVec = self.player.getPos() - self.player2.getPos()
        playerDist = playerVec.length()
        x = self.player.getX() + playerDist / 2.0
        self.camera.setX(x)

        zoomout = False
        if not self.cam.node().isInView(self.player.getPos(self.cam)):
            camPosUpdate = -2 * globalClock.getDt()
            self.camera.setY(self.camera, camPosUpdate)
            zoomout = True
        if not self.cam.node().isInView(self.player2.getPos(self.cam)):
            camPosUpdate = -2 * globalClock.getDt()
            self.camera.setY(self.camera, camPosUpdate)
            zoomout = True
        if not zoomout:
            if self.camera.getY() < -5:
                camPosUpdate = 2 * globalClock.getDt()
                self.camera.setY(self.camera, camPosUpdate)
        return task.cont

    def __escape(self):
        """Handle user escape key klicks"""
        if self.state == "Menu":
            # In this state, we will stop the application
            self.userExit()
        elif self.state == "LevelSelection":
            self.request("CharSelection")
        else:
            # In every other state, we switch back to the Menu state
            self.request("Menu")

    def __writeConfig(self):
        """Save current config in the prc file or if no prc file exists
        create one. The prc file is set in the prcFile variable"""
        page = None

        #
        #TODO: add any configuration variable names that you have added
        #      to the dictionaries in the next lines. Set the current
        #      configurations value as value in this dictionary and it's
        #      name as key.
        configVariables = {
            # set the window size in the config file
            "win-size": ConfigVariableString("win-size", "{} {}".format(self.dispWidth, self.dispHeight)).getValue(),
            # set the default to fullscreen in the config file
            "fullscreen": "#t" if ConfigVariableBool("fullscreen", True).getValue() else "#f",
            # particles
            "particles-enabled": "#t" if self.particleMgrEnabled else "#f",
            # audio
            "audio-volume": str(round(self.musicManager.getVolume(), 2)),
            "audio-music-active": "#t" if ConfigVariableBool("audio-music-active").getValue() else "#f",
            "audio-sfx-active": "#t" if ConfigVariableBool("audio-sfx-active").getValue() else "#f",
            # logging
            "notify-output": os.path.join(basedir, "game.log"),
            # window
            "framebuffer-multisample": "#t" if ConfigVariableBool("framebuffer-multisample").getValue() else "#f",
            "multisamples": str(ConfigVariableInt("multisamples", 8).getValue()),
            "texture-anisotropic-degree": str(ConfigVariableInt("texture-anisotropic-degree").getValue()),
            "textures-auto-power-2": "#t" if ConfigVariableBool("textures-auto-power-2", True).getValue() else "#f",
            }

        page = None
        # Check if we have an existing configuration file
        if os.path.exists(prcFile):
            # open the config file and change values according to current
            # application settings
            page = loadPrcFile(Filename.fromOsSpecific(prcFile))
            removeDecls = []
            for dec in range(page.getNumDeclarations()):
                # Check if our variables are given.
                # NOTE: This check has to be done to not loose our base or other
                #       manual config changes by the user
                if page.getVariableName(dec) in configVariables.keys():
                    removeDecls.append(page.modifyDeclaration(dec))
            for dec in removeDecls:
                page.deleteDeclaration(dec)
        else:
            # Create a config file and set default values
            cpMgr = ConfigPageManager.getGlobalPtr()
            page = cpMgr.makeExplicitPage("Application Config")

        # always write custom configurations
        for key, value in configVariables.items():
            page.makeDeclaration(key, value)
        # create a stream to the specified config file
        configfile = OFileStream(prcFile)
        # and now write it out
        page.write(configfile)
        # close the stream
        configfile.close()

    #
    # BASIC END
    #
# CLASS Main END

#
# START GAME
#
Game = Main()
Game.run()
