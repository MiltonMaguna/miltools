
##---------- Ym_alignNodes ----------
import os 
import Ym_alignNodes


BASE_PATH = os.path.dirname(__file__)
# F:\nuke\env\2022\scripts\Ym_alignNodes_v1.5\icons

toolbar = nuke.toolbar('Nodes')
# mcMenu = toolbar.addMenu('Ym_alignNodes Ver1.5', icon=os.path.join(BASE_PATH, 
#                                                                     "icons", "alignNodes.png")

ngz = toolbar.addMenu("gz", icon='F:\\nuke\\arcane\\dev\\custom_gizmo\\icons\\gz.png')

ngz.addCommand('align_nodes/Left X', 'Ym_alignNodes.alignLX()', '+F1',icon='leftX.png')
ngz.addCommand('align_nodes/Center X', 'Ym_alignNodes.alignCX()', '+F2',icon='centerX.png')
ngz.addCommand('align_nodes/Right X', 'Ym_alignNodes.alignRX()', '+F3',icon='rightX.png')
ngz.addCommand('align_nodes/Interval X', 'Ym_alignNodes.align_intX()', '+F4',icon='intervalX.png')

ngz.addCommand('align_nodes/Top Y', 'Ym_alignNodes.alignTY()', '+F5',icon='topY.png')
ngz.addCommand('align_nodes/Center Y', 'Ym_alignNodes.alignCY()', '+F6',icon='centerY.png')
ngz.addCommand('align_nodes/Under Y', 'Ym_alignNodes.alignUY()', '+F7',icon='underY.png')
ngz.addCommand('align_nodes/Interval Y', 'Ym_alignNodes.align_intY()', '+F8',icon='intervalY.png')

ngz.addCommand('align_nodes/Interval XX', 'Ym_alignNodes.align_intXX()', '+F9',icon='intervalXX.png')
ngz.addCommand('align_nodes/Interval YY', 'Ym_alignNodes.align_intYY()', '+F10',icon='intervalYY.png')
