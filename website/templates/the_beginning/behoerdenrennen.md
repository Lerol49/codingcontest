
### Das Behördenrennen

Du kommst in ein großes Bürogebäude, das von oben bis unten in allen $n$ 
Stockwerken genau eine deutsche Behörde sitzen hat. Du möchtest dir jetzt deinen
neuen Personalausweis abholen, den du vor ein paar Monaten beantragt hast.
Du weißt aber nicht genau, in welches Stockwerk du musst.
Also fragst du einfach im Erdgeschoss nach und wirst dann in das vierte Stockwerk
verwiesen. Dort angekommen wird aber behauptet, dass du in das dritte müsstest.
Im dritten Stockwerk ist aber die Führerscheinbehörde, du solltest es doch mal im
ersten Stock versuchen...

<br>


In der Input Datei steht in der ersten Zeile die Anzahl an Stockwerken $n$.
Danach folgen alle Stockwerke von $1$ (Erdgeschoss) bis $n$ mit einem Verweis auf
ein anderes Stockwerk.

```
n
s_1
s_2
...
s_n
```

Frage dich so lange durch, bis du in dem Stockwerk angekommen
bist, in dem der Verweis die Zahl $0$ ist, da ist die Personalausweisbehörde. 
<br>
Gib alle Stockwerke, die du besucht hast in der richtigen Reihenfolge aus.



### Beispiel
#### Inputs
```
5
4
0
2
5
3
```
#### Output
```
4
5
3
2
0
```
