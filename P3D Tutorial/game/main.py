#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

# Python imports
import __builtin__
import os
import atexit
import logging

# Panda3D imoprts
#from pandac.PandaModules import loadPrcFileData
from direct.showbase.ShowBase import ShowBase
from direct.fsm.FSM import FSM
from panda3d.core import (
    CollisionTraverser,
    CollisionHandlerPusher,
    AntialiasAttrib,
    ConfigPageManager,
    ConfigVariableBool,
    OFileStream,
    WindowProperties,
    loadPrcFileData,
    loadPrcFile,
    MultiplexStream,
    Notify,
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
# set the application Name
__builtin__.companyName = "Grimfang Studios"
__builtin__.appName = "Tatakai no ikimono"
__builtin__.versionstring = "15.11"
home = os.path.expanduser("~")
__builtin__.basedir = os.path.join(
    home,
    __builtin__.companyName,
    __builtin__.appName)
if not os.path.exists(__builtin__.basedir):
    os.makedirs(__builtin__.basedir)
prcFile = os.path.join(__builtin__.basedir, "%s.prc"%__builtin__.appName)
if os.path.exists(prcFile):
    loadPrcFile(Filename.fromOsSpecific(prcFile))
loadPrcFileData("",
"""
    window-title %s
    cursor-hidden 0
    notify-timestamp 1
    #show-frame-rate-meter 1
    model-path $MAIN_DIR/assets/
    framebuffer-multisample 1
    multisamples 8
    texture-anisotropic-degree 0
"""%__builtin__.appName)
#
# PATHS AND CONFIGS END
#

#
# LOGGING
#
# setup Logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s: %(message)s",
    filename=os.path.join(__builtin__.basedir, "game.log"),
    datefmt="%d-%m-%Y %H:%M:%S",
    filemode="w")

# First log entry, the program version
logging.info("Version %s" % __builtin__.versionstring)

# redirect the notify output to a log file
nout = MultiplexStream()
Notify.ptr().setOstreamPtr(nout, 0)
nout.addFile(Filename(os.path.join(__builtin__.basedir, "game_p3d.log")))
#
# LOGGING END
#

class Main(ShowBase, FSM):
    """Main function of the application
    initialise the engine (ShowBase)"""

    def __init__(self):
        """initialise the engine"""
        ShowBase.__init__(self)
        FSM.__init__(self, "FSM-Game")

        #
        # BASIC APPLICATION CONFIGURATIONS
        #
        # disable pandas default camera driver
        self.disableMouse()
        # set background color to black
        self.setBackgroundColor(0, 0, 0)
        # set antialias for the complete sceen to automatic
        self.render.setAntialias(AntialiasAttrib.MAuto)
        # shader generator
        render.setShaderAuto()

        #
        # CONFIGURATION LOADING
        #
        # load given variables or set defaults
        # check if audio should be muted
        mute = ConfigVariableBool("audio-mute", False).getValue()
        if mute:
            self.disableAllAudio()
        else:
            self.enableAllAudio()
        # check if particles should be enabled
        particles = ConfigVariableBool("particles-enabled", True).getValue()
        if particles:
            self.enableParticles()
        # check if the config file hasn't been created
        if not os.path.exists(prcFile):
            # get the displays width and height
            w = self.pipe.getDisplayWidth()
            h = self.pipe.getDisplayHeight()
            # set window properties
            # clear all properties not previously set
            base.win.clearRejectedProperties()
            # setup new window properties
            props = WindowProperties()
            # Fullscreen
            props.setFullscreen(True)
            # set the window size to the screen resolution
            props.setSize(w, h)
            # request the new properties
            base.win.requestProperties(props)
        # automatically safe configuration at application exit
        atexit.register(self.__writeConfig)

        #
        # initialize game content
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
        # Event handling
        #
        self.accept("escape", self.__escape)

        #
        # Start with the menu
        #
        self.request("Menu")

    #
    # FSM PART
    #
    def enterMenu(self):
        show_cursor()
        self.accept("Menu-Start", self.request, ["CharSelection"])
        self.accept("Menu-Credits", self.request, ["Credits"])
        self.accept("Menu-Quit", self.quit)
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
        if self.state == "Menu":
            self.quit()
        elif self.state == "LevelSelection":
            self.request("CharSelection")
        else:
            self.request("Menu")

    def quit(self):
        """This function will stop the application"""
        if self.appRunner:
            self.appRunner.stop()
        else:
            exit(0)

    def __writeConfig(self):
        """Save current config in the prc file or if no prc file exists
        create one. The prc file is set in the prcFile variable"""
        page = None

        #TODO: get values of configurations here
        particles = "#f" if not base.particleMgrEnabled else "#t"
        volume = str(round(base.musicManager.getVolume(), 2))
        mute = "#f" if base.AppHasAudioFocus else "#t"
        #TODO: add any configuration variable name that you have added
        customConfigVariables = [
            "", "particles-enabled", "audio-mute", "audio-volume"]
        if os.path.exists(prcFile):
            # open the config file and change values according to current
            # application settings
            page = loadPrcFile(Filename.fromOsSpecific(prcFile))
            removeDecls = []
            for dec in range(page.getNumDeclarations()):
                # Check if our variables are given.
                # NOTE: This check has to be done to not loose our base or other
                #       manual config changes by the user
                if page.getVariableName(dec) in customConfigVariables:
                    decl = page.modifyDeclaration(dec)
                    removeDecls.append(decl)
            for dec in removeDecls:
                page.deleteDeclaration(dec)
            # NOTE: particles-enabled and audio-mute are custom variables and
            #       have to be loaded by hand at startup
            # Particles
            page.makeDeclaration("particles-enabled", particles)
            # audio
            page.makeDeclaration("audio-volume", volume)
            page.makeDeclaration("audio-mute", mute)
        else:
            # Create a config file and set default values
            cpMgr = ConfigPageManager.getGlobalPtr()
            page = cpMgr.makeExplicitPage("%s Pandaconfig"%appName)
            # set OpenGL to be the default
            page.makeDeclaration("load-display", "pandagl")
            # get the displays width and height
            w = self.pipe.getDisplayWidth()
            h = self.pipe.getDisplayHeight()
            # set the window size in the config file
            page.makeDeclaration("win-size", "%d %d"%(w, h))
            # set the default to fullscreen in the config file
            page.makeDeclaration("fullscreen", "1")
            # particles
            page.makeDeclaration("particles-enabled", "#t")
            # audio
            page.makeDeclaration("audio-volume", volume)
            page.makeDeclaration("audio-mute", "#f")
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

Game = Main()
Game.run()
