#!/usr/bin/env python3
"""Erzeugt kalender.ics aus data/termine.json und data/plan.json.

Nach jeder Änderung an data/termine.json ausführen:
    python3 tools/build_ics.py
"""
import hashlib
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def esc(text):
    return (str(text).replace("\\", "\\\\").replace(";", "\\;")
            .replace(",", "\\,").replace("\n", "\\n"))


def fold(line):
    """Zeilen nach RFC 5545 auf 75 Bytes umbrechen."""
    raw = line.encode("utf-8")
    if len(raw) <= 75:
        return line
    parts, chunk = [], b""
    for ch in line:
        b = ch.encode("utf-8")
        if len(chunk) + len(b) > (75 if not parts else 74):
            parts.append(chunk.decode("utf-8"))
            chunk = b""
        chunk += b
    parts.append(chunk.decode("utf-8"))
    return "\r\n ".join(parts)


def main():
    termine = json.loads((ROOT / "data/termine.json").read_text(encoding="utf-8"))["items"]
    plan = json.loads((ROOT / "data/plan.json").read_text(encoding="utf-8"))
    names = {p["id"]: p["name"] for p in plan.get("positionen", []) + plan.get("warteliste", [])}
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    lines = [
        "BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Depotbuch//Planspiel Boerse//DE",
        "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
        "X-WR-CALNAME:Planspiel Börse – Termine",
        "X-WR-CALDESC:Wichtige Termine für unser Depot beim Planspiel Börse 2026",
        "X-WR-TIMEZONE:Europe/Berlin",
        "REFRESH-INTERVAL;VALUE=DURATION:PT6H", "X-PUBLISHED-TTL:PT6H",
    ]
    for it in sorted(termine, key=lambda x: x["datum"]):
        d = date.fromisoformat(it["datum"])
        titel = it["titel"] + (" (Datum unsicher)" if it.get("unsicher") else "")
        betrifft = [names.get(i, i) for i in it.get("betrifft", [])]
        desc = []
        if betrifft:
            desc.append("Betrifft: " + ", ".join(betrifft))
        for key, label in (("erwartung", "Erwartet"), ("gut", "Wenn gut"), ("schlecht", "Wenn schlecht"), ("frage", "Für euch")):
            if it.get(key):
                desc.append(f"{label}: {it[key]}")
        uid = hashlib.sha1((it["datum"] + it["titel"]).encode("utf-8")).hexdigest()[:16]
        lines += [
            "BEGIN:VEVENT",
            f"UID:{uid}@depotbuch",
            f"DTSTAMP:{stamp}",
            f"DTSTART;VALUE=DATE:{d:%Y%m%d}",
            f"DTEND;VALUE=DATE:{d + timedelta(days=1):%Y%m%d}",
            f"SUMMARY:{esc(titel)}",
            f"DESCRIPTION:{esc(chr(10).join(desc))}",
            "URL:https://nahol2021.github.io/depotbuch/termine.html",
            "TRANSP:TRANSPARENT",
            # Erinnerung am Vorabend um 18 Uhr und am Morgen um 7 Uhr
            "BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:Morgen: {esc(titel)}", "TRIGGER:-PT6H", "END:VALARM",
            "BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:Heute: {esc(titel)}", "TRIGGER:PT7H", "END:VALARM",
            "END:VEVENT",
        ]
    lines.append("END:VCALENDAR")
    (ROOT / "kalender.ics").write_bytes(("\r\n".join(fold(l) for l in lines) + "\r\n").encode("utf-8"))
    print(f"kalender.ics: {len(termine)} Termine")


if __name__ == "__main__":
    main()
