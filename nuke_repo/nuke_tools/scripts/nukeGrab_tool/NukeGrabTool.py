# Nuke Advanced Grab Tool v3.8
#
# This script implements an advanced grab tool to mimic Nuke's native node movement behavior.
#
# Features:
# - Standard Grab (E): Moves only selected nodes.
# - Input Tree Grab (Cmd+Option+E): Moves the selected node and all its upstream nodes.
# - Full Tree Grab (Cmd+E): Moves the entire connected node tree (upstream and downstream).
# - Exit grab mode by pressing 'E' again
# - Option to keep nodes selected after exiting grab mode
# - Proper handling of zoom levels for consistent movement speed
# - Middle mouse button or Alt + Left click freezes movement without changing position on release
#
# Usage:
# 1. Select a node or nodes in Nuke
import nuke

# Global variables for user customization
OFFSET_X = 250
OFFSET_Y = 200
MERGE_OFFSET_Y = 400
BACKDROP_COLOR = 0x7F7F7FFF  # Gray color
BACKDROP_LABEL_FONT_SIZE = 42
BACKDROP_PADDING = 100  # Padding around nodes inside backdrop


def split_light_channels(node):
    # Get all channels and filter for light channels, excluding 'lighting' and 'lightning'
    all_channels = node.channels()
    light_channels = [
        chan.split('.')[0]
        for chan in all_channels
        if ('light' in chan.lower() or 'lght' in chan.lower())
        and not chan.lower().startswith(('lighting', 'lightning'))
    ]
    light_channels = list(set(light_channels))  # Remove duplicates
    light_channels.sort(key=str.lower)

    if not light_channels:
        nuke.message(f'No suitable light channels found in node: {node.name()}')
        return

    dot_nodes = []
    shuffle_nodes = []
    remove_nodes = []
    merge_nodes = []
    second_dot_nodes = []

    # Calculate the starting position
    start_x = node.xpos() + BACKDROP_PADDING
    start_y = node.ypos() + BACKDROP_PADDING

    # Create Dot, Shuffle, and Remove nodes for each light channel
    for i, chan in enumerate(light_channels):
        dot_node = nuke.nodes.Dot()
        shuf_node = nuke.nodes.Shuffle2(
            name=f'{node.name()}_{chan}',
            inputs=[dot_node],
            postage_stamp=True,
            hide_input=False,
        )
        shuf_node['in1'].setValue(chan)
        remove_node = nuke.nodes.Remove(
            operation='keep',
            channels='rgb',
            name=f'Keep_{node.name()}_{chan}',
            label='keep [value channels]',
            inputs=[shuf_node],
        )
        xpos = start_x + OFFSET_X * i
        ypos = start_y + OFFSET_Y
        dot_node.setXYpos(xpos, ypos)
        shuf_node.setXYpos(xpos - 34, dot_node.ypos() + 100)
        remove_node.setXYpos(xpos - 34, shuf_node.ypos() + 100)
        shuffle_nodes.append(shuf_node)
        remove_nodes.append(remove_node)
        dot_nodes.append(dot_node)

    # Connect Dot nodes
    for i, dot in enumerate(dot_nodes):
        if i == 0:
            dot.setInput(0, node)
        else:
            dot.setInput(0, dot_nodes[i - 1])

    # Create Merge nodes to combine shuffled and removed channels
    for i, remove in enumerate(remove_nodes):
        if i == 0:
            continue
        else:
            dot_node = nuke.nodes.Dot()
            second_dot_nodes.append(dot_node)
            dot_node.setInput(0, remove)
            merge = nuke.nodes.Merge2(
                inputs=[remove_nodes[0] if i == 1 else merge_nodes[-1], dot_node],
                operation='plus',
                label=shuffle_nodes[i].name(),
                output='rgb',
            )
            merge.setXYpos(
                remove_nodes[0].xpos(),
                remove_nodes[0].ypos() + MERGE_OFFSET_Y + (i - 1) * 100,
            )
            dot_node.setXYpos(remove.xpos() + 34, merge.ypos() + 5)
            merge_nodes.append(merge)

    # Create backdrop
    all_nodes = dot_nodes + shuffle_nodes + remove_nodes + merge_nodes + second_dot_nodes
    bdX = min(node.xpos() for node in all_nodes) - BACKDROP_PADDING
    bdY = min(node.ypos() for node in all_nodes) - BACKDROP_PADDING
    bdW = (
        max(node.xpos() + node.screenWidth() for node in all_nodes)
        - bdX
        + BACKDROP_PADDING * 2
    )
    bdH = (
        max(node.ypos() + node.screenHeight() for node in all_nodes)
        - bdY
        + BACKDROP_PADDING * 2
    )

    backdrop = nuke.nodes.BackdropNode(
        xpos=bdX,
        bdwidth=bdW,
        ypos=bdY,
        bdheight=bdH,
        tile_color=BACKDROP_COLOR,
        note_font_size=BACKDROP_LABEL_FONT_SIZE,
        label=f'Light Channel Splitter - {node.name()}',
    )


