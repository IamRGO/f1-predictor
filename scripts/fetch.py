import requests
import json
from pathlib import Path

def get_race_sessions(year):
    url = f"https://api.openf1.org/v1/sessions?year={year}"
    data = requests.get(url).json()
    return [s for s in data if s.get("session_type") == "Race"]

def get_meetings_by_key(year):
    url = f"https://api.openf1.org/v1/meetings?year={year}"
    data = requests.get(url).json()
    return {m["meeting_key"]: m for m in data}

def get_race_results(session_key):
    url = f"https://api.openf1.org/v1/session_result?session_key={session_key}"
    print(url)
    return requests.get(url).json()

data_path = Path("data/f1_race_results.json")
existing = json.loads(data_path.read_text()) if data_path.exists() else {}

def load_driver_info(year):
    path = Path(f"data/{year}.json")
    return json.loads(path.read_text()) if path.exists() else {}

def get_race_results(session_key):
    url = f"https://api.openf1.org/v1/session_result?session_key={session_key}"
    print(url)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Failed to fetch data for session_key {session_key}: {e}")
        return []

all_races = {}

for year in [2025, 2026]:
    drivers = load_driver_info(year)
    meetings = get_meetings_by_key(year)
    sessions = get_race_sessions(year)
    if not sessions:
        all_races[year] = existing.get(str(year), [])
        continue

    existing_by_session = {r["session_key"]: r for r in existing.get(str(year), [])}
    races = []

    def race_entry(s, results):
        meeting = meetings.get(s["meeting_key"], {})
        return {
            "session_key": s["session_key"],
            "meeting_key": s["meeting_key"],
            "circuit_name": meeting.get("circuit_short_name") or s.get("circuit_short_name"),
            "race_name": meeting.get("meeting_name"),
            "results": results
        }

    for s in sessions[:-1]:
        session_key = s["session_key"]
        if session_key in existing_by_session:
            cached = existing_by_session[session_key]
            if "circuit_name" not in cached or "race_name" not in cached:
                meeting = meetings.get(s["meeting_key"], {})
                cached["circuit_name"] = cached.get("circuit_name") or meeting.get("circuit_short_name") or s.get("circuit_short_name")
                cached["race_name"] = cached.get("race_name") or meeting.get("meeting_name")
            races.append(cached)
            print(f"Skipping {session_key} because it already exists")
        else:
            results = get_race_results(session_key)
            add_driver_info_to_results(results, drivers)
            races.append(race_entry(s, results))

    s = sessions[-1]
    results = get_race_results(s["session_key"])
    add_driver_info_to_results(results, drivers)
    races.append(race_entry(s, results))

    all_races[year] = races

with open(data_path, "w") as f:

    json.dump(all_races, f, indent=2)

print("Saved race results")