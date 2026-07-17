# Calendrier « météo migraine » — Paris, Porte d'Aubervilliers.
# Règle calibrée sur 9,5 ans de journal (2017-2026), stable sur les deux moitiés de la période :
#   ORANGE  baisse modérée de pression prévue (-3 à -1 hPa vs la veille)  -> risque ~13 % (habituel 10 %)
#   VERT    remontée franche (>= +6 hPa)                                   -> risque ~6 %
# Aucune donnée personnelle : uniquement des prévisions météo publiques.
import json, urllib.request, datetime as dt, sys

LAT, LON = 48.898, 2.370
URL = (f"https://api.open-meteo.com/v1/forecast?latitude={LAT}&longitude={LON}"
       "&hourly=pressure_msl&past_days=3&forecast_days=7&timezone=Europe%2FParis")

with urllib.request.urlopen(URL, timeout=60) as r:
    data = json.load(r)

# moyenne quotidienne de la pression (niveau mer)
psum, pcnt = {}, {}
for t, v in zip(data["hourly"]["time"], data["hourly"]["pressure_msl"]):
    if v is None:
        continue
    day = t[:10]
    psum[day] = psum.get(day, 0.0) + v
    pcnt[day] = pcnt.get(day, 0) + 1
pmean = {d: psum[d] / pcnt[d] for d in psum if pcnt[d] >= 12}

# « aujourd'hui » heure de Paris = dernier jour de prévision - 6 (past_days=3, forecast_days=7)
today = (dt.date.fromisoformat(data["hourly"]["time"][-1][:10]) - dt.timedelta(days=6)).isoformat()
events = []
for day in sorted(pmean):
    d = dt.date.fromisoformat(day)
    prev = (d - dt.timedelta(days=1)).isoformat()
    if day < today or prev not in pmean:
        continue
    d24 = pmean[day] - pmean[prev]
    if -3 <= d24 < -1:
        events.append((day, d24, "orange"))
    elif d24 >= 6:
        events.append((day, d24, "vert"))

def esc(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")

def fold(line):
    # plie à <= 73 octets UTF-8 sans couper un caractère
    out, cur, n = [], "", 0
    for ch in line:
        b = len(ch.encode("utf-8"))
        if n + b > 73:
            out.append(cur)
            cur, n = " " + ch, 1 + b
        else:
            cur += ch
            n += b
    out.append(cur)
    return "\r\n".join(out)

RAPPEL = ("Rappel des signaux plus forts que la météo : lendemain d'un jour de crise = "
          "journée fragile (~40 %) ; jours 3 à 5 après une crise = les plus sûrs (~4 %).")

now = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
lines = [
    "BEGIN:VCALENDAR",
    "VERSION:2.0",
    "PRODID:-//meteo-migraine-paris//FR",
    "CALSCALE:GREGORIAN",
    "METHOD:PUBLISH",
    "X-WR-CALNAME:Météo migraine (Paris)",
    "X-WR-CALDESC:Vigilance migraine selon la pression atmosphérique prévue à Paris",
    "X-PUBLISHED-TTL:PT12H",
    "REFRESH-INTERVAL;VALUE=DURATION:PT12H",
]
for day, d24, kind in events:
    d = dt.date.fromisoformat(day)
    delta = f"{d24:+.1f}".replace(".", ",").replace("-", "−")
    if kind == "orange":
        summary = "🟠 Migraine : météo défavorable"
        desc = (f"Baisse modérée de pression prévue ({delta} hPa par rapport à la veille) : "
                "le profil qui, historiquement, accompagne le plus ses migraines "
                "(~13 % de risque au lieu de 10 %). Facteur aggravant, pas une alarme. " + RAPPEL)
    else:
        summary = "🟢 Migraine : météo favorable"
        desc = (f"Remontée franche de la pression prévue ({delta} hPa) : historiquement l'un des "
                "profils les plus calmes (~6 % de risque au lieu de 10 %). " + RAPPEL)
    lines += [
        "BEGIN:VEVENT",
        f"UID:{day}@meteo-migraine-paris",
        f"DTSTAMP:{now}",
        f"DTSTART;VALUE=DATE:{day.replace('-', '')}",
        f"DTEND;VALUE=DATE:{(d + dt.timedelta(days=1)).isoformat().replace('-', '')}",
        f"SUMMARY:{esc(summary)}",
        f"DESCRIPTION:{esc(desc)}",
        "TRANSP:TRANSPARENT",
        "END:VEVENT",
    ]
lines.append("END:VCALENDAR")

with open("meteo-migraine.ics", "w", encoding="utf-8", newline="") as f:
    f.write("\r\n".join(fold(l) for l in lines) + "\r\n")

print(f"{len(events)} événement(s) sur les 7 prochains jours :")
for day, d24, kind in events:
    print(f"  {day}  {kind:<6}  d24 {d24:+.1f} hPa")
