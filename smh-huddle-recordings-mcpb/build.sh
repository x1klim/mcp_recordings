#!/bin/bash

# Build script for SMH Huddle Recordings MCPB Extension

echo "Building SMH Huddle Recordings Desktop Extension..."

# Check if we're in the right directory
if [ ! -f "manifest.json" ]; then
    echo "Error: manifest.json not found. Run this script from the extension root directory."
    exit 1
fi

# Clean up any previous builds
rm -f ../smh-huddle-recordings.mcpb

# Install Python dependencies into the vendor directory
echo "Installing Python dependencies..."
pip3 install --target server/vendor --upgrade -r server/requirements.txt --quiet 2>/dev/null || echo "Note: Dependencies installation failed. Make sure pip3 is installed."

# Create the MCPB package (files must be at root level of ZIP)
echo "Creating MCPB package..."
# Important: We must be IN the directory when creating the ZIP
# so that manifest.json is at the root level of the archive
zip -r ../smh-huddle-recordings.mcpb . \
    -x "*.git*" \
    -x "*__pycache__*" \
    -x "*.pyc" \
    -x ".DS_Store" \
    -x "build.sh" \
    -x "test_server.py" \
    -x "*.mcpb" \
    -q

if [ $? -eq 0 ]; then
    echo "✓ Successfully created smh-huddle-recordings.mcpb"
    echo "  File size: $(ls -lh ../smh-huddle-recordings.mcpb | awk '{print $5}')"
    echo ""
    echo "Installation instructions:"
    echo "1. Open Claude Desktop"
    echo "2. Go to Settings → Extensions"
    echo "3. Click 'Install Extension'"
    echo "4. Select the smh-huddle-recordings.mcpb file"
    echo "5. Configure your API credentials when prompted"
else
    echo "Error: Failed to create MCPB package"
    exit 1
fi