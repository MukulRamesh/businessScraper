from geopy.distance import geodesic

center = {
	37.7937,
	-122.3965,
}

location1 = {
	37.793832099999996,
	-122.3966844
}

location2 = {
	37.79379110000001,
	-122.3967923
}

loc3 = {
	37.7938153,
	-122.39675349999999
},

print(geodesic(center, location1).km)

print(geodesic(center, loc3).km)

print(geodesic(center, location2).km)
