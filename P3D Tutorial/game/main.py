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
    AntialiasAttrib,
    ConfigPageManager,
    ConfigVariableBool,
    OFileStream,
    WindowProperties,
    loadPrcFileData,
    loadPrcFile,
    MultiplexStream,
    Notify,
    Filename)

# Game imports
from player import Player

#
# PATHS AND CONFIGS
#
# set the application Name
__builtin__.appName = "Game Name"
__builtin__.versionstring = "15.07"
home = os.path.expanduser("~")
__builtin__.basedir = os.path.join(home, __builtin__.appName)
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
        self.player = Player(1)

        #
        # Event handling
        #
        self.accept("escape", self.__escape)

        #
        # Start with the menu
        #
        #TODO: Change this to any state you want the game to start with
        self.request("Game")

    #
    # FSM PART
    #

    def enterGame(self):
        # main game code should be called here
        self.player.start((0, 20, 0))

    def exitGame(self):
        # cleanup for game code
        pass

    #
    # FSM PART END
    #

    #
    # BASIC FUNCTIONS
    #

    def __escape(self):
        if self.state == "Game":
            self.quit()
        else:
            self.request("Game")

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
