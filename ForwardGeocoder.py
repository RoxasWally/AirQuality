import json
from RetrieveHandlers import RequestHandler, FileHandler

class ForwardGeocoding:
    def __init__(self):
        self.geolocation = None

    def retrieveData(self):
        pass
    
    def getGeolocation(self):
        return self.geolocation
    
    def getSourceInfo(self):
        pass

class NominatimGeocoding(ForwardGeocoding):
    def __init__(self, address):
        self.address = address
        self.apiUrl = "https://nominatim.openstreetmap.org/search/{}?format=json".format(address)
        self.apiUrl = self.apiUrl.replace(" ", "%20")
        self.retrieveData()

    def retrieveData(self):
        req = RequestHandler(self.apiUrl, "forward_cache.txt")
        self.data = req.makeRequest(True)
        self.geolocation = req.getGeolocation(self.data)

    def getSourceInfo(self):
        return self.apiUrl

class FileGeocoding(ForwardGeocoding):
    def __init__(self, filepath="forward_cache.txt"):
        self.filePath = filepath
        self.retrieveData()
    
    def retrieveData(self):
        req = FileHandler(self.filePath)
        self.data = req.parseFile()[0]
        self.geolocation = req.getGeolocation(self.data)
    
    def getSourceInfo(self):
        return self.filePath