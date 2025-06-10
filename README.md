# MCP сервер для recorder.vless-vpn-v.com

### Установка:

1. Установите uv если он ещё не установлен:
   ```shell
   brew install uv
   ```
2. Добавьте конфигурацию (змените `/ABSOLUTE/PATH/TO/PARENT/FOLDER/` на настоящий путь к папке):
   ```json
    "mcpServers": {
      "SMH Huddle Recordings": {
        "command": "uv",
        "args": [
          "--directory",
          "/ABSOLUTE/PATH/TO/PARENT/FOLDER/mcp_recordings",
          "run",
          "main.py"
        ],
        "env": {
          "API_BASE_URL": "ссылка_на_апи",
          "API_KEY": "ключ_апи"
        }
      },
      ...
    }
   ```
