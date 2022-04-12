import json
from tkinter import Widget
import requests
import webbrowser
import jwt
import time
import subprocess

token = 'NzYxZWVhNzAtNTQ4My00MjdhLTkxNjQtMTNiY2E5ZGFhZjJmNDY0YjU2YzItNzU2_PE93_298d3c23-9d31-4483-9cfa-1e6a5288cf32'
gi_id = 'Y2lzY29zcGFyazovL3VybjpURUFNOmV1LWNlbnRyYWwtMV9rL09SR0FOSVpBVElPTi9kNDg0YjExMS02MGUwLTQwNTYtOTQ1Ni1iMjIxZGI1NTJhZmY'
gi_pwd = 'A/kOKIqrHh6Er/tYsVcG1KbN1Owaa2C0qt9jO4dTfjA='

def create_meeting(title, start, end):
    url = "https://webexapis.com/v1/meetings"

    payload = json.dumps({
    "enabledAutoRecordMeeting": False,
    "allowAnyUserToBeCoHost": False,
    "enabledJoinBeforeHost": False,
    "enableConnectAudioBeforeHost": False,
    "excludePassword": True,
    "publicMeeting": False,
    "enabledWebcastView": False,
    "enableAutomaticLock": False,
    "allowFirstUserToBeCoHost": False,
    "allowAuthenticatedDevices": False,
    "sendEmail": False,
    "title": title,
    "start": start,
    "end": end,
    "timezone": "Europe/Vienna"
    })
    headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
    text = response.json()
    print(f"Meeting Created! {text['id']}")
    meetings_db = open('meetings.json', 'r')
    meetings = json.load(meetings_db)
    meetings_db.close()
    if not meetings:
        meetings = list()
    meetings.append(text)
    meetings_db = open('meetings.json', 'w+')
    json.dump(meetings, meetings_db, indent = 4)
    


def add_part(name, mail, meeting_id):
    url = "https://webexapis.com/v1/meetingInvitees"

    payload = json.dumps({
    "email": mail,
    "displayName": name,
    "meetingId": meeting_id,
    "coHost": False,
    "panelist": False,
    "sendEmail": False
    })
    headers = {
    'Authorization': f'Bearer {token}',
    'Content-Type': 'application/json',
}

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.status_code)
    print("participant added")


def goto_meeting(meeting_id):
    meeting_db = open('meetings.json', 'r')
    meetings = json.load(meeting_db)

    for meeting in meetings:
        if meeting['id'] == meeting_id:
            webbrowser.open(meeting['webLink'])
            break


def create_jwt(sub, name):
    payload = {
        "sub":sub,
        "name": name,
        "iss": gi_id,
        "exp" : int(time.time())+3600*8
    }

    return jwt.encode(payload, gi_pwd, algorithm='HS256')


def token_exchange(jwt):
    header = {'Authorization': f'Bearer {jwt}'}
    resp = requests.post('https://webexapis.com/v1/jwt/login', headers=header)
    return resp.json()


def goto_widget(meeting, token):
    widget = f"""import logo from './logo.svg';
                import './App.css';

                import {{WebexMeetingsWidget}} from '@webex/widgets';

                import '@webex/widgets/dist/css/webex-widgets.css';

                export default function App() {{
                return (
                    <WebexMeetingsWidget
                    style={{{{width: "1000px", height: "500px"}}}} // Substitute with any arbitrary size or use `className`
                    accessToken="Bearer {token}"
                    meetingDestination= "{meeting}"
                    />
                );
                }}
                """
    with open('src/App.js', 'w+') as app:
        app.write(widget)
    subprocess.run(['npm', 'start'])


def shell():
    print('ich.app demoscript: ')
    help = '''
    1. create meeting (title, start, end)   -> create <title>, <start>, <end>
    2. add participant (name, mail, meeting_id) -> add <name>, <mail>, <meeting_id>
    3. goto meeting (meeting_id) -> goto <meeting_id>
    4. exit
    5. help -> display this help

    '''
    while True:
        inp = input('> ')
        inp = inp.split(' ')
        if inp[0] == 'exit':
            break
        elif inp[0] == 'create':
            create_meeting(inp[1], inp[2], inp[3])
        elif inp[0] == 'add':
            add_part(inp[1], inp[2], inp[3])
        elif inp[0] == 'goto':
            goto_meeting(inp[1])
        elif inp[0] == 'help':
            print(help)
        
def main():
    shell()



if __name__ == '__main__':
    #main()
    #print(token_exchange('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ0ZXN0dXNlciIsIm5hbWUiOiJKb2huIERvZSIsImlzcyI6IlkybHpZMjl6Y0dGeWF6b3ZMM1Z5YmpwVVJVRk5PbVYxTFdObGJuUnlZV3d0TVY5ckwwOVNSMEZPU1ZwQlZFbFBUaTlrTkRnMFlqRXhNUzAyTUdVd0xUUXdOVFl0T1RRMU5pMWlNakl4WkdJMU5USmhabVkiLCJleHAiOjE2NDk4MTcxOTV9.Y501Rvd3JvLI30o9KRWMCjAuAhOZ0A1-70YE-_5oMLs'))
    goto_widget('alex@kbgc.eu', 'NTVjYzFmNTItMWM1NC00ZmFlLWE0NWYtN2EyYmQxMGU5ZmNkOTdhYzRkMTQtZGZl_PE93_d484b111-60e0-4056-9456-b221db552aff')