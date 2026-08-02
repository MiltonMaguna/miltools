# -----------------------------------------------------------------------------
# prerender.py
# Milton Maguna / milton.maguna@gmail.com
# 1.0.0 - First Release -  03/02/2022
# -----------------------------------------------------------------------------

import os

import colorsys
import operator

import nuke
from nukescripts import autobackdrop
from nukescripts import misc

# Panel 
NAME = 'pre_render'
EXTENSION  = "exr png dpx "
CHANNELS = "all rgba rgb "

# knob write
NAME_WRITE = 'prerenders_'

# offset position
OFFSET = 150

# backdrop 
PRESET_LABEL = 'PRERENDERS'
PRESET_COLOR = colorsys.hsv_to_rgb(0.16, 1, 0.8)



class PreRenderTools():
    def create(self) -> None:
        if nuke.Root().name() == 'Root':
            nuke.message('the script is not in pipeline')
            return
        node = ''
        node = nuke.selectedNode()
        self.pre_render_panel(node)
    
    def pre_render_panel(self, node:str) -> None:
        # PANEL
        panel = nuke.Panel('Pre_Render')
        panel.addSingleLineInput("name:", '')
        panel.addEnumerationPulldown("channels:", CHANNELS)
        panel.addEnumerationPulldown("filetype:", EXTENSION)

        panel.addButton("Cancel")
        panel.addButton("OK")
        result = panel.show()

        if not result:
            print ('prerender cancel')
            return ''

        # VARIABLES PANEL
        custom_name = panel.value("name:")
        channel = panel.value("channels:")
        extension = panel.value("filetype:")

        # FILE
        list_script_name = nuke.scriptName().split('/')
        base_path = ('/').join(list_script_name[:-2])

        if not custom_name:
            # self.file = os.path.join(base_path, 'prerenders', 'prerenders')
            nuke.message('It missing a name')
            result = panel.show()

            if not result:
                print ('prerender cancel')
                return ''

        name_file = f'{custom_name}_%04d.{extension}'
        file = os.path.join(base_path, 'prerenders',custom_name, name_file).replace('\\', '/')
        print ('create pre render', file)

        # POSITION 
        pos = [node.xpos() , 
               node.ypos() + (node.screenWidth() / 2) ] 

        # CREATE WRITE and DOT
        dot_pre = nuke.nodes.Dot()
        dot_pre['xpos'].setValue(pos[0] + (node.screenWidth()/2) - (dot_pre.screenWidth()/2))
        dot_pre['ypos'].setValue(pos[1] + OFFSET)
        dot_pre.setInput(0, node)

        self.create_pre_render_write(dot_pre, 
                                    (NAME_WRITE+ custom_name), 
                                    channel, 
                                    file, 
                                    pos, 
                                    extension )

    def create_pre_render_write(self,
                                input: str,
                                name: str,
                                channel: str,
                                filename: str, 
                                pos: list, 
                                filetype: str) -> None:

        write_exr = nuke.nodes.Write(name = name,
                                    channels = channel,
                                    file = filename,
                                    file_type = filetype,
                                    create_directories = True, 
                                    xpos = pos[0], 
                                    ypos = pos[1] + OFFSET*2)
        write_exr.setInput(0, input)

        misc.clear_selection_recursive()

        self.autobackdrop(name)
    
    def autobackdrop(self, name_node: str) -> None:

        # custom backdrop
        # RGB to HEX
        r = PRESET_COLOR[0]
        g = PRESET_COLOR[1]
        b = PRESET_COLOR[2]
        hexColour = int('%02x%02x%02x%02x' % (int(r*255),int(g*255),int(b*255),1), 16)

        extend_bdrop = 100
        bdX = (nuke.toNode(name_node).xpos()) - extend_bdrop
        bdY = (nuke.toNode(name_node).ypos()) - extend_bdrop
        bdW = (nuke.toNode(name_node).xpos() - bdX + 80) + extend_bdrop
        bdH = (nuke.toNode(name_node).ypos() - bdY + 150) + extend_bdrop

        nuke.nodes.BackdropNode(
            xpos=bdX,
            ypos=bdY,
            bdwidth=bdW,
            bdheight=bdH,
            tile_color=hexColour,
            note_font_size=30,
            label=f'<left>{PRESET_LABEL}',
        )
