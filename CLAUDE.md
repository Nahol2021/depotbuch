# Depotbuch

Team-Übersicht für das Planspiel Börse 2026 (Schülerwettbewerb, Spielgeld).
Live: https://nahol2021.github.io/depotbuch/ (öffentlich, ohne Login).

- Daten: `data/{plan,kurse,termine,bericht,trades,notizen}.json`. Das Team schreibt per
  GitHub-Token direkt aus der Seite, deshalb **vor jeder Änderung `git pull`**.
- Nach jeder Änderung an `data/termine.json`: `python3 tools/build_ics.py` ausführen und
  `kalender.ics` mitcommitten.
- Keine Screenshots auf der öffentlichen Seite.
- Keine Kaufbefehle, sondern Infos und Szenarien. Entscheiden tut das Team. Einfach auf Deutsch
  erklären, Johan ist Börsen-Anfänger.
- Diese Datei ist öffentlich, sobald sie gepusht wird. Deshalb keine privaten Angaben hier eintragen.
