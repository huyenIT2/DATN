import os
import base64
import requests
import json
def read_json():
    endpoint = "http://localhost:9200"
    # Encode the username and password

    credentials = base64.b64encode(b'elastic:fJI8JOlpqnlk1lacO8=c').decode('utf-8')
    # Set the headers for the request
    token = {"Authorization" : f"Basic {credentials}"}
    # Send the GET request
    response = requests.get(endpoint, headers=token, timeout=10)
    # Check for a successful request
    if response.status_code != 200:
        print(response.status_code)
        raise Exception("Request failed with status code {}".format(response.status_code))
    # Return the JSON object
    return response.json()
if __name__ == "__main__":
    # get response and create JSON file
    json_file = json.dumps(read_json(), indent=4)
    with open('some-file.json', 'w') as f:
        f.write(json_file)