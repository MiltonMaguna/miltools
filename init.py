import os

import nuke


repo_dir = os.path.dirname(os.path.abspath(__file__))
nuke_repo_path = os.path.join(repo_dir, "nuke_repo")

if os.path.isdir(nuke_repo_path):
    nuke.pluginAddPath(nuke_repo_path)
else:
    print(f"[nuke_repo] Missing path: {nuke_repo_path}")
