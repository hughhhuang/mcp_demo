import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("My MCP Server")


@mcp.tool()
def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculate BMI given weight in kg and height in meters"""
    return weight_kg / (height_m**2)


@mcp.tool()
async def fetch_weather(city: str) -> str:
    """Fetch current weather for a city"""
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.weatherapi.com/v1/current.json?key=4f600d1c9e454d10988235730251905&q={city}")
        return response.text

if __name__ == "__main__":
    mcp.run()