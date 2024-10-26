

woerter = {
    "passwoerter_aufschreiben_ist_gefaehrlich": "wurzel aNAnaS",
    "die_heiligen_worte": " Brot Tomaten Kaese Pizza Brot Tomaten Kaese Pizza bread",
    "passwort_karte": "5l@t1sPiN4t 4Pfe1mUss pf@nNkucH3n b4gu3t1e br0mb3Ere nvDe1@uf1auF erDBe3rt0r1E vollmilchschokoladenpudding",
    "skript": "Buchstabensuppe"
}


total = 0
for problem in woerter.keys():
    for char in problem:
        if char == " ":
            continue
        total += ord(char)

out = str(total) + "\n"
with open("output.txt", "w") as f:
    f.write(out)
