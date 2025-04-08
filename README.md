# qube25
Mini Prosjekt - Oliver &amp; Eldar - Gruppe 25

Hei!

Ønsker du å kjøre qube kontrolleren kan du følge denne oppskriften.
Dette vil være en veiledning for de som kjører dette i ubuntu

# Oppsett:
1. Det første du må gjøre er å innstallere ROS2, du kan følge denne veiledningen: https://docs.ros.org/en/jazzy/Installation/Ubuntu-Install-Debs.html
2. Gå til mappen du ønsker å laste ned prosjektet til, høyreklikk innei mappen og velg "Åpne i terminal". Lim inn følgende kommando:

            git clone https://github.com/DeusDiver/qube25.git
4. Dette vil klone prosjektet til ønsket mappe. Dette blir ditt workspace fra nå av.
5. Du må laste ned to stykk ROS 2 kontroller-pakker, som inneholder spesifikke noder for å håndtere robotens kontrollmekanismer. Disse sørger for kommunikasjon med robotens 
maskinvare eller simulator. Åpne en terminal (Ctrl+Alt+T) og kjør disse to comandoene: 

         sudo apt install -y ros-jazzy-ros2-control ros-jazzy-ros2-controllers
6. Du har nå alt du trenger for å kjøre koden

Man har to valg når man skal kjøre koden. Man kan velge å kjøre kun simulering eller man kan kjøre med hardware.

# Kjøre kode med kun simulering:
1. Åpne mappen til prosjektet.
2. Høyreklikk i mappen og velg "Åpne i Terminal". 
3. I terminalen må du bygge prosjeket med kommandoen. Når du kjører kommandoen, starter du prosessen med å kompilere og bygge prosjektets kildekode. Avhengigheter og pakker        oppdages, kildekoden kompileres og oppsettfiler genereres.
   Dette gjør du ved å kjøre følgende comando i terminalen:

               colcon build 
5. Når pakkene er bygget må du sette opp miljøvariablene dine slik at systemet vet hvor det kan finne de nylig bygde pakkene.
   Dette gjør du ved kjøre følgende kommando i teminalen:

               source install/setup.bash
7.  Prosjektet inneholder to lounch filer. Dette er filer som åpner pakker og noder og evetuelt andre lounch filer du trenger.  Forskjellen på disse filene er at "launch2" 
    kjører uten PID slik at man kan velge å kjøre denne manuelt om ønskelig.
    I teminalen kan du lime inn ønsket lauch fil for å starte prosjektet:

                ros2 launch qube_bringup bringup.launch.py

    
                ros2 launch qube_bringup bringup.launch2.py
    Med launch filene kan man sette flere parameter. Se veiledning for launch-filer lengre nede (link)
9. For å kjøre PIDen manuelt åpner du en terminal (Ctrl+Alt+T) og kjør følgende komando:"ros2 run qube_controller pid"
7.Første gang du kjører dette må du lagre configfil. Dette gjør du slik:

Sett inn bilde veiledning her 

# Kjøre kode med hardware:
Kjøring av kode med kun simulering:
1. Sett sammen quben og koble til strøm.
2. Åpne en terminal (Ctrl+Alt+T)
3. Kjør følgende kommando: ls /dev/tty*

   Du vil da få opp et skjermbilde som dette:

         (sett inn skjermbilde)
   
5. Koble kuben til en USB port på PCen din.
6. Åpne en terminal (Ctrl+Alt+T)
7. Kjør følgende kommando: ls /dev/tty*

   Du vil få opp et tilsvarende skjermbilde men med en ekstra "enhet" til i listen

    (sett inn skjermbilde)
   
8. Åpne mappen til prosjektet.
9. Høyreklikk i mappen og velg "Åpne i Terminal". 
10. I terminalen må du bygge prosjeket med kommandoen. Når du kjører kommandoen, starter du prosessen med å kompilere og bygge prosjektets kildekode. Avhengigheter og pakker        oppdages, kildekoden kompileres og oppsettfiler genereres.
   Dette gjør du ved å kjøre følgende comando i terminalen: "colcon build". 
11. Når pakkene er bygget må du sette opp miljøvariablene dine slik at systemet vet hvor det kan finne de nylig bygde pakkene.
   Dette gjør du ved kjøre følgende kommando i teminalen : "source install/setup.bash" 
12.  Prosjektet inneholder to launch filer. Dette er filer som åpner pakker og noder og evetuelt andre lounch filer du trenger.  Forskjellen på disse filene er at "launch2" 
    kjører uten PID slik at man kan velge å kjøre denne manuelt om ønskelig.
    I teminalen kan du lime inn ønsket lauch fil for å starte prosjektet:
    - "ros2 launch qube_bringup bringup.launch.py device:=/dev/ttyACM0" (dev/ttyACM0 må her byttes ut med den "IDen" du fikk i steg 7)
    - "ros2 launch qube_bringup bringup.launch2.py device:=/dev/ttyACM0" (dev/ttyACM0 må her byttes ut med den "IDen" du fikk i steg 7)

Med launch filene kan man sette flere parameter. Se veiledning for lauchfiler lengre nede (link)

13. For å kjøre PIDen manuelt åpner du en terminal (Ctrl+Alt+T) og kjør følgende komando:"ros2 run qube_controller pid"
14.Første gang du kjører dette må du lagre configfil. Dette gjør du slik:

