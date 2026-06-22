

# das hier ist der leichteste Ansatz

import file_handling

# eure funktion soll genauso aufgebaut sein: 
# sie bekommt zwei Argumente, das erste ist n als Anzahl an 
# Zeilen in der input Datei und das zweite ist data als Rest der Datei
def solve(n, data):
    # die Lösung bei euch ist natürlich anders
    for i in range(n):
        sol = sum(data[i])
        print(sol)


# so generiert ihr euch die output datei.
# denkt dran, den richtigen Namen für die input datei zu nehmen
file_handling.run_function(solve, "input.txt")



# falls jemand mehr Kontrolle haben möchte, hier noch ein zweiter Ansatz
def solve2():
    # für maximale Kontrolle könnt ihr die nächste Zeile auch noch selber machen
    n, data = file_handling.read_input_file("input.txt")
    out = ""
    for i in range(n):
        sol = sum(data[i])
        out += str(sol) + "\n"

    with open("output.txt", "w") as f:
        f.write(out)

solve2()


# so klappt das auch, in der test.py wird alles mit input und output gemacht.
# Wenn ihr die Variante machen möchtet, braucht ihr eure Lösungsdatei (hier test.py)
# und eine Datei mit dieser Zeile (und dem import natürlich). 
# Hierbei müsst ihr aber komplett selber die inputs parsen (also von einen großen 
# String in brauchbare Daten umwandeln). Siehe dazu test.py

file_handling.run_file("test.py", "input.txt")


