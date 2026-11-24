import requests
from datetime import datetime
from pydantic import BaseModel

# data fetching helpers as simbrief values are all string

def isBlank(value):
  return value is None or value is False or value == "" or value == [] or value == {}

def getStr(data, key, default=""):
  value = data.get(key, default)
  return default if isBlank(value) else str(value)

def getInt(data, key, default=0):
  value = data.get(key, default)
  if isBlank(value):
    return default
  try:
    return int(float(value))
  except (TypeError, ValueError):
    return default

def getFloat(data, key, default=0.0):
  value = data.get(key, default)
  if isBlank(value):
    return default
  try:
    return float(value)
  except (TypeError, ValueError):
    return default

def getBool(data, key, default=False):
  value = data.get(key, default)
  if isBlank(value):
    return default
  if isinstance(value, str):
    return value.strip().lower() in ("1", "true", "yes")
  return bool(value)

def getDate(data, key, default=None):
  value = data.get(key, default)
  return default if isBlank(value) else value

def getStrList(data, key):
  value = data.get(key, [])
  if isBlank(value):
    return []
  if isinstance(value, list):
    return [str(v) for v in value if not isBlank(v)]
  return [str(value)]

class Fetch(BaseModel):
  userID: int = 0
  status: str = ""
  time: float = 0.0

class Params(BaseModel):
  requestID: str = ""
  userID: str = ""
  ofpLayout: str = ""
  airac: str = ""
  units: str = ""

class General(BaseModel):
  airline: str = "" #AAL
  flightNumber: str = "" #1234
  cruiseProfile: str = "" #CI 14
  alternateProfile: str = "" #CI0
  costIndex: int = 0 #14
  initialAltitude: int = 0 #39000
  airDistance: int = 0 #340
  passengers: int = 0 #123
  route: str = "" #dep fix DCT fix DCT arr
  routeIFPS: str = ""
  routeNavigraph: str = ""

class ATIS(BaseModel):
  network: str = "" #pilotedge
  issued: datetime | None = None
  letter: str = "" #X
  phonetic: str = "" #X-RAY
  type: str = "" #DEP/ARR
  message: str = "" #long atis

class NOTAM(BaseModel):
  accountID: str = ""
  notamID: str = ""
  locationID: str = ""
  locationICAO: str = ""
  locationName: str = ""
  locationType: str = ""
  dateEffective: datetime | None = None
  dateExpire: datetime | None = None
  notamText: str = ""
  notamQcodeCategory: str = ""
  notamQcodeSubject: str = ""
  notamQcodeStatus: str = ""
  notamIsObstacle: bool = False

class Airport(BaseModel):
  icaoCode: str = ""
  iataCode: str = ""
  faaCode: str = ""
  elevation: int = 0
  lat: float = 0.0
  long: float = 0.0
  name: str = ""
  planRwy: str = ""
  transAlt: int = 0
  transLevel: int = 0
  metar: str = ""
  metarTime: datetime | None = None
  metarCategory: str = ""
  metarVisibility: int = 0
  metarCeiling: int = 0
  atis: list[ATIS] = []
  notam: list[NOTAM] = []

class Alternate(Airport):
  cruiseAltitude: int = 0
  airDistance: int = 0
  trackTrue: int = 0
  trackMag: int = 0
  avgWindComp: str = "" # M011 / P011 (minus/plus)
  avgWindDir: int = 0
  avgWindSpd: int = 0
  ete: str = "" # HH:MM:SS
  route: str = ""
  routeIFPS: str = ""
  routeNavigraph: str = ""

class Fix(BaseModel):
  ident: str = ""
  name: str = ""
  type: str = "" # wpt, vor, ...
  frequency: str = "" # vor freq, etc. kept as str to preserve formatting (116.80)
  lat: float = 0.0
  long: float = 0.0
  stage: str = "" # CLB, CRZ, DES
  via: str = "" # SID name, DCT, STAR name, J or V airway?
  isSidStar: bool = False
  distance: int = 0 # leg distance in nm
  track: int = 0 # true track
  altitude: int = 0
  windComponent: int = 0
  timeLeg: str = "" # HH:MM:SS duration of the leg
  timeTotal: str = "" # HH:MM:SS total elapsed time upon reaching leg
  fuelLeg: int = 0 # fuel used in leg
  fuelTotalUsed: int = 0 # total fuel used
  oat: int = 0
  windDir: int = 0 # wind direction at altitude
  windSpd: int = 0 # wind speed at altitude
  shear: int = 0 # wind shear value

class Aircraft(BaseModel):
  icaoCode: str = ""
  iataCode: str = ""
  baseType: str = ""
  name: str = ""
  reg: str = ""
  selcal: str = ""

class Fuel(BaseModel):
  block: int = 0
  takeoff: int = 0
  landing: int = 0

