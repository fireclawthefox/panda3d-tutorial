#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

class Arena:
    def __init__(self, arenaNr):
        arenaPath = "levels/arena%d/" % arenaNr
        self.arena = loader.loadModel(arenaPath + "arena")
        self.arena.setScale(2)

    def start(self):
        self.arena.reparentTo(render)

    def getStartPos(self, charNr):
        if charNr == 1:
            return self.arena.find("**/StartPosA").getPos() * 2
        elif charNr == 2:
            return self.arena.find("**/StartPosB").getPos() * 2
        else:
            return (0,0,0)
