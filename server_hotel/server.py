from mcp import tool, Server

@tool
def hotel_booking(location: str, check_in_date: str, nights: int, guests: int) -> dict:
    return {
        "confirmation_id": "HOTEL-12345",
        "message": f"Hotel booked in {location} for {guests} guests from {check_in_date} for {nights} nights."
    }

server = Server(tools=[hotel_booking])

if __name__ == "__main__":
    server.serve(port=8001)