#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from panda3d.core import (
    TextNode,
    Texture)
from direct.gui.DirectGui import (
    DirectFrame,
    DirectButton,
    DGG)

class CharacterSelection:
    def __init__(self):

        self.frameMain = DirectFrame(
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dTop, base.a2dBottom),
            frameColor = (0.05, 0.05, 0.05, 1))
        self.frameMain.setTransparency(1)

        width = abs(base.a2dLeft) + base.a2dRight

        red = loader.loadTexture("assets/gui/CharRedBG.png")
        red.setWrapU(Texture.WM_repeat)
        red.setWrapV(Texture.WM_repeat)
        self.char1Frame = DirectFrame(
            text = "Player 1",
            text_fg = (1,1,1,1),
            text_scale = 0.1,
            text_pos = (0, base.a2dTop - 0.2),
            frameSize = (-width/6.0, width/6.0,
                         base.a2dTop, base.a2dBottom),
            frameTexture = red,
            pos = (base.a2dLeft+width/6.0, 0, 0))
        self.char1Frame.updateFrameStyle()
        self.char1Frame.setTransparency(1)
        self.char1Frame.reparentTo(self.frameMain)

        blue = loader.loadTexture("assets/gui/CharBlueBG.png")
        blue.setWrapU(Texture.WM_repeat)
        blue.setWrapV(Texture.WM_repeat)
        self.char2Frame = DirectFrame(
            text = "Player 2",
            text_fg = (1,1,1,1),
            text_scale = 0.1,
            text_pos = (0, base.a2dTop - 0.2),
            frameSize = (-width/6.0, width/6.0,
                         base.a2dTop, base.a2dBottom),
            frameTexture = blue,
            pos = (base.a2dRight-width/6.0, 0, 0))
        self.char2Frame.setTransparency(1)
        self.char2Frame.reparentTo(self.frameMain)

        self.footerFrame = DirectFrame(
            text = "PLAYER 1 - CHOOSE YOUR CHARACTER",
            text_fg = (1,1,1,1),
            text_scale = 0.08,
            text_pos = (0, -0.03),
            frameSize = (base.a2dLeft, base.a2dRight,
                         -0.1, 0.1),
            pos = (0, 0, base.a2dBottom + 0.2),
            frameColor = (0, 0, 0, 0.5))
        self.footerFrame.setTransparency(1)
        self.footerFrame.reparentTo(self.frameMain)

        self.charSelectFrame = DirectFrame(
            text = "VS",
            text_fg = (1,1,1,1),
            text_scale = 0.1,
            text_pos = (0, base.a2dTop - 0.2),
            frameSize = (-width/6.0, width/6.0,
                         base.a2dTop, base.a2dBottom),
            frameColor = (0,0,0,0))
        self.charSelectFrame.reparentTo(self.frameMain)

        self.btnChar1 = self.createCharacterButton(
            (-0.2, 0, 0),
            "assets/gui/Char1Button.png",
            1)
        self.btnChar1.reparentTo(self.charSelectFrame)

        self.btnChar2 = self.createCharacterButton(
            (0.2, 0, 0),
            "assets/gui/Char2Button.png",
            2)
        self.btnChar2.reparentTo(self.charSelectFrame)

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
                (0.1,0.1,0.1,0.8)),
            relief = 1,
            command = base.messenger.send,
            extraArgs = ["CharSelection-Back"],
            pressEffect = False,
            rolloverSound = None,
            clickSound = None)
        self.btnBack.setTransparency(1)
        self.btnBack.reparentTo(self.footerFrame)

        self.btnStart = DirectButton(
            text = "START",
            text_fg = (1,1,1,1),
            text_align = TextNode.ARight,
            scale = 0.1,
            pad = (0.15, 0.15),
            pos = (base.a2dRight - 0.08, 0, -0.03),
            relief = 1,
            frameColor = (
                (0.2,0.2,0.2,0.8),
                (0.4,0.4,0.4,0.8),
                (0.4,0.4,0.4,0.8),
                (0.1,0.1,0.1,0.8)),
            command = base.messenger.send,
            extraArgs = ["CharSelection-Start"],
            pressEffect = False,
            rolloverSound = None,
            clickSound = None)
        self.btnStart.setTransparency(1)
        self.btnStart.reparentTo(self.footerFrame)
        self.btnStart["state"] = DGG.DISABLED

    def createCharacterButton(self, pos, image, charNr):
        btn = DirectButton(
            scale = 0.1,
            relief = 0,
            frameColor = (0,0,0,0),
            pos = pos,
            image = image,
            command = self.selectCharacter,
            extraArgs = [charNr],
            rolloverSound = None,
            clickSound = None)
        btn.setTransparency(1)
        return btn

    def selectCharacter(self, charNr):
        if self.char1Frame["image"] == None:
            self.char1Frame["image"] = "assets/gui/Char%d_L.png" % charNr
            self.char1Frame["image_scale"] = (0.5,1, 1)
            self.selectedCharacter1 = charNr
            self.footerFrame["text"] = "PLAYER 2 - CHOOSE YOUR CHARACTER"
        elif self.char2Frame["image"] == None:
            self.char2Frame["image"] = "assets/gui/Char%d_R.png" % charNr
            self.char2Frame["image_scale"] = (0.5,1, 1)
            self.selectedCharacter2 = charNr
            self.btnStart["state"] = DGG.NORMAL
            self.footerFrame["text"] = "START THE FIGHT >"

    def show(self):
        self.selectedCharacter1 = None
        self.selectedCharacter2 = None
        self.char1Frame["image"] = None
        self.char2Frame["image"] = None
        self.footerFrame["text"] = "PLAYER 1 - CHOOSE YOUR CHARACTER"
        self.btnStart["state"] = DGG.DISABLED
        self.frameMain.show()

    def hide(self):
        self.frameMain.hide()
