#!/usr/bin/env python3
"""Package the built WatchSync plugin as a Jellyfin-installable zip.

Ship only the plugin assembly (the server already provides Jellyfin.* and its
transitive dependencies) plus a generated meta.json and the plugin image.
"""
import json
import pathlib
import subprocess
import sys
import zipfile

root = pathlib.Path(__file__).resolve().parent.parent
plugin_dir = root / "WatchSync/Jellyfin.Plugin.WatchSync"
dll = plugin_dir / "bin/Release/net10.0/Jellyfin.Plugin.WatchSync.dll"
png = plugin_dir / "WatchSync.png"
meta = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("/tmp/watchsync-meta.json")
out = pathlib.Path(sys.argv[2]) if len(sys.argv) > 2 else root.parent / "watchsync.zip"

if not dll.exists():
    raise SystemExit(f"missing build output: {dll}")

version = json.loads(meta.read_text())["version"]
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    z.write(dll, "Jellyfin.Plugin.WatchSync.dll")
    z.write(meta, "meta.json")
    if png.exists():
        z.write(png, "WatchSync.png")

print(f"{out} ({out.stat().st_size} bytes) version {version}")
