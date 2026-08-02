import os
import importlib

import nuke

from repo_config import get_config, is_enabled

# --------------------------------------------------------------------------------------------
# MENU & TOOLBAR
# --------------------------------------------------------------------------------------------

print("-" * 30)
print("PIMBA MENU")

config = get_config(os.path.dirname(__file__))


def safe_import(module_name, key):
    if not is_enabled(config, "menu", key):
        print(f"- Disabled module: {module_name}")
        return None

    try:
        module = importlib.import_module(module_name)
        print(f"+ Loaded module: {module_name}")
        return module
    except Exception as exc:
        print(f"! Failed to import {module_name}: {exc}")
        return None


# -----------------------------------------------------------------------------
# DEFAULTS NODES, SHORCUTS, CALLBACKS
# -----------------------------------------------------------------------------

safe_import("custom_pimba.studio_defaults_nodes", "defaults_nodes")
safe_import("custom_pimba.studio_shorcut", "shortcuts")
safe_import("custom_pimba.studio_callbacks", "callbacks")

# -----------------------------------------------------------------------------
# PIMBA TOOLS
# -----------------------------------------------------------------------------

safe_import("custom_pimba.pimba_tools", "pimba_tools")

# ------------------------------------------------------------------------------
# ANIMATED SNAP 3D
# ------------------------------------------------------------------------------

# import animatedSnap3D_master.animatedSnap3D
# animatedSnap3D.run()

# ------------------------------------------------------------------------------
# NUKE GRAB TOOLS
# ------------------------------------------------------------------------------

safe_import("nukeGrab_tool.NukeGrabTool", "nuke_grab")


if is_enabled(config, "menu", "cattery_menu"):
    toolbar = nuke.menu("Nodes")
    toolbar.addCommand(
        "Cattery/Depth Estimation/DepthAnythingV2",
        'nuke.createNode("DepthAnythingV2")',
        icon="DepthAnythingV2.png",
    )
    toolbar.addCommand(
        "Cattery/Segmentation/ViTMatte",
        'nuke.createNode("vitmatte")',
        icon="vitmatte.png",
    )
else:
    print("- Disabled Cattery toolbar entries")

print("-" * 30)
