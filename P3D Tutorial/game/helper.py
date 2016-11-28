#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = "Fireclaw the Fox"
__license__ = """
Simplified BSD (BSD 2-Clause) License.
See License.txt or http://opensource.org/licenses/BSD-2-Clause for more info
"""

#
# PYTHON IMPORTS
#
import sys

#
# PANDA3D ENGINE IMPORTS
#
from panda3d.core import WindowProperties

def hide_cursor():
    """set the Cursor invisible"""
    props = WindowProperties()
    props.setCursorHidden(True)
    # somehow the window gets undecorated after hiding the cursor
    # so we reset it here to the value we need
    #props.setUndecorated(settings.fullscreen)
    base.win.requestProperties(props)

def show_cursor():
    """set the Cursor visible again"""
    props = WindowProperties()
    props.setCursorHidden(False)
    # set the filename to the mouse cursor
    x11 = "assets/gui/Cursor.x11"
    win = "assets/gui/Cursor.ico"
    if sys.platform.startswith("linux"):
        props.setCursorFilename(x11)
    else:
        props.setCursorFilename(win)
    base.win.requestProperties(props)
