import json
import requests
import os
import time
import sys
from concurrent.futures import ThreadPoolExecutor
import threading

# Lock for file writing
file_lock = threading.Lock()

def clear_json(filename='json_samples/factions.json'):
    with open(filename, 'w') as file:
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
        file_data = {"categories": {"Government": Government}, "systems": []}
        json.dump(file_data, file, indent=4)

def write_json(new_data, filename='json_samples/factions.json'):
    with file_lock:
        with open(filename, 'r+') as file:
            file_data = json.load(file)
            file_data["systems"].append(new_data)
            file.seek(0)
            json.dump(file_data, file, indent=4)

def getEDBGSData(url, pageNumber):
    d = requests.get(url + str(pageNumber))
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
                cat = [1]
            elif allegiance == "federation":
                cat = [2]
            else:
                continue

            systemDict = {"name": systemName, "coords": coords, "cat": cat}
            write_json(systemDict)
        if data['hasNextPage']:
            nextPage = data['nextPage']
            pageNumber += 1
            getEDBGSData(url, pageNumber)
        return True
    else:
        return False

def process_allegiance(url, allegiance):
    print(f"{allegiance} SYSTEMS STARTED AT {time.strftime('%X')}")
    start_time = time.time()
    
    page_number = 1
    getEDBGSData(url,page_number)

    elapsed_time = time.time() - start_time
    print(f"{allegiance} SYSTEMS COMPLETED AT {time.strftime('%X')} (Duration: {elapsed_time:.2f} seconds)", flush=True)

def main():
    clear_json()
    sys.setrecursionlimit(3000)

    allegiance_urls = [
        ("https://elitebgs.app/api/ebgs/v5/systems?allegiance=empire&page=", "IMPERIAL"),
        ("https://elitebgs.app/api/ebgs/v5/systems?allegiance=federation&page=", "FEDERAL"),
        ("https://elitebgs.app/api/ebgs/v5/systems?allegiance=alliance&page=", "ALLIED"),
        ("https://elitebgs.app/api/ebgs/v5/systems?allegiance=independent&page=", "INDEPENDENT"),
    ]

    total_start_time = time.time()  # Record the start time for total duration

    with ThreadPoolExecutor() as executor:
        futures = [executor.submit(process_allegiance, url, allegiance) for url, allegiance in allegiance_urls]

        # Wait for all tasks to complete
        for future in futures:
            future.result()

    total_elapsed_time = time.time() - total_start_time
    print(f"TOTAL DURATION: {total_elapsed_time:.2f} seconds")

    sys.setrecursionlimit(1000)

if __name__ == "__main__":
    main()
