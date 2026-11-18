#!/usr/bin/env python3
"""Generate a Jellyfin plugin meta.json from build.yaml.

Jellyfin reads meta.json (JSON) in the plugin folder; build.yaml is JPRM's
source format and must not be copied verbatim. Only the scalar fields we
actually maintain are mapped.
"""
import json
import pathlib
import re
import sys

src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "build.yaml")
dst = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "meta.json")
text = src.read_text()


def scalar(key: str) -> str:
    m = re.search(rf'^{key}:\s*"?([^"\n]+)"?\s*$', text, re.M)
    if not m:
        raise SystemExit(f"missing {key} in {src}")
    return m.group(1).strip()


def block(key: str) -> str:
    m = re.search(rf"^{key}: \|\n((?:  .*\n|\n)+)", text, re.M)
    return m.group(1).strip() if m else ""


meta = {
    "category": scalar("category"),
    "changelog": block("changelog"),
    "description": " ".join(line.strip() for line in block("description").splitlines() if line.strip()),
    "guid": scalar("guid"),
    "name": scalar("name"),
    "overview": scalar("overview"),
    "owner": scalar("owner"),
    "targetAbi": scalar("targetAbi"),
    "timestamp": scalar("timestamp") if re.search(r"^timestamp:", text, re.M) else "2026-11-18T00:00:00.0000000Z",
    "version": scalar("version"),
    "status": "Active",
    "autoUpdate": True,
    "assemblies": [],
}

dst.write_text(json.dumps(meta, indent=2) + "\n")
print(f"wrote {dst} ({meta['name']} {meta['version']} abi {meta['targetAbi']})")
