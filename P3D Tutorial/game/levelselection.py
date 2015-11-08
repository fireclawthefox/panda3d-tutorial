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
            extraArgs = ["escape"],
            pressEffect = False,
            rolloverSound = None,
            clickSound = None)
        self.btnBack.setTransparency(1)
        self.btnBack.reparentTo(self.footerFrame)
