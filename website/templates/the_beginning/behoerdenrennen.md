
### Das Behördenrennen

Du kommst in ein großes Bürogebäude, das von oben bis unten in allen <i>n</i> 
Stockwerken genau eine deutsche Behörde sitzen hat. Du möchtest dir jetzt deinen
neuen Personalausweis abholen, den du vor ein paar Monaten beantragt hast.
Du weißt aber nicht genau, in welches Stockwerk du musst.
Also fragst du einfach im Erdgeschoss nach und wirst dann in das vierte Stockwerk
verwiesen. Dort angekommen wird aber behauptet, dass du in das dritte müsstest.
Im dritten Stockwerk ist aber die Führerscheinbehörde, du solltest es doch mal im
ersten Stock versuchen...



In der Input Datei steht in der ersten Zeile die Anzahl an Stockwerken n.
Danach folgen alle Stockwerke von 0 (Erdgeschoss) bis n-1 mit einem Verweis auf
ein anderes Stockwerk. Frage dich so lange durch, bis du in dem Stockwerk angekommen
bist, in dem der Verweis die Zahl 0 ist, da ist die Personalausweisbehörde. <br>
Gib alle Stockwerke, die du besucht hast in der richtigen Reihenfolge aus.



Beispiel (Die Bemerkungen rechts werden nicht mit übergeben):
### Inputs
```
4       # Erdgeschoss
5       # Anzahl an Stockwerken
0       # 1. Stock
2       # 2. Stock
1       # 3. Stock
3       # 4. Stock
```
### Output
```
0
3
1
4
```
