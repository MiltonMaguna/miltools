import os

import nuke

from repo_config import get_config, is_enabled

print("-" * 30)
print("PIMBA INIT ")
print(f"NUKE {nuke.NUKE_VERSION_STRING}")

root_dir = os.path.join(os.path.dirname(__file__), "nuke_tools")
nuke.pluginAddPath(root_dir)
print(f"Adding Plugin Path: {root_dir}")

config = get_config(os.path.dirname(__file__))

enabled_tools = []
disabled_tools = []
missing_tools = []


def _tool_name(label, rel_path):
    return label or rel_path


def add_plugin_path(rel_path, key, label=None):
    name = _tool_name(label, rel_path)

    if not is_enabled(config, "paths", key):
        disabled_tools.append(name)
        print(f"- Disabled: {name}")
        return

    path = os.path.join(root_dir, rel_path)
    if not os.path.isdir(path):
        missing_tools.append(f"{name} -> {path}")
        print(f"! Missing path: {path}")
        return

    nuke.pluginAddPath(path)
    enabled_tools.append(name)
    print(f"+ Enabled: {name} -> {path}")


def print_tools_report():
    print("-" * 30)
    print("PIMBA TOOLS REPORT")
    print(f"Enabled ({len(enabled_tools)}):")
    for tool in sorted(enabled_tools):
        print(f"  + {tool}")

    print(f"Disabled ({len(disabled_tools)}):")
    for tool in sorted(disabled_tools):
        print(f"  - {tool}")

    print(f"Missing ({len(missing_tools)}):")
    for tool in sorted(missing_tools):
        print(f"  ! {tool}")


# --------------------------------------------------------------------------------------------
# GIZMOS / PLUGINS
# --------------------------------------------------------------------------------------------

add_plugin_path("gizmos", "gizmos")
add_plugin_path("icons", "icons")
add_plugin_path("scripts", "scripts")
add_plugin_path("scripts/menumaker_master", "scripts_menumaker", "menumaker_master")
add_plugin_path(
    "scripts/NukeSurvivalToolkit", "scripts_nukesurvivalkit", "NukeSurvivalToolkit"
)
add_plugin_path(
    "scripts/nuke_nodegraph_utils", "scripts_nodegraph_utils", "nuke_nodegraph_utils"
)
add_plugin_path("scripts/Stamps-master", "scripts_stamps", "Stamps-master")
add_plugin_path("scripts/Stamps-master/stamps", "scripts_stamps_core", "Stamps core")
add_plugin_path("plugins", "plugins")
add_plugin_path("ToolSets", "toolsets")

for extra_path in config.get("extra_plugin_paths", []):
    if not isinstance(extra_path, str) or not extra_path.strip():
        continue

    resolved = (
        extra_path if os.path.isabs(extra_path) else os.path.join(root_dir, extra_path)
    )
    if not os.path.isdir(resolved):
        missing_tools.append(f"extra:{extra_path} -> {resolved}")
        print(f"! Missing extra path: {resolved}")
        continue

    nuke.pluginAddPath(resolved)
    enabled_tools.append(f"extra:{extra_path}")
    print(f"+ Extra path: {resolved}")

# ------------------------------------------------------------------------------
# CATERRY
# ------------------------------------------------------------------------------
print("- Loading Cattery plugin")
add_plugin_path(
    "plugins/Cattery/DepthAnythingV2",
    "cattery_depthanything",
    "Cattery DepthAnythingV2",
)
add_plugin_path("plugins/Cattery/vitmatte", "cattery_vitmatte", "Cattery vitmatte")

print_tools_report()

print("-" * 30)
