import os
import json
from xml.etree.ElementTree import Element, SubElement, ElementTree

def convert_to_gpx(points, name=""):
    gpx = Element('gpx', version='1.1', creator='SOTA Map', xmlns='http://www.topografix.com/GPX/1/1')
    trk = SubElement(gpx, 'trk')
    if name:
        SubElement(trk, 'name').text = name
    trkseg = SubElement(trk, 'trkseg')

    for pt in points:
        trkpt = SubElement(trkseg, 'trkpt', lat=str(pt['latitude']), lon=str(pt['longitude']))
        SubElement(trkpt, 'ele').text = str(pt.get('altitude', 0))

    return gpx

def main():
    data_dir = 'data'
    for filename in os.listdir(data_dir):
        if filename.endswith('.json'):
            json_path = os.path.join(data_dir, filename)
            base = filename.replace('.json', '')

            with open(json_path, 'r', encoding='utf-8') as f:
                try:
                    routes = json.load(f)
                except json.JSONDecodeError:
                    print(f"Skipping {filename}, invalid JSON")
                    continue

            if not routes:
                print(f"Skipping {filename}, no routes found.")
                continue

            valid_routes = [r for r in routes if r.get('points')]
            if not valid_routes:
                print(f"Skipping {filename}, all routes are empty.")
                continue

            for idx, route in enumerate(valid_routes):
                points = route['points']
                title = route.get('track_title', f'Route {idx}')
                gpx_element = convert_to_gpx(points, title)
                gpx_filename = f"{base}_route{idx}.gpx"
                gpx_path = os.path.join(data_dir, gpx_filename)
                ElementTree(gpx_element).write(gpx_path, encoding='utf-8', xml_declaration=True)
                print(f"Generated {gpx_path}")

if __name__ == '__main__':
    main()
