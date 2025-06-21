import asyncio
import os

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_core.messages import HumanMessage

if os.getenv("GOOGLE_API_KEY") is None:
    raise ValueError("GOOGLE_API_KEY is not set")


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-001")


# Stdio server are used for local development and testing.
server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=[
        "/Users/rajatsharma/Desktop/MCP-Langchain-Adapter/mcp-server/math_server_stdio.py"
    ],
)


async def main():
    print("Hello from mcp-langchain-adapter!")

    # Create a client that acts as a proxy for our MCP host (Langgraph create_react_agent).
    # The 'async with' statement automatically opens and closes the connection to the MCP server.
    async with stdio_client(server_params) as (read, write):
        # Every client connects to a server via a session and provides the session with the (read, write) streams.
        # This ClientSession handles communication between the MCP server and the client.
        async with ClientSession(read_stream=read, write_stream=write) as session:
            # Refer this : https://www.notion.so/MCP-Model-Context-Protocol-20c195c5bfdb80388491f0dd194af34f?source=copy_link#218195c5bfdb803ca787f83ed3fd4564
            await session.initialize()
            # print("Session initialized")
            # List all the available tools MCP Server offers.
            tools = await session.list_tools()
            # print("Available tools:", tools)

            # create_react_agent requires tool to be in the form of a dictionary.
            # The load_mcp_tools function converts the tools list into a dictionary format.
            tools_dict = await load_mcp_tools(session)
            # print("Tools loaded:", tools_dict)
            agent = create_react_agent(
                model=llm,
                tools=tools_dict,
            )

            """
            'ainvoke' is being used in docs.
                'ainvoke' is used for asynchronous invocation of the agent.
                'invoke' is used for synchronous invocation of the agent.
            Both methods return the response from the agent.
            """
            print("\n\n\n\n")
            # ! Make sure to run the MCP server - math_server(stdio) before running this client code.
            agent_response = await agent.ainvoke(
                {"messages": HumanMessage(content="What is 2 + 2? Use the add tool.")}
            )
            for messages in agent_response["messages"]:
                print(messages)

            print("\n\n\n\n")

            agent_response2 = await agent.ainvoke(
                {
                    "messages": HumanMessage(
                        content="What is 2 * 2? Use the multiply tool."
                    )
                }
            )
            for messages in agent_response2["messages"]:
                print(messages)


if __name__ == "__main__":
    asyncio.run(main())
