import asyncio
import os
import sys
import json
from typing import Optional
from contextlib import AsyncExitStack
from dotenv import load_dotenv

import openai

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

load_dotenv()

class MCPClient:
  def __init__(self):
    self.session: Optional[ClientSession] = None
    self.exit_stack = AsyncExitStack()

  async def connect_to_server(self, server_script_path: str):
    is_python = server_script_path.endswith('.py')
    is_js = server_script_path.endswith('.js')
    if not (is_python or is_js):
      raise ValueError("Server script must be a .py or .js file")

    command = "python" if is_python else "node"
    server_params = StdioServerParameters(
      command=command,
      args=[server_script_path],
      env=None
    )

    stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
    self.stdio, self.write = stdio_transport
    self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))
    await self.session.initialize()

    response = await self.session.list_tools()
    tools = response.tools
    print("\nConnected to server with tools:", [tool.name for tool in tools])

  async def process_query(self, query: str) -> str:
    messages = [{"role": "user", "content": query}] # 每轮调用 process_query(query) 都是从空白上下文开始，不会保留历史记忆

    # 获取可用工具
    response = await self.session.list_tools()
    available_tools = [{
      "type": "function",
      "function": {
          "name": tool.name,
          "description": tool.description,
          "parameters": tool.inputSchema
      }
    } for tool in response.tools]

    # 初始化 DeepSeek Client
    client = openai.OpenAI(
      api_key=os.getenv("OPENAI_API_KEY"),
      base_url=os.getenv("OPENAI_API_BASE")
    )

    final_text = []

    # 首轮交互
    chat_response = client.chat.completions.create(
      model=os.getenv("OPENAI_API_MODEL"),
      messages=messages,
      tools=available_tools,
      tool_choice="auto"
    )

    for choice in chat_response.choices:
        message = choice.message

        # 若直接生成文本
        if message.content:
            final_text.append(message.content)

        # 若调用工具
        elif message.tool_calls:
            tool_call_messages = []

            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args_raw = tool_call.function.arguments

                try:
                    tool_args = json.loads(tool_args_raw)
                except Exception as e:
                    return f"工具参数解析失败: {e}"

                result = await self.session.call_tool(tool_name, tool_args)

                # 构造 tool message
                tool_call_messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result.content)
                })

            # 添加 assistant tool call 信息
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": message.tool_calls
            })

            # 添加 tool 响应
            messages.extend(tool_call_messages)

            # 再次发送给模型
            next_response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
            )

            for next_choice in next_response.choices:
                if next_choice.message.content is not None:
                    final_text.append(next_choice.message.content)

    return "\n".join(final_text)

  async def chat_loop(self):
      print("\nMCP Client Started!")
      print("Type your queries or 'quit' to exit.")
      while True:
          try:
              query = input("\nQuery: ").strip()
              if query.lower() == 'quit':
                  break
              response = await self.process_query(query)
              print("\n" + response)
          except Exception as e:
              print(f"\nError: {str(e)}")

  async def cleanup(self):
      await self.exit_stack.aclose()


async def main():
  if len(sys.argv) < 2:
      print("Usage: python client.py <path_to_server_script>")
      sys.exit(1)

  client = MCPClient()
  try:
      await client.connect_to_server(sys.argv[1])
      await client.chat_loop()
  finally:
      await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
