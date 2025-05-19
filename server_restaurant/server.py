from mcp import tool, Server

@tool
def restaurant_booking(cuisine: str, party_size: int, date: str, time: str) -> dict:
    return {
        "confirmation_id": "RESTAURANT-56789",
        "message": f"{cuisine} restaurant booked for {party_size} people on {date} at {time}."
    }

server = Server(tools=[restaurant_booking])

if __name__ == "__main__":
    server.serve(port=8002)