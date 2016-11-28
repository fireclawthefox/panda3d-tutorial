#!/usr/bin/python
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

from panda3d.core import (
    TextNode,
    TextProperties,
    TextPropertiesManager)
from direct.gui.DirectGui import (
    DirectFrame,
    DirectLabel,
    DirectButton)
from direct.stdpy.file import open
from direct.interval.LerpInterval import LerpPosInterval

class Credits:
    def __init__(self):

        self.frameMain = DirectFrame(
            frameSize = (base.a2dLeft, base.a2dRight,
                         base.a2dBottom, base.a2dTop),
            frameColor = (0.05, 0.05, 0.05, 1))
        self.frameMain.setTransparency(1)

        tpBig = TextProperties()
        tpBig.setTextScale(1.5)
        tpSmall = TextProperties()
        tpSmall.setTextScale(0.75)
        tpUs = TextProperties()
        tpUs.setUnderscore(True)
        tpMgr = TextPropertiesManager.getGlobalPtr()
        tpMgr.setProperties("big", tpBig)
        tpMgr.setProperties("small", tpSmall)
        tpMgr.setProperties("us", tpUs)

        creditsText = ""
        with open("credits.txt") as f:
            creditsText = f.read()
        self.lblCredits = DirectLabel(
            text = creditsText,
            text_fg = (1,1,1,1),
            text_bg = (0,0,0,0),
            frameColor = (0,0,0,0),
            text_align = TextNode.ACenter,
            scale = 0.1,
            pos = (0, 0, base.a2dTop - 0.2))
        self.lblCredits.setTransparency(1)
        self.lblCredits.reparentTo(self.frameMain)

        self.creditsScroll = LerpPosInterval(
            self.lblCredits,
            12.0,
            (0, 0, base.a2dTop + 3.5),
            startPos=(0, 0, base.a2dBottom),
            name="CreditsScroll")

        self.btnBack = DirectButton(
            text = "BACK",
            text_fg = (1,1,1,1),
            text_align = TextNode.ALeft,
            scale = 0.1,
            pad = (0.15, 0.15),
            pos = (base.a2dLeft + 0.08, 0, base.a2dBottom + 0.05),
            frameColor = (
                (0.2,0.2,0.2,0.8),
                (0.4,0.4,0.4,0.8),
                (0.4,0.4,0.4,0.8),
                (0.1,0.1,0.1,0.8),
                ),
            relief = 1,
            command = base.messenger.send,
            extraArgs = ["Credits-Back"],
            pressEffect = False,
            rolloverSound = None,
            clickSound = None)
        self.btnBack.setTransparency(1)
        self.btnBack.reparentTo(self.frameMain)

        self.hide()

    def show(self):
        self.frameMain.show()
        self.creditsScroll.loop()

    def hide(self):
        self.frameMain.hide()
        self.creditsScroll.finish()
