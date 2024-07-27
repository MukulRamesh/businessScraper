from geopy.distance import geodesic

upBound = 90
downBound = -90

rightBound = 180
leftBound = -180

# This dictionary stores distict mapped areas. Mapped area is always a circle, so we store the center and the radius.
mappedDict = {} # id : (coords, radii)


# checks if a point is inside of already mapped area, or is outside the bounding box
def isWithinUnmapped(inputCoords):

	for point in mappedDict:
		coords, radius = mappedDict[point]
		if (geodesic(inputCoords, coords).km < radius):
			return False

	lat, long = inputCoords
	return (lat < upBound and lat > downBound) and (long > leftBound and long < rightBound)


def distanceToNearestEdge(queryCoords):
	lat, long = queryCoords

	smallestDist = min(
		geodesic(queryCoords, (upBound, long)).km,
		geodesic(queryCoords, (downBound, long)).km,
		geodesic(queryCoords, (lat, leftBound)).km,
		geodesic(queryCoords, (lat, rightBound)).km
	)

	for point in mappedDict:
		coords, radius = mappedDict[point]
		distanceFromBoundary = geodesic(queryCoords, coords).km - radius
		smallestDist = min(smallestDist, distanceFromBoundary)

	return smallestDist

# divisor = 21 # heuristic for below function. larger number means more manual checking. smaller number means slower convergence.
# numTrials = 21 # number of iterations (higher number takes longer but is more accurate)
# Current plan is to run this 3 times, and double the divisor and half the numTrials each time.
def findPoleOfInaccessibility(lat, long, divisor, numTrials):
	verticalSeperation = (upBound - downBound) / divisor
	horizontalSeperation = (rightBound - leftBound) / divisor

	maxDistance = -1
	maxCoord = None

	for horiNum in range((divisor + 1)):
		for vertiNum in range((divisor + 1)):
			coords = (downBound + (vertiNum * verticalSeperation), leftBound + (horiNum * horizontalSeperation))
			if isWithinUnmapped(coords):
				maxDistance = max(maxDistance, distanceToNearestEdge(coords))
				maxCoord = coords

	# i need to make it iterate. so...
	# i need to figure out how long/wide the original bounding box is in km, divide by 2 sqrt(2),
	# go that much up/sideways from the maxCoord, and that will be the new bounding box