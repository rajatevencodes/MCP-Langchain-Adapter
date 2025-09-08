#### MCP Langchain Adapter

A simple project that shows how to connect multiple AI tools (MCP servers) to LangChain and create a smart agent.

## Official Documentation

- [LangChain MCP Adapters](https://github.com/langchain-ai/langchain-mcp-adapters)
- [Client Implementation](https://github.com/langchain-ai/langchain-mcp-adapters/blob/a8d05174fa2abf8bf3abcb40e8e05efd5190b812/langchain_mcp_adapters/client.py#L35)

## What is this?

This project creates an AI agent that can:

- Do math (add, multiply numbers)
- Get weather information
- Use both tools together to answer questions

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up Google API Key

Create a `.env` file:

```
GOOGLE_API_KEY=your_google_api_key_here
```

### 3. Run Everything

```bash
# Start both servers
python start_servers.py

# In another terminal, run the client
python mcp-client/client-langchain-multi_mcp.py
```

## How to Use

Once running, you can ask questions like:

- "What is 5 + 3?"
- "What's the weather in New York?"
- "Calculate 10 \* 4 and tell me the weather in London"

## Project Structure

```
├── mcp-client/          # Main program
├── mcp-server/          # AI tools (math & weather)
├── requirements.txt     # Dependencies
└── README.md           # This file
```

## Manual Setup (if needed)

If the automatic setup doesn't work:

1. **Start weather server:**

   ```bash
   python mcp-server/weather_server_sse.py
   ```

2. **Start math server:**

   ```bash
   python mcp-server/math_server_stdio.py
   ```

3. **Run client:**
   ```bash
   python mcp-client/client-langchain-multi_mcp.py
   ```

## Troubleshooting

**Server not starting?**

- Make sure port 8000 is free
- Check if all dependencies are installed

**Connection errors?**

- Verify your Google API key is correct
- Ensure both servers are running

**Missing dependencies?**

```bash
pip install mcp fastmcp
```

## What You'll See

When it works, you'll see:

```
Successfully loaded 3 tools:
  - add
  - multiply
  - get_weather

Agent response: [Your answer here]
```

## Key Dependencies

- `langchain-mcp-adapters` - Connects to AI tools
- `langgraph` - Creates the smart agent
- `langchain-google-genai` - Uses Google's AI
- `mcp` & `fastmcp` - For the AI tools
