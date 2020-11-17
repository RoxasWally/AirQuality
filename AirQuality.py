from RetrieveHandlers import RequestHandler, FileHandler


class AirQualityData:
    def __init__(self):
        self.data = {}

    def retrieveData(self):
        pass

    def filterData(self, filterController):
        self.data = filterController.filter(self.data)

    def reverseLocations(self, reverseHandler):
        geolocations = []
        for value in self.data['data']:
            geolocation = (value[27], value[28])
            geolocations.append(geolocation)
        locations = reverseHandler.makeConversions(geolocations)
        final_info = []
        for index, value in enumerate(self.data['data']):
            info = {}
            info["geo_location"] = (value[27], value[28])
            info["aqi"] = value[1]
            info["location"] = locations[index]
            final_info.append(info)
        return final_info


class FileData(AirQualityData):
    def __init__(self, filepath = "purpleair_cache.txt"):
        self.filePath = filepath
        self.retrieveData()

    def retrieveData(self):
        file = FileHandler(self.filePath)
        self.data = file.parseFile()


class PurpleAirData(AirQualityData):
    def __init__(self):
        self.apiUrl = "https://www.purpleair.com/data.json"
        self.retrieveData()

    def retrieveData(self):
        req = RequestHandler(self.apiUrl, "purpleair_cache.txt")
        self.data = req.makeRequest()

