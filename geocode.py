import pandas as pd
from geopy.geocoders import OpenCage
import time

# 1. Load the CSV file
df = pd.read_csv("locations.csv")

# 2. Set up the OpenCage API
API_KEY = "54639f67db5248bf922a9ad77e60eb31"  # Get this from https://opencagedata.com/
geolocator = OpenCage(API_KEY)

# 3. Function to get location details
def get_location(lat, lon):
    try:
        location = geolocator.reverse((lat, lon), exactly_one=True)
        if location:
            city = ""
            country = ""
            for comp in location.raw['components']:
                if 'city' in location.raw['components']:
                    city = location.raw['components']['city']
                elif 'town' in location.raw['components']:
                    city = location.raw['components']['town']
                elif 'village' in location.raw['components']:
                    city = location.raw['components']['village']
                country = location.raw['components']['country']
            return f"{city}, {country}"
        else:
            return "Not Found"
    except:
        return "Error"

# 4. Apply function to each row
df["City, Country"] = df.apply(lambda row: get_location(row["latitude"], row["longitude"]), axis=1)

# 5. Save to new CSV file
df.to_csv("locations_with_city.csv", index=False)

print("Process completed! Check 'locations_with_city.csv'")