class Times(BaseModel):
  ete: str = "" # HH:MM:SS
  schedDep: datetime | None = None
  schedArr: datetime | None = None

class Weights(BaseModel):
  paxCountActual: int = 0
  paxWeight: int = 0
  bagWeight: int = 0
  cargo: int = 0
  estZFW: int = 0
  estTOW: int = 0
  estLDW: int = 0

class Weather(BaseModel):
  origMETAR: str = ""
  destMETAR: str = ""
  altnMETAR: list[str] = []

class PDF(BaseModel):
  name: str = ""
  link: str = ""

class Files(BaseModel):
  directory: str = ""
  pdf: PDF = PDF()

def fetchOTP(id):
  url = f"https://www.simbrief.com/api/xml.fetcher.php?userid={id}&json=v2" # id: 405981
  response = requests.get(url)
  responseJSON = response.json()
  return responseJSON

def buildATISList(airportData):
  atisList = []
  for atis in airportData.get("atis") or []:
    atisList.append(ATIS(
      network=getStr(atis, "network"),
      issued=getDate(atis, "issued"),
      letter=getStr(atis, "letter"),
      phonetic=getStr(atis, "phonetic"),
      type=getStr(atis, "type"),
      message=getStr(atis, "message")
    ))
  return atisList

def buildNOTAMList(airportData):
  notamList = []
  for notam in airportData.get("notam") or []:
    notamList.append(NOTAM(
      accountID=getStr(notam, "account_id"),
      notamID=getStr(notam, "notam_id"),
      locationID=getStr(notam, "location_id"),
      locationICAO=getStr(notam, "location_icao"),
      locationName=getStr(notam, "location_name"),
      locationType=getStr(notam, "location_type"),
      dateEffective=getDate(notam, "date_effective"),
      # date_expire is False for PERM notams
      dateExpire=getDate(notam, "date_expire", "2099-12-31T11:59:00Z"),
      notamText=getStr(notam, "notam_text"),
      notamQcodeCategory=getStr(notam, "notam_qcode_category"),
      notamQcodeSubject=getStr(notam, "notam_qcode_subject"),
      notamQcodeStatus=getStr(notam, "notam_qcode_status"),
      notamIsObstacle=getBool(notam, "notam_is_obstacle")
    ))
  return notamList

def airportFields(airportData):
  # shared fields for origin, destination and alternates
  return dict(
    icaoCode=getStr(airportData, "icao_code"),
    iataCode=getStr(airportData, "iata_code"),
    faaCode=getStr(airportData, "faa_code"),
    elevation=getInt(airportData, "elevation"),
    lat=getFloat(airportData, "pos_lat"),
    long=getFloat(airportData, "pos_long"),
    name=getStr(airportData, "name"),
    planRwy=getStr(airportData, "plan_rwy"),
    transAlt=getInt(airportData, "trans_alt"),
    transLevel=getInt(airportData, "trans_level"),
    metar=getStr(airportData, "metar"),
    metarTime=getDate(airportData, "metar_time"),
    metarCategory=getStr(airportData, "metar_category"),
    metarVisibility=getInt(airportData, "metar_visibility"),
    metarCeiling=getInt(airportData, "metar_ceiling"),
    atis=buildATISList(airportData),
    notam=buildNOTAMList(airportData)
  )

