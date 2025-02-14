import math
import requests
import parseString
from geopy.distance import geodesic
import distance
import csv

key = open("./key.txt", 'r').readline().strip()


def sendReq(coords):
	print("Sending Google API request...")
	lat, long = coords

	headers = {
    'Content-Type': 'application/json',
    'X-Goog-Api-Key': key,
    'X-Goog-FieldMask': """
	places.id,
	places.displayName,
	places.primaryType,
	places.formattedAddress,
	places.location,
	places.nationalPhoneNumber,
	places.currentOpeningHours,
	places.websiteUri,
	places.businessStatus,
	""".replace("\n\t","")
	}

	json_data = {
		# 'includedTypes': [
		#     '*',
		# ],
		'excludedTypes': [
			'library',
			'school',
			'preschool',
			'secondary_school',
			'university',

			'historical_landmark',

			'electric_vehicle_charging_station',
			'parking',
			'rest_stop',

			'art_gallery',
			'hiking_area',
			'park',

			'atm',

			'city_hall',
			'courthouse',
			'embassy',
			'fire_station',
			'local_government_office',
			'police',
			'post_office',

			'medical_lab',

			'campground',

			'church',
			'hindu_temple',
			'mosque',
			'synagogue',

			'cemetery'

			'athletic_field',
			'playground',

			'airport',
			'bus_station',
			'bus_stop',

			'ferry_terminal',
			'heliport',
			'light_rail_station',
			'park_and_ride',
			'subway_station',
			'taxi_stand',
			'train_station',
			'transit_depot',
			'transit_station',
			'truck_stop',
		],
		'maxResultCount': 20,
		'locationRestriction': {
			'circle': {
				'center': {
					'latitude': lat,
					'longitude': long,
				},
				'radius': 9001.0,
			},
		},
		'rankPreference': 'DISTANCE',
	}


	res = requests.post('https://places.googleapis.com/v1/places:searchNearby', headers=headers, json=json_data)
	try:
		return res.json()
	except:
		print(res.text)






# print(json.dumps(sendReq(37.7937, -122.3965), indent=4))

distance.upBound = 41.5055
distance.downBound = 41.0649

distance.rightBound = -79.9832
distance.leftBound = -80.5449



# contains output
# id : (place data in json form)
outputDictionary = {}
maxReqs = 1000
totalAreaMapped = 0

def runRound(div, trials):
	roundAreaMapped = 0 # in km^2
	coord = distance.findPoleOfInaccessibility(divisor=div,numTrials=trials)

	numReq = 1
	while coord != None:
		print(numReq, ": Sending request for:", coord)
		placesData = sendReq(coord)["places"]

		numReq += 1
		if numReq > maxReqs:
			break

		numPlaces = len(placesData) # should be 20

		if (numPlaces < 20):
			print("WARN: Got fewer than 20 places from API call.")

		numAdded = 0
		for place in placesData:
			placeID = place["id"]

			if placeID not in outputDictionary:
				outputDictionary[placeID] = place
				numAdded += 1
			else:
				print("Found an overlap.")
		
		print("Found", numAdded, "places.")

		farthestPlace = placesData[-1]
		farPlaceCoord = (farthestPlace["location"]["latitude"], farthestPlace["location"]["longitude"])

		# The distance from the request coord to the farthest place is the radius of the mapped/"known" area
		radiusOfMapped = geodesic(farPlaceCoord, coord).km

		print("Mapped a circle of radius", radiusOfMapped, "kilometers.")
		roundAreaMapped += (math.pi * (radiusOfMapped ** 2))
		print("Total area mapped:", (roundAreaMapped + totalAreaMapped), "km^2")

		distance.mappedDict[farthestPlace["id"]] = (coord, radiusOfMapped)

		coord = distance.findPoleOfInaccessibility(divisor=div,numTrials=trials)

	print("Round over.")
	return roundAreaMapped

def writeCSV():
	columns = """
	id,
	displayName,
	primaryType,
	formattedAddress,
	location[latitude],
	location[longitude],
	nationalPhoneNumber,
	currentOpeningHours,
	websiteURL,
	""".replace("\n","").replace("\t","").split(",")

	with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
		writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(columns)

		for placeid in outputDictionary:
			place = outputDictionary[placeid]

			businessStatus = place.get("businessStatus")


			# we only want the operational ones
			if (businessStatus != None and businessStatus == "OPERATIONAL"):
				newRow = []
				newRow.append(place.get("id"))
				newRow.append(place.get("displayName").get("text"))
				newRow.append(place.get("primaryType"))
				newRow.append(place.get("formattedAddress"))
				newRow.append(place.get("location").get("latitude"))
				newRow.append(place.get("location").get("longitude"))
				newRow.append(place.get("nationalPhoneNumber"))
				newRow.append(parseString.parseOpeningHours(place.get("currentOpeningHours")))
				newRow.append(place.get("websiteUri"))
				# print(newRow)

				try:
					writer.writerow(newRow)
				except:

					try:
						print("Failed on this row:", newRow)
					except:
						print("Couldn't print failed row!")

runRound(10,2)
runRound(20,2)
runRound(25,5)
writeCSV()



