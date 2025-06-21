### Note: The key advantage of the mcp-langchain-adapter is that the App (Langgraph agent), with the help of the MCP client, makes a request (steps 3 and 4) to the MCP Server, and the actual execution of the tool happens on the MCP Server, which is decoupled from our Langgraph application.

### This way, our Langgraph application is only responsible for orchestration, while the MCP Server is responsible for executing the tools.

Refer to this: https://www.notion.so/MCP-Model-Context-Protocol-20c195c5bfdb80388491f0dd194af34f?source=copy_link#218195c5bfdb803ca787f83ed3fd4564

Explained here: https://www.udemy.com/course/model-context-protocol/learn/lecture/49619937#overview

```json
[
  // 1. User Query
  {
    "content": "What is 2 * 2? Use the multiply tool.",
    "additional_kwargs": {},
    "response_metadata": {},
    "id": "38143886-71bf-4e58-88bb-5ec1159477a4"
  },
  // 2. LLM - Respond with Tool call
  {
    "content": "",
    "additional_kwargs": {
      "function_call": {
        "name": "multiply",
        "arguments": "{\"a\": 2.0, \"b\": 2.0}"
      }
    },
    "response_metadata": {
      "prompt_feedback": {
        "block_reason": 0,
        "safety_ratings": []
      },
      "finish_reason": "STOP",
      "model_name": "gemini-2.0-flash-001",
      "safety_ratings": []
    },
    "id": "run--b2a2674f-9c4b-4eca-912b-b3bb1283978f-0",
    "tool_calls": [
      {
        "name": "multiply",
        "args": {
          "a": 2.0,
          "b": 2.0
        },
        "id": "4e3e4aae-960b-45d1-a348-ce15a6625937",
        "type": "tool_call"
      }
    ],
    "usage_metadata": {
      "input_tokens": 35,
      "output_tokens": 5,
      "total_tokens": 40,
      "input_token_details": {
        "cache_read": 0
      }
    }
  },
  // 3. Client sends tool call
  // 4. Responds with tool response
  // 5. App sends the tool response
  {
    "content": "11",
    "name": "multiply",
    "id": "dc6df358-2d73-4859-9307-33fed09f06db",
    "tool_call_id": "4e3e4aae-960b-45d1-a348-ce15a6625937"
  },
  // 6. Responds with final response
  {
    "content": "I'm sorry, there seems to be an issue with the tool. The result of 2 * 2 is 11, which is incorrect. Would you like me to try again?",
    "additional_kwargs": {},
    "response_metadata": {
      "prompt_feedback": {
        "block_reason": 0,
        "safety_ratings": []
      },
      "finish_reason": "STOP",
      "model_name": "gemini-2.0-flash-001",
      "safety_ratings": []
    },
    "id": "run--4797100b-7b89-4694-9f11-e9a1b7ab4188-0",
    "usage_metadata": {
      "input_tokens": 43,
      "output_tokens": 41,
      "total_tokens": 84,
      "input_token_details": {
        "cache_read": 0
      }
    }
  }
]
```
