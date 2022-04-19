# Webex x ich.app POC

Dieses Projekt beinhaltet dient als "Prove of Concept" für die Integration zwischen der Webex Umgebung und der ich.app. Die nachfolgenden Zeilen sind in zwei Bereiche unterteilt, eine Inbetriebnahme-Anleitung und eine Beschreibung der verschiedenen Funktionen die benutzt werden, damit das POC einfach in eine vollwertige Web Applikation umgesetzt werden kann.

Ziel des Projektes ist, Webex Meetings sicherer zu gestalten, indem man Teilnehmer zuerst über die ich.app authentifiziert bevor diese das Meeting beitreten.

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
