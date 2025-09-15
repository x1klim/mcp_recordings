# SMH Huddle Recordings - Claude Desktop Extension

A powerful Claude Desktop Extension for accessing and analyzing SMH huddle (call) recordings.

## 📥 Installation

### Step 1: Download for Your Platform

Download the latest release from the [**Releases page**](https://github.com/x1klim/mcp_recordings/releases/latest).

Choose the right version for your system:
- 🖥️ **macOS Intel**: `smh-huddle-recordings-macos-intel.mcpb`
- 🍎 **macOS Apple Silicon (M1/M2/M3)**: `smh-huddle-recordings-macos-arm64.mcpb`
- 🪟 **Windows**: `smh-huddle-recordings-windows-x64.mcpb`

#### How to Check Your Mac Type
1. Click the Apple menu → About This Mac
2. Look for "Chip" or "Processor":
   - **Intel processor**: Download the Intel version
   - **Apple M1/M2/M3**: Download the ARM64 version

### Step 2: Install in Claude Desktop

<img src="/install_guide.png" width="100%">

1. Open Claude Desktop
2. Go to **Settings** → **Extensions**
3. Click **"Install Extension"**
4. Select the downloaded `.mcpb` file
5. Enter your API credentials when prompted:
   - **API Base URL**: Your SMH API endpoint
   - **API Key**: Your authentication key

## ✨ Features

- 📋 **List Recordings**: Browse all huddle recordings with summaries
- 🔍 **Get Recording Details**: Access full transcripts with speaker diarization
- 📊 **Smart Summaries**: Generate structured meeting summaries
- 🔄 **Pagination**: Navigate through large recording lists
- 🛡️ **Secure**: API credentials stored securely by Claude Desktop

## 🚀 Usage

Once installed, you can ask Claude:

- "Show me the latest huddle recordings"
- "Get the recording from yesterday's meeting"
- "Create a summary of recording [ID]"
- "List recordings from this week"

## 🔧 For Developers

### Building from Source

1. Clone the repository:
   ```bash
   git clone https://github.com/x1klim/mcp_recordings.git
   cd mcp_recordings
   ```

2. Build for your platform:
   ```bash
   python scripts/build.py
   ```

3. The MCPB file will be created with your platform suffix.

### Creating a Release

Releases are automatically created when you push a version tag:

```bash
# Patch release (1.0.0 → 1.0.1)
npm run release

# Minor release (1.0.0 → 1.1.0)
npm run release:minor

# Major release (1.0.0 → 2.0.0)
npm run release:major
```

GitHub Actions will automatically build for all platforms and create a release.

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🤝 Support

- For extension issues: [Create an issue](https://github.com/x1klim/mcp_recordings/issues)
- For Claude Desktop support: [Anthropic Support](https://support.anthropic.com)

## 🔐 Privacy

- All API requests go directly to your configured SMH server
- No data is stored locally or sent to third parties
- Credentials are managed securely by Claude Desktop