#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

# Panda3D imoprts
from direct.actor.Actor import Actor
from direct.fsm.FSM import FSM
from panda3d.core import KeyboardButton

class Player(FSM):
    def __init__(self, charNr):
        FSM.__init__(self, "FSM-Player%d"%charNr)
        charPath = "characters/character%d/" % charNr
        self.character = Actor(
            charPath + "char"#, {
                #"Idle":charPath + "idle",
                #"walk":charPath + "walk",
                #"punch_l":charPath + "punch_l",
                #"punch_r":charPath + "punch_r",
                #"kick_l":charPath + "kick_l",
                #"kick_r":charPath + "kick_r",
                #"defend":charPath + "defend"
            #}
        )
        self.character.reparentTo(render)
        self.character.hide()
        self.walkSpeed = 5.0 # units per second
        self.leftButton = KeyboardButton.asciiKey('a')
        self.rightButton = KeyboardButton.asciiKey('d')

    def start(self, startPos):
        self.character.setPos(startPos)
        self.character.show()
        self.request("Idle")
        taskMgr.add(self.moveTask, "move task")

    def moveTask(self, task):
        speed = 0.0
        isDown = base.mouseWatcherNode.isButtonDown
        if isDown(self.leftButton):
            speed -= self.walkSpeed
        if isDown(self.rightButton):
            speed += self.walkSpeed
        xDelta = speed * globalClock.getDt()
        self.character.setX(self.character, xDelta)
        return task.cont

    def enterIdle(self):
        self.character.loop("Idle")
