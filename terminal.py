import requests
import sys

link = sys.argv[1]
serial = sys.argv[2]


def sendCommand(command):
    r = requests.post(f'http://{link}/device/{serial}', data="{\"command\": \"" + command + "\"}")
    if r.status_code != 200: print(f'{r.status_code}: {r.text}')

    print(r.json().get('status'), r.json().get('result'))


while True:
    try:
        sendCommand(input('>>> '))
    except KeyboardInterrupt: break