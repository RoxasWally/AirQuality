import math


class FilterData:
    
    def __init__(self, info, geolocation):
        self.info = info
        self.geolocation = geolocation
        
    def filter(self, data) -> list:
        self.setIndexMap(data)
        data['data'] = self.filter_type(data['data'], self.mapping['Type'])
        data['data'] = self.filter_age(data['data'], self.mapping['age'])
        data['data'] = self.filter_distance(data['data'], self.info['range'], self.geolocation, self.mapping['Lat'], self.mapping['Lon'])
        self.convert_p_to_aqi(data['data'], self.mapping['pm'])
        data['data'] = self.filter_threshold(data['data'], self.info['threshold'], self.mapping['pm'])
        data['data'] = sorted(data['data'], key = lambda x: x[self.mapping['pm']], reverse=True)
        data['data'] = data['data'][:self.info['max']]
        return data

    def getIndex(self) -> list:
        return self.mapping

    def filter_threshold(self, data, threshold, p_index) -> list:
        """ makes a list of threshold and filters out and only obtains the requested ones"""
        filtered_data = []
        for value in data:
            if(value[p_index] is None):
                continue
            if(value[p_index] >= threshold):
                filtered_data.append(value)
        return filtered_data

    def filter_type(self, data, type_index, required=0) -> list:
        """ makes a list and filters out the indoor calcualtion
        as it is not considered and only interested in outdoors"""
        filtered_data = []
        for values in data:
            if(values[type_index] == required):
                filtered_data.append(values)
        return filtered_data

    def filter_age(self, data, age_index, required = 3600):
        """filters out data that is has not been reported in the last hour"""
        filtered_data = []
        for values in data:
            if values[age_index] < required:
                filtered_data.append(values)
        return filtered_data

    def filter_distance(self, data, range_to_collect, center, lat_index, lon_index):
        """ filters out data that is over the requested range"""
        filtered_data = []
        for values in data:
            if values[lat_index] is None or values[lon_index] is None:
                continue
            other_point = (values[lat_index], values[lon_index])
            distance = self.calculate_distance(center, other_point)
            if distance <= range_to_collect:
                filtered_data.append(values)
        return filtered_data

    def calculate_distance(self, center, other_point) :
        """ calculautes the equirectangular approimxation between two distances"""
        dlat = math.radians(center[0] - other_point[0])
        dlon = math.radians(center[1] - other_point[1])
        alat = math.radians((center[0] + other_point[0])/2)
        R = 3958.8
        x = dlon * math.cos(alat)
        d = math.sqrt(math.pow(x, 2) + math.pow(dlat, 2))*R
        return d


    def setIndexMap(self, data):
        fields = ['pm', 'Type', 'Lat', 'Lon', 'age']
        self.mapping = {}
        fields_locations = data['fields']
        for field in fields:
            self.mapping[field] = fields_locations.index(field)

    def convert_p_to_aqi(self, data, p_index):
        """ converts PM2.5 to the AQI value, which air quality"""
        conversion = {  (0.0, 12.0): (0, 50), 
                    (12.1, 35.4): (51, 100), 
                    (35.5, 55.4): (101, 150), 
                    (55.5, 150.4): (151, 200),
                    (150.5, 250.4): (201, 300),
                    (250.5, 350.4): (301, 400),
                    (350.5, 500.4): (401, 500)
    }
        for index, value in enumerate(data):
            found_range = False
            for p_range in conversion:
                if p_range[0] <= value[p_index] <= p_range[1]:
                    found_range = True
                    position = (value[p_index] - p_range[0])/(p_range[1] - p_range[0])
                    converted_value = (conversion[p_range][1] - conversion[p_range][0])*position + conversion[p_range][0]
                    data[index][p_index] = round(converted_value)
                    break
            if not found_range:
                data[index][p_index] = 501
