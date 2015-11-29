#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from panda3d.core import (
    AmbientLight,
    Spotlight,
    PerspectiveLens,
    Fog)
from direct.particles.ParticleEffect import ParticleEffect

class Arena:
    def __init__(self, arenaNr):
        arenaPath = "levels/arena%d/" % arenaNr
        self.arena = loader.loadModel(arenaPath + "arena")
        self.arena.setScale(2)
        self.arena.reparentTo(render)
        self.arena.hide()

        ambientLight = AmbientLight('ambient_light')
        ambientLight.setColor((0.2, 0.2, 0.2, 1))
        self.alnp = render.attachNewNode(ambientLight)

        sun = Spotlight('sun')
        sun.setColor((1, 1, 1, 1))
        sunLens = PerspectiveLens()
        sun.setLens(sunLens)
        self.sunNp = render.attachNewNode(sun)
        self.sunNp.setPos(-10, 10, 30)
        self.sunNp.lookAt(0,0,0)

        self.ambientSound = loader.loadSfx("assets/audio/ambientLevel1.ogg")
        self.ambientSound.setLoop(True)

        self.fog = Fog("Fog Name")
        self.fog.setColor(0.3,0.3,0.5)
        self.fog.setExpDensity(0.025)

        self.levelParticles = None
        if arenaNr == 1:
            self.levelParticles = ParticleEffect()
            self.levelParticles.loadConfig("assets/fx/Leafs.ptf")
            self.levelParticles.start(parent = render2d, renderParent = render2d)

    def start(self):
        self.arena.show()
        render.setLight(self.alnp)
        render.setLight(self.sunNp)
        self.ambientSound.play()
        render.setFog(self.fog)

    def stop(self):
        self.arena.hide()
        render.clearLight()
        self.ambientSound.stop()
        render.clearFog()
        if self.levelParticles != None:
            self.levelParticles.cleanup()

    def getStartPos(self, charNr):
        if charNr == 1:
            return self.arena.find("**/StartPosA").getPos() * 2
        elif charNr == 2:
            return self.arena.find("**/StartPosB").getPos() * 2
        else:
            return (0,0,0)
