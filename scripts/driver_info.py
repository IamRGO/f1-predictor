import requests
import json

def get_drivers_for_year(year):
    """Fetch driver info for a year, keyed by driver_number."""
    url = f"https://api.openf1.org/v1/sessions?year={year}"
    sessions = requests.get(url).json()
    if not sessions:
        return {}

    session_key = sessions[0]["session_key"]
    drivers_url = f"https://api.openf1.org/v1/drivers?session_key={session_key}"
    drivers = requests.get(drivers_url).json()

    return {
        str(d["driver_number"]): {
            "full_name": d.get("full_name"),
            "broadcast_name": d.get("broadcast_name"),
            "first_name": d.get("first_name"),
            "last_name": d.get("last_name"),
            "name_acronym": d.get("name_acronym"),
            "team_name": d.get("team_name"),
            "country_code": d.get("country_code"),
        }
        for d in drivers
    }

for year in [2025, 2026]:
    drivers = get_drivers_for_year(year)
    with open(f"data/{year}.json", "w") as f:
        json.dump(drivers, f, indent=2)
    print(f"Saved {len(drivers)} drivers to data/{year}.json")
