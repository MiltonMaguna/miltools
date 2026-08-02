# -----------------------------------------------------------------------------
# V!ctor Tools
# Copyright (c) 2011 Victor Perez.  All Rights Reserved.
# V_PresetBackdrop.py
# editor - Milton Maguna / milton.maguna@gmail.com
# 1.0.0 - First Release -  02/23/2021
# -----------------------------------------------------------------------------


import nuke
import colorsys
import operator

### Preset Backdrop
def presetBackdrop():
    customPreset = None
    sep = '"'
    presets = ['BG','CAM','CLEANUP','COLORCORRECTION','DESPILL','FG', 'FOOTAGE', 
                'KEY', 'MG','ROTO','REFERENCES', 'PRERENDERS', 'TRACKER']

    p = nuke.Panel('Preset Backdrop')
    p.addEnumerationPulldown('Preset',' '.join(presets))
    p.addSingleLineInput('Custom Label','')
    if p.show():
        customPreset = p.value('Preset')
        customLabel = p.value('Custom Label')
    
    # Backdrop presets
    if customPreset == 'BG':
        presetLabel = 'BG'
        presetColor = colorsys.hsv_to_rgb(0.98, 0.7, 0.4)
        
    if customPreset == 'CAM':
        presetLabel = 'CAM'
        presetColor = colorsys.hsv_to_rgb(0, 1, 0.49)
        
    if customPreset == 'CLEANUP':
        presetLabel = 'CLEANUP'
        presetColor = colorsys.hsv_to_rgb(0.53, 0.44, 0.38)
        
    if customPreset == 'COLORCORRECTION':
        presetLabel = 'COLORCORRECTION'
        presetColor = colorsys.hsv_to_rgb(0.84, 0.53, 0.49)
        
    if customPreset == 'DESPILL':
        presetLabel = 'DESPILL'
        presetColor = colorsys.hsv_to_rgb(0.67, 0.53, 0.49)
        
    if customPreset == 'FG':
        presetLabel = 'FG'
        presetColor = colorsys.hsv_to_rgb(0.85, 0.6, 0.4)

    if customPreset == 'FOOTAGE':
        presetLabel = 'FOOTAGE'
        presetColor = colorsys.hsv_to_rgb(0, 0, 0.49)
        
    if customPreset == 'KEY':
        presetLabel = 'KEY'
        presetColor = colorsys.hsv_to_rgb(0.33, 1, 0.49)
        
    if customPreset == 'MG':
        presetLabel = 'MG'
        presetColor = colorsys.hsv_to_rgb(0.47, 0.65, 0.4)
        
    if customPreset == 'ROTO':
        presetLabel = 'ROTO'
        presetColor = colorsys.hsv_to_rgb(0.33, 0.44, 0.38)
        
    if customPreset == 'REFERENCES':
        presetLabel = 'REFERENCES'
        presetColor = colorsys.hsv_to_rgb(0.16, 0, 0.29)
        
    if customPreset == 'PRERENDERS':
        presetLabel = 'PRERENDERS'
        presetColor = colorsys.hsv_to_rgb(0.16, 1, 0.8)
        
    if customPreset == 'TRACKER':
        presetLabel = 'TRACKER'
        presetColor = colorsys.hsv_to_rgb(0.16, 0, 0.4)
        
    ### Backdrop creation based on presets
    if customPreset is not None:
        # RGB to HEX
        r = presetColor[0]
        g = presetColor[1]
        b = presetColor[2]
        hexColour = int('%02x%02x%02x%02x' % (int(r*255),int(g*255),int(b*255),1), 16)
            
        selNodes = nuke.selectedNodes()
        if not selNodes:
            if customLabel == '':
                return nuke.nodes.BackdropNode(label = '<center>'+presetLabel, tile_color = hexColour, note_font_size = 50)
            else:
                return nuke.nodes.BackdropNode(label = '<center>'+customLabel, tile_color = hexColour, note_font_size = 50)
    
        # Find Min. and Max. of Positions
        positions = [(i.xpos(), i.ypos()) for i in selNodes]
        xPos = sorted(positions, key = operator.itemgetter(0))
        yPos = sorted(positions, key = operator.itemgetter(1))
        xMinMaxPos = (xPos[0][0], xPos[-1:][0][0])
        yMinMaxPos = (yPos[0][1], yPos[-1:][0][1])
        
        if customLabel == '':
            n = nuke.nodes.BackdropNode(xpos = xMinMaxPos[0]-10, bdwidth = xMinMaxPos[1]-xMinMaxPos[0]+110, ypos = yMinMaxPos[0]-85, bdheight = yMinMaxPos[1]-yMinMaxPos[0]+160, label = '<center>'+presetLabel, tile_color = hexColour, note_font_size = 50)
        else:
            n = nuke.nodes.BackdropNode(xpos = xMinMaxPos[0]-10, bdwidth = xMinMaxPos[1]-xMinMaxPos[0]+110, ypos = yMinMaxPos[0]-85, bdheight = yMinMaxPos[1]-yMinMaxPos[0]+160, label = '<center>'+customLabel, tile_color = hexColour, note_font_size = 50)
            
        n['selected'].setValue(False)
       
        # Revert to Previous Selection
        [i['selected'].setValue(True) for i in selNodes]
        
        return n
    else:
        pass