#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from panda3d.core import (
    AmbientLight,
    Spotlight,
    PerspectiveLens)

class Arena:
    def __init__(self, arenaNr):
        arenaPath = "levels/arena%d/" % arenaNr
        self.arena = loader.loadModel(arenaPath + "arena")
        self.arena.setScale(2)

        ambientLight = AmbientLight('ambient_light')
        ambientLight.setColor((0.2, 0.2, 0.2, 1))
        alnp = render.attachNewNode(ambientLight)
        render.setLight(alnp)

        sun = Spotlight('sun')
        sun.setColor((1, 1, 1, 1))
        sunLens = PerspectiveLens()
        sun.setLens(sunLens)
        sunNp = render.attachNewNode(sun)
        sunNp.setPos(-10, 10, 30)
        sunNp.lookAt(0,0,0)
        render.setLight(sunNp)

    def start(self):
        self.arena.reparentTo(render)

    def getStartPos(self, charNr):
        if charNr == 1:
            return self.arena.find("**/StartPosA").getPos() * 2
        elif charNr == 2:
            return self.arena.find("**/StartPosB").getPos() * 2
        else:
            return (0,0,0)
