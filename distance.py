from geopy.distance import geodesic
import math


#Below values should be set: Default is Mercer County, PA
upBound = 41.5055
downBound = 41.0649

rightBound = -79.9832
leftBound = -80.5449


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
def findPoleOfInaccessibility(divisor, numTrials):
	curUpBound = upBound
	curDownBound = downBound

	curRightBound = rightBound
	curLeftBound = leftBound

	for _ in range(numTrials):

		verticalSeperation = (curUpBound - curDownBound) / divisor
		horizontalSeperation = (curRightBound - curLeftBound) / divisor

		maxDistance = -1
		maxCoord = None

		for horiNum in range((divisor + 1)):
			for vertiNum in range((divisor + 1)):
				coords = (curDownBound + (vertiNum * verticalSeperation), curLeftBound + (horiNum * horizontalSeperation))
				if isWithinUnmapped(coords) and (distanceToNearestEdge(coords) > maxDistance):
						maxDistance = distanceToNearestEdge(coords)
						maxCoord = coords

		if (maxDistance == -1):
			# every sample was outside of the bounds
			return None

		assert(maxCoord != None)

		# This is imprecise, but I dont think it matters: a potentially more effective solution is to
		# calculate the vertical and horizontal *distance in km*, and do math with that.
		newVertical = (curUpBound - curDownBound) / (2 * math.sqrt(2))
		newHorizontal = (curRightBound - curLeftBound) / (2 * math.sqrt(2)) # we divide by 2sqrt(2) because we double the distance in the next step

		newLat, newLong = maxCoord

		curUpBound = newLat + newVertical
		curDownBound = newLat - newVertical

		curRightBound = newLong + newHorizontal
		curLeftBound = newLong - newHorizontal


	return maxCoord


