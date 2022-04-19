# Webex x ich.app POC

Diese Repository dient als "prove-of-concept" für eine Integration zwischen einer Authentifizierungssoftware und der Webex umgebung. Ziel des Projektes ist es, Unternehmen mehr Kontrolle und Sicherheit zu gewährleisten, indem man (vorallem Unternehmensexterne) Meeting-Teilnehmer über sichere dritte Stelle authentifiziert bevor diese ein Meeting beitreten. Auf diesen Grund kann "Inpersonation" weitensgehend verhindert werden, was es sicherer macht, sensible Informationen weiter zu geben. Auch die Meetings an sich werden sicherer, weil Meeting Inforamtionen nicht direkt mit User geteilt werden. Sollten diese dennoch freigegeben werden, sind nicht-authentifizierte Benutzer trotzdem nicht in der Lage ein gesichertes Meeting beizutreten. 

## Dokumentation
Folgend werden die technischen Aspekte der Integration im Einzelnen beschrieben, erklärt und begründet. Das System besteht aus mehreren, von einander unabhängigen Bauteile nämlich:

1. Meeting Creation
2. Invite Creation
3. Authentication Landing Page
4. Authorization Server
5. Webex Meetings React Widget

Das Projekt wird immer aus der sicht zweier Aktoren beschrieben, der Meeting-erstellen und der Meeting Teilnehmer.

### Meeting Creation
Als erster Schritt muss ein Meeting erzeugt werden. Es gäbe die möglichkeit Meetings auch über die von Webex bereitgestellten Tools (Outlook scheduler, Webex-Site etc. ) zu erstellen. Damit aber die höchste Sicherheit erreicht werden kann. werden die Meetings über die Webex API erstellt. Dau wird eine Eigene Web App benötigt, die ein Erstellungsformular bereitstellt.
##### API Kommunikation
Um mit der API zu kommunizieren benötigt der erstellende Benutzer ein Lizensiertes Webex-Account. Die Standardlizensierung genügt. Die REST API verwendet als Authorizierung den OAuth 2.0 Standard.  

