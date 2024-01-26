import requests
import json

def fetchOTP(id):
  url = f"https://www.simbrief.com/api/xml.fetcher.php?userid={id}&json=v2"
  response = requests.get(url)
  responseJSON = response.json()
  return responseJSON

def filterOTP(otp):
  data = otp

  atisTemplate = {
    "network": "",
    "issued": "",
    "letter": "",
    "phonetic": "",
    "type": "",
    "message": ""
  }

  notamTemplate = { 
    "accountID": "",
    "notamID": "",
    "locationID": "",
    "locationICAO": "",
    "locationName": "",
    "locationType": "",
    "dateEffective": "",
    "dateExpire": "",
    "notamText": "",
    "notamQcodeCategory": "",
    "notamQcodeSubject": "",
    "notamQcodeStatus": "",
    "notamIsObstacle": False
  }

  # defaults
  params = {}
  general = {}
  origin = {}
  destination = {}
  alternates = []
  aircraft = {}
  fuel = {}
  times = {}
  weights = {}
  weather = {}
  files = {}

  if data.get("params"):
    params = { 
      "requestID": data.get("params").get("request_id", ""),
      "userID": data.get("params").get("user_id", ""),
      "ofpLayout": data.get("params").get("ofp_layout", ""),
      "airac": data.get("params").get("airac", ""),
      "units": data.get("params").get("units", "")
    }
  else:
    params = { 
      "requestID": "",
      "userID": "",
      "ofpLayout": "",
      "airac": "",
      "units": ""
    }
  
  if data.get("general"):
    general = { 
      "airline": data.get("general").get("icao_airline", ""),
      "flightNumber": data.get("general").get("flight_number", ""),
      "cruiseProfile": data.get("general").get("cruise_profile", ""),
      "alternateProfile": data.get("general").get("alternate_profile", ""),
      "costIndex": data.get("general").get("costindex", ""),
      "initialAltitude": data.get("general").get("initial_altitude", ""),
      "airDistance": data.get("general").get("air_distance", ""),
      "passengers": data.get("general").get("passengers", ""),
      "route": data.get("general").get("route", ""),
      "routeIFPS": data.get("general").get("route_ifps", ""),
      "routeNavigraph": data.get("general").get("route_navigraph", "")
    }
  else:
    general = { 
      "airline": "",
      "flightNumber": "",
      "cruiseProfile": "",
      "alternateProfile": "",
      "costIndex": "",
      "initialAltitude": "",
      "airDistance": "",
      "passengers": "",
      "route": "",
      "routeIFPS": "",
      "routeNavigraph": ""
    }
    
  # Origin, Destination, Alternate need iterated for ATIS and NOTAM

  if data.get("origin"):
    atisList = []
    notamList = []
    
    if data.get("origin").get("atis"):
      for atis in data.get("origin").get("atis"):
        temp = { 
          "network": atis.get("network", ""),
          "issued": atis.get("issued", ""),
          "letter": atis.get("letter", ""),
          "phonetic": atis.get("phonetic", ""),
          "type": atis.get("type", ""),
          "message": atis.get("message", "")
        }
        atisList.append(temp)
    else:
      atisList = [atisTemplate]
    
    if data.get("origin").get("notam"):
      for notam in data.get("origin").get("notam"):
        temp = { 
          "accountID": notam.get("account_id", ""),
          "notamID": notam.get("notam_id", ""),
          "locationID": notam.get("location_id", ""),
          "locationICAO": notam.get("location_icao", ""),
          "locationName": notam.get("location_name", ""),
          "locationType": notam.get("location_type", ""),
          "dateEffective": notam.get("date_effective", ""),
          "dateExpire": notam.get("date_expire", ""),
          "notamText": notam.get("account_id", ""),
          "notamQcodeCategory": notam.get("account_id", ""),
          "notamQcodeSubject": notam.get("account_id", ""),
          "notamQcodeStatus": notam.get("account_id", ""),
          "notamIsObstacle": notam.get("notam_is_obstacle", False)
        }
        notamList.append(temp)
    else: 
      notamList = [notamTemplate]

    origin = { 
      "icaoCode": data.get("origin").get("icao_code", ""),
      "iataCode": data.get("origin").get("iata_code", ""), 
      "faaCode": data.get("origin").get("faa_code", ""),
      "elevation": data.get("origin").get("elevation", ""),
      "posLat": data.get("origin").get("pos_lat", ""), 
      "posLong": data.get("origin").get("pos_long", ""), 
      "name": data.get("origin").get("name", ""),
      "planRwy": data.get("origin").get("plan_rwy", ""), 
      "transAlt": data.get("origin").get("trans_alt", ""),
      "transLevel": data.get("origin").get("trans_level", ""),
      "metar": data.get("origin").get("metar", ""),
      "metarTime": data.get("origin").get("metar_time", ""), 
      "metarCategory": data.get("origin").get("metar_category", ""),
      "metarVisibility": data.get("origin").get("metar_visibility", ""),
      "metarCeiling": data.get("origin").get("metar_ceiling", ""),
      "atis": atisList,
      "notam": notamList
    }
  else:
    origin = { 
      "icaoCode": "",
      "iataCode": "",
      "faaCode": "",
      "elevation": "",
      "posLat": "",
      "posLong": "",
      "name": "",
      "planRwy": "",
      "transAlt": "",
      "transLevel": "",
      "metar": "",
      "metarTime": "",
      "metarCategory": "",
      "metarVisibility": "",
      "metarCeiling": "",
      "atis": [atisTemplate],
      "notam": [notamTemplate]
    }

  if data.get("destination"):
    atisList = []
    notamList = []
    
    if data.get("destination").get("atis"):
      for atis in data.get("destination").get("atis"):
        temp = { 
          "network": atis.get("network", ""),
          "issued": atis.get("issued", ""),
          "letter": atis.get("letter", ""),
          "phonetic": atis.get("phonetic", ""),
          "type": atis.get("type", ""),
          "message": atis.get("message", "")
        }
        atisList.append(temp)
    else:
      atisList = [atisTemplate]
    
    if data.get("destination").get("notam"):
      for notam in data.get("destination").get("notam"):
        temp = { 
          "accountID": notam.get("account_id", ""),
          "notamID": notam.get("notam_id", ""),
          "locationID": notam.get("location_id", ""),
          "locationICAO": notam.get("location_icao", ""),
          "locationName": notam.get("location_name", ""),
          "locationType": notam.get("location_type", ""),
          "dateEffective": notam.get("date_effective", ""),
          "dateExpire": notam.get("date_expire", ""),
          "notamText": notam.get("account_id", ""),
          "notamQcodeCategory": notam.get("account_id", ""),
          "notamQcodeSubject": notam.get("account_id", ""),
          "notamQcodeStatus": notam.get("account_id", ""),
          "notamIsObstacle": notam.get("notam_is_obstacle", False)
        }
        notamList.append(temp)
    else: 
      notamList = [notamTemplate]
    
    destination = { 
      "icaoCode": data.get("destination").get("icao_code", ""),
      "iataCode": data.get("destination").get("iata_code", ""), 
      "faaCode": data.get("destination").get("faa_code", ""),
      "elevation": data.get("destination").get("elevation", ""),
      "posLat": data.get("destination").get("pos_lat", ""), 
      "posLong": data.get("destination").get("pos_long", ""), 
      "name": data.get("destination").get("name", ""),
      "planRwy": data.get("destination").get("plan_rwy", ""), 
      "transAlt": data.get("destination").get("trans_alt", ""),
      "transLevel": data.get("destination").get("trans_level", ""),
      "metar": data.get("destination").get("metar", ""),
      "metarTime": data.get("destination").get("metar_time", ""), 
      "metarCategory": data.get("destination").get("metar_category", ""),
      "metarVisibility": data.get("destination").get("metar_visibility", ""),
      "metarCeiling": data.get("destination").get("metar_ceiling", ""),
      "atis": atisList,
      "notam": notamList
    }
  else:
    destination = { 
      "icaoCode": "",
      "iataCode": "",
      "faaCode": "",
      "elevation": "",
      "posLat": "",
      "posLong": "",
      "name": "",
      "planRwy": "",
      "transAlt": "",
      "transLevel": "",
      "metar": "",
      "metarTime": "",
      "metarCategory": "",
      "metarVisibility": "",
      "metarCeiling": "",
      "atis": [atisTemplate],
      "notam": [notamTemplate]
    }
  
  if data.get("alternate"):
    for item in data["alternate"]:
      atisList = []
      notamList = []

      if item.get("atis"):
        for atis in item.get("atis"):
          temp = { 
            "network": atis.get("network", ""),
            "issued": atis.get("issued", ""),
            "letter": atis.get("letter", ""),
            "phonetic": atis.get("phonetic", ""),
            "type": atis.get("type", ""),
            "message": atis.get("message", "")
          }
          atisList.append(temp)
      else:
        atisList = [atisTemplate]

      if item.get("notam"):
        for notam in item.get("notam"):
          temp = { 
            "accountID": notam.get("account_id", ""),
            "notamID": notam.get("notam_id", ""),
            "locationID": notam.get("location_id", ""),
            "locationICAO": notam.get("location_icao", ""),
            "locationName": notam.get("location_name", ""),
            "locationType": notam.get("location_type", ""),
            "dateEffective": notam.get("date_effective", ""),
            "dateExpire": notam.get("date_expire", ""),
            "notamText": notam.get("account_id", ""),
            "notamQcodeCategory": notam.get("account_id", ""),
            "notamQcodeSubject": notam.get("account_id", ""),
            "notamQcodeStatus": notam.get("account_id", ""),
            "notamIsObstacle": notam.get("notam_is_obstacle", False)
          }
          notamList.append(temp)
      else: 
        notamList = [notamTemplate]

      obj = { 
        "icaoCode": item.get("icao_code", ""),
        "iataCode": item.get("iata_code", ""),
        "faaCode": item.get("faa_code", ""),
        "elevation": item.get("elevation", ""),
        "posLat": item.get("pos_lat", ""),
        "posLong": item.get("pos_long", ""),
        "name": item.get("name", ""),
        "planRwy": item.get("plan_rwy", ""),
        "transAlt": item.get("trans_alt", ""),
        "transLevel": item.get("trans_level", ""),
        "cruiseAltitude": item.get("cruise_altitude", ""),
        "airDistance": item.get("air_distance", ""),
        "trackTrue": item.get("track_true", ""),
        "trackMag": item.get("track_mag", ""),
        "avgWindComp": item.get("avg_wind_comp", ""),
        "avgWindDir": item.get("avg_wind_dir", ""),
        "ete": item.get("ete", ""),
        "route": item.get("route", ""),
        "routeIFPS": item.get("route", ""),
        "routeNavigraph": item.get("route_navigraph", ""),
        "metar": item.get("metar", ""),
        "metarTime": item.get("metar_time", ""),
        "metarCategory": item.get("metar_category", ""),
        "metarVisibility": item.get("metar_visibility", ""),
        "metarCeiling": item.get("metar_ceiling", ""),
        "atis": atisList,
        "notam": notamList
      }
      alternates.append(obj)
  else: 
    alternates = [{
      "icaoCode": "",
      "iataCode": "",
      "faaCode": "",
      "elevation": "",
      "posLat": "",
      "posLong": "",
      "name": "",
      "planRwy": "",
      "transAlt": "",
      "transLevel": "",
      "cruiseAltitude": "",
      "airDistance": "",
      "trackTrue": "",
      "trackMag": "",
      "avgWindComp": "",
      "avgWindDir": "",
      "ete": "",
      "route": "",
      "routeIFPS": "",
      "routeNavigraph": "",
      "metar": "",
      "metarTime": "",
      "metarCategory": "",
      "metarVisibility": "",
      "metarCeiling": "",
      "atis": [atisTemplate],
      "notam": [notamTemplate]
    }]

  if data.get("aircraft"):
    aircraft = { 
      "icaoCode": data.get("aircraft").get("icao_code", ""), 
      "iataCode": data.get("aircraft").get("iatacode", ""), 
      "baseType": data.get("aircraft").get("base_type", ""),
      "name": data.get("aircraft").get("name", ""),
      "reg": data.get("aircraft").get("reg", ""),
      "selcal": data.get("aircraft").get("selcal", "")
    }
  else:
    aircraft = { 
      "icaoCode": "",
      "iataCode": "",
      "baseType": "",
      "name": "",
      "reg": "",
      "selcal": ""
    }
  
  if data.get("fuel"):
    fuel = { 
      "block": data.get("fuel").get("plan_ramp", ""),
      "takeoff": data.get("fuel").get("plan_takeoff", ""),
      "landing": data.get("fuel").get("plan_landing", "")
    }
  else:
    fuel = { 
      "block": "",
      "takeoff": "",
      "landing": ""
    }
  
  if data.get("times"):
    times = { 
      "ete": data.get("times").get("est_time_enroute", ""),
      "schedDep": data.get("times").get("sched_off", ""),
      "schedArr": data.get("times").get("sched_in", "")
    }
  else:
    times = { 
      "ete": "",
      "schedDep": "",
      "schedArr": "",
    }
  
  if data.get("weights"):
    weights = { 
      "paxCountActual": data.get("weights").get("pax_count_actual", ""),
      "paxWeight": data.get("weights").get("pax_weight", ""),
      "bagWeight": data.get("weights").get("bag_weight", ""),
      "cargo": data.get("weights").get("cargo", ""),
      "estZFW": data.get("weights").get("est_zfw", ""),
      "estTOW": data.get("weights").get("est_tow", ""),
      "estLDW": data.get("weights").get("est_ldw", "")
    }
  else:
    weights = { 
      "paxCountActual": "",
      "paxWeight": "",
      "bagWeight": "",
      "cargo":  "",
      "estZFW": "",
      "estTOW": "",
      "estLDW": ""
    }
  
  if data.get("weather"):
    weather = { 
      "origMETAR": data.get("weather").get("orig_metar", ""),
      "destMETAR": data.get("weather").get("dest_metar", ""),
      "altnMETAR": data.get("weather").get("altn_metar", "")
    }
  else:
    weather = { 
      "origMETAR": "",
      "destMETAR": "",
      "altnMETAR": ""
    }
  
  if data.get("files"):
    files = { 
      "directory": data.get("files").get("directory", ""),
      "pdf": data.get("files").get("pdf", "")
    }
  else:
    files = { 
      "directory": "",
      "pdf": ""
    }

  filter = { 
    "fetch": { 
      "userID": data["fetch"]["userid"],
      "status": data["fetch"]["status"],
      "time": data["fetch"]["time"]
    },
    "params": params,
    "general": general, 
    "origin": origin,
    "destination": destination,
    "alternate": alternates,
    "aircraft": aircraft,
    "fuel": fuel,
    "times": times, 
    "weights": weights,
    "weather": weather,
    "files": files
  }
  return filter

def main(id):
  otp = fetchOTP(id)
  filteredOTP = filterOTP(otp)
  return filteredOTP

if __name__ == '__main__':
  temp = 123456
  main(temp)