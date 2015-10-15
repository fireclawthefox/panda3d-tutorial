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
            charPath + "char", {
                "Idle":charPath + "idle",
                "Walk":charPath + "walk",
                "Punch_l":charPath + "punch_l",
                "Punch_r":charPath + "punch_r",
                "Kick_l":charPath + "kick_l",
                "Kick_r":charPath + "kick_r",
                "Defend":charPath + "defend",
                #"Defeated":charPath + "defeated"
            }
        )
        self.character.setH(90)
        self.character.reparentTo(render)
        self.character.hide()
        self.walkSpeed = 2.0 # units per second
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
            speed += self.walkSpeed
        if isDown(self.rightButton):
            speed -= self.walkSpeed
        yDelta = speed * globalClock.getDt()
        self.character.setY(self.character, yDelta)
        if speed != 0.0 and self.state != "Walk":
            self.request("Walk")
        elif speed == 0.0 and self.state != "Idle":
            self.request("Idle")
        return task.cont

    def enterIdle(self):
        self.character.loop("Idle")
    def exitIdle(self):
        self.character.stop()

    def enterWalk(self):
        self.character.loop("Walk")
    def exitWalk(self):
        self.character.stop()
