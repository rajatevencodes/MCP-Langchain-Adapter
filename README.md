# MCP Langchain Adapter

Official Docs :
https://github.com/langchain-ai/langchain-mcp-adapters
https://github.com/langchain-ai/langchain-mcp-adapters/blob/a8d05174fa2abf8bf3abcb40e8e05efd5190b812/langchain_mcp_adapters/client.py#L35

This project demonstrates how to use LangChain's MultiServerMCPClient to connect to multiple MCP (Model Context Protocol) servers and create an agent that can use tools from both servers.

## Project Structure

```
MCP-Langchain-Adapter/
├── mcp-client/
│   └── client-langchain-multi_mcp.py  # Main client that connects to MCP servers
├── mcp-server/
│   ├── math_server_stdio.py           # Math server using stdio transport
│   └── weather_server_sse.py          # Weather server using SSE transport
├── requirements.txt                   # Python dependencies
└── README.md                         # This file
```

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   # or using uv
   uv pip install -r requirements.txt
   ```

2. **Set up environment variables:**
   Create a `.env` file with your Google API key:
   ```
   GOOGLE_API_KEY=your_google_api_key_here
   ```

## Running the Project

### Option 1: Using the helper script (Recommended)

1. **Start both servers:**

   ```bash
   python start_servers.py
   ```

   This will start both the math server (stdio) and weather server (SSE) automatically.

2. **In another terminal, run the client:**
   ```bash
   python mcp-client/client-langchain-multi_mcp.py
   # or using uv
   uv run mcp-client/client-langchain-multi_mcp.py
   ```

### Option 2: Manual server startup

1. **Start the weather server (SSE):**

   ```bash
   python mcp-server/weather_server_sse.py
   ```

   This will start the weather server on `http://127.0.0.1:8000/`

2. **Start the math server (stdio):**

   ```bash
   python mcp-server/math_server_stdio.py
   ```

   This will start the math server using stdio transport.

3. **Run the client:**
   ```bash
   python mcp-client/client-langchain-multi_mcp.py
   # or using uv
   uv run mcp-client/client-langchain-multi_mcp.py
   ```

## Important Notes

### Path Configuration

The client currently uses a hardcoded absolute path for the math server. If you're running this on a different machine or directory, you'll need to update the path in `mcp-client/client-langchain-multi_mcp.py`:

```python
"args": [
    "/path/to/your/MCP-Langchain-Adapter/mcp-server/math_server_stdio.py"
],
```

### Server Dependencies

The MCP servers require additional dependencies that are not in the main requirements.txt. You may need to install:

```bash
pip install mcp fastmcp
# or
uv pip install mcp fastmcp
```

## Troubleshooting

### Common Issues

1. **404 Error for weather server:**

   - Make sure the weather server is running before starting the client
   - Check that port 8000 is not being used by another application

2. **Connection errors:**

   - Ensure both servers are running
   - Check that all dependencies are installed
   - Verify your Google API key is set correctly
   - Update the hardcoded path in the client if needed

3. **Import errors:**

   - Make sure you've installed all dependencies from `requirements.txt`
   - Install additional server dependencies: `pip install mcp fastmcp`

4. **"'dict' object has no attribute 'ainvoke'" error:**
   - This has been fixed in the current version
   - Make sure you're using the latest code

### Server Status Check

You can check if the weather server is running by visiting:

```
http://127.0.0.1:8000/
```

If it's running, you should see a response (even if it's an error page, it means the server is up).

## How it Works

1. **MCP Servers:** The project includes two MCP servers:

   - **Math Server:** Provides `add` and `multiply` functions using stdio transport
   - **Weather Server:** Provides `get_weather` function using SSE transport

2. **MultiServerMCPClient:** The client connects to both servers and loads their tools into LangChain-compatible format

3. **LangGraph Agent:** Creates a ReAct agent that can use tools from both servers to answer queries

## Example Usage

Once everything is running, the client will:

1. Connect to both MCP servers
2. Load available tools (add, multiply, get_weather)
3. Create a ReAct agent with the loaded tools
4. Process queries like "What is 5 + 3?" or "What is the weather in New York?"

## Dependencies

- `langchain-mcp-adapters`: For connecting to MCP servers
- `langgraph`: For creating the ReAct agent
- `langchain-google-genai`: For the Gemini LLM
- `python-dotenv`: For environment variable management
- `isort`: For import sorting

### Additional Server Dependencies

- `mcp`: Core MCP functionality
- `fastmcp`: FastAPI-based MCP server framework

## Expected Output

When running successfully, you should see:

```
Successfully loaded 3 tools:
  - add
  - multiply
  - get_weather

Agent response (math):
[Agent response with calculation]

Agent response (weather):
[Agent response with weather information]
```
