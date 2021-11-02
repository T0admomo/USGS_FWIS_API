import requests as re
import json


def format_api_req(siteCode: int, output='json', paramCodes=['00060', '00065'], siteStatus='All', *args, **kwargs):
    """
   :param siteCode: USGS site identifier
   :param output: default = json, determines the return object type
   :param paramCodes: single value or list of measurement codes ex (00060 = CubicFlowFt, 00065 = GageHeightFt)
   :param siteStatus: single value, one of either [all, active, inactive]

   :return url: formatted url string for use with requests library
   """

    url = (f"https://waterservices.usgs.gov/nwis/iv/ \n"
           f"?format={output} \n"
           f"&sites={siteCode} \n"
           f"&parameterCd={','.join(paramCodes)} \n"
           f"&siteStatus={siteStatus}")
    url = url.replace('\n', '')
    url = url.replace(' ', '')
    return url


def get_time_series(url: str):
    """
    Return the timeSeries sensorlib data from the api request/response

    :type url: str
    :returns json: dict
    """
    res = re.get(url).json()
    data = res['value']['timeSeries']
    return data


print("Imported fwis_api module")

#
# def url_from_input_values():
#     """
#     For use in running the Command Line application, create api req url from user inputs
#
#     :return url : string
#     """
#     print('Please Provide Sensor Parameters')
#     print('\tSeparate Multiple Values with a comma and no white space.')
#
#     # turn the input into a list of siteCodes
#     site_input = input('\nInput siteCodes: ')
#     sites = [site_input.split(',')[i] for i in range(len(site_input.split(",")))]
#
#     paramCodes_input = input('\nInput Parameter Codes: ')
#     paramCodes = [paramCodes_input.split(',')[i] for i in range(len(paramCodes_input.split(",")))]
#
#     url = format_api_req(sites=sites, paramCodes=paramCodes)
#     return url
