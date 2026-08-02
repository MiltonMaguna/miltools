# -----------------------------------------------------------------------------
# studio_shorcut.py
# Milton Maguna / milton.maguna@gmail.com
# 1.0.0 - First Release / 01/23/2022
# -----------------------------------------------------------------------------

import nuke

nuke.menu('Nodes').addCommand('Merge/Premult', 'nuke.createNode("Premult")', 'p')
nuke.menu('Nodes').addCommand('Merge/Unpremult', 'nuke.createNode("Unpremult")', 'u')
nuke.menu('Nodes').addCommand('Transform/Reformat', 'nuke.createNode("Reformat")', 'ctrl+r')
nuke.menu('Nodes').addCommand('Transform/Crop', 'nuke.createNode("Crop")', 'ctrl+shift+c')
nuke.menu('Nodes').addCommand('Color/ColorLookup', 'nuke.createNode("ColorLookup")', 'ctrl+l')
nuke.menu('Nodes').addCommand('Other/Backdrop', 'nukescripts.autoBackdrop()', 'alt+b')