import unicodedata

# takes in a "currentOpeningHours" obj
def parseOpeningHours(obj) -> str:
    if (obj == None):
        return None

    descs = obj["weekdayDescriptions"]
    output = ""
    for desc in descs:
        assert(type(desc) == str)
        newStr = desc.replace("\u202f", " ").replace("\u2009", " ").replace("\u2013", "-")
        output += newStr + "|"

    return output