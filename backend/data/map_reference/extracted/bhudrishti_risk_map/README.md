# Bhudrishti Risk Map (Sikkim)

30 researched landslide/flood locations on a working map. Red = High, Yellow = Medium, Green = Low.

## Files
- `index.html` - the whole app (Leaflet + plain JavaScript, no build step)
- `data/locations.json` - map data (same 30 rows as `Map_Locations.xlsx`)
- `locations.js` - embedded offline copy of the same data
- `Map_Locations.xlsx` - research table for submission

## Setup
1. Unzip the folder.
2. In a terminal inside the folder run: `python -m http.server 8000`
3. Open `http://localhost:8000` in Chrome or Edge and click **See the Map**.

Opening `index.html` by double-click also works, but it always uses the offline data and the browser may block "My location". Use localhost for the full demo.

## Features
- **See the Map** opens the map full screen (Full screen / Back buttons in the top bar)
- **Search** by location or district (falls back to the online place search for other places)
- **My location** shows a blue dot and the nearest researched risk site
- **Marker click** shows warning, safe place, alternative route, reason, and the official source link

## Offline behaviour
- Data file unreachable: the app switches to the embedded data in `locations.js` and says so on screen.
- Map tiles unreachable: markers and popups still work on a plain background.
- Map library unreachable: a plain list of the 30 locations is shown.

To test: disconnect the internet and reload, or rename the `data` folder.

## Before final submission
- Latitude/longitude are approximate placements (nearest named town or road). Check each against the GPS listed in the SSDMA landslide inventory and correct `Map_Locations.xlsx`, then update `data/locations.json` and `locations.js`.
- Ratings are a project research classification, not a live government alert.
- The research has no Low-risk cases, so no green markers appear yet. The code already supports them: set `level` to `Low`.

## Demo video (60-90 seconds, screen recording)
1. Home screen, click **See the Map**.
2. Show red and yellow markers; click one marker and read the popup.
3. Search "Chungthang" and "Rangpo".
4. Click **My location**.
5. Turn off the internet, reload, and show the offline data message.
