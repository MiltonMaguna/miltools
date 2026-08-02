# modified: 2021-03-28 by @milton
""" DAG utilities"""
import os
from functools import partial

import nuke

from . import align
from . import dag
from . import labeler
from . import scale_widget
# Experimental
from . import snippy
from . import snappy


# Mini functions definitions, can be called via menus or API
def align_selection(direction):
    nodes = nuke.selectedNodes()
    align.smart_align(direction, nodes)


def scale_tree():
    """ Scale tree with a bounding widget. """
    global scale_tree_widget
    this_dag = dag.get_current_dag()
    scale_tree_widget = scale_widget.ScaleWidget(this_dag)
    scale_tree_widget.show()


def mirror_nodes():
    """ Mirror nodes in X """
    align.mirror_nodes(nuke.selectedNodes())


def relabel():
    """ Change the node(s) label"""
    global relabel_popup
    relabel_popup = labeler.Labeller()
    relabel_popup.run()


def interval(axis=dag.AXIS_X):
    align.distribute_nodes(nuke.selectedNodes(), axis, 6 if axis == dag.AXIS_X else 2)


def install_menus(icons_root=None):
    """ Create menu entry for all the alignment nodes """
    def _get_icon(name):
        if not icons_root:
            return '/'
        path = os.path.join(icons_root, name) + '.png'
        return path.replace('\\', '/')

    organize_menu = nuke.menu('Nuke').addMenu('Organize Nodes',
                                              icon=_get_icon('align_center_x'))

    organize_menu.addCommand('Align Nodes - Left',
                             partial(align_selection, dag.LEFT), 'alt+1',
                             shortcutContext=2, icon=_get_icon('align_left'))
    organize_menu.addCommand('Align Nodes - Right',
                             partial(align_selection, dag.RIGHT), 'alt+2',
                             shortcutContext=2, icon=_get_icon('align_right'))
    organize_menu.addCommand('Align Nodes - Center Y',
                             partial(align_selection, dag.CENTER_Y), 'alt+3',
                             shortcutContext=2, icon=_get_icon('align_center_y'))
    organize_menu.addCommand('Align Nodes - Top',
                             partial(align_selection, dag.UP), 'ctrl+1',
                             shortcutContext=2, icon=_get_icon('align_top'))
    organize_menu.addCommand('Align Nodes - Bottom',
                             partial(align_selection, dag.DOWN), 'ctrl+2',
                             shortcutContext=2, icon=_get_icon('align_bottom'))
    organize_menu.addCommand('Align Nodes - Center X',
                             partial(align_selection, dag.CENTER_X), 'ctrl+3',
                             shortcutContext=2, icon=_get_icon('align_center_x'))

    organize_menu.addSeparator()

    organize_menu.addCommand('Scale Nodes', scale_tree, 'alt+5',
                             shortcutContext=2, icon=_get_icon('scale_nodes'))
    organize_menu.addCommand('Distribute Nodes Horizontally',
                             partial(interval, dag.AXIS_X), 'ctrl+4',
                             shortcutContext=2, icon=_get_icon('space_x'))
    organize_menu.addCommand('Distribute Nodes Vertically',
                             partial(interval, dag.AXIS_Y), 'alt+4',
                             shortcutContext=2, icon=_get_icon('space_y'))
    organize_menu.addCommand('Mirror Nodes', mirror_nodes, 'ctrl+5',
                             shortcutContext=2, icon=_get_icon('mirror_x'))
