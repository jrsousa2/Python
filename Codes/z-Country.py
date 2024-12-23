from geopy.geocoders import Nominatim

def get_country_from_address(address):
    geolocator = Nominatim(user_agent="myGeocoder")
    location = geolocator.geocode(address)

    if location:
        return location.address.split(",")[-1].strip()
    else:
        return "Country not found"

# Example usage
address = "De las artes 23342 # B21 Calle Laolla Villa Fontana"
country = get_country_from_address(address)
print(f"The address is in {country}")
