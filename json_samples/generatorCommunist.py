# Python program to update communist.json file
 
import json
import requests
import os
import time
import sys

def clear_json(filename='json_samples/communist.json'):
    with open(filename,'w') as file:
        # First we load existing data into a dict.
        Government = {
            "1": {
                "name": "Communist Systems",
                "color": "CC0000"
            },
            "2": {
                "name": "Federal Systems",
                "color": "0000EF"
            }
        }
        file_data = {"categories":{"Government":Government},"systems":[]}
        # convert back to json.
        json.dump(file_data, file, indent=4)

# function to add to JSON
def write_json(new_data, filename='json_samples/communist.json'):
    with open(filename,'r+') as file:
        # First we load existing data into a dict.
        file_data = json.load(file)
        # Join new_data with file_data inside emp_details
        file_data["systems"].append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # convert back to json.
        json.dump(file_data, file, indent = 4)

# API handling for EDBGS --- Collects + processes list of systems with Nova Paresa presence
def getEDBGSData(url,pageNumber):
    d = requests.get(url+str(pageNumber))
    if d.status_code == 200:
        data = json.loads(d.text)
        rawSystemData = data['docs']
        for rawSystemDataArray in rawSystemData:
            systemName = rawSystemDataArray['name']
            coords = {
                "x": rawSystemDataArray['x'],
                "y": rawSystemDataArray['y'],
                "z": rawSystemDataArray['z']
            }
            government = rawSystemDataArray['government']
            allegiance = rawSystemDataArray['allegiance']
            if government == "$government_communism;":
                cat = [
                    1
                ]
            elif allegiance == "federation":
                cat = [
                    2
                ]
            else:
                break
            systemDict={"name":systemName,"coords":coords,"cat":cat}
            write_json(systemDict)
        if data['hasNextPage'] == True:
            nextPage = data['nextPage']
            pageNumber = pageNumber+1
            getEDBGSData(url,pageNumber)
        rslt = True
    else:
        rslt = False
    return rslt

def main():
    print(f"IMPERIAL SYSTEMS STARTED AT {time.strftime('%X')}")
    if getEDBGSData("https://elitebgs.app/api/ebgs/v5/systems?allegiance=empire&page=",1) == True:
        
        print(f"IMPERIAL SYSTEMS COMPLETED AT {time.strftime('%X')}")
        time.sleep(2)

        print(f"FEDERAL SYSTEMS STARTED AT {time.strftime('%X')}")
        if getEDBGSData("https://elitebgs.app/api/ebgs/v5/systems?allegiance=federation&page=",1) == True:
            
            print(f"FEDERAL SYSTEMS COMPLETED AT {time.strftime('%X')}")
            time.sleep(2)
            
            print(f"ALLIED SYSTEMS STARTED AT {time.strftime('%X')}")
            if getEDBGSData("https://elitebgs.app/api/ebgs/v5/systems?allegiance=alliance&page=",1) == True:
                
                print(f"ALLIED SYSTEMS COMPLETED AT {time.strftime('%X')}")
                time.sleep(2)

                print(f"INDEPENDENT SYSTEMS STARTED AT {time.strftime('%X')}")
                if getEDBGSData("https://elitebgs.app/api/ebgs/v5/systems?allegiance=independent&page=",1) == True:
                    
                    print(f"INDEPENDENT SYSTEMS COMPLETED AT {time.strftime('%X')}")

                    print("ALL GENERATION HAS COMPLETED")

clear_json()
sys.setrecursionlimit(3000)
main()
sys.setrecursionlimit(1000)