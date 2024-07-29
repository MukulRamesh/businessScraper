import csv

def checkAddressInMercer(str):
	lis = str.split(',')
	if "Mercer" not in lis[1]:
		return False 
	return True


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

with open('output.csv', 'r', newline='', encoding='utf-8') as oldcsvfile:
	with open('filteredOutput.csv', 'w', newline='', encoding='utf-8') as newcsvfile:
		reader = csv.DictReader(oldcsvfile)
		writer = writer = csv.DictWriter(newcsvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL, fieldnames=columns)

		writer.writeheader()

		for row in reader:
			newrow = dict(row)

			if newrow['primaryType'] == "cemetery":
				continue
			
			if not checkAddressInMercer(newrow["formattedAddress"]):
				continue

			for col in columns:
				if (col == 'id'): continue
				newrow[col] = str(newrow[col]).replace('_',' ')

			# print(newrow)

			writer.writerow(newrow)
		
			