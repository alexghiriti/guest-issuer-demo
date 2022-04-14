import json
import traceback
import requests
import webbrowser
import jwt
import time
import base64

creds = None
with open('credentials.json', 'r') as c:
    creds = json.load(c)

int_creds = creds['integration_creds']
gi_creds = creds['guest_issuer']
token = creds['token']


def create_meeting(title: str, start, end):
    url = "https://webexapis.com/v1/meetings"

    payload = json.dumps({
    "enabledAutoRecordMeeting": False,
    "allowAnyUserToBeCoHost": False,
    "enabledJoinBeforeHost": True,
    "enableConnectAudioBeforeHost": False,
    "excludePassword": True,
    "publicMeeting": False,
    "enabledWebcastView": False,
    "enableAutomaticLock": False,
    "allowFirstUserToBeCoHost": False,
    "allowAuthenticatedDevices": False,
    "sendEmail": False,
    "title": title.replace('_', ' '),
    "start": start,
    "end": end,
    "timezone": "Europe/Vienna"
    })
    headers = {
    'Authorization': f'Bearer {token["access_token"]}',
    'Content-Type': 'application/json',
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    print(f"\nPOST\nURL:     {url}\nHEADERS: {headers}\nPAYLOAD: {payload}\n\nResponse\n")
    text = response.json()
    print(f"Meeting Created! {text['id']}, Meeting No: {text['meetingNumber']}")
    meetings = list()
    try:
        meetings_db = open('meetings.json', 'r')
        meetings = json.load(meetings_db)
        meetings_db.close()
    except FileNotFoundError as e:
        print(e)
    meetings.append(text)
    meetings_db = open('meetings.json', 'w+')
    json.dump(meetings, meetings_db, indent = 4)

def login():
    webbrowser.open(int_creds['auth_uri'])

def authorize(code):
    url = "https://webexapis.com/v1/access_token"

    payload = json.dumps({
    "grant_type": int_creds['grant_type'],
    "client_id": int_creds['client_id'],
    "client_secret": int_creds['client_secret'],
    "code": code,
    "redirect_uri": int_creds['redirect_uri']
    })
    headers = {
    'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"\nPOST\nURL:     {url}\nHEADERS: {headers}\nPAYLOAD: {payload}\n\nResponse\n")
    print(response.json())
    token = response.json()
    data = ''
    with open('credentials.json', 'r+') as c:
        data = json.load(c)
    with open('credentials.json', 'w+') as c:
        data['token'] = token
        json.dump(data, c, indent=4)

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
    'Authorization': f'Bearer {token["access_token"]}',
    'Content-Type': 'application/json',
}

    response = requests.request("POST", url, headers=headers, data=payload)
    print(f"\nPOST\nURL:     {url}\nHEADERS: {headers}\nPAYLOAD: {payload}\n\nResponse\n")
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
        "iss": gi_creds['gi_id'],
        "exp" : int(time.time())+3600*8

    }
    decoded_secret =base64.b64decode(gi_creds['gi_secret'])
    code = jwt.encode(payload, decoded_secret, algorithm='HS256')
    print(code)
    return code


def token_exchange(jwt):
    headers = {'Authorization': f'Bearer {jwt}'}
    url = 'https://webexapis.com/v1/jwt/login'
    resp = requests.post(url, headers=headers)
    print(f"\nPOST\nURL:     {url}\nHEADERS: {headers}\nPAYLOAD: {''}\n\nResponse\n")
    print(resp.json())
    return resp.json()
    


def create_widget(meeting, token):
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


def shell():
    print('ich.app demoscript: ')
    help = '''
    Description -> Command

    1.  create meeting (title, start, end)   -> create <title>, <start>, <end>
    2.  add participant (name, mail, meeting_id) -> add <name>, <mail>, <meeting_id>
    3.  goto meeting (meeting_id) -> goto <meeting_id>
    4.  exit the programm -> exit
    5.  help -> display this help
    6.  issue guest ticket -> jwt <sub> <name>
    7.  exchange guest ticket for for access token -> exchange <jwt>
    8.  create widget -> widget <meeting> <token>
    9.  authorize webex integration -> login
    10. create oauth access token -> auth <code>

    '''
    while True:
        try:
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
            elif inp[0] == 'jwt':
                create_jwt(inp[1], inp[2])
            elif inp[0] == 'exchange':
                token_exchange(inp[1])
            elif inp[0] == 'widget':
                create_widget(inp[1], inp[2])
            elif inp[0] == 'login':
                login()
            elif inp[0] == 'auth':
                authorize(inp[1])
        except KeyboardInterrupt as e:
            exit()
        except Exception as e:
            print(traceback.format_exc())

        
def main():
    shell()



if __name__ == '__main__':
    main()