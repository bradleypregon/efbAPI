import requests

def fetchOTP(id):
  url = f"https://www.simbrief.com/api/xml.fetcher.php?userid={id}&json=v2"
  response = requests.get(url)
  responseJSON = response.json()
  return responseJSON

def filterOTP(otp):
  data = otp

  filteredOFP = {}

  # defaults
  params = {}
  general = {}
  origin = {}
  destination = {}
  alternates = []
  navlog = []
  aircraft = {}
  fuel = {}
  times = {}
  weights = {}
  weather = {}
  files = {}

  if data.get("fetch"):
    fetch = { 
      "userID": data.get("fetch").get("userid", ""),
      "status": data.get("fetch").get("status", ""),
      "time": data.get("fetch").get("time", "")
    }
    filteredOFP["fetch"] = fetch

  if data.get("params"):
    params = { 
      "requestID": data.get("params").get("request_id", 0),
      "userID": data.get("params").get("user_id", ""),
      "ofpLayout": data.get("params").get("ofp_layout", ""),
      "airac": data.get("params").get("airac", ""),
      "units": data.get("params").get("units", "")
    }
    filteredOFP["params"] = params
  
  if data.get("general"):
    general = { 
      "airline": data.get("general").get("icao_airline", ""),
      "flightNumber": data.get("general").get("flight_number", ""),
      "cruiseProfile": data.get("general").get("cruise_profile", ""),
      "alternateProfile": data.get("general").get("alternate_profile", ""),
      "costIndex": data.get("general").get("costindex", ""),
      "initialAltitude": data.get("general").get("initial_altitude", 0),
      "airDistance": data.get("general").get("air_distance", 0),
      "passengers": data.get("general").get("passengers", 0),
      "route": data.get("general").get("route", ""),
      "routeIFPS": data.get("general").get("route_ifps", ""),
      "routeNavigraph": data.get("general").get("route_navigraph", "") # MONTN2 SEA DCT ZADON DCT ZELAK DCT ZIRAN DCT ZAXBY DCT OLIBY DCT
    }
    filteredOFP["general"] = general
    
  # Origin, Destination, Alternate need iterated for ATIS and NOTAM

  if data.get("origin"):
    atisList = []
    notamList = []

    origin = { 
      "icaoCode": data.get("origin").get("icao_code", ""),
      "iataCode": data.get("origin").get("iata_code", ""), 
      "faaCode": data.get("origin").get("faa_code", ""),
      "elevation": data.get("origin").get("elevation", 0),
      "posLat": data.get("origin").get("pos_lat", 0.0), 
      "posLong": data.get("origin").get("pos_long", 0.0), 
      "name": data.get("origin").get("name", ""),
      "planRwy": data.get("origin").get("plan_rwy", ""), 
      "transAlt": data.get("origin").get("trans_alt", 0),
      "transLevel": data.get("origin").get("trans_level", 0),
      "metar": data.get("origin").get("metar", ""),
      "metarTime": data.get("origin").get("metar_time", ""), 
      "metarCategory": data.get("origin").get("metar_category", ""),
      "metarVisibility": data.get("origin").get("metar_visibility", ""),
      "metarCeiling": data.get("origin").get("metar_ceiling", "")
    }
    
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
      origin["atis"] = atisList
    
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
          "dateExpire": notam.get("date_expire", "") if notam.get("date_expire") != False else "2099-12-31T11:59:00Z",
          "notamText": getStringValue(notam, "notam_text"),
          "notamQcodeCategory": getStringValue(notam, "notam_qcode_category"),
          "notamQcodeSubject": getStringValue(notam, "notam_qcode_subject"),
          "notamQcodeStatus": getStringValue(notam, "notam_qcode_status"),
          "notamIsObstacle": notam.get("notam_is_obstacle", False)
        }
        notamList.append(temp)
      origin["notam"] = notamList
    
    filteredOFP["origin"] = origin

  if data.get("destination"):
    atisList = []
    notamList = []

    destination = { 
      "icaoCode": data.get("destination").get("icao_code", ""),
      "iataCode": data.get("destination").get("iata_code", ""), 
      "faaCode": data.get("destination").get("faa_code", ""),
      "elevation": data.get("destination").get("elevation", 0),
      "posLat": data.get("destination").get("pos_lat", 0.0), 
      "posLong": data.get("destination").get("pos_long", 0.0), 
      "name": data.get("destination").get("name", ""),
      "planRwy": data.get("destination").get("plan_rwy", ""), 
      "transAlt": data.get("destination").get("trans_alt", ""),
      "transLevel": data.get("destination").get("trans_level", ""),
      "metar": data.get("destination").get("metar", ""),
      "metarTime": data.get("destination").get("metar_time", ""), 
      "metarCategory": data.get("destination").get("metar_category", ""),
      "metarVisibility": data.get("destination").get("metar_visibility", ""),
      "metarCeiling": data.get("destination").get("metar_ceiling", "")
    }
    
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
      destination["atis"] = atisList
    
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
          "dateExpire": notam.get("date_expire", "") if notam.get("date_expire") != False else "2099-12-31T11:59:00Z",
          "notamText": getStringValue(notam, "notam_text"),
          "notamQcodeCategory": getStringValue(notam, "notam_qcode_category"),
          "notamQcodeSubject": getStringValue(notam, "notam_qcode_subject"),
          "notamQcodeStatus": getStringValue(notam, "notam_qcode_status"),
          "notamIsObstacle": notam.get("notam_is_obstacle", False)
        }
        notamList.append(temp)
      destination["notam"] = notamList
    
    filteredOFP["destination"] = destination
  
  if data.get("alternate"):
    for item in data["alternate"]:
      atisList = []
      notamList = []

      obj = { 
        "icaoCode": item.get("icao_code", ""),
        "iataCode": item.get("iata_code", ""),
        "faaCode": item.get("faa_code", ""),
        "elevation": item.get("elevation", 0),
        "posLat": item.get("pos_lat", 0.0),
        "posLong": item.get("pos_long", 0.0),
        "name": item.get("name", ""),
        "planRwy": item.get("plan_rwy", ""),
        "transAlt": item.get("trans_alt", 0),
        "transLevel": item.get("trans_level", 0),
        "cruiseAltitude": item.get("cruise_altitude", ""),
        "airDistance": item.get("air_distance", ""),
        "trackTrue": item.get("track_true", ""),
        "trackMag": item.get("track_mag", ""),
        "avgWindComp": item.get("avg_wind_comp", ""),
        "avgWindDir": item.get("avg_wind_dir", ""),
        "avgWindSpd": item.get("avg_wind_spd", ""),
        "ete": item.get("ete", ""),
        "route": item.get("route", ""),
        "routeIFPS": item.get("route", ""),
        "routeNavigraph": item.get("route_navigraph", ""),
        "metar": item.get("metar", ""),
        "metarTime": item.get("metar_time", ""),
        "metarCategory": item.get("metar_category", ""),
        "metarVisibility": item.get("metar_visibility", ""),
        "metarCeiling": item.get("metar_ceiling", "")
        # "atis": atisList,
        # "notam": notamList
      }

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
        obj["atis"] = atisList
      # else:
      #   atisList = [atisTemplate]

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
            "dateExpire": notam.get("date_expire", "") if notam.get("date_expire") != False else "2099-12-31T11:59:00Z",
            "notamText": getStringValue(notam, "notam_text"),
            "notamQcodeCategory": getStringValue(notam, "notam_qcode_category"),
            "notamQcodeSubject": getStringValue(notam, "notam_qcode_subject"),
            "notamQcodeStatus": getStringValue(notam, "notam_qcode_status"),
            "notamIsObstacle": notam.get("notam_is_obstacle", False)
          }
          notamList.append(temp)
        obj["notam"] = notamList

      alternates.append(obj)
    filteredOFP["alternate"] = alternates

  if data.get("navlog"):
    for item in data["navlog"]:
      obj = { 
        "ident": item.get("ident", ""),
        "name": item.get("name", ""),
        "type": item.get("type", ""), # wpt, vor, ...
        "frequency": item.get("frequency", ""), # vor freq, etc
        "lat": item.get("pos_lat", 0.0),
        "long": item.get("pos_long", 0.0),
        "stage": item.get("stage", ""), # CLB, CRZ, DES
        "via": item.get("via_airway", ""), # SID name, DCT, STAR name, J or V airway?
        "isSidStar": item.get("is_sid_star", ""), # 0 or 1
        "distance": item.get("distance", ""), # leg distance in... miles? 
        "track": item.get("track_true", ""), # true or mag?
        "altitude": item.get("altitude_feet", ""),
        "windComponent": item.get("wind_component", ""),
        "timeLeg": item.get("time_leg", ""), # time duration of the leg
        "timeTotal": item.get("time_total", ""), # total elapsed time upon reaching leg
        "fuelLeg": item.get("fuel_leg", ""), # fuel used in leg
        "fuelTotalUsed": item.get("fuel_total_used", ""), # total fuel used
        "oat": item.get("oat", ""),
        "windDir": item.get("wind_dir", ""), # wind direction at altitude?
        "windSpd": item.get("wind_spd", ""), # wind speed at altitude?
        "shear": item.get("shear", ""), # 0 or 1 for windshear, like a turbulence?
      }
      navlog.append(obj)
    filteredOFP["navlog"] = navlog

  if data.get("aircraft"):
    aircraft = { 
      "icaoCode": data.get("aircraft").get("icao_code", ""), 
      "iataCode": data.get("aircraft").get("iatacode", ""), 
      "baseType": data.get("aircraft").get("base_type", ""),
      "name": data.get("aircraft").get("name", ""),
      "reg": data.get("aircraft").get("reg", ""),
      "selcal": data.get("aircraft").get("selcal", "")
    }
    filteredOFP["aircraft"] = aircraft
  
  if data.get("fuel"):
    fuel = { 
      "block": data.get("fuel").get("plan_ramp", ""),
      "takeoff": data.get("fuel").get("plan_takeoff", ""),
      "landing": data.get("fuel").get("plan_landing", "")
    }
    filteredOFP["fuel"] = fuel
  
  if data.get("times"):
    times = { 
      "ete": data.get("times").get("est_time_enroute", ""),
      "schedDep": data.get("times").get("sched_off", ""),
      "schedArr": data.get("times").get("sched_in", "")
    }
    filteredOFP["times"] = times
  
  if data.get("weights"):
    weights = { 
      "paxCountActual": data.get("weights").get("pax_count_actual", 0),
      "paxWeight": data.get("weights").get("pax_weight", 0),
      "bagWeight": data.get("weights").get("bag_weight", 0),
      "cargo": data.get("weights").get("cargo", 0),
      "estZFW": data.get("weights").get("est_zfw", 0),
      "estTOW": data.get("weights").get("est_tow", 0),
      "estLDW": data.get("weights").get("est_ldw", 0)
    }
    filteredOFP["weights"] = weights
  
  if data.get("weather"):
    weather = { 
      "origMETAR": data.get("weather").get("orig_metar", ""),
      "destMETAR": data.get("weather").get("dest_metar", ""),
      "altnMETAR": data.get("weather").get("altn_metar", "")
    }
    filteredOFP["weather"] = weather
  
  if data.get("files"):
    files = { 
      "directory": data.get("files").get("directory", ""),
      "pdf": data.get("files").get("pdf", "")
    }
    filteredOFP["files"] = files
  return filteredOFP

def getStringValue(data, key):
  value = data.get(key, "")
  if isinstance(value, list) and not value:
    return ""
  return value

def main(id):
  otp = fetchOTP(id)
  filteredOTP = filterOTP(otp)
  return filteredOTP

if __name__ == '__main__':
  temp = 405981
  main(temp)