def batch_split_light_channels():
    selected_nodes = nuke.selectedNodes()
    if not selected_nodes:
        nuke.message('Please select at least one node.')
        return

    for node in selected_nodes:
        split_light_channels(node)

    nuke.message(f'Processed {len(selected_nodes)} node(s).')


# Run the batch operation
# batch_split_light_channels()
# 2. Press 'E' to move only the selected node(s)
# 3. Press 'Cmd+Option+E' to move the selected node and all its inputs
# 4. Press 'Cmd+E' to move the entire connected node tree
# 5. Move the mouse to reposition the nodes
# 6. Hold middle mouse button or Alt + Left click to freeze movement
# 7. Left-click, press 'Enter', or press 'E' again to confirm the new position
# 8. Press 'Esc' to cancel the operation
# 9. Press 'Z' to lock movement to X-axis, 'Y' to lock movement to Y-axis

import nuke

try:
    from PySide2 import QtCore, QtGui, QtWidgets

    PYSIDE_VERSION = 2
except ImportError:
    from PySide6 import QtCore, QtGui, QtWidgets

    PYSIDE_VERSION = 6

# User variable to control whether nodes remain selected after grab mode
KEEP_NODES_SELECTED = True


class AdvancedGrabTool(QtCore.QObject):
    def __init__(self):
        super(AdvancedGrabTool, self).__init__()
        self.grab_active = False
        self.start_pos = None
        self.last_pos = None
        self.selected_nodes = []
        self.affected_nodes = set()
        self.original_positions = {}
        self.current_positions = {}
        self.original_cursor = None
        self.locked = False
        self.lock_x = False
        self.lock_y = False
        self.grab_mode = 'standard'
        self.freeze_movement = False
        self.alt_pressed = False

    def get_input_tree(self, node, upstream=None):
        if upstream is None:
            upstream = set()
        if node not in upstream:
            upstream.add(node)
            for i in range(node.inputs()):
                input_node = node.input(i)
                if input_node:
                    self.get_input_tree(input_node, upstream)
        return upstream

    def get_connected_nodes(self, start_node):
        connected = set()
        to_process = [start_node]

        while to_process:
            node = to_process.pop(0)
            if node not in connected:
                connected.add(node)

                inputs = node.dependencies(nuke.INPUTS | nuke.HIDDEN_INPUTS)
                to_process.extend([n for n in inputs if n not in connected])

                outputs = node.dependent(nuke.INPUTS | nuke.HIDDEN_INPUTS)
                to_process.extend([n for n in outputs if n not in connected])

        return connected

    def activate_grab(self, mode='standard'):
        if self.locked:
            return

        self.selected_nodes = nuke.selectedNodes()
        if not self.selected_nodes:
            return

        self.grab_active = True
        self.locked = True
        self.grab_mode = mode

        if self.grab_mode == 'input_tree':
            self.affected_nodes = set()
            for node in self.selected_nodes:
                self.affected_nodes.update(self.get_input_tree(node))
        elif self.grab_mode == 'full_tree':
            self.affected_nodes = set()
            for node in self.selected_nodes:
                self.affected_nodes.update(self.get_connected_nodes(node))
        else:  # standard mode
            self.affected_nodes = set(self.selected_nodes)

        self.original_positions = {
            node: (node.xpos(), node.ypos()) for node in self.affected_nodes
        }
        self.current_positions = self.original_positions.copy()

        self.start_pos = QtGui.QCursor.pos()
        self.last_pos = self.start_pos

        app = QtWidgets.QApplication.instance()
        self.original_cursor = app.overrideCursor()
        app.setOverrideCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))

        app.installEventFilter(self)

        nuke.Undo().begin('Grab Tool')

    def deactivate_grab(self):
        self.grab_active = False
        self.locked = False
        self.lock_x = False
        self.lock_y = False
        self.grab_mode = 'standard'
        self.freeze_movement = False
        self.last_pos = None
        self.alt_pressed = False

        app = QtWidgets.QApplication.instance()
        while app.overrideCursor() is not None:
            app.restoreOverrideCursor()

        if self.original_cursor:
            app.setOverrideCursor(self.original_cursor)

        QtWidgets.QApplication.instance().removeEventFilter(self)

        if not KEEP_NODES_SELECTED:
            for node in self.affected_nodes:
                node.setSelected(False)

        self.affected_nodes.clear()

        nuke.Undo().end()

    def apply_grab(self):
        for node, (x, y) in self.current_positions.items():
            node.setXYpos(int(x), int(y))
        self.deactivate_grab()

    def cancel_grab(self):
        for node, (x, y) in self.original_positions.items():
            node.setXYpos(x, y)
        self.deactivate_grab()

    def _mouse_global_pos(self, event):
        # Qt6 deprecates globalPos() in favor of globalPosition().
        if hasattr(event, 'globalPosition'):
            return event.globalPosition().toPoint()
        return event.globalPos()

    def eventFilter(self, obj, event):
        if self.grab_active:
            if event.type() == QtCore.QEvent.MouseMove:
                app = QtWidgets.QApplication.instance()
                app.changeOverrideCursor(QtGui.QCursor(QtCore.Qt.ClosedHandCursor))
                if not self.freeze_movement:
                    self.update_positions(self._mouse_global_pos(event))
            elif event.type() == QtCore.QEvent.MouseButtonPress:
                if event.button() == QtCore.Qt.MiddleButton:
                    self.freeze_movement = True
                elif event.button() == QtCore.Qt.LeftButton and self.alt_pressed:
                    self.freeze_movement = True
            elif event.type() == QtCore.QEvent.MouseButtonRelease:
                if event.button() == QtCore.Qt.LeftButton and not self.alt_pressed:
                    self.apply_grab()
                elif event.button() == QtCore.Qt.MiddleButton or (
                    event.button() == QtCore.Qt.LeftButton and self.alt_pressed
                ):
                    self.freeze_movement = False
                    self.last_pos = self._mouse_global_pos(event)
            elif event.type() == QtCore.QEvent.KeyPress:
                if event.key() == QtCore.Qt.Key_Alt:
                    self.alt_pressed = True
                elif event.key() == QtCore.Qt.Key_Z:
                    self.lock_x = True
                    self.lock_y = False
                    return True
                elif event.key() == QtCore.Qt.Key_Y:
                    self.lock_y = True
                    self.lock_x = False
                    return True
                elif (
                    event.key() == QtCore.Qt.Key_Return
                    or event.key() == QtCore.Qt.Key_Enter
                ):
                    self.apply_grab()
                    return True
                elif event.key() == QtCore.Qt.Key_Escape:
                    self.cancel_grab()
                    return True
                elif event.key() == QtCore.Qt.Key_E:
                    self.apply_grab()
                    return True
            elif event.type() == QtCore.QEvent.KeyRelease:
                if event.key() == QtCore.Qt.Key_Alt:
                    self.alt_pressed = False
                    if self.freeze_movement:
                        self.freeze_movement = False
                        self.last_pos = QtGui.QCursor.pos()
        return False

    def update_positions(self, current_pos):
        if self.last_pos is None:
            self.last_pos = self.start_pos

        offset = current_pos - self.last_pos

        # Get the current zoom level
        zoom = nuke.zoom()

        # Apply zoom-adjusted scaling
        scaled_offset = QtCore.QPointF(offset.x() / zoom, offset.y() / zoom)

        for node in self.affected_nodes:
            current_x, current_y = self.current_positions[node]
            if self.lock_x:
                new_x = current_x + scaled_offset.x()
                new_y = current_y
            elif self.lock_y:
                new_x = current_x
                new_y = current_y + scaled_offset.y()
            else:
                new_x = current_x + scaled_offset.x()
                new_y = current_y + scaled_offset.y()

            self.current_positions[node] = (new_x, new_y)
            node.setXYpos(int(new_x), int(new_y))

        self.last_pos = current_pos


