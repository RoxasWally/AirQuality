"""Yousef Wally ID# 32179033
    ICS32A
    Project 3, Try not to breathe"""

from ForwardGeocoder import NominatimGeocoding, FileGeocoding
from AirQuality import FileData, PurpleAirData
from ReverseGeocoder import NominatimReverse, FileReverse
from FilterData import FilterData

class Controller:

    def __init__(self):
        self.collect_inputs()
        if(self.info['center'].startswith("NOMINATIM")):
            self.info['center'] = self.info['center'][9:].strip()
            self.centerLocation = NominatimGeocoding(self.info['center'])
        else:
            self.info['center'] = self.info['center'][4:].strip()
            self.centerLocation = FileGeocoding(self.info['center'])
        if(self.info['aqi'] == "PURPLEAIR"):
            data = PurpleAirData()
        else:
            self.info['aqi'] = self.info['aqi'][4:].strip()
            data = FileData(self.info['aqi'])
        self.create_filter()
        data.filterData(self.filter)
        if(self.info['reverse'] == "NOMINATIM"):
            reverser = NominatimReverse()
        else:
            self.info['reverse'] = self.info['reverse'][5:].strip()
            files = self.info['reverse'].split(" ")
            reverser = FileReverse(files)
        data = data.reverseLocations(reverser)
        self.print_locations(data, self.centerLocation.getGeolocation())


    def create_filter(self) -> None:
        """ Creates a filter to collect information"""
        self.filter = FilterData(self.info, self.centerLocation.getGeolocation())


    def collect_inputs(self) -> None:
        """ Collect user's request"""
        self.info = {}
        self.info["center"] = input("CENTER ")
        self.info["range"] = int(input("RANGE "))
        self.info["threshold"] = int(input("THRESHOLD "))
        self.info['max'] = int(input("MAX "))
        self.info["aqi"] = input("AQI ")
        self.info["reverse"] = input('REVERSE ')
    
    def print_locations(self, data, geo_location) -> None:
        "Prints the requested location "
        print("CENTER {}".format(self.create_location_string(geo_location)))
        for point in data:
            print("AQI", point['aqi'])
            print(self.create_location_string(point['geo_location']))
            print(point['location'])
    
    def create_location_string(self, geo_location) -> list:
        """creates a string to get location data and appoints it to it's lat and lan"""
        location = ''
        if(geo_location[0] >= 0):
            location += "{}/N ".format(abs(geo_location[0]))
        else:
            location += "{}/S ".format(abs(geo_location[0]))
        if(geo_location[1] >= 0):
            location += "{}/E".format(abs(geo_location[1]))
        else:
            location += "{}/W".format(abs(geo_location[1]))
        return location

if __name__ == "__main__":
    app = Controller()