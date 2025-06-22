"""
Offical : https://github.com/langchain-ai/langchain-mcp-adapters/blob/a8d05174fa2abf8bf3abcb40e8e05efd5190b812/langchain_mcp_adapters/client.py#L35
Just Following the docs through out this file.
* Langchain's MultiServerMCPclient : Client for connecting to multiple MCP servers and loading LangChain-compatible tools, prompts and resources from them.
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage
import asyncio
import sys


load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")


async def main():

    # Use the correct SSE endpoint for the weather server
    connections = {
        "math": {
            "command": "python",
            "args": [
                "/Users/rajatsharma/Desktop/MCP-Langchain-Adapter/mcp-server/math_server_stdio.py"
            ],
            "transport": "stdio",
        },
        "weather": {
            "url": "http://127.0.0.1:8000/sse",  # Correct endpoint for SSE
            "transport": "sse",
        },
    }

    try:
        client = MultiServerMCPClient(connections)
        tools = await client.get_tools()

        if not tools:
            print("No tools were loaded. Please check if the servers are running.")
            return

        print(f"Successfully loaded {len(tools)} tools:")
        for tool in tools:
            print(f"  - {tool.name}")

        agent = create_react_agent(
            model=llm,
            tools=tools,
        )

        # Try a math query
        agent_state_math = {"messages": [HumanMessage(content="What is 5 + 3?")]}
        response = await agent.ainvoke(agent_state_math)
        print("\nAgent response (math):")
        print(response)

        # Try a weather query
        agent_state_weather = {
            "messages": [HumanMessage(content="What is the weather in New York?")]
        }
        result_weather = await agent.ainvoke(agent_state_weather)
        print("\nAgent response (weather):")
        print(result_weather)

    except Exception as e:
        print(f"Error connecting to MCP servers: {e}")
        print(
            """
   ========>Troubleshooting:
            1. Make sure you have installed all dependencies: pip install -r requirements.txt
            2. Start the math server: python mcp-server/math_server_stdio.py
            3. Start the weather server: python mcp-server/weather_server_sse.py
            4. Check that the weather server is accessible at http://127.0.0.1:8000/sse
            """
        )
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
