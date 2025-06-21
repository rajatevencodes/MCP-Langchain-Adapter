### Note: The key advantage of the mcp-langchain-adapter is that the App (Langgraph agent), with the help of the MCP client, makes a request (steps 3 and 4) to the MCP Server, and the actual execution of the tool happens on the MCP Server, which is decoupled from our Langgraph application.

### This way, our Langgraph application is only responsible for orchestration, while the MCP Server is responsible for executing the tools.

Refer to this: https://www.notion.so/MCP-Model-Context-Protocol-20c195c5bfdb80388491f0dd194af34f?source=copy_link#218195c5bfdb803ca787f83ed3fd4564

Explained here: https://www.udemy.com/course/model-context-protocol/learn/lecture/49619937#overview

```json
[
  // 1. User Query
  {
    "content": "What is 2 + 2? Use the add tool.",
    "additional_kwargs": {},
    "response_metadata": {},
    "id": "6b99ac67-0d12-4478-a5e7-1abd9cb82499"
  },
  // 2. Respond with Tool Call
  {
    "content": "",
    "additional_kwargs": {
      "function_call": {
        "name": "add",
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
    "id": "run--879c2717-9215-4113-b54e-8c571f805599-0",
    "tool_calls": [
      {
        "name": "add",
        "args": {
          "a": 2.0,
          "b": 2.0
        },
        "id": "4ddf10d2-830f-4768-b8cc-88ba6f3a1379",
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
  // 3. Sends Tool Call
  // 4. MCP Responds with tool response
  // 5. Sends tool Response
  {
    "content": "11",
    "name": "add",
    "id": "b5d5eb6b-30fc-4c90-9499-b2be45f769f7",
    "tool_call_id": "4ddf10d2-830f-4768-b8cc-88ba6f3a1379"
  },
  // 6. Sends the final response
  {
    "content": "2 + 2 is 11.",
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
    "id": "run--86a5ccdd-3ed4-4a03-a0f6-2c7a2f0840d0-0",
    "usage_metadata": {
      "input_tokens": 43,
      "output_tokens": 10,
      "total_tokens": 53,
      "input_token_details": {
        "cache_read": 0
      }
    }
  }
]
```
