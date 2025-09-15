# SMH Huddle Recordings Desktop Extension

A Claude Desktop Extension (MCPB) for accessing and analyzing SMH huddle (call) recordings. This extension provides a seamless interface to browse recordings and generate summaries from transcripts.

## Features

- **List Recordings**: Browse huddle recordings sorted by date
- **Get Recording Details**: Access full diarized transcripts
- **Smart Summaries**: Generate structured summaries with:
  - What was done
  - Problems encountered
  - Future plans
  - Agreements reached
- **Pagination Support**: Navigate through large recording lists
- **Error Handling**: Robust error handling with retry logic
- **Debug Mode**: Optional debug logging for troubleshooting

## Installation

1. Download the `smh-huddle-recordings.mcpb` file
2. In Claude Desktop, go to Settings → Extensions
3. Click "Install Extension" and select the downloaded file
4. Configure your API credentials when prompted

## Configuration

When installing the extension, you'll be prompted to provide:

| Setting | Description | Required |
|---------|-------------|----------|
| `api_base_url` | Base URL for the SMH recordings API (without trailing slash) | Yes |
| `api_key` | API key for authentication | Yes |
| `debug` | Enable debug logging | No (default: false) |

### Security Note
Your API credentials are stored securely by Claude Desktop and are never exposed to other extensions or sent to third parties.

## Usage

Once installed, the extension provides two main tools:

### List Recordings

```
"Show me the latest huddle recordings"
"List recordings from this week"
"Get the 5 most recent recordings"
```

Parameters:
- `skip`: Number of recordings to skip (pagination)
- `limit`: Number of recordings to return (max: 100)
- `period`: Time period filter (e.g., "today", "week", "month")

### Get Recording Details

```
"Get the details for recording [ID]"
"Show me the transcript for the latest recording"
"Create a summary of recording [ID]"
```

The tool returns:
- Full diarized transcript
- Recording metadata
- Participant information
- Meeting duration

## Building the Extension

### Prerequisites
- Python 3.9 or higher
- pip package manager

### Build Steps

1. Clone this repository
2. Navigate to the extension directory
3. Run the build script:
   ```bash
   ./build.sh
   ```

This will create `smh-huddle-recordings.mcpb` in the parent directory, ready for distribution and installation.

The build script will:
- Install Python dependencies
- Package all required files
- Create the MCPB extension file
- Display installation instructions

## Troubleshooting

### Enable Debug Logging

Set the `debug` configuration option to `true` to see detailed logs:
- API request/response details
- Error stack traces
- Connection attempts

### Common Issues

1. **Connection Timeout**
   - Check your internet connection
   - Verify the API base URL is correct
   - Ensure the API server is accessible

2. **Authentication Errors**
   - Verify your API key is correct
   - Check if the API key has expired
   - Ensure the key has necessary permissions

3. **No Recordings Found**
   - Check if the time period filter is too restrictive
   - Verify you have access to recordings
   - Try without any filters first

## Development

### Project Structure

```
smh-huddle-recordings-mcpb/
├── manifest.json           # Extension metadata and configuration
├── server/
│   ├── main.py            # MCP server implementation
│   └── requirements.txt   # Python dependencies
├── build.sh               # Build script
├── test_server.py         # Test suite
├── LICENSE                # MIT license
└── README.md              # This file
```

### Testing

Run the test suite to validate the extension:
```bash
python test_server.py
```

## Privacy & Security

- **Data Handling**: All API requests are sent directly to your configured SMH server
- **No Data Storage**: No recordings or transcripts are stored locally
- **Credential Security**: API credentials are managed securely by Claude Desktop
- **Network Access**: Only communicates with your configured API endpoint

## License

MIT License - See [LICENSE](LICENSE) file for details

## Support

For issues specific to this extension, please contact your system administrator or the SMH development team.

For Claude Desktop support, visit: https://support.anthropic.com