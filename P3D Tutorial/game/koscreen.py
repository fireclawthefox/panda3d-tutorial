#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

# Panda3D imoprts
from direct.showbase.DirectObject import DirectObject
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectButton)

class KoScreen(DirectObject):
    def __init__(self):
        self.frameMain = DirectFrame(
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dBottom, base.a2dTop),
            frameColor = (0, 0, 0, 0.75))
        self.frameMain.setTransparency(1)

        self.lbl_KO = DirectLabel(
            text = "K.O.",
            text_fg = (1,1,1,1),
            scale = 1,
            pos = (0, 0, 0),
            frameColor = (0,0,0,0))
        self.lbl_KO.setTransparency(1)
        self.lbl_KO.reparentTo(self.frameMain)

        self.lbl_PlayerXWon = DirectLabel(
            text = "PLAYER X WON",
            text_fg = (1,1,1,1),
            scale = 0.25,
            pos = (0, 0, -0.5),
            frameColor = (0,0,0,0))
        self.lbl_PlayerXWon.setTransparency(1)
        self.lbl_PlayerXWon.reparentTo(self.frameMain)

        self.btnContinue = DirectButton(
            text = "CONTINUE",
            text_fg = (1,1,1,1),
            scale = 0.1,
            pad = (0.15, 0.15),
            pos = (0, 0, -0.8),
            frameColor = (
                (0.2,0.2,0.2,0.8),
                (0.4,0.4,0.4,0.8),
                (0.4,0.4,0.4,0.8),
                (0.1,0.1,0.1,0.8),
                ),
            relief = 1,
            command = base.messenger.send,
            extraArgs = ["KoScreen-Back"],
            pressEffect = False,
            rolloverSound = None,
            clickSound = None)
        self.btnContinue.setTransparency(1)
        self.btnContinue.reparentTo(self.frameMain)

        self.hide()

    def show(self, succseedingPlayer):
        self.frameMain.show()
        self.lbl_PlayerXWon["text"] = "PLAYER {} WON".format(succseedingPlayer)

    def hide(self):
        self.frameMain.hide()
