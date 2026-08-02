import json
import os


DEFAULT_CONFIG = {
    "paths": {
        "gizmos": True,
        "icons": True,
        "scripts": True,
        "scripts_menumaker": True,
        "scripts_nukesurvivalkit": True,
        "scripts_nodegraph_utils": True,
        "scripts_stamps": True,
        "scripts_stamps_core": True,
        "toolsets": True,
        "plugins": True,
        "cattery_depthanything": True,
        "cattery_vitmatte": True,
    },
    "menu": {
        "defaults_nodes": True,
        "shortcuts": True,
        "callbacks": True,
        "pimba_tools": True,
        "nuke_grab": True,
        "cattery_menu": True,
    },
    "extra_plugin_paths": [],
}


def _deep_merge(base, override):
    if not isinstance(base, dict) or not isinstance(override, dict):
        return override

    merged = dict(base)
    for key, value in override.items():
        if key in merged and isinstance(merged[key], dict) and isinstance(value, dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return None
    except Exception as exc:
        print(f"[nuke_repo] Could not read config at {path}: {exc}")
        return None


def get_config(base_dir):
    config_path = os.environ.get("NUKE_REPO_CONFIG")
    if not config_path:
        config_path = os.path.join(base_dir, "config.json")

    user_config = _load_json(config_path)
    if user_config is None:
        print(f"[nuke_repo] Using default config (missing file): {config_path}")
        return dict(DEFAULT_CONFIG)

    merged = _deep_merge(DEFAULT_CONFIG, user_config)
    print(f"[nuke_repo] Loaded config: {config_path}")
    return merged


def is_enabled(config, section, key):
    return bool(config.get(section, {}).get(key, False))
