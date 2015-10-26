#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

# Panda3D imoprts
from direct.actor.Actor import Actor
from direct.fsm.FSM import FSM
from panda3d.core import (
    CollisionSphere,
    CollisionNode,
    KeyboardButton)

class Player(FSM):
    def __init__(self, charNr, controls):
        FSM.__init__(self, "FSM-Player%d"%charNr)
        charPath = "characters/character%d/" % charNr
        self.character = Actor(
            charPath + "char", {
                "Idle":charPath + "idle",
                "Walk":charPath + "walk",
                "Walk_back":charPath + "walk_back",
                "Punch_l":charPath + "punch_l",
                "Punch_r":charPath + "punch_r",
                "Kick_l":charPath + "kick_l",
                "Kick_r":charPath + "kick_r",
                "Defend":charPath + "defend",
                "Defeated":charPath + "defeated"
            }
        )
        self.character.reparentTo(render)
        self.character.hide()
        self.walkSpeed = 2.0 # units per second
        if controls == "p1":
            self.character.setH(90)
            self.leftButton = KeyboardButton.asciiKey('d')
            self.rightButton = KeyboardButton.asciiKey('f')
            self.punchLButton = KeyboardButton.asciiKey('q')
            self.punchRButton = KeyboardButton.asciiKey('w')
            self.kickLButton = KeyboardButton.asciiKey('a')
            self.kickRButton = KeyboardButton.asciiKey('s')
            self.defendButton = KeyboardButton.asciiKey('e')
        elif controls == "p2":
            self.character.setH(-90)
            self.leftButton = KeyboardButton.right()
            self.rightButton = KeyboardButton.left()
            self.punchLButton = KeyboardButton.asciiKey('i')
            self.punchRButton = KeyboardButton.asciiKey('o')
            self.kickLButton = KeyboardButton.asciiKey('k')
            self.kickRButton = KeyboardButton.asciiKey('l')
            self.defendButton = KeyboardButton.asciiKey('p')

        self.getPos = self.character.getPos
        self.getX = self.character.getX

        playerSphere = CollisionSphere(0, 0, 0.8, 0.7)
        playerColNode = CollisionNode("playerCollision")
        playerColNode.addSolid(playerSphere)
        self.playerCollision = self.player.attachNewNode(playerColNode)
        base.pusher.addCollider(self.playerCollision, self.player)

    def attackAnimationPlaying(self):
        actionAnimations = [
            "Punch_l",
            "Punch_r",
            "Kick_l",
            "Kick_r"]
        if self.character.getCurrentAnim() in actionAnimations: return True

    def start(self, startPos):
        self.character.setPos(startPos)
        self.character.show()
        self.request("Idle")
        taskMgr.add(self.moveTask, "move task")

    def moveTask(self, task):
        if self.attackAnimationPlaying(): return task.cont
        speed = 0.0
        isDown = base.mouseWatcherNode.isButtonDown

        if isDown(self.defendButton):
            if self.state != "Defend":
                self.request("Defend")
            return task.cont

        # Check for attack keys
        isAction = False
        if isDown(self.punchLButton):
            isAction = True
            self.request("Punch_l")
        elif isDown(self.punchRButton):
            isAction = True
            self.request("Punch_r")
        elif isDown(self.kickLButton):
            isAction = True
            self.request("Kick_l")
        elif isDown(self.kickRButton):
            isAction = True
            self.request("Kick_r")
        if isAction:
            return task.cont

        if isDown(self.leftButton):
            speed += self.walkSpeed
        if isDown(self.rightButton):
            speed -= self.walkSpeed
        yDelta = speed * globalClock.getDt()
        self.character.setY(self.character, yDelta)
        if speed != 0.0 and self.state != "Walk" and self.state != "Walk_back":
            if speed < 0:
                self.request("Walk")
            else:
                self.request("Walk_back")
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

    def enterWalk_back(self):
        self.character.loop("Walk_back")
    def exitWalk_back(self):
        self.character.stop()

    def enterPunch_l(self):
        self.character.play("Punch_l")
    def exitPunch_l(self):
        self.character.stop()

    def enterPunch_r(self):
        self.character.play("Punch_r")
    def exitPunch_r(self):
        self.character.stop()

    def enterKick_l(self):
        self.character.play("Kick_l")
    def exitKick_l(self):
        self.character.stop()

    def enterKick_r(self):
        self.character.play("Kick_r")
    def exitKick_r(self):
        self.character.stop()

    def enterDefend(self):
        self.character.play("Defend")
    def exitDefend(self):
        self.character.stop()

    def enterDefeated(self):
        self.character.play("Defeated")
    def exitDefeated(self):
        self.character.stop()
