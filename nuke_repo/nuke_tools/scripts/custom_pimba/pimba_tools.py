# -----------------------------------------------------------------------------
# open_tools.py
# Milton Maguna / milton.maguna@gmail.com
# 1.0.0 - First Release -  01/12/2021
# 2.0.0 - python 3.7 revision  -  01/23/2022
# 2.0.1 - python 3.7 revision  -  03/02/2022
# 2.0.2 - add readFromtWrite   -  04/03/2022
# -----------------------------------------------------------------------------

import nuke

menubar = nuke.menu("Nuke")
pimba_menu = menubar.addMenu('Pimba Tools')

from browserDir.browseDir import browseDirByNode
pimba_menu.addCommand('BrowserDir', lambda: browseDirByNode(), 'shift+b')

from nukescripts import refreshToolsetsMenu
# nukescripts.refreshToolsetsMenu()
pimba_menu.addCommand('Refresh_ToolsSets', lambda: refreshToolsetsMenu())

from copyConnect.copyConnected import copyConnected
pimba_menu.addCommand('copyConnected', lambda: copyConnected(), 'Ctrl+alt+v')

from setKnobValue.sb_setKnobValue import sb_setKnobValue
pimba_menu.addCommand('SetKnobValue', lambda: sb_setKnobValue())

from WrapItUp_pimba.WrapItUp import WrapItUp
pimba_menu.addCommand('Wrap It Up', lambda: WrapItUp())

from V_Tools.V_PresetBackdrop import presetBackdrop
pimba_menu.addCommand('Preset Backdrop', lambda: presetBackdrop(), 'ctrl+alt+b')

from pre_render.prerender import PreRenderTools
pimba_menu.addCommand('pre Renders', lambda: PreRenderTools().create(), 'shift+p')

from readFromWrite.readFromWrite import ReadFromWrite
pimba_menu.addCommand('Read from Write', lambda: ReadFromWrite(), 'shift+r')

# COPY CONNECTED
from copyConnect.copyConnected import copyConnected
pimba_menu.addCommand('copyConnected', lambda: copyConnected(), 'Ctrl+alt+v')

# SET KNOB VALUE
from setKnobValue.sb_setKnobValue import sb_setKnobValue
pimba_menu.addCommand('SetKnobValue', lambda: sb_setKnobValue())