import requests as re
from sensor import *
import csv
# read in api request ( change this to take CL input )

siteCodes = ['07079300','07081200','07083710','07083200','07083000']
siteNames = ['HeadWater', 'Leadville', 'EmpireGulch', 'HalfMoonDiversion', 'HalfMoonCreek']
paramCodes = ['00060', '00065']
sites = list()
for i, site in enumerate(siteCodes):
    sites.append(StreamSensor(site_code=siteCodes[i], param_codes=paramCodes))
    print('\nNickname:  ' + siteNames[i])
    sites[i].sensor_results()
    sites[i].log_data()


