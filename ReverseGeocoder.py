from RetrieveHandlers import RequestHandler, FileHandler


class ReverseGeocoder:
    def makeConversion(self, geolocations) -> None:
        pass


class NominatimReverse(ReverseGeocoder):
    def __init__(self):
        self.baseURL = "https://nominatim.openstreetmap.org/reverse?lat={}&lon={}&format=json"

    def makeConversions(self, geolocations) -> list:
        " Does the reverse geocoding by taking the name using the api"
        locations = []
        for index, geolocation in enumerate(geolocations):
            url = self.baseURL.format(geolocation[0], geolocation[1])
            cache_name = "cache_reverse{}.txt".format(index)
            handler = RequestHandler(url, cache_name)
            location = handler.makeRequest(True)['display_name']
            locations.append(location)
        return locations


class FileReverse(ReverseGeocoder):
    def __init__(self, files = []):
        self.files = files

    def makeConversions(self, geolocations) -> list:
        ''' Does reverse geocoding by taking the name using filepath'''
        locations = []
        for file in self.files:
            handler = FileHandler(file)
            location = handler.parseFile()['display_name']
            locations.append(location)
        return locations