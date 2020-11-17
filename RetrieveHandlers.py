import json
import sys
import urllib.request 

class RequestHandler:
    def __init__(self, requestUrl, cachePath):
        self.requestUrl = requestUrl
        self.cachePath = cachePath

    def makeRequest(self, includeReferer = False) -> list:
        '''makes a request to collect the json data'''
        try:
            req = urllib.request.Request(self.requestUrl)
            if(includeReferer):
                req.add_header('Referer', 'https://www.ics.uci.edu/~thornton/ics32a/ProjectGuide/Project3/wallyy')
            response = urllib.request.urlopen(req).read()
        except:
            print("FAILED\n{}\nNETWORK".format(self.requestUrl))
            sys.exit(0)
        try:
            data = json.loads(response)
        except:
            print("FAILED\n{}\nFORMAT".format(self.requestUrl))
            sys.exit(0)
        self.writeCache(data)
        return data
    
    def getGeolocation(self, data) -> list:
        '''get the get location from the api'''
        try:
            data = data[0]
            geolocation = (float(data['lat']), float(data['lon']))
        except:
            print("FAILED\n{}\nFORMAT".format(self.requestUrl))
            sys.exit(0)
        return geolocation

    
    def writeCache(self, data) -> None:
        with open(self.cachePath, "w") as file:
            json.dump(data, file)


class FileHandler:
    def __init__(self, filePath):
        self.filePath = filePath

    def parseFile(self) -> None:
        '''opens the files, if not found prints an error and exists the program'''
        try:
            with open(self.filePath, "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            print("FAILED\n{}\nMISSING".format(self.filePath))
            sys.exit(0)
        except TypeError:
            print("FAILED\n{}\nFORMAT".format(self.filePath))
            sys.exit(0)
        return data

    def getGeolocation(self, data) -> list:
        '''get the get location from the file'''
        try:
            geolocation = (float(data['lat']), float(data['lon']))
        except:
            print("FAILED\n{}\nFORMAT".format(self.filePath))
            sys.exit(0)
        return geolocation