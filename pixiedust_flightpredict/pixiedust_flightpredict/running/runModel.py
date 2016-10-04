# -------------------------------------------------------------------------------
# Copyright IBM Corp. 2016
# 
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
# http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -------------------------------------------------------------------------------

from .flightAccess import *
from .weatherAccess import *

"""
{'appendix': {'airlines': [{'active': True,
    'fs': 'NK',
    'iata': 'NK',
    'icao': 'NKS',
    'name': 'Spirit Airlines',
    'phoneNumber': '800-772-7117'}],
  'airports': [{'active': True,
    'city': 'Boston',
    'cityCode': 'BOS',
    'classification': 1,
    'countryCode': 'US',
    'countryName': 'United States',
    'elevationFeet': 19,
    'faa': 'BOS',
    'fs': 'BOS',
    'iata': 'BOS',
    'icao': 'KBOS',
    'latitude': 42.36646,
    'localTime': '2016-10-03T23:57:34.128',
    'longitude': -71.020176,
    'name': 'Logan International Airport',
    'postalCode': '02128-2909',
    'regionName': 'North America',
    'stateCode': 'MA',
    'street1': 'One Harborside Drive',
    'street2': '',
    'timeZoneRegionName': 'America/New_York',
    'utcOffsetHours': -4.0,
    'weatherZone': 'MAZ015'},
   {'active': True,
    'city': 'Las Vegas',
    'cityCode': 'LAS',
    'classification': 1,
    'countryCode': 'US',
    'countryName': 'United States',
    'elevationFeet': 2095,
    'faa': 'LAS',
    'fs': 'LAS',
    'iata': 'LAS',
    'icao': 'KLAS',
    'latitude': 36.081,
    'localTime': '2016-10-03T20:57:34.128',
    'longitude': -115.147599,
    'name': 'McCarran International Airport',
    'postalCode': '89119',
    'regionName': 'North America',
    'stateCode': 'NV',
    'street1': '5757 Wayne Newton Boulevard',
    'timeZoneRegionName': 'America/Los_Angeles',
    'utcOffsetHours': -7.0,
    'weatherZone': 'NVZ020'}],
  'equipments': [{'iata': '32S',
    'jet': True,
    'name': 'Airbus A318 / A319 / A320 / A321',
    'regional': False,
    'turboProp': False,
    'widebody': False}]},
 'request': {'carrier': {'fsCode': 'NK', 'requestedCode': 'NK'},
  'codeType': {},
  'date': {'day': '12',
   'interpreted': '2016-10-12',
   'month': '10',
   'year': '2016'},
  'departing': True,
  'flightNumber': {'interpreted': '641', 'requested': '641'},
  'url': 'https://api.flightstats.com/flex/schedules/rest/v1/json/flight/NK/641/departing/2016/10/12'},
 'scheduledFlights': [{'arrivalAirportFsCode': 'LAS',
   'arrivalTerminal': '1',
   'arrivalTime': '2016-10-12T19:34:00.000',
   'carrierFsCode': 'NK',
   'codeshares': [],
   'departureAirportFsCode': 'BOS',
   'departureTerminal': 'B',
   'departureTime': '2016-10-12T16:40:00.000',
   'flightEquipmentIataCode': '32S',
   'flightNumber': '641',
   'isCodeshare': False,
   'isWetlease': False,
   'referenceCode': '1874-588916--',
   'serviceClasses': ['R', 'Y'],
   'serviceType': 'J',
   'stops': 0,
   'trafficRestrictions': []}]}
"""