grab_tool = AdvancedGrabTool()


def grab_standard():
    if grab_tool.grab_active:
        grab_tool.apply_grab()
    else:
        grab_tool.activate_grab(mode='standard')


def grab_input_tree():
    grab_tool.activate_grab(mode='input_tree')


def grab_full_tree():
    grab_tool.activate_grab(mode='full_tree')


# Add the Grab tool commands to Nuke's menu
# nuke.menu('Nuke').addCommand('Edit/Grab Tool', grab_standard, 'e')
# nuke.menu('Nuke').addCommand('Edit/Grab Input Tree', grab_input_tree, 'ctrl+e')
# nuke.menu('Nuke').addCommand('Edit/Grab Full Tree', grab_full_tree, 'alt+ctrl+e')


menubar = nuke.menu('Nuke')
gzm_open_menu = menubar.addMenu('Gizmo Tools')
# Add the Grab tool commands to Nuke's menu
gzm_open_menu.addCommand('Grab_tool/Grab Tool', lambda: grab_standard(), 'e')
gzm_open_menu.addCommand('Grab_tool/Grab Input Tree', lambda: grab_input_tree(), 'ctrl+e')
gzm_open_menu.addCommand(
    'Grab_tool/Grab Full Tree', lambda: grab_full_tree(), 'alt+ctrl+e'
)
