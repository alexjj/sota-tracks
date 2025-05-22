import requests
import pandas as pd
import os
import json
import time

# Create output directory
output_dir = "data"
os.makedirs(output_dir, exist_ok=True)

# Load summit codes
df = pd.read_csv("uksummits.csv")
summit_codes = df['SummitCode'].dropna().unique()

# API template
api_url = "https://api-db.sota.org.uk/smp/gpx/summit/{}"

# Loop through summit codes
for code in summit_codes:
    safe_code = code.replace("/", "-")
    output_path = os.path.join(output_dir, f"{safe_code}.json")

    if os.path.exists(output_path):
        continue  # Skip if already downloaded

    try:
        response = requests.get(api_url.format(code))
        response.raise_for_status()

        data = response.json()

        # Save only relevant parts
        for route in data:
            route.pop('hdr_id', None)  # Remove unused fields
            # keep: callsign, posted_date, track_title, track_notes, points

        with open(output_path, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"Saved: {code}")
        time.sleep(0.5)  # Be nice to the server

    except Exception as e:
        print(f"Failed to get {code}: {e}")
