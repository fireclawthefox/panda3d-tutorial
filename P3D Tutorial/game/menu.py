#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from panda3d.core import TextNode
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectButton)

class Menu:
    def __init__(self):

        self.frameMain = DirectFrame(
            image = "gui/MenuBackground.png",
            image_scale = (1.7778, 1, 1),
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dBottom, base.a2dTop),
            frameColor = (0, 0, 0, 0))
        self.frameMain.setTransparency(1)

        self.title = DirectLabel(
            scale = 0.15,
            text_align = TextNode.ALeft,
            pos = (base.a2dLeft + 0.2, 0, 0),
            frameColor = (0, 0, 0, 0),
            text = "Main Menu",
            text_fg = (1,1,1,1))
        self.title.setTransparency(1)
        self.title.reparentTo(self.frameMain)

        self.btnStart = self.createButton(
            "Start",
            -.10,
            ["Menu-Start"])

        self.btnStart = self.createButton(
            "Credits",
            -.25,
            ["Menu-Credits"])

        self.btnExit = self.createButton(
           "Quit",
            -.40,
            ["Menu-Quit"])

        self.hide()

    def createButton(self, text, verticalPos, eventArgs):
        maps = loader.loadModel("gui/button_map")
        btnGeom = (maps.find("**/btn_ready"),
                    maps.find("**/btn_click"),
                    maps.find("**/btn_rollover"),
                    maps.find("**/btn_disabled"))
        btn = DirectButton(
            text = text,
            text_fg = (0,0,0,1),
            text_scale = 0.05,
            text_pos = (0.02, -0.015),
            text_align = TextNode.ALeft,
            scale = 2,
            pos = (base.a2dLeft + 0.2, 0, verticalPos),
            geom = btnGeom,
            relief = 0,
            frameColor = (0,0,0,0),
            command = base.messenger.send,
            extraArgs = eventArgs,
            pressEffect = False,
            rolloverSound = None,
            clickSound = None)
        btn.reparentTo(self.frameMain)

    def show(self):
        self.frameMain.show()

    def hide(self):
        self.frameMain.hide()
