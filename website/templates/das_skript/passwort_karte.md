### Passwortkarte 
Ihr kommt im Büro von Prestin an und schaut euch um. Einer von euch hat als HiWi
schon einmal an dem PC von Prestin ein technisches Problem behoben und dabei direkt
unter der Nase des Professors den Hash seines Passworts geklaut. Was man nicht alles
machen kann, wenn man als root in der home directory eines fremden Linux Computers eingeloggt ist...

Nur mit dem Hash kommt ihr aber nicht weit, ihr wisst aber bereits dass hier irgendwo eine Passwortkarte
rumliegt. Damit versucht ihr jetzt, das richige Passwort zu finden.


### Beispiel 1
Die erste Zeile im Dokument ist die Anzahl an Passwordkarten in der Datei. Die erste
Zeile in einem Absatz gibt an, wie viele Zeilen die folgende Karte hat. Danach kommt
der Hash des Passworts, dafür wird immer sha512 verwendet. 
Das Passwort kann horizontal oder vertikal und vorwärts oder rückwärts, aber nicht 
diagonal geschrieben sein. 
#### Input
```
2
2
150a14ed5bea6cc731cf86c41566ac427a8db48ef1b9fd626664b3bfbb99071fa4c922f33dde38719b8c8354e2b7ab9d77e0e67fc12843920a712e73d558e197
ih
g$

5
e85b5191a9cd4dc4c635c34fc3df63e55badab4ceb2c378bed4ac2aa81786f7135b3f85f1d8e952a202a2d39dd71ca507844c583bac548fbad666ba1ce0dac30
zGktl
Ubzqy
1uiG5
3l#Q?
fb.VI
```
#### Output
```
hi
blub
```
