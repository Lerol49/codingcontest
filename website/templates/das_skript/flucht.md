### Flucht
Auf dem Desktop findet ihr eine Datei mit den Namen "skript.pdf", ihr kopiert sie schnell
auf einen USB-Stick. Als der Kopiervorgang gerade abgeschlossen ist, hört ihr Schritte auf
dem Flur. "HEY! Was machen Sie da?!" Ihr steckt den USB-Stick ein und rennt los zur Bushaltestelle.
Ihr schafft es kurz vor eurem Verfolger in den Bus, der zum Glück direkt losfährt. Jetzt müsst ihr
schnellstmöglich zum Bahnhof kommen, von dort aus ist es praktisch unmöglich euch weiter zu verfolgen.



Die Zahl in der ersten Zeile gibt an, wie viele Zeilen folgen.
Die erste Zahl pro Zeile gibt an, wie viele Zahlen in der Zeile folgen.
Die zweite Zahl in der Zeile ist die erste Bushaltestelle. Ihr könnt so viele
Haltestellen nach links oder rechts fahren, wie der Wert der Zahl ist. Die Enden sind
nicht verbunden, die \(-1\) ist der Bahnhof. Findet den Weg dort hin, bei dem ihr
am wenigsten umsteigen müsst. Gebt dafür immer den Index der Station an, bei
dem ihr gerade seid. Jede Zeile ist ein eingenes Problem, sie hängen nicht miteinander zusammen.
### Beispiel
#### Input
```
2
7 2 5 1 2 0 1 -1 
9 4 1 5 0 1 1 5 -1 7
```

#### Output
```
0 2 1 6
0 4 5 6 1 2 7
```
