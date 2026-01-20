# tools.py
"""
Hardcoded tools for the ReAct agent. Each tool is a function. All tools are registered in the TOOLS dict.
"""

import os
import requests

def get_artworks_by_artist(artist: str) -> list[dict]:
    """Return artworks by a given artist from local hardcoded data. Args: artist (str)."""
    artworks = [
        {"title": "Starry Night", "artist": "Vincent van Gogh", "year": 1889, "medium": "Oil on canvas", "style": "Post-Impressionism"},
        {"title": "Mona Lisa", "artist": "Leonardo da Vinci", "year": 1503, "medium": "Oil on poplar", "style": "Renaissance"},
        {"title": "The Persistence of Memory", "artist": "Salvador Dalí", "year": 1931, "medium": "Oil on canvas", "style": "Surrealism"},
        {"title": "Girl with a Pearl Earring", "artist": "Johannes Vermeer", "year": 1665, "medium": "Oil on canvas", "style": "Baroque"},
        {"title": "The Scream", "artist": "Edvard Munch", "year": 1893, "medium": "Oil, tempera, pastel on cardboard", "style": "Expressionism"},
        {"title": "Water Lilies", "artist": "Claude Monet", "year": 1916, "medium": "Oil on canvas", "style": "Impressionism"},
    ]
    artist_lower = artist.strip().lower()
    return [a for a in artworks if artist_lower in a["artist"].lower()]

def search_books_by_title(title: str) -> list[dict]:
    """Search local hardcoded book data by title substring. Args: title (str)."""
    books = [
        {"title": "The Story of Art", "author": "E.H. Gombrich", "year": 1950, "tags": ["art", "history"]},
        {"title": "Van Gogh: The Life", "author": "Steven Naifeh & Gregory White Smith", "year": 2011, "tags": ["art", "biography", "artist"]},
        {"title": "The Coffee Dictionary", "author": "Maxwell Colonna-Dashwood", "year": 2017, "tags": ["coffee", "reference"]},
        {"title": "The Book of Matcha", "author": "Louise Cheadle & Nick Kilby", "year": 2017, "tags": ["matcha", "tea", "health"]},
        {"title": "Steal Like an Artist", "author": "Austin Kleon", "year": 2012, "tags": ["art", "creativity"]},
        {"title": "The Art of Coffee", "author": "Jason Scheltus", "year": 2017, "tags": ["coffee", "art"]},
        {"title": "Japanese Tea Culture", "author": "Kumiko Nakata", "year": 2015, "tags": ["matcha", "tea", "culture"]},
    ]
    title_lower = title.strip().lower()
    return [b for b in books if title_lower in b["title"].lower()]

def coffee_shop_near(lat: float, lon: float) -> dict:
    """Call a JSON HTTP places API (e.g., Geoapify) to find a nearby coffee shop given lat/lon."""
    api_key = os.environ.get("GEOAPIFY_API_KEY")
    if not api_key:
        return {"error": "Geoapify API key not found in environment."}
    url = f"https://api.geoapify.com/v2/places?categories=cafe.coffee_shop&filter=circle:{lon},{lat},2000&limit=1&apiKey={api_key}"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        features = data.get("features", [])
        if not features:
            return {"error": "No coffee shop found nearby."}
        prop = features[0]["properties"]
        name = prop.get("name", "Unknown")
        address = prop.get("formatted", "Unknown")
        distance_km = prop.get("distance", 0) / 1000 if prop.get("distance") else 0
        return {"name": name, "address": address, "distance_km": distance_km}
    except Exception as e:
        return {"error": f"API request failed: {e}"}

def matcha_trend_data(region: str) -> dict:
    """Call the Open-Meteo weather JSON API and derive a fake 'matcha_trend_score' from weather for a given region string."""
    region_map = {
        "us-west": {"lat": 37.7749, "lon": -122.4194},  # San Francisco
        "japan": {"lat": 35.6895, "lon": 139.6917},     # Tokyo
        "uk": {"lat": 51.5074, "lon": -0.1278},         # London
        "france": {"lat": 48.8566, "lon": 2.3522},      # Paris
    }
    loc = region_map.get(region.lower())
    if not loc:
        return {"error": f"Unknown region: {region}"}
    url = f"https://api.open-meteo.com/v1/forecast?latitude={loc['lat']}&longitude={loc['lon']}&current_weather=true"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        weather = data.get("current_weather", {})
        temp = weather.get("temperature")
        precip = weather.get("precipitation", 0)
        # Fake matcha trend score: higher with mild temp (10-25C) and low precip
        score = 0
        if temp is not None:
            score += max(0, 25 - abs(temp - 17))  # peak at 17C
        score += max(0, 10 - precip)  # penalize high precipitation
        if score > 25:
            trend = "high"
        elif score > 15:
            trend = "medium"
        else:
            trend = "low"
        return {
            "region": region,
            "temperature_c": temp,
            "precipitation_mm": precip,
            "matcha_trend_score": score,
            "trend": trend,
        }
    except Exception as e:
        return {"error": f"API request failed: {e}"}

TOOLS = {
    "get_artworks_by_artist": get_artworks_by_artist,
    "search_books_by_title": search_books_by_title,
    "coffee_shop_near": coffee_shop_near,
    "matcha_trend_data": matcha_trend_data,
}
