import numpy as np
import matplotlib.pyplot as plt
from datetime import date
import requests
import argparse

parser = argparse.ArgumentParser(description =
                                 'Smithsonian Eruption Database')
parser.add_argument('-y', '--year', type=int, help='year of eruption')
parser.add_argument('-e', '--explosivity', type=int,
                    help='explosivity threshold')
args = parser.parse_args()
e_arg = args.explosivity is not None
y_arg = args.year is not None

# Create class
class eruption:
    def __init__(self, name, date, vei, lat, lon):
        self.name = name
        self.date = date
        if vei is not None:
            self.vei = vei
        else:
            self.vei = -1
        self.lat = lat
        self.lon = lon
    def __str__(self):
        return ('(' + '%.1f'%(self.lat) + ',' + '%.1f'%(self.lon) + ') ' + \
                self.name + ' ' + str(self.date) + ' VEI: ' + \
                str(self.vei))

# Fetch JSON
url = 'https://webservices.volcano.si.edu/geoserver/GVP-VOTW/ows'
if not e_arg:
    if y_arg:
        filter='<PropertyIsEqualTo><PropertyName>StartDateYear</PropertyName><Literal>'+str(args.year)+'</Literal></PropertyIsEqualTo>'
    else:
        filter='<PropertyIsGreaterThan><PropertyName>StartDateYear</PropertyName><Literal>2000</Literal></PropertyIsEqualTo>'
else:
    filter='<PropertyIsGreaterThanOrEqualTo><PropertyName>ExplosivityIndexMax</PropertyName><Literal>'+str(args.explosivity)+'</Literal></PropertyIsGreaterThanOrEqualTo>'

params = dict(
        service='WFS',
        version='1.0.0',
        request='GetFeature',
        typeName='GVP-VOTW:Smithsonian_VOTW_Holocene_Eruptions',
        maxFeatures='2000',
        outputFormat='json',
        filter=filter
)
resp = requests.get(url=url, params=params)
data = resp.json()
data = np.asarray(data['features'])

eruptions = []
for i in range(len(data)):
    if not y_arg and (data[i]['properties']['StartDateYear'] > 2000):
        eruption_date = date(data[i]['properties']['StartDateYear'],
                    data[i]['properties']['StartDateMonth'],
                    data[i]['properties']['StartDateDay'])
        eruptions.append(eruption(
                    data[i]['properties']['Volcano_Name'],
                    eruption_date,
                    data[i]['properties']['ExplosivityIndexMax'],
                    data[i]['geometry']['coordinates'][1],
                    data[i]['geometry']['coordinates'][0]))
    elif e_arg and y_arg and (data[i]['properties']['StartDateYear'] == args.year):
        eruption_date = date(data[i]['properties']['StartDateYear'],
                    data[i]['properties']['StartDateMonth'],
                    data[i]['properties']['StartDateDay'])
        eruptions.append(eruption(
                    data[i]['properties']['Volcano_Name'],
                    eruption_date,
                    data[i]['properties']['ExplosivityIndexMax'],
                    data[i]['geometry']['coordinates'][1],
                    data[i]['geometry']['coordinates'][0]))
    else:
        eruption_date = date(data[i]['properties']['StartDateYear'],
                    data[i]['properties']['StartDateMonth'],
                    data[i]['properties']['StartDateDay'])
        eruptions.append(eruption(
                    data[i]['properties']['Volcano_Name'],
                    eruption_date,
                    data[i]['properties']['ExplosivityIndexMax'],
                    data[i]['geometry']['coordinates'][1],
                    data[i]['geometry']['coordinates'][0]))

eruptions.sort(key=lambda eruption: eruption.date)
#eruptions.sort(key=lambda eruption: eruption.vei)
for i in eruptions: print(i)
