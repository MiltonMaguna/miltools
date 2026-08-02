import nuke

t=nuke.menu("Nodes")
u=t.addMenu("ap_tools", icon="ap_tools.png")
 
t.addCommand( "ap_tools/apDespill", "nuke.createNode('apDespill')", icon="apDespill.png")
t.addCommand( "ap_tools/apScreenClean", "nuke.createNode('apScreenClean')", icon="apScreenClean.png")
t.addCommand( "ap_tools/apScreenGrow", "nuke.createNode('apScreenGrow')", icon="apScreenGrow.png")
t.addCommand( "ap_tools/apEdgePush", "nuke.createNode('apEdgePush')", icon="apEdgePush.png")
t.addCommand( "ap_tools/apDirLight", "nuke.createNode('apDirLight')", icon="apDirLight.png")
t.addCommand( "ap_tools/apHeatDistortion", "nuke.createNode('apHeatDistortion')", icon="apHeatDistortion.png")
t.addCommand( "ap_tools/apDisabler", "nuke.createNode('apDisabler')", icon="apDisabler.png")
t.addCommand( "ap_tools/apJoinChannels", "nuke.createNode('apJoinChannels')", icon="apJoinChannels.png")
t.addCommand( "ap_tools/apKeyer", "nuke.createNode('apKeyer')", icon="apKeyer.png")
t.addCommand( "ap_tools/apDirBlur", "nuke.createNode('apDirBlur')", icon="apDirBlur.png")
t.addCommand( "ap_tools/apGlow", "nuke.createNode('apGlow')", icon="apGlow.png")
