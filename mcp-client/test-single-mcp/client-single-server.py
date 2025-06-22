"""
Simple client that connects to a single MCP server
"""

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import HumanMessage, AIMessage
import asyncio
import sys


load_dotenv()


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")


async def test_math_server():
    """Test connection to math server only"""
    print("Testing math server connection...")

    connections = {
        "math": {
            "command": "python",
            "args": [
                "/Users/rajatsharma/Desktop/MCP-Langchain-Adapter/mcp-server/math_server_stdio.py"
            ],
            "transport": "stdio",
        },
    }

    try:
        client = MultiServerMCPClient(connections)
        tools = await client.get_tools()

        if not tools:
            print("No tools were loaded from math server.")
            return

        print(f"Successfully loaded {len(tools)} tools from math server:")
        for tool in tools:
            print(f"  - {tool.name}")

        # Create the agent
        agent = create_react_agent(
            model=llm,
            tools=tools,
        )

        # Create the agent state
        agent_state = {"messages": [HumanMessage(content="What is 5 + 3?")]}

        # Run the agent
        result = agent.invoke(agent_state)
        print("\nAgent response:")
        print(result)

    except Exception as e:
        print(f"Error connecting to math server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure the math server is running")
        print("2. Check that all dependencies are installed")
        sys.exit(1)


async def test_weather_server():
    """Test connection to weather server only"""
    print("Testing weather server connection...")

    connections = {
        "weather": {
            "url": "http://127.0.0.1:8000/",
            "transport": "sse",
        },
    }

    try:
        client = MultiServerMCPClient(connections)
        tools = await client.get_tools()

        if not tools:
            print("No tools were loaded from weather server.")
            return

        print(f"Successfully loaded {len(tools)} tools from weather server:")
        for tool in tools:
            print(f"  - {tool.name}")

        # Create the agent
        agent = create_react_agent(
            model=llm,
            tools=tools,
        )

        # Create the agent state
        agent_state = {
            "messages": [HumanMessage(content="What is the weather in New York?")]
        }

        # Run the agent
        result = agent.invoke(agent_state)
        print("\nAgent response:")
        print(result)

    except Exception as e:
        print(f"Error connecting to weather server: {e}")
        print("\nTroubleshooting:")
        print("1. Make sure the weather server is running")
        print("2. Check that the server is accessible at http://127.0.0.1:8000/")
        sys.exit(1)


async def main():
    print("Hello from single-server MCP client!")
    print()

    # Test math server first
    await test_math_server()
    print("\n" + "=" * 50 + "\n")

    # Test weather server
    await test_weather_server()


if __name__ == "__main__":
    asyncio.run(main())
