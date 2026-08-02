# -----------------------------------------------------------------------------
# studio_callbacks.py
# Milton Maguna / milton.maguna@gmail.com
# 1.0.0 - First Release -  01/23/2021
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# CALLBACKS
# -----------------------------------------------------------------------------
import nuke

# frame hold
def getCurrentFrame():  # sourcery skip: inline-immediately-returned-variable
    curFrame = nuke.root()['frame'].value()
    return curFrame

def setDefaultFrameHold():
    tn = nuke.thisNode()
    tn['first_frame'].setValue(getCurrentFrame())

nuke.callbacks.addOnUserCreate(setDefaultFrameHold, nodeClass = 'FrameHold')

# frame range

def frameRangeGetLabel():
    tn = nuke.thisNode()
    curName = tn['name'].value()
    f_frame = tn['first_frame'].value()
    l_frame = tn['last_frame'].value()
    return '%s\n [%s - %s]' % (curName, int(f_frame), int(l_frame))

nuke.callbacks.addAutolabel(frameRangeGetLabel, nodeClass = 'FrameRange')
