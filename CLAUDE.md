# Depotbuch

Team-Übersicht für das Planspiel Börse 2026 (Schülerwettbewerb, Spielgeld).
Live: https://nahol2021.github.io/depotbuch/ (öffentlich, ohne Login).

- Daten: `data/{plan,kurse,termine,bericht,trades,notizen}.json`. Das Team schreibt per
  GitHub-Token direkt aus der Seite, deshalb **vor jeder Änderung `git pull`**.
- Nach jeder Änderung an `data/termine.json`: `python3 tools/build_ics.py` ausführen und
  `kalender.ics` mitcommitten.
- Keine Screenshots auf der öffentlichen Seite.
- Nachrichten-Seite: Oberfläche bewusst sehr schlicht (keine Depotbuch-Optik, keine Karten).
  Oben ein Kasten „Heute wichtig“ mit Info und nächstem Termin, aber keine „Was tun?“-Zeile.
  Quellen-Links hellgrau statt blau, die Seite soll nicht bunt wirken.
- Keine Kaufbefehle, sondern Infos und Szenarien. Entscheiden tut das Team. Einfach auf Deutsch
  erklären, Johan ist Börsen-Anfänger.
- Diese Datei ist öffentlich, sobald sie gepusht wird. Deshalb keine privaten Angaben hier eintragen.

## Bekannte Fallen
- `data/nachrichten.json` wird fortgeschrieben (Meldungen der letzten 7 Tage, je mit `datum`,
  `quelle`, `url`), nicht jeden Tag neu angefangen. Sonst verschwinden Meldungen von gestern.
- Nachrichten-Seite und Tagesbericht müssen dieselben Fakten gleich darstellen. Wer eines ändert,
  gleicht das andere ab.
- Texte in den Daten: nur `**fett**`, kein anderes Markdown. Die Seite zeigt jede Aktie aus dem Plan
  in einem festen Abschnitt, Leeres wird nicht zusammengefasst.
- Die Vorgaben des Tagesupdates stehen in der Cloud-Routine, nicht im Repo. Wer das Datenformat
  ändert, ändert dort mit.
- Kasten „Heute wichtig“: Text kommt aus `heute` in `data/nachrichten.json`, der nächste Termin
  rechnet die Seite selbst aus `data/termine.json`. Termine nie doppelt pflegen.
- Termine mit `unsicher: true` in allen Texten als „voraussichtlich“ bezeichnen. Daten als TT.MM.
