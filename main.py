import requests
import json


key = "AIzaSyDaN8bquMsna8j_yaD2J2Z9YM_fiBvtYiU"

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
    'maxResultCount': 10,
    'locationRestriction': {
        'circle': {
            'center': {
                'latitude': 37.7937,
                'longitude': -122.3965,
            },
            'radius': 1000.0,
        },
    },
    'rankPreference': 'DISTANCE',
}

print("Sending Google API request...")
res = requests.post('https://places.googleapis.com/v1/places:searchNearby', headers=headers, json=json_data)

try:
	print(json.dumps(res.json(), indent=4))
except:
	print(res.text)