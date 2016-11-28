#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

# Panda3D imoprts
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import DirectWaitBar, DGG
from panda3d.core import TextNode

class Hud(DirectObject):
    def __init__(self):
        self.lifeBar1 = DirectWaitBar(
            text = "Player1",
            text_fg = (1,1,1,1),
            text_pos = (-1.2, -0.18, 0),
            text_align = TextNode.ALeft,
            value = 100,
            barColor = (0, 1, 0.25, 1),
            barRelief = DGG.RAISED,
            barBorderWidth = (0.03, 0.03),
            borderWidth = (0.01, 0.01),
            relief = DGG.RIDGE,
            frameColor = (0.8,0.05,0.10,1),
            frameSize = (-1.2, 0, 0, -0.1),
            pos = (-0.2,0,base.a2dTop-0.15))
        self.lifeBar1.setTransparency(1)

        self.lifeBar2 = DirectWaitBar(
            text = "Player2",
            text_fg = (1,1,1,1),
            text_pos = (1.2, -0.18, 0),
            text_align = TextNode.ARight,
            value = 100,
            barColor = (0, 1, 0.25, 1),
            barRelief = DGG.RAISED,
            barBorderWidth = (0.03, 0.03),
            borderWidth = (0.01, 0.01),
            relief = DGG.RIDGE,
            frameColor = (0.8,0.05,0.10,1),
            frameSize = (0, 1.2, 0, -0.1),
            pos = (0.2,0,base.a2dTop-0.15))
        self.lifeBar2.setTransparency(1)

        self.accept("hud_setLifeBarValue", self.setLifeBarValue)
        self.hide()

    def show(self):
        self.lifeBar1["value"] = 100
        self.lifeBar2["value"] = 100
        self.lifeBar1.show()
        self.lifeBar2.show()

    def hide(self):
        self.lifeBar1.hide()
        self.lifeBar2.hide()

    def setLifeBarValue(self, barNr, newValue):
        if barNr == 0:
            self.lifeBar1["value"] = newValue
        elif barNr == 1:
            self.lifeBar2["value"] = newValue
