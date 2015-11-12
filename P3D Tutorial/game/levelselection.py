#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from panda3d.core import TextNode
from direct.gui.DirectGui import (
    DirectFrame,
    DirectButton)

class LevelSelection:
    def __init__(self):

        self.frameMain = DirectFrame(
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dTop, base.a2dBottom),
            frameColor = (0.05, 0.05, 0.05, 1))
        self.frameMain.setTransparency(1)

        self.btnLevel1 = self.createLevelButton(
            (-0.6, 0, 0.15),
            "assets/gui/Level1Button.png",
            0)
        self.btnLevel1.reparentTo(self.frameMain)

        self.btnLevel2 = self.createLevelButton(
            (0.6, 0, 0.15),
            "assets/gui/Level2Button.png",
            1)
        self.btnLevel2.reparentTo(self.frameMain)

        self.footerFrame = DirectFrame(
            text = "SELECT THE ARENA",
            text_fg = (1,1,1,1),
            text_scale = 0.08,
            text_pos = (0, -0.03),
            frameSize = (base.a2dLeft, base.a2dRight,
                         -0.1, 0.1),
            pos = (0, 0, base.a2dBottom + 0.2),
            frameColor = (0, 0, 0, 0.5))
        self.footerFrame.setTransparency(1)
        self.footerFrame.reparentTo(self.frameMain)

        self.btnBack = DirectButton(
            text = "BACK",
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            scale = 0.1,
            pad = (0.15, 0.15),
            pos = (base.a2dLeft + 0.08, 0, -0.03),
            frameColor = (
                (0.2,0.2,0.2,0.8),
                (0.4,0.4,0.4,0.8),
                (0.4,0.4,0.4,0.8),
                (0.1,0.1,0.1,0.8),
                ),
            relief = 1,
            command = base.messenger.send,
            extraArgs = ["LevelSelection-Back"],
            pressEffect = False,
            rolloverSound = None,
            clickSound = None)
        self.btnBack.setTransparency(1)
        self.btnBack.reparentTo(self.footerFrame)

        self.hide()

    def createLevelButton(self, pos, image, levelNr):
        self.selectedLevel = levelNr
        btn = DirectButton(
            scale = (0.5, 1, 0.75),
            relief = 0,
            frameColor = (0,0,0,0),
            pos = pos,
            image = image,
            command = base.messenger.send,
            extraArgs = ["LevelSelection-Start"],
            rolloverSound = None,
            clickSound = None)
        btn.setTransparency(1)
        return btn

    def show(self):
        self.frameMain.show()

    def hide(self):
        self.frameMain.hide()
