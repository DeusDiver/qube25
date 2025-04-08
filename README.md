# qube25
Mini Prosjekt - Oliver &amp; Eldar - Gruppe 25









Kommandoer:

ros2 launch qube_bringup bringup.launch.py
ros2 launch qube_bringup bringup.launch2.py


Eksempel på å kjøre launch fil med andre verdier:

ros2 launch qube_bringup bringup.launch.py baud_rate:=9600 simulation:=false device:=/dev/ttyACM0 p:=12.5 i:=0.05 d:=0.2


Man må ikke endre alt, uendra verdiar bruker standard verdiene definert i launch fila.

"baud_rate" spørs på kva microkontroller som skal brukes. F.eks en arduino uno har en baud rate på 9600, og ein eps32 har 115200.

"simulation" velg true eller false basert på om ein Qube faktisk er tilkoblet eller ikke.

"device" velg riktig! Sjå over hvordan du finner hva du skal velge

"p", "i", "d" PID verdier, start gjerne med kun et P ledd, så øk I / D forsiktig. OBS! Float, så om du skal velge "0" må du skrive "0.0"!!! 