# Python program to update
# JSON
 
import json
import requests
import os

API_EDBGS_URL_NONA = "https://elitebgs.app/api/ebgs/v5/factions?id=61894ad88c6309f8d8b83b6c"
API_EDBGS_URL_LAVIGNYLEGION = "https://elitebgs.app/api/ebgs/v5/factions?id=59e7b78cd22c775be0fe6a41"
API_EDBGS_URL_NOVASCIENCETEAM = "https://elitebgs.app/api/ebgs/v5/factions?id=6320d2975ec5c1af81dd9fac"
API_EDBGS_URL_SALUSIMPERIALSOCIETY = "https://elitebgs.app/api/ebgs/v5/factions?id=61ddd8b95ec5c1af81ed3b16"
API_EDBGS_URL_LIKEDEELERMICHEL = "https://elitebgs.app/api/ebgs/v5/factions?id=59e7ce19d22c775be0ff32f0"

# API handling for EDSM --- Collects + processes list of systems with co-ordinates
def getEDSMData(url,category):
    d = requests.get(url)
    if d.status_code == 200:
        data = json.loads(d.text)
        data.pop('coordsLocked')
        data.update({"cat":[category]})
        r = data
    else:
        r = print(f"EDSM API Error: {d.status_code}")
    return r

# API handling for EDBGS --- Collects + processes list of systems with Nova Paresa presence
def getEDBGSData(url):
    responses = []
    d = requests.get(url)
    if d.status_code == 200:
        data = json.loads(d.text)
        rawFactionData = data['docs']
        rawFactionDataArray = rawFactionData[0]
        systemsData = rawFactionDataArray['faction_presence']
        factionName = rawFactionDataArray['name']
        if factionName == "Nova Paresa":
            category = 1
        elif factionName == "Lavigny's Legion":
            category = 2
        elif factionName == "Nova Science Team":
            category = 3
        elif factionName == "Salus Imperial Society":
            category = 4
        elif factionName == "Likedeeler of Michel":
            category = 5
        else:
            print("ERROR: TARGETTED FACTIONS NOT SUPPPORTED YET!")
        for systemData in systemsData:
            EDSMUrlPrefix = "https://www.edsm.net/api-v1/system?systemName="
            EDSMUrlSuffix = "&showCoordinates=1"
            EDSMUrl = EDSMUrlPrefix + systemData['system_name'] + EDSMUrlSuffix
            responses.append(getEDSMData(EDSMUrl,category))
        r = responses
    else:
        r = print(f"EDBGS API Error: {d.status_code}")
    return r

def clear_json(filename='json_samples/factions.json'):
    with open(filename,'w') as file:
        # First we load existing data into a dict.
        Factions = {
            "1": {
                "name": "Nova Paresa",
                "color": "A1A4DB"
            },
            "2": {
                "name": "Lavigny's Legion",
                "color": "7F00FF"
            },
            "3": {
                "name": "Nova Science Team",
                "color": "A0A2DA"
            },
            "4": {
                "name": "Salus Imperial Society",
                "color": "E7CD54"
            },
            "5": {
                "name": "Likedeeler of Michel",
                "color": "D2083A"
            }
        }
        file_data = {"categories":{"Factions":Factions},"systems":[]}
        # convert back to json.
        json.dump(file_data, file, indent=4)

# function to add to JSON
def write_json(new_data, filename='json_samples/factions.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["systems"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

# Retrieve API data
NovaParesaSystemsListEDBGS = getEDBGSData(API_EDBGS_URL_NONA)
LavignyLegionSystemsListEDBGS = getEDBGSData(API_EDBGS_URL_LAVIGNYLEGION)
NovaScienceTeamSystemsListEDBGS = getEDBGSData(API_EDBGS_URL_NOVASCIENCETEAM)
SalusImperialSocietySystemsListEDBGS = getEDBGSData(API_EDBGS_URL_SALUSIMPERIALSOCIETY)
LikedeelerMichelSystemsListEDBGS = getEDBGSData(API_EDBGS_URL_LIKEDEELERMICHEL)

# JSON Cleanup
clear_json()

# Nova Navy system generation
for system in NovaParesaSystemsListEDBGS:
    write_json(system)

# Lavigny's Legion system generation
for system in LavignyLegionSystemsListEDBGS:
    write_json(system)

# Nova Science Team system generation
for system in NovaScienceTeamSystemsListEDBGS:
    write_json(system)

# Salus Imperial Society system generation
for system in SalusImperialSocietySystemsListEDBGS:
    write_json(system)

# Likedeeler of Michel system generation
for system in LikedeelerMichelSystemsListEDBGS:
    write_json(system)