Sett inn bilde veiledning her 


# Hvordan bruke launch filer
Ved hjelp av lauch filer kan man sette forskjellige parameter. Under ser du et eksempel på hvordan dette kan gjøres.

ros2 launch qube_bringup bringup.launch.py baud_rate:=9600 simulation:=false device:=/dev/ttyACM0 p:=12.5 i:=0.05 d:=0.2

Man må ikke endre alt, uendra verdiar bruker standard verdiene definert i bunnen av launch fila.

"baud_rate" spørs på kva microkontroller som skal brukes. F.eks en arduino uno har vanligvis en baud rate på 9600, og ein eps32 har vanligvis 115200 (dette er standard verdien i prosjektet).

"simulation" velg true eller false basert på om ein Qube faktisk er tilkoblet eller ikke.

"device" velg riktig! Sjå over hvordan du finner hva du skal velge

"p", "i", "d" PID verdier, start gjerne med kun et P ledd, så øk I / D forsiktig. OBS! Float, så om du skal velge "0" må du skrive "0.0"!!! 





colcon build # Bygger alle pakkene i workspace
colcon build --packages-select qube_bringup  # Bygger kun den spesifiserte pakken
source install/setup.bash  # Kilde oppsett etter bygging
ros2 launch qube_bringup bringup.launch.py
ros2 launch qube_bringup bringup.launch2.py







Her er viktige kommandoer du trenger:
colcon build
source install/setup.bash

ros2 launch qube_description view_qube.launch.py
ros2 launch qube_bringup bringup.launch.py
ros2 launch qube_bringup bringup.launch2.py
ros2 launch qube_bringup bringup.launch2.py baud_rate:=9600 simulation:=false device:=/dev/ttyUSB0





Husk å sjekk!:
    Bringup: Sjekk baud rate (9600???), com port(Bruk arduino IDE)


    Oppgave 5: Selvevaluering
Det siste dere skal gjøre er å evaluere deres eget arbeid. Dette gjør dere individuelt, og leveres inn på blackboard sammen med en link til repo-et dere har laget.

Dere skal svare i prosent hva dere tenker om arbeidet dere har gjort i prosjektet

## qube_description
# Hvor godt dokumentert er filene i pakken?
vi må dokumentere
# Hvor godt dokumentert er selve pakken?
vi må dokumentere

# Hvor lik er URDF-beskrivelsen en ekte Qube?
Det kommer litt ann på hvor man legger listen. Kuben vår ser lik ut den som er i dokumentasjonen til mini prosjektet, men den fysiske quben har ting som lys markeringer ledninger som ikke er i URDF-beskrivelsen. Men man ser tydelig at dette er en representasjon av quben og til det fungerer den veldig bra. 

Hvor godt funker launch-filen til å visualisere quben?
Launch-filen fungerer greit men ikke perfekt. Visualisering i RViz blir lastet men man må manuelt gå inn å velge config filen for å få kuben til å dukke opp riktig.

## qube_bringup
# Hvor godt funker launch-filen til å starte opp alle elementene?
qube_bringup fungerer som den skal, man kjører launchfilen og alt som skal åpne seg gjør det.
Vi har laget 2 launh filer navn 1 og navn 2. ved å kjøre kommando 1 starter bring up filen med PID Controller, kjører man kommando 2 starter bring up uten PID kontroller slik at man kan kjøre denne separat.
# Hvor enkelt kan man endre på hardware-paramererne som baud_rate, device og simulation? (Det å endre parametrene når man kjører launch-filen er enkelt. Det å måtte endre en hardkodet verdi en tilfeldig plass inni launch-filen og måtte bygge den etterpå er ikke enkelt.)
Det er veldig enkelt man kan sette 
# Hvor godt dokumentert er pakken?
Her må vi dokumentere




## qube_controller

# Hvor godt regulerer regulatoren?
Med verdiene P:10.0, I:0.01, D:0.0 så regulerer pid regulatoren greit. Med meir testing så kunne den nok ha blitt bedre/mer stabil, men den leiter tydelig etter setpunktet, og når fram relativt raskt

# Hvor enkelt er det å endre på parametere?
Ved å kjøre: ros2 launch qube_bringup bringup.launch.py p:=5.0 i:=1.0 d:=0.2 (Med ønska verdi) så kan man enkelt velge verdiene for P I D som man vil, uten å gjøre endringer på prosjektet. Man kan f.eks kjøre ros2 launch qube_bringup bringup.launch.py p:=5.0 om man bare ønsker å endre en verdi, men då vil I og D bruke standard verdiene fra koden.

# Hvor godt dokumentert er pakken?



# Hvor enkelt er det å endre på referansevinkelen?
Sånn som koden er nå så må dette endres i koden, men det er ikke mye som skal til for å legge dette til. Men ved å bruke rviz slideren så kan referansevinkelen endres en del. (Ikkje nemne første delen?)



Kommentering::

Vi har fått en del hjelp av KI som liker å kommentere alt. Vi har latt noko være, tatt vekk delar og endra / lagt til kommentarer slik at koden er mest mulig delbar.





# Google Drive link:
https://drive.google.com/drive/folders/1MlKgm74x8dr88riOgZhLQA8-UEuPzxm0?usp=sharing
