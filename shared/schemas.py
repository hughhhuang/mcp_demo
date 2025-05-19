from pydantic import BaseModel

class HotelBookingRequest(BaseModel):
    location: str
    check_in_date: str
    nights: int
    guests: int

class RestaurantBookingRequest(BaseModel):
    cuisine: str
    party_size: int
    date: str
    time: str