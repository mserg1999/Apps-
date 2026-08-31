# Wedding Planner

A personal wedding planning app covering everything from vendor research to the wedding-day countdown. It's a Progressive Web App (PWA), so it can be installed like a real app — its own icon, its own window, and it keeps working offline.

## Features

- **Dashboard** — couple names, wedding date with a live countdown, budget snapshot, checklist progress, and vendor booking status at a glance.
- **Budget** — a categorized breakdown (venue, catering, photography, attire, flowers, music, stationery, rings, transportation, favors, officiant, and a miscellaneous buffer) with editable planned/actual/paid amounts, automatic "owed" and "variance" calculations, and category totals against your overall budget.
- **Checklist** — a categorized to-do list with due dates and priorities, filterable by category or status (open/done).
- **Calendar** — a month view showing task due dates and appointments together; click any day to see its agenda and add appointments (dress fittings, venue tours, photographer meetings, etc.).
- **Photographers** — tracks candidates and bookings grouped by location: **Scotland**, **Washington DC**, and **California** (plus "Other"), with contact info, quoted price, status, and portfolio links.
- **Dress Shopping** — boutique appointments, the dress/item tried, price, and status (researching through ready for pickup).
- **Venue & Catering** — reception venues and caterers for the **DMV area** (DC / Maryland / Virginia), with capacity, estimated cost, cuisine/style, and status.
- **Installable app** — add it to your home screen or desktop with its own icon and window, and it keeps working offline once installed (via a service worker).
- **Backup & restore** — export all your data as a `.json` file at any time, and import it back (e.g. on a new device). There's also a "Save Offline Copy" button that saves the whole page as a single self-contained HTML file.
- Everything is saved to the browser's local storage — nothing is sent anywhere, and refreshing the page (or reopening the installed app) won't lose your data.

## Installing it as a real app

Installing (rather than just opening the HTML file) needs the app served over `http://` or `https://` — browsers won't let a page installed from a bare double-clicked file register a service worker or show an install prompt.

1. Go to [netlify.com](https://www.netlify.com) and sign in with GitHub (free).
2. **Add new site → Import an existing project → GitHub**, authorize it, and pick this repository.
3. Set the base/publish directory to `wedding-planning-app/` (this repo's `netlify.toml` currently points at a different app — if you're deploying this one as its own Netlify site, set the base directory in the Netlify UI, or update `netlify.toml`).
4. You'll get a URL like `https://your-site-name.netlify.app` in under a minute.

If you'd rather use GitHub Pages, flip the repo to public (Settings → General → Danger Zone → Change visibility), then Settings → Pages → Source → deploy from a branch → root. The app will be reachable at `<pages-url>/wedding-planning-app/`.

Once hosted, open the link once, then use your browser's "Install app" / "Add to Home Screen" option to get an icon on your phone or desktop.

## Just running it locally

Open `index.html` directly in a browser to use every planning feature immediately — no build step, dependencies, or server needed. The only things that require real hosting are installability and the service worker's offline cache; the app tells you which mode you're in and adjusts its instructions accordingly.

## Your data

All data (couple/wedding info, budget, checklist, calendar events, and vendor lists) lives only in this browser's local storage on this device. Use **Export Backup (.json)** on the Dashboard regularly, and **Import Backup** to restore it or move it to another device/browser.
