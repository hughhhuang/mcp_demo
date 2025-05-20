from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "mistral"

async def ask_ollama_for_tool_and_args(user_input: str) -> dict:
    prompt = f"""
You are a function calling router agent. You have access to two tools:

1. calculate_bmi(weight_kg: float, height_m: float): calculates BMI.
2. fetch_weather(city: str): fetches the current weather for a city.

Given the user input, decide which tool to call and provide a JSON object like:
{{
  "tool": "tool_name",
  "args": {{...parameters...}}
}}

Respond with only a valid JSON object.

User input: "{user_input}"
"""

    payload = {
        "model": OLLAMA_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    res = requests.post(OLLAMA_URL, json=payload)
    res.raise_for_status()
    response_text = res.json()["message"]["content"]
    print("[DEBUG] Raw response from Ollama:")
    print(response_text)
    try:
        plan = eval(response_text)  # Replace with json.loads if Ollama reliably produces valid JSON
        print("[INFO] Parsed plan:", plan)
        return plan
    except Exception as e:
        print("Failed to parse Ollama response:", response_text)
        return {}

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["example_server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write
        ) as session:
            # Initialize the connection
            await session.initialize()

            while True:
                user_input = input("\nWhat would you like to do? (type 'exit' to quit)\n> ")
                if user_input.lower() in ["exit", "quit"]:
                    break

                plan = await ask_ollama_for_tool_and_args(user_input)

                tool = plan.get("tool")
                args = plan.get("args", {})

                # Dynamically fetch available tools from the MCP server
                tool_result = await session.list_tools()
                available_tools = tool_result.tools
                available_tool_names = [t.name for t in available_tools]
                print(f"[INFO] Available tools from server: {available_tool_names}")

                if tool not in available_tool_names:
                    print(f"[WARN] Tool '{tool}' not found in server registry.")
                    continue

                print(f"[INFO] Calling MCP tool: {tool} with args: {args}")
                result = await session.call_tool(tool, args)
                print("[RESULT]", result.content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
