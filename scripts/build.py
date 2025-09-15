#!/usr/bin/env python3
"""
Build MCPB package for current platform
Automatically detects the platform and creates appropriately named package
"""

import os
import sys
import platform
import subprocess
import shutil
import zipfile
import json
from pathlib import Path

def get_platform_suffix():
    """Determine platform suffix for the package"""
    system = platform.system().lower()
    machine = platform.machine().lower()

    if system == 'darwin':
        # macOS
        if 'arm' in machine or 'aarch64' in machine:
            return 'macos-arm64'
        else:
            return 'macos-intel'
    elif system == 'windows':
        # Windows (not currently supported)
        print("Warning: Windows builds are not currently supported")
        return 'windows-x64'
    elif system == 'linux':
        # Linux (future support)
        if 'arm' in machine or 'aarch64' in machine:
            return 'linux-arm64'
        else:
            return 'linux-x64'
    else:
        return 'unknown'

def clean_vendor_directory():
    """Clean existing vendor directory"""
    vendor_path = Path('smh-huddle-recordings-mcpb/server/vendor')
    if vendor_path.exists():
        print(f"Cleaning existing vendor directory...")
        shutil.rmtree(vendor_path)

def install_dependencies():
    """Install platform-specific dependencies"""
    platform_suffix = get_platform_suffix()
    print(f"Installing dependencies for {platform_suffix}...")

    vendor_path = Path('smh-huddle-recordings-mcpb/server/vendor')
    vendor_path.mkdir(parents=True, exist_ok=True)

    # Install dependencies with pip
    result = subprocess.run([
        sys.executable, '-m', 'pip', 'install',
        '--target', str(vendor_path),
        '--upgrade',
        '-r', 'smh-huddle-recordings-mcpb/server/requirements.txt'
    ], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Warning: pip install had issues: {result.stderr}")
        print("Continuing with build...")
    else:
        print(f"✓ Dependencies installed to {vendor_path}")

def update_manifest_version():
    """Update manifest.json with version from package.json if it exists"""
    try:
        # Try to read version from package.json
        package_json_path = Path('package.json')
        if package_json_path.exists():
            with open(package_json_path, 'r') as f:
                package_data = json.load(f)
                version = package_data.get('version', '1.0.0')

            # Update manifest.json
            manifest_path = Path('smh-huddle-recordings-mcpb/manifest.json')
            with open(manifest_path, 'r') as f:
                manifest_data = json.load(f)

            manifest_data['version'] = version

            with open(manifest_path, 'w') as f:
                json.dump(manifest_data, f, indent=2, ensure_ascii=False)

            print(f"✓ Updated manifest version to {version}")
            return version
    except Exception as e:
        print(f"Note: Could not update version: {e}")
        return '1.0.0'

def create_package():
    """Create MCPB package with platform suffix"""
    platform_suffix = get_platform_suffix()
    package_name = f"smh-huddle-recordings-{platform_suffix}.mcpb"

    print(f"Creating {package_name}...")

    # Remove existing package if it exists
    if os.path.exists(package_name):
        os.remove(package_name)

    # Create zip file
    with zipfile.ZipFile(package_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        # Walk through the source directory
        source_dir = Path('smh-huddle-recordings-mcpb')

        for file_path in source_dir.rglob('*'):
            # Skip directories and unwanted files
            if file_path.is_dir():
                continue

            # Get relative path
            relative_path = file_path.relative_to(source_dir)

            # Skip unwanted files
            path_str = str(relative_path)
            if any(skip in path_str for skip in [
                '__pycache__', '.pyc', '.pyo', '.DS_Store',
                '.git', 'test_server.py', 'build.sh'
            ]):
                continue

            # Add file to zip
            zipf.write(file_path, relative_path)
            print(f"  Added: {relative_path}")

    # Get file size
    file_size = os.path.getsize(package_name)
    size_mb = file_size / (1024 * 1024)

    print(f"✓ Package created: {package_name} ({size_mb:.1f} MB)")
    return package_name

def main():
    """Main build process"""
    print("=" * 60)
    print("SMH Huddle Recordings MCPB Builder")
    print("=" * 60)

    # Change to project root directory
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    os.chdir(project_root)
    print(f"Working directory: {os.getcwd()}")

    # Check if source directory exists
    if not Path('smh-huddle-recordings-mcpb').exists():
        print("Error: smh-huddle-recordings-mcpb directory not found!")
        sys.exit(1)

    try:
        # Clean and install dependencies
        clean_vendor_directory()
        install_dependencies()

        # Update version
        version = update_manifest_version()

        # Create package
        package = create_package()

        print("=" * 60)
        print(f"✅ Build successful!")
        print(f"📦 Package: {package}")
        print(f"🏷️  Version: {version}")
        print(f"🖥️  Platform: {get_platform_suffix()}")
        print("=" * 60)

    except Exception as e:
        print(f"❌ Build failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()