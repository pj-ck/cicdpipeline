#!/bin/bash

set -e

echo "📦 Zipping source code..."
zip -r source.zip background.js icon.png manifest.json

echo "⬆️  Bumping version..."
# Extract current version from manifest.json
VERSION=$(grep '"version":' manifest.json | cut -d '"' -f 4)
IFS='.' read -r major minor patch <<< "$VERSION"
NEW_VERSION="$major.$minor.$((patch + 1))"

# Update manifest.json with new version
sed -i "s/\"version\": \"$VERSION\"/\"version\": \"$NEW_VERSION\"/" manifest.json
echo "🔄 Updated version: $VERSION → $NEW_VERSION"

echo "🧱 Building .xpi file..."
zip -r ../my-ext.xpi background.js icon.png manifest.json

echo "🚀 Running upload script..."
VERSION="$NEW_VERSION" python3 ../upload_extension.py
