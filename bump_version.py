import json

MANIFEST_PATH = "my-extension/manifest.json"

# Load the manifest
with open(MANIFEST_PATH, "r") as f:
    manifest = json.load(f)

# Get current version
current_version = manifest["version"]
major, minor, patch = map(int, current_version.split("."))

# Bump patch version
patch += 1
new_version = f"{major}.{minor}.{patch}"

# Update manifest
manifest["version"] = new_version

# Save the updated manifest
with open(MANIFEST_PATH, "w") as f:
    json.dump(manifest, f, indent=2)

print(f"🔄 Updated version: {current_version} → {new_version}")
