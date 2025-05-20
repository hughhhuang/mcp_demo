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

    try:
        return eval(response_text)  # Replace with json.loads if Ollama reliably produces valid JSON
    except Exception as e:
        print("Failed to parse Ollama response:", response_text)
        return {}

# Create server parameters for stdio connection
server_params = StdioServerParameters(
    command="python",  # Executable
    args=["example_server.py"],  # Optional command line arguments
    env=None,  # Optional environment variables
)

# Optional: create a sampling callback
async def handle_sampling_message(
    message: types.CreateMessageRequestParams,
) -> types.CreateMessageResult:
    return types.CreateMessageResult(
        role="assistant",
        content=types.TextContent(
            type="text",
            text="Hello, world! from model",
        ),
        model="gpt-3.5-turbo",
        stopReason="endTurn",
    )


async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(
            read, write, sampling_callback=handle_sampling_message
        ) as session:
            # Initialize the connection
            await session.initialize()

            user_input = input("What would you like to do? ")
            plan = await ask_ollama_for_tool_and_args(user_input)

            tool = plan.get("tool")
            args = plan.get("args", {})

            if tool not in ["calculate_bmi", "fetch_weather"]:
                print("Sorry, could not determine a valid tool.")
                return

            result = await session.call_tool(tool, args)
            print("\nResult:", result.content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(run())
