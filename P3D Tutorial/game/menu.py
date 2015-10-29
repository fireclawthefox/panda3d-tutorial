#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectButton)

class Menu:
    def __init__(self):

        self.frameMain = DirectFrame(
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dTop, base.a2dBottom),
            frameColor = (0, 0, 0, 0))
        self.frameMain.setTransparency(1)

        self.title = DirectLabel(
            scale = 0.25,
            pos = (0.0, 0.0, base.a2dTop - 0.25),
            frameColor = (0, 0, 0, 0),
            text = "The Game",
            text_fg = (1,1,1,1))
        self.title.setTransparency(1)
        self.title.reparentTo(self.frameMain)

        self.btnStart = self.createButton(
            "Start",
            .25,
            ["Menu-Start"])

        self.btnExit = self.createButton(
           "Quit",
            -.25,
            ["Menu-Quit"])

        self.hide()

    def createButton(self, text, verticalPos, eventArgs):
        btn = DirectButton(
            text = text,
            scale = 0.25,
            pos = (0, 0, verticalPos),
            command = base.messenger.send,
            extraArgs = eventArgs,
            rolloverSound = None,
            clickSound = None)
        btn.reparentTo(self.frameMain)

    def show(self):
        self.frameMain.show()

    def hide(self):
        self.frameMain.hide()
