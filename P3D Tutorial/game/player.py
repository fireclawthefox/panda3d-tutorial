#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

# Panda3D imoprts
from direct.showbase.DirectObject import DirectObject
from direct.actor.Actor import Actor
from direct.fsm.FSM import FSM
from panda3d.core import (
    CollisionSegment,
    CollisionSphere,
    CollisionNode,
    KeyboardButton,
    AudioSound)
from direct.particles.ParticleEffect import ParticleEffect

class Player(FSM, DirectObject):
    def __init__(self, charId, charNr, controls):
        FSM.__init__(self, "FSM-Player%d"%charNr)
        self.charId = charId
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
                "Hit":charPath + "hit",
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

        characterSphere = CollisionSphere(0, 0, 1.0, 0.5)
        self.collisionNodeName = "character%dCollision"%charId
        characterColNode = CollisionNode(self.collisionNodeName)
        characterColNode.addSolid(characterSphere)
        self.characterCollision = self.character.attachNewNode(characterColNode)
        # Uncomment this line to show collision solids
        #self.characterCollision.show()
        base.pusher.addCollider(self.characterCollision, self.character)
        base.cTrav.addCollider(self.characterCollision, base.pusher)

        characterHitRay = CollisionSegment(0, -0.5, 1.0, 0, -0.8, 1.0)
        characterColNode.addSolid(characterHitRay)

        self.audioStep = base.audio3d.loadSfx("assets/audio/step.ogg")
        self.audioStep.setLoop(True)
        base.audio3d.attachSoundToObject(self.audioStep, self.character)

        self.audioHit = base.audio3d.loadSfx("assets/audio/hit.ogg")
        self.audioHit.setLoop(False)
        base.audio3d.attachSoundToObject(self.audioStep, self.character)

    def setEnemy(self, enemyColName):
        self.enemyColName = enemyColName
        inEvent = "%s-into-%s"%(enemyColName,self.collisionNodeName)
        base.pusher.addInPattern(inEvent)
        self.accept(inEvent, self.setCanBeHit, [True])
        outEvent = "%s-out-%s"%(enemyColName,self.collisionNodeName)
        base.pusher.addOutPattern(outEvent)
        self.accept(outEvent, self.setCanBeHit, [False])

    def setCanBeHit(self, yes, collission):
        eventName = "hitEnemy%s"%self.collisionNodeName
        if yes:
            self.accept(eventName, self.gotHit)
        else:
            self.ignore(eventName)
        self.canBeHit = yes

    def gotHit(self):
        if not self.canBeHit or self.isDefending: return

        self.bloodsplat = ParticleEffect()
        self.bloodsplat.loadConfig("assets/fx/BloodSplat.ptf")
        floater = self.character.attachNewNode("particleFloater")
        if self.character.getH() == 90:
            floater.setPos(-1, 0, 1)
        if self.character.getH() == -90:
            floater.setPos(1, 0, 1)
        self.bloodsplat.start(parent = floater, renderParent = render)
        taskMgr.doMethodLater(0.5, self.bloodsplat.cleanup,
            "stop Particle", extraArgs = [])

        self.health -= 10
        base.messenger.send(
            "lifeChanged",
            [self.charId, self.health])
        if self.health <= 0:
            self.gotDefeated = True
            self.request("Defeated")
            base.messenger.send("gameOver", [self.charId])
        else:
            self.request("Hit")

    def attackAnimationPlaying(self):
        actionAnimations = [
            "Punch_l",
            "Punch_r",
            "Kick_l",
            "Kick_r",
            "Hit"]
        if self.character.getCurrentAnim() in actionAnimations: return True

    def start(self, startPos):
        self.character.setPos(startPos)
        self.character.show()
        self.request("Idle")
        self.canBeHit = False
        self.isDefending = False
        self.gotDefeated = False
        self.health = 100
        taskMgr.add(self.moveTask, "move task %d"%self.charId)

    def stop(self):
        taskMgr.remove("move task %d"%self.charId)
        base.audio3d.detachSound(self.audioStep)
        base.audio3d.detachSound(self.audioHit)
        self.character.cleanup()
        self.character.removeNode()

    def moveTask(self, task):
        if self.gotDefeated:
            base.messenger.send("GameOver")
            return task.done
        if self.attackAnimationPlaying(): return task.cont
        speed = 0.0
        isDown = base.mouseWatcherNode.isButtonDown

        if isDown(self.defendButton):
            if self.state != "Defend":
                self.isDefending = True
                self.request("Defend")
            return task.cont
        self.isDefending = False

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
            base.messenger.send("hitEnemy%s"%self.enemyColName)
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
        if self.audioStep.status() != AudioSound.PLAYING:
            self.audioStep.play()
    def exitWalk(self):
        self.character.stop()
        if self.audioStep.status() == AudioSound.PLAYING:
            self.audioStep.stop()

    def enterWalk_back(self):
        self.character.loop("Walk_back")
        if self.audioStep.status() != AudioSound.PLAYING:
            self.audioStep.play()
    def exitWalk_back(self):
        self.character.stop()
        if self.audioStep.status() == AudioSound.PLAYING:
            self.audioStep.stop()

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

    def enterHit(self):
        self.character.play("Hit")
        self.audioHit.play()
    def exitHit(self):
        self.character.stop()

    def enterDefeated(self):
        self.character.play("Defeated")
    def exitDefeated(self):
        self.character.stop()
