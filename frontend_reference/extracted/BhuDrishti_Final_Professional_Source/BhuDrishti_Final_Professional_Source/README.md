# BhuDrishti AI — Final Professional Frontend

This is a plain **HTML + CSS + JavaScript** frontend. There is no backend requirement for this prototype.

## Start the project

Open `index.html` directly, or serve the folder locally:

```bash
py -m http.server 8000
```

Then open `http://localhost:8000`.

## Demo flow

1. Login from `index.html`.
2. Verify with demo OTP `123456`.
3. Continue to Home and the remaining pages.

## Source structure

```text
BhuDrishti_Final_Professional_Source/
├── index.html
├── verify.html
├── home.html
├── map.html
├── alerts.html
├── assistant.html
├── area-safety.html
├── change-detection.html
├── saved-places.html
├── settings.html
├── help.html
├── insights.html          # compatibility redirect
├── css/
│   ├── base.css           # base components and page structures
│   ├── theme.css          # premium glass light/dark visual theme
│   ├── responsive-fixes.css
│   └── final-polish.css   # final responsive/overflow/menu safeguards
└── js/
    ├── app.js             # shared shell, language, theme, sidebar, alerts
    ├── risk-data.js       # 30 researched risk locations
    ├── login.js
    ├── verify-page.js
    ├── home-page.js
    ├── map-page.js
    ├── alerts-page.js
    ├── assistant-page.js
    ├── safety-page.js
    ├── change-page.js
    ├── saved-page.js
    └── settings-page.js
```

## Important UI behavior

- The left dashboard remains fixed on desktop while the main content scrolls.
- The three-line menu collapses/expands the sidebar on desktop.
- On tablet/mobile the same menu opens a proper slide-out navigation drawer.
- Sidebar navigation scroll position is stored in `sessionStorage`, so moving between pages keeps the navigation at the same scroll position.
- The language menu is a custom app-controlled menu, so Windows/Chrome native select colors cannot break it.
- English, Hindi and Hinglish are supported through the shared translation layer.
- Light and dark themes are saved in `localStorage`.
- Alert badge disappears when unread count becomes zero.
- Area Safety uses the included 30-location offline research dataset.

## Notes

This is a research prototype. Risk scores shown in the interface are project research classifications, not live government alerts.
