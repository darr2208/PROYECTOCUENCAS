from geopy.geocoders import Nominatim

def obtener_coordenadas(lugar):
    try:
        geolocator = Nominatim(user_agent="cuenca-app")
        location = geolocator.geocode(lugar)
        if location:
            return [location.latitude, location.longitude]
        else:
            return None
    except:
        return None
