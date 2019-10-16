import geocoder

g = geocoder.google([29.9287839, -90.08421849999999], method='reverse')
print(g.city)
# Create your tests here.
