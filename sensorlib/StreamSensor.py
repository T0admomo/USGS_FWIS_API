from sensor.fwis_api import *
import json
import os.path

class StreamSensor:

    
    def _get_api_request(self):
        """
        calls the api request method
        :param url:
        :return dict:
        """
        url = format_api_req(siteCode=self._site_code, paramCodes= self.param_codes)
        return get_time_series(url)

    def _get_meta(self):
        """
        check that the sensors come from the same site and if so take the first sensors meta info

        :return: dict
        """
        sensor_1_meta = self.json[0]['sourceInfo']
        sensor_2_meta = self.json[1]['sourceInfo']
        # checking that both measures come from the same site
        try:
            sensor_2_meta == sensor_1_meta
        except ValueError:
            print('Failed: cannot read data from multiple sites')
        meta = self.json[0]['sourceInfo']
        return meta

    def _get_geolocation(self) -> tuple:
        geoLoc = self._meta["geoLocation"]["geogLocation"]
        geoLoc = (geoLoc["latitude"], geoLoc["longitude"])
        return geoLoc

    def _get_siteCode(self):
        return self._meta['siteCode'][0]['value']

        ### Translate Senor Value Methods

    SENSOR_DICT = {
        'flow': 0,
        'height': 1
    }

    def _get_value(self, sensorType):
        sensorType = self.SENSOR_DICT[sensorType]
        return self.json[sensorType]['values'][0]['value'][0]['value']

    def _get_datetime(self):
        return self.json[0]['values'][0]['value'][0]['dateTime']

    # @property
    # def meta(self):
    #     return self._meta()

    @property
    def geolocation(self):
        return self._geolocation

    @property
    def flow(self):
        return self._flow

    @property
    def height(self):
        return self._height

    @property
    def datetime(self):
        return self._datetime

    @property
    def values(self):
        return self._values

    @property
    def site_code(self):
        return self._site_code

    @property
    def param_codes(self):
        return self._param_codes

    def __init__(self, site_code, param_codes):
        """

        :type url: str
        """
        ### API CALL
        self._site_code = site_code
        self._param_codes = param_codes
        self.json = self._get_api_request()
        ### META
        self._meta = self._get_meta()
        self._datetime = self._get_datetime()
        self._geolocation = self._get_geolocation()
        ### MEASUREMENTS
        self._flow = self._get_value('flow')
        self._height = self._get_value('height')
        self._values = (self._get_value('flow'), self._get_value('height'), self._get_datetime())

    def sensor_results(self):
        return print(f"""Latest Sensor Data for site: {self.site_code}
        Flow: {self.flow} 3ft/sc at \
        \n\tHeight: {self.height}   \
        \n\tTimeStamp: {self.datetime}\n""")

    def log_data(self):

        # Use site_code for path_name
        path_name = f'/home/timo/PycharmProjects/ArkansasRiver/data/streamflow.{self.site_code}.json'

        def write_json(data, filename):
            with open(filename, 'w') as f:
                json.dump(data, f, indent = 4)
                f.close()
        # create the json file on first run.
        if not os.path.isfile(path_name):
            new_data = \
                {
                    'site_name': self._meta['siteName'],
                    'site_code': self._site_code,
                    'time_zone': self._meta['timeZoneInfo']['defaultTimeZone']['zoneAbbreviation'],
                    'coordinates': self._geolocation,
                    'observations': [
                    {'Stream_flow': self.flow, 'Gage_height': self.height, 'Datetime': self.datetime}
                ]}

            write_json(new_data, path_name)
        # update the json file is it already exists
        else:
            new_data = {'Stream_flow': self.flow, 'Gage_height': self.height, 'Datetime': self.datetime}
            with open(path_name) as file:
                data = json.load(file)
                temp = data['observations']
                temp.append(new_data)
            write_json(data, path_name)
