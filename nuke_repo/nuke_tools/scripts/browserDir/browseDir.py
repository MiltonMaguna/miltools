# Browse Directory v1.0, 2011-11-12
# by Fredrik Averpil, fredrik.averpil [at] gmail.com, www.averpil.com/fredrik
# -----------------------------------------------------------------------------
# Editor Milton Maguna / milton.maguna@gmail.com
# 2.0.0 - python 3.9 revision  -  01/23/2022
# -----------------------------------------------------------------------------
#
# Usage:
# a) select any Write node or Read node and run browseDirByNode()
# b) open any path via command browseDir(path)
#
# Example of menu.py:
# import browseDir
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Browse/Node\'s file path',
# "browseDir.browseDirByNode()", 'shift+b')
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Browse/Scripts folder',
# "browseDir.browseDir('scripts')" )
#
# And if your folder structure looks like this -
# serverpath/ ... sequence_folder/shot_folder/nuke/scripts/
# you should be able to use the following as well:
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Browse/Scripts folder',
# "browseDir.browseDir('sequence')" )
# nuke.menu( 'Nuke' ).addCommand( 'My file menu/Browse/Scripts folder',
# "browseDir.browseDir('shot')" )


import os
import sys

import nuke


def launch(directory):
    # Open folder
    print('Attempting to open folder: ' + {directory})
    if os.path.exists(directory):
        if sys.platform == 'darwin':
            os.system('open ' + directory)
        elif sys.platform == 'win32':
            os.system('start ' + directory)
    else:
        nuke.message('Path does not exist:\n' + directory)


def browseDirByNode2():

    error = False

    try:
        selectedNodeFilePath = nuke.callbacks.filenameFilter(
            nuke.selectedNode()['file'].getValue())

    except ValueError:
        error = True
        nuke.message('No node selected.')
    except NameError:
        error = True
        nuke.message('You must select a Read node or a Write node.')

    if error == False:
        filePathSplitted = str.split(selectedNodeFilePath, '/')

        dirFromNode = ''
        for i in range(0, (len(filePathSplitted) - 1)):
            dirFromNode = dirFromNode + filePathSplitted[i] + '/'

        launch(dirFromNode)


def browseDirByNode():
    for a in nuke.selectedNodes():
        if not a:
            print('select a node')
            return
        try:
            path = a.knob('file').getValue()
            dir = os.path.dirname(path)
            dir = dir.replace('/', '\\')
            print(f'opening {dir}')

            if (sys.platform == 'win32'):
                os.system('start explorer "%s"' % dir)
            elif (sys.platform == 'darwin'):
                os.system('open "%s"' % dir)
        except Exception:
            print(f'failed!{dir}')

# File menu browseDir


def browseDir(action):

    if (nuke.root().name() == 'Root') and (action != 'Path'):
        nuke.message('You need to save the Nuke script first!')

    else:

        # Get full path to script
        scriptPath = nuke.callbacks.filenameFilter(nuke.root().name())

        # Divide up the paths
        scriptPathSplitted = str.split(scriptPath, '/')

        # Reset
        openMe = ''

        if action == 'scripts':
            for i in range(0, (len(scriptPathSplitted) - 1)):
                openMe = openMe + scriptPathSplitted[i] + '/'

        elif action == 'sequence':
            for i in range(0, (len(scriptPathSplitted) - 4)):
                openMe = openMe + scriptPathSplitted[i] + '/'

        elif action == 'shot':
            for i in range(0, (len(scriptPathSplitted) - 3)):
                openMe = openMe + scriptPathSplitted[i] + '/'

        launch(openMe)
