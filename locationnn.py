import geocoder

g=geocoder.ip('me')
print("lattitude, longitude = ",g.latlng)