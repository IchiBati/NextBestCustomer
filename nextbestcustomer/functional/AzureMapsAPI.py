import time
import requests
import json
import os


azure_key = os.environ["azure_maps_key"]

def wait_for_result(apiurl: str, max_attemtps=10, waittime=2):
    attempts = 0

    while attempts < max_attemtps:

        response = requests.get(apiurl)

        if response.status_code == 200:
            return response.json()

        elif response.status_code == 202:
            time.sleep(waittime)
            attempts += 1

        else:
            return None


def post_routematrix_http(lat, long, destination_geojson):
    try:

        geojson_dumps = json.dumps(destination_geojson)

        headers = {"Content-Type": "application/json"}

        computed_route_response = requests.post(
            f"https://atlas.microsoft.com/route/matrix/sync/json?api-version=1.0&subscription-key={azure_key}",
            data=geojson_dumps,
            headers=headers)

        computed_route_response.raise_for_status()

        if computed_route_response.status_code == 200:
            return computed_route_response.json()

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        # Handle specific HTTP errors if needed
        return None
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        # Handle other request exceptions if needed
        return None


def get_reverse_address(lat, long):
    try:
        address_reponse = requests.get(
            f"https://atlas.microsoft.com/search/address/reverse/json?api-version=1.0&query={lat}, {long}&subscription-key={azure_key}"
        )
        address_reponse.raise_for_status()

        if address_reponse.status_code == 200:
            return address_reponse.json()["addresses"][0]['address']

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        # Handle specific HTTP errors if needed
        return None
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        # Handle other request exceptions if needed
        return None


def get_reverse_address_batch(input_data):
    api_body_dump = json.dumps(input_data)
    try:
        headers = {"Content-Type": "application/json"}
        api_response = requests.post(
            f"https://atlas.microsoft.com/search/address/reverse/batch/sync/json?api-version=1.0&subscription-key={azure_key}",
            data=api_body_dump,
            headers=headers
        )

        api_response.raise_for_status()

        if api_response.status_code == 200:
            repsonse_json = api_response.json()['batchItems']
            return repsonse_json

    except requests.exceptions.HTTPError as errh:
        print(f"HTTP Error: {errh}")
        # Handle specific HTTP errors if needed
        return None
    except requests.exceptions.RequestException as err:
        print(f"Request Exception: {err}")
        # Handle other request exceptions if needed
        return None
