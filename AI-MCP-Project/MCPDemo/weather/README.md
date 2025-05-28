# 启动MCP程序
## 在windows中有的同学使用了miniconde建议先退出conda环境
conda deactivate

当然推出uv/venv环境用deactivate命令

```java
(py310) (weather) PS D:\306Datawhale\MCPDemo\weather>  conda deactivate
(base) (weather) PS D:\306Datawhale\MCPDemo\weather> conda deactivate
(weather) PS D:\306Datawhale\MCPDemo\weather> python --version
Python 3.12.8
(weather) PS D:\306Datawhale\MCPDemo\weather> deactivate
PS D:\306Datawhale\MCPDemo\weather> deactivate
```

## 官方文档：
https://modelcontextprotocol.io/quickstart/server
## 安装uv环境 以windows为例子
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

## 1. 激活虚拟环境

# 创建weather项目
uv init weather


# 在名为 “weather” 的文件夹中创建一个虚拟环境并激活它
cd weather
## 创建环境
uv venv weather_env
## 激活环境
.\weather_env\Scripts\activate

# Install dependencies to activate env
uv add mcp[cli] httpx --active

# Create our server file
new-item weather.py

## 2. 安装依赖


## 3. 启动MCP程序
mcp dev weather.py

uv run --active D:\\306Datawhale\\MCPDemo\\weather\\weather.py

## 4. 其他

如有疑问或项目结构不同，请补充 README 或联系开发者。
