
[官网链接](https://modelcontextprotocol.io/quickstart/client)

# 创建环境
uv init mcp-client
cd mcp-client

# Create virtual environment
uv venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate

# On Unix or MacOS:
source .venv/bin/activate

# Install required packages
# uv add mcp anthropic python-dotenv
uv add mcp openai python-dotenv

# Remove boilerplate files
# On Windows:
del main.py
# On Unix or MacOS:
rm main.py

# Create our main file
touch client.py

# 执行
uv run client.py path/to/server.py # python server
uv run --active client.py path/to/build/index.js # node server

# 启动client和server服务
uv run --active client.py D:\\306Datawhale\\MCPDemo\\weather\\weather.py
```shell
(mcp-client) PS D:\306Datawhale\MCPDemo\mcp-client> uv run client.py D:\\306Datawhale\\MCPDemo\\weather\\weather.py

已连接到MCP服务，可用的工具列表: ['get_weather', 'get_forecast', 'weather_report', 'get_server_info']

DeepSeek MCP 客户端已经启动!
请输入你的问题，输入'quit'退出。

问题: 
```