def filterOTP(otp):
  data = otp

  filteredOFP = {}

  if data.get("fetch"):
    fetchData = data.get("fetch")
    filteredOFP["fetch"] = Fetch(
      userID=getInt(fetchData, "userid"),
      status=getStr(fetchData, "status"),
      time=getFloat(fetchData, "time")
    )

  if data.get("params"):
    paramData = data.get("params")
    filteredOFP["params"] = Params(
      requestID=getStr(paramData, "request_id"),
      userID=getStr(paramData, "user_id"),
      ofpLayout=getStr(paramData, "ofp_layout"),
      airac=getStr(paramData, "airac"),
      units=getStr(paramData, "units")
    )

  if data.get("general"):
    generalData = data.get("general")
    filteredOFP["general"] = General(
      airline=getStr(generalData, "icao_airline"),
      flightNumber=getStr(generalData, "flight_number"),
      cruiseProfile=getStr(generalData, "cruise_profile"),
      alternateProfile=getStr(generalData, "alternate_profile"),
      costIndex=getInt(generalData, "costindex"),
      initialAltitude=getInt(generalData, "initial_altitude"),
      airDistance=getInt(generalData, "air_distance"),
      passengers=getInt(generalData, "passengers"),
      route=getStr(generalData, "route"),
      routeIFPS=getStr(generalData, "route_ifps"),
      routeNavigraph=getStr(generalData, "route_navigraph")
    )

  if data.get("origin"):
    filteredOFP["origin"] = Airport(**airportFields(data.get("origin")))

  if data.get("destination"):
    filteredOFP["destination"] = Airport(**airportFields(data.get("destination")))

  if data.get("alternate"):
    alternateData = data.get("alternate")
    # a single alternate may come back as a dict instead of a list
    if isinstance(alternateData, dict):
      alternateData = [alternateData]
    alternates = []
    for item in alternateData:
      alternates.append(Alternate(
        **airportFields(item),
        cruiseAltitude=getInt(item, "cruise_altitude"),
        airDistance=getInt(item, "air_distance"),
        trackTrue=getInt(item, "track_true"),
        trackMag=getInt(item, "track_mag"),
        avgWindComp=getStr(item, "avg_wind_comp"),
        avgWindDir=getInt(item, "avg_wind_dir"),
        avgWindSpd=getInt(item, "avg_wind_spd"),
        ete=getStr(item, "ete"),
        route=getStr(item, "route"),
        routeIFPS=getStr(item, "route_ifps"),
        routeNavigraph=getStr(item, "route_navigraph")
      ))
    filteredOFP["alternate"] = alternates

  if data.get("navlog"):
    navlogData = data.get("navlog")
    navlog = []
    for item in navlogData:
      navlog.append(Fix(
        ident=getStr(item, "ident"),
        name=getStr(item, "name"),
        type=getStr(item, "type"),
        frequency=getStr(item, "frequency"),
        lat=getFloat(item, "pos_lat"),
        long=getFloat(item, "pos_long"),
        stage=getStr(item, "stage"),
        via=getStr(item, "via_airway"),
        isSidStar=getBool(item, "is_sid_star"),
        distance=getInt(item, "distance"),
        track=getInt(item, "track_true"),
        altitude=getInt(item, "altitude_feet"),
        windComponent=getInt(item, "wind_component"),
        timeLeg=getStr(item, "time_leg"),
        timeTotal=getStr(item, "time_total"),
        fuelLeg=getInt(item, "fuel_leg"),
        fuelTotalUsed=getInt(item, "fuel_totalused"),
        oat=getInt(item, "oat"),
        windDir=getInt(item, "wind_dir"),
        windSpd=getInt(item, "wind_spd"),
        shear=getInt(item, "shear")
      ))
    filteredOFP["navlog"] = navlog

  if data.get("aircraft"):
    aircraftData = data.get("aircraft")
    filteredOFP["aircraft"] = Aircraft(
      icaoCode=getStr(aircraftData, "icao_code"),
      iataCode=getStr(aircraftData, "iatacode"),
      baseType=getStr(aircraftData, "base_type"),
      name=getStr(aircraftData, "name"),
      reg=getStr(aircraftData, "reg"),
      selcal=getStr(aircraftData, "selcal")
    )

  if data.get("fuel"):
    fuelData = data.get("fuel")
    filteredOFP["fuel"] = Fuel(
      block=getInt(fuelData, "plan_ramp"),
      takeoff=getInt(fuelData, "plan_takeoff"),
      landing=getInt(fuelData, "plan_landing")
    )

  if data.get("times"):
    timesData = data.get("times")
    filteredOFP["times"] = Times(
      ete=getStr(timesData, "est_time_enroute"),
      schedDep=getDate(timesData, "sched_off"),
      schedArr=getDate(timesData, "sched_in")
    )

  if data.get("weights"):
    weightsData = data.get("weights")
    filteredOFP["weights"] = Weights(
      paxCountActual=getInt(weightsData, "pax_count_actual"),
      paxWeight=getInt(weightsData, "pax_weight"),
      bagWeight=getInt(weightsData, "bag_weight"),
      cargo=getInt(weightsData, "cargo"),
      estZFW=getInt(weightsData, "est_zfw"),
      estTOW=getInt(weightsData, "est_tow"),
      estLDW=getInt(weightsData, "est_ldw")
    )

  if data.get("weather"):
    weatherData = data.get("weather")
    filteredOFP["weather"] = Weather(
      origMETAR=getStr(weatherData, "orig_metar"),
      destMETAR=getStr(weatherData, "dest_metar"),
      altnMETAR=getStrList(weatherData, "altn_metar")
    )

  if data.get("files"):
    filesData = data.get("files")
    pdfData = filesData.get("pdf") or {}
    filteredOFP["files"] = Files(
      directory=getStr(filesData, "directory"),
      pdf=PDF(
        name=getStr(pdfData, "name"),
        link=getStr(pdfData, "link")
      )
    )

  return filteredOFP

def main(id):
  otp = fetchOTP(id)
  filteredOTP = filterOTP(otp)
  return filteredOTP

if __name__ == '__main__':
  temp = 405981
  main(temp)
