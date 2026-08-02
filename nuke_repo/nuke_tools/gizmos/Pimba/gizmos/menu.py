# add fxT menu
sideBar = nuke.menu('Nodes')
fxT = sideBar.addMenu('fxT', icon='fxT_menu.png')

# add fxT_chromaticAberration Group to the fxT menu
fxT.addCommand('fxT_chromaticAberration', "nuke.createNode('fxT_chromaticAberration')", icon='Shuffle.png')