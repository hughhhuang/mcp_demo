# Connect to both servers
hotel_client = Client("http://localhost:8001")
restaurant_client = Client("http://localhost:8002")

# User request
user_prompt = input("What would you like to do? ")

if "hotel" in user_prompt.lower():
    print("→ Routing to hotel server")
    result = hotel_client.call_tool("hotel_booking", {
        "location": "New York",
        "check_in_date": "2025-05-20",
        "nights": 2,
        "guests": 1
    })
    print(result)

elif "restaurant" in user_prompt.lower():
    print("→ Routing to restaurant server")
    result = restaurant_client.call_tool("restaurant_booking", {
        "cuisine": "Italian",
        "party_size": 2,
        "date": "2025-05-20",
        "time": "19:00"
    })
    print(result)

else:
    print("Sorry, I can only help with hotel or restaurant bookings.")