![API Sequenzdi](http://placehold.jp/3d4070/ffffff/500x500.png)

Das obige Sequenzdiagramm Zeigt den Datenfluss zwichen User, App und die Webex Server. Als ersten Schritt, nachdem ein Meeting-Ersteller die URL der App navigiert ist ein neuer Access Token zu erzeugen. Dazu sollte die App auf die Authentication-Page unserer Webex Integration zeigen. Diese wird ergeugt nachdem eine Integration auf developer.webex.com erstellt wird. Die Integration muss einmalig vom App ersteller Erzeugt werden diese ist dann allgemein gültig für alle Webex-Organizationen. Nachdem der User sich erfolgreich mit seinen Webex-Credentials angemeldet hat, wird ein Authorization Code erzeugt und per redirect an einen von uns erstellten Endpoint gesendet. Der Code wird dann per POST request gegen einen OAuth Bearer Token getauscht. Der Token ist standardmäßig 14 Tage lang gültig, kann aber mittels refresh token immer wieder refreshed werden. Mit diesem Token können nun per API Meetings erzeugt werden. 
##### Das Meeting
Meetings werden über den Meetings Enpoint erzeugt, die Dokumentation dieses Endpoints findet man [hier](https://developer.webex.com/docs/api/v1/meetings/create-a-meeting). Es werden folgende Parameter verwendet:
```
{
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
"title": <title>,
"start": <start>,
"end": <end>,
"timezone": "Europe/Vienna"
}
```
`excludePassword` und `publicMeeting` stellen sicher, dass keine unerwünschten Teilnehmer das Meeting Teilehmen können. das Password darf nicht weitergegeben werden. Da man damit die Meetings auch ohne sich vorher zu registrieren, erstellen könnte. Im Erfolgsfall erhält man eine JSON-Antwort retour mit dem Meeting details. Wichtig für das Projekt ist die 11-Stellige Meetingnummer unter `"meetingNumber": "xxxxxxxxxxx"`. Die erzeugten Meetings sind nun so gesperrt, dass Sie keine Teilnehmer außer den erzuger selbst den Beitritt erlauben. Die Meetings gemeinsam mit den Access Token der Sie erzeugt hat müssen Serverseitig gesichert werden. 
### Invite Creation
Da man kein Einfluss über die eigenen Invitations von Webex nehmen kann, müssen eigene Invitations erstellt werden. Dazu wird nach dem Erstellen des Meetings zu einen neuen Formular weitergeleitet. Der Erstellende User wir hier gebeten, die E-Mail seiner Teilnehmer bekannt zu geben. Aus diesen E-Mails wird dann die interne Teilnehmerliste erzeugt. Die Teilnehmer erhalten dann die Meetingeinladung per E-Mail als .ics
  


## Inbetriebnahme
### Step-by-Step installation
Step-by-Step Anleitung für die Inbetriebnahme des Projekts
##### Step 1 Admin Rechte
Die Webapp kann auf allen gängigen Betriebsysteme ausgeführt werden. Ggf. werden Admin Rechte benötigt für die Installation der nötigen Software.
##### Step 2 Node.js installieren
Die Webapp basiert auf React, somit wird node.js benötigt. Die App läuft in der jetzigen Form nur mit der LTS version (16.14.2 LTS). Download link: https://nodejs.org/en/download/
##### Step 3 Python installieren
Das Projekt und bestimmte module benötigen Python3. Unter Windows kann während der Installation folgende Option gesetzt werden damit Python3 gleich mitinstalliert wird. 
_insert picture here_
Sonnst kann Python auch über der offiziellen Website heruntergeladen und installiert werden:
https://www.python.org/downloads. Sollte python unter Windows in dieser weise installiert werden, muss die executable zum "PATH" als system variable hinzugefügt werden. Das erledigt der installer wenn folgende option gesetzt wird.
_insert_another_pic_here_
##### Step 3.5 PC Neustart
Ein Neustart ist nicht immer notwendig, jenachdem was man alles bereits installiert gehabt hat. Falls alles frisch unter Windows installiert wurde, wird ein neustart empfolen. 
##### Step 4 Diese Repository Clonen
Sollte git vorhanden sein kann diese Repository einfach über:
 
`git clone https://github.com/alexghiriti/guest-issuer-demo.git` 

ansonsten unter Code auf ZIP hrunterladen clicken und irgendwo entpacken. 
##### Step 5 Dependenicies Installieren
Ein neues Admin-Terminal Fenster öffen, in den Projektordner navigieren und folgende Commands ausführen:

Webex Widget packages installieren mit:
``npx install-peerdeps @webex/widgets``
Python dependencies installieren mit:
``pip install -r .\requirements.txt``
npm dependencies installieren mit:
``npm install``
Bei SSL issues:
``npm config set strict-ssl false``
##### Step 6 Programm Starten
Sobald alles installiert ist kann das Pythonskript über folgenden Kommand (dasselbe Terminal benutzen) ausgeführt werden:
``py main.py``

### Bedienung des Python Skripts
Das Skript verfügt über einen CMD und versteht 10 commands: 

1. create meeting (title, start, end) -> `create <title>, <start>, <end>`
2. add participant (name, mail, meeting_id) -> `add <name>, <mail>, <meeting_id>`
3. goto meeting (meeting_id) -> ``goto <meeting_id>``
4. exit the programm -> ``exit``
5. help -> ``display this help``
6. issue guest ticket -> ``jwt <sub> <name>``
7. exchange guest ticket for for access token -> ``exchange <jwt>``
8. create widget -> ``widget <meeting> <token>``
9. authorize webex integration -> ``login``
10. create oauth access token -> ``auth <code>``

Um das Widget zu starten und einen User zu authorisieren werden folgende Kommands in dieser Reihenfolge, benötigt.

1. `login` - Öffnet ein Webex Login Fenster. Hier kann man die Webex Integration Authorizieren damit man einen Zugang zu der Webex API bekommt. Falls das Erfolgreich gewesen ist wird auf der Seite einen Code angezeigt.
2. `auth <code>` - Dieser Code (Lifetime 30 min) kann für einen OAuth2 Bearer Access Token getauscht werden. Im erfolgsfall wird dieser Token automatisch in `credentials.json` gespeichert.
3. (optional) `create <title> <start> <end>` - Es kann nun einen Meeting erstellt werden. `<title>` ist der Namen  des Meetings (Namen die aus meheren Wörter bestehen werden mit "_" notiert z.B.: Mein_Meeting = Mein Meeting). `<start> / <end>` bezeichnen das Start- und Enddatum des meetings in ISO-Format yyyy-mm-ddTHH:MM:SS (2022-03-15T12:30:00)
4. ``jwt <sub> <name>`` - Damit kann einen Guest Token erstellt werden. `<sub>` ist ein eindeutiger identifier und kann benutzt werden um user intern zu identifizieren. `<name>` ist der Anzeigenamen des Users. Spaces werden mit "_" dargestellt (z.B.: John_Doe=John Doe)
5. ``exchange <jwt>`` - Damit ein User einem Meeting beitreten kann muss dieser jwt gegen einen Bearer Access Token getauscht werden. Im Erfolgsfall wird hier eien Token zurückgegeben.
6. `Exchange <jwt>` - Der Guest Token muss in ein Api Access Token umgeandlet werden damit User Meetings beitreten können.
7. `widget <meeting> <token>` - Damit kann das Reac Widget getartet werden. `<meeting>` kann entwerder die im Schritt 3 erzeugte Meetingnummer oder eine E-Mail von einem Webex user verwendet werden. `<token>` steht für den in vorhinein erzeugte Token. 
8. Das Python Skript kann nun geschlossen werden (Strg+C). Im Selben Terminal nun `npm start` ausführen. das Widget wird in ein Browserfenster starten. 