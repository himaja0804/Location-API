
from fastapi import FastAPI, Query
import math

app = FastAPI()

restaurants = [
    {"id": 1, "name": "Spicy Hub", "lat": 17.3850, "lon": 78.4867},
    {"id": 2, "name": "Food Palace", "lat": 12.9716, "lon": 77.5946},
    {"id": 3, "name": "Tasty Bites", "lat": 28.7041, "lon": 77.1025}
]

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)

    a = (
        math.sin(d_lat/2)**2 +
        math.cos(math.radians(lat1)) *
        math.cos(math.radians(lat2)) *
        math.sin(d_lon/2)**2
    )

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@app.get("/restaurants/nearby")
def get_nearby_restaurants(
    lat: float = Query(...),
    lon: float = Query(...),
    radius: float = Query(10)
):
    nearby = []

    for r in restaurants:
        distance = calculate_distance(lat, lon, r["lat"], r["lon"])

        if distance <= radius:
            r_copy = r.copy()
            r_copy["distance_km"] = round(distance, 2)
            nearby.append(r_copy)

    return {
        "user_location": {"lat": lat, "lon": lon},
        "radius_km": radius,
        "restaurants_found": len(nearby),
        "restaurants": nearby
    }
