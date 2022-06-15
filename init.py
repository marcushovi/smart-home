import json
import urllib

import requests

users = [
    {'username': 'sobKarsob', 'password': '123456'},
    {'username': 'karlik', 'password': '123456'},
    {'username': 'losKarlos', 'password': '123456'},
    {'username': 'zelvickaJulie', 'password': '123456'}
]

lights_info = [
    {"room": "SobKarsob", "owner": "sobKarsob", "css_id": "levyHorniPokoj"},
    {"room": "Los Karlos", "owner": "losKarlos", "css_id": "pravyHorniPokoj"},
    {"room": "Koupelna", "owner": "every", "css_id": "levaSpolenaMistnost"},
    {"room": "Kuchyne", "owner": "every", "css_id": "pravaSpolecnaMistnost"},
    {"room": "Zelvicka Julie", "owner": "zelvickaJulie", "css_id": "pravyDolniPokoj"},
    {"room": "Karlik", "owner": "karlik", "css_id": "levyDolniPokoj"},
    {"room": "Obyvak", "owner": "every", "css_id": "obyvak"}
]

smart_devices = {}
lights = []
switch_sensors = []
motion_sensors = []

####
# smart lights
####

for i in range(len(lights_info)):
    lights.append(requests.get('https://home_automation.iamroot.eu/newSmartLight').json())
    requests.post(lights[i]['actions']['set_notes_POST'],
                  data=json.dumps(lights_info[i]))

####
# motion sensors
####
motion_sensors.append(requests.get('https://home_automation.iamroot.eu/newMotionSensor').json())
requests.post(motion_sensors[0]['actions']['set_notes_POST'],
              data='{"room": "Kuchyne", "owner":"every"}')
requests.get("http://home_automation.iamroot.eu/device/" + motion_sensors[0][
    'id'] + "/report_url?url=" + urllib.parse.quote_plus(lights[3]['actions']['turn_on']))

motion_sensors.append(requests.get('https://home_automation.iamroot.eu/newMotionSensor').json())
requests.post(motion_sensors[1]['actions']['set_notes_POST'],
              data='{"room": "Obyvak", "owner":"every"}')
requests.get("http://home_automation.iamroot.eu/device/" + motion_sensors[1][
    'id'] + "/report_url?url=" + urllib.parse.quote_plus(lights[6]['actions']['turn_on']))
####
# switch sensor
####
for i in range(len(lights_info)):
    switch_sensors.append(requests.get('https://home_automation.iamroot.eu/newSwitchSensor').json())
    requests.post(switch_sensors[i]['actions']['set_notes_POST'],
                  data=json.dumps(lights_info[i]))
    requests.get("http://home_automation.iamroot.eu/device/" + switch_sensors[i][
        'id'] + "/report_url?url=" + urllib.parse.quote_plus(lights[i]['actions']['toggle_state']))

smart_devices['lights'] = lights
smart_devices['switch_sensors'] = switch_sensors
smart_devices['motion_sensors'] = motion_sensors
