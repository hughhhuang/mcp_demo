import httpx
from dotenv import load_dotenv
import os
from mcp.server.fastmcp import FastMCP
load_dotenv()
mcp = FastMCP("My MCP Server")
weatherapi_key = os.getenv("WEATHERAPI_KEY")

@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)


@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weatherapi.com/v1/current.json?key={weatherapi_key}&q={city}")
        return response.text

if __name__ == "__main__":
    mcp.run()