def runModel(flight, date):
    response = getFlightSchedule(flight, date)
    if "error" in response:
        return {"error": "Unable to access schedule {0}".format(response["error"])}

    payload={}
    appendix=response['appendix']
    payload["flightInfo"]=scheduledFlight=response["scheduledFlights"][0]
    
    payload["departureInfo"]=departureInfo={}
    departureInfo["airportInfo"]=depAirportJSON=appendix["airports"][0]
    departureInfo["weatherForecast"]= depWeather = getWeather(depAirportJSON['latitude'], depAirportJSON['longitude'], scheduledFlight["departureTime"])

    payload["arrivalAirportInfo"]=arrivalInfo={}
    arrivalInfo["airportInfo"]=arrAirportJSON=appendix["airports"][1]
    arrivalInfo["weatherForecast"]= arrWeather=getWeather(arrAirportJSON['latitude'], arrAirportJSON['longitude'], scheduledFlight["arrivalTime"] )

    payload["prediction"]={
        "overall": "Delayed between 13 and 41 minutes",
        "models":[
            {"model":"NaiveBayesModel", "prediction":"Delayed between 13 and 41 minutes"},
            {"model":"DecisionTreeModel: Delayed between 13 and 41 minutes"},
            {"model":"LogisticRegressionModel: Delayed between 13 and 41 minutes"},
            {"model":"RandomForestModel: Delayed between 13 and 41 minutes"}
        ]
    }
    return payload   

    """
    #create the features vector
    features=[]
    for attr in f.attributes:
        features.append(depWeather[mapAttribute(attr)])
    for attr in f.attributes:
        features.append(arrWeather[mapAttribute(attr)])
    
    #Call training handler for custom features
    s=type('dummy', (object,), {'departureTime':departureDT, 'arrivalTime':arrivalDT, 'arrivalAirportFsCode': arrAirportCode, 
                    'departureAirportFsCode':depAirportCode,'departureWeather': depWeather, 'arrivalWeather': arrWeather})
    customFeaturesForRunModel=f.getTrainingHandler().customTrainingFeatures(s) 
    for value in customFeaturesForRunModel:
        features.append( value )

    for model in mlModels:
        label= model.__class__.__name__
        html+='<li>' + label + ': ' + f.getTrainingHandler().getClassLabel(model.predict(features)) + '</li>'
    """

    #payload format
    """
    {
        "flightInfo": <flightInfo>,
        "departureAirportInfo":{
            "airportInfo": <airport>
            "weatherForecast": <weather>
        },
        "arrivalAirportInfo":{
            "airportInfo": <airport>
            "weatherForecast": <weather>
        },
        "prediction": {
            "overall": <prediction>,
            "models":[
                { 
                    "model": <modelName>
                    "prediction": <prediction>
                },
                ...
            ]
        }
    }
    """

def runModelTest(flight, date):
    return {'arrivalAirportInfo': {'airportInfo': {'active': True,
   'city': 'Las Vegas',
   'cityCode': 'LAS',
   'classification': 1,
   'countryCode': 'US',
   'countryName': 'United States',
   'elevationFeet': 2095,
   'faa': 'LAS',
   'fs': 'LAS',
   'iata': 'LAS',
   'icao': 'KLAS',
   'latitude': 36.081,
   'localTime': '2016-10-04T12:28:48.884',
   'longitude': -115.147599,
   'name': 'McCarran International Airport',
   'postalCode': '89119',
   'regionName': 'North America',
   'stateCode': 'NV',
   'street1': '5757 Wayne Newton Boulevard',
   'timeZoneRegionName': 'America/Los_Angeles',
   'utcOffsetHours': -7.0,
   'weatherZone': 'NVZ020'},
  'weatherForecast': {'class': 'fod_short_range_hourly',
   'clds': 0,
   'day_ind': 'D',
   'dewpt': -9,
   'dow': 'Tuesday',
   'expire_time_gmt': 1475609398,
   'fcst_valid': 1475622000,
   'fcst_valid_local': '2016-10-04T16:00:00-0700',
   'feels_like': 26,
   'golf_category': 'Very Good',
   'golf_index': 9,
   'gust': None,
   'hi': 26,
   'icon_code': 32,
   'icon_extd': 3200,
   'mslp': 1006.5,
   'num': 4,
   'phrase_12char': 'Sunny',
   'phrase_22char': 'Sunny',
   'phrase_32char': 'Sunny',
   'pop': 0,
   'precip_type': 'rain',
   'qpf': 0.0,
   'rh': 9,
   'severity': 1,
   'snow_qpf': 0.0,
   'subphrase_pt1': 'Sunny',
   'subphrase_pt2': '',
   'subphrase_pt3': '',
   'temp': 26,
   'uv_desc': 'Low',
   'uv_index': 2,
   'uv_index_raw': 1.7,
   'uv_warning': 0,
   'vis': 16.0,
   'wc': 26,
   'wdir': 112,
   'wdir_cardinal': 'ESE',
   'wspd': 8,
   'wxman': 'wx1000'}},
 'departureInfo': {'airportInfo': {'active': True,
   'city': 'Boston',
   'cityCode': 'BOS',
   'classification': 1,
   'countryCode': 'US',
   'countryName': 'United States',
   'elevationFeet': 19,
   'faa': 'BOS',
   'fs': 'BOS',
   'iata': 'BOS',
   'icao': 'KBOS',
   'latitude': 42.36646,
   'localTime': '2016-10-04T15:28:48.884',
   'longitude': -71.020176,
   'name': 'Logan International Airport',
   'postalCode': '02128-2909',
   'regionName': 'North America',
   'stateCode': 'MA',
   'street1': 'One Harborside Drive',
   'street2': '',
   'timeZoneRegionName': 'America/New_York',
   'utcOffsetHours': -4.0,
   'weatherZone': 'MAZ015'},
  'weatherForecast': {'class': 'fod_short_range_hourly',
   'clds': 29,
   'day_ind': 'D',
   'dewpt': 10,
   'dow': 'Tuesday',
   'expire_time_gmt': 1475609399,
   'fcst_valid': 1475611200,
   'fcst_valid_local': '2016-10-04T16:00:00-0400',
   'feels_like': 14,
   'golf_category': 'Very Good',
   'golf_index': 8,
   'gust': None,
   'hi': 15,
   'icon_code': 34,
   'icon_extd': 3400,
   'mslp': 1027.1,
   'num': 1,
   'phrase_12char': 'M Sunny',
   'phrase_22char': 'Mostly Sunny',
   'phrase_32char': 'Mostly Sunny',
   'pop': 0,
   'precip_type': 'rain',
   'qpf': 0.0,
   'rh': 69,
   'severity': 1,
   'snow_qpf': 0.0,
   'subphrase_pt1': 'Mostly',
   'subphrase_pt2': 'Sunny',
   'subphrase_pt3': '',
   'temp': 15,
   'uv_desc': 'Low',
   'uv_index': 1,
   'uv_index_raw': 1.31,
   'uv_warning': 0,
   'vis': 16.0,
   'wc': 14,
   'wdir': 54,
   'wdir_cardinal': 'NE',
   'wspd': 24,
   'wxman': 'wx1000'}},
 'flightInfo': {'arrivalAirportFsCode': 'LAS',
  'arrivalTerminal': '1',
  'arrivalTime': '2016-10-12T19:34:00.000',
  'carrierFsCode': 'NK',
  'codeshares': [],
  'departureAirportFsCode': 'BOS',
  'departureTerminal': 'B',
  'departureTime': '2016-10-12T16:40:00.000',
  'flightEquipmentIataCode': '32S',
  'flightNumber': '641',
  'isCodeshare': False,
  'isWetlease': False,
  'referenceCode': '1875-576194--',
  'serviceClasses': ['R', 'Y'],
  'serviceType': 'J',
  'stops': 0,
  'trafficRestrictions': []},
 'prediction': {'models': [{'model': 'NaiveBayesModel',
    'prediction': 'Delayed between 13 and 41 minutes'},
   {'model': 'DecisionTreeModel: Delayed between 13 and 41 minutes'},
   {'model': 'LogisticRegressionModel: Delayed between 13 and 41 minutes'},
   {'model': 'RandomForestModel: Delayed between 13 and 41 minutes'}],
  'overall': 'Delayed between 13 and 41 minutes'}}