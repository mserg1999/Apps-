# Work Tracking Dashboard

A single-page work dashboard: a live pending-task tracker plus a data-sheet importer for quick CSV/Excel analysis. It's a Progressive Web App (PWA), so it can be installed like a real app and keeps working offline once installed.

Everything — tasks and imported data sheets — is saved to your browser's local storage. Nothing is uploaded anywhere; it's entirely private to your device/browser.

## Features

**Overview tab**
- Live counts: total tasks, in progress, overdue, completed this week.
- "Coming Up" list of your nearest due dates, with overdue items flagged.
- Quick summary of which data sheets you've loaded.

**Tasks tab**
- Add/edit/delete tasks: title, notes, status (Not started / In progress / Blocked / Done), priority (Low/Medium/High/Urgent), due date, and free-form tags.
- Search, filter by status/priority, sort by due date/priority/status/newest, and hide completed tasks.
- **List view** (a flat, sortable list with inline checkboxes) or **Board view** (a 4-column kanban-style layout you reassign with a dropdown per card).
- Overdue tasks are highlighted automatically based on today's date.
- Import/export tasks as CSV.

**Data Sheets tab**
- Upload a `.csv`, `.xlsx`, or `.xls` file — parsed entirely in your browser (via the bundled SheetJS library).
- Multiple sheets can be loaded and switched between; each is saved locally so it's still there next time you open the app.
- Sortable, filterable data table with pagination ("Show more rows").
- **Column Stats** — pick any column to see count/sum/average/min/max (numeric) or distinct-value breakdown with a top-values bar chart (categorical).
- **Breakdown Chart** — group rows by any column and measure by row count or the sum of a numeric column, rendered as a bar chart (via Chart.js).
- Export the current (filtered) view back out as CSV.

**Installable app**
- Add it to your home screen or desktop with its own icon and window; it keeps working offline once installed (via a service worker).
- **Offline Copy** button saves the whole page as a single self-contained HTML file you can keep or move around without hosting anything.

## Just running it locally

Open `index.html` directly in a browser to use every dashboard feature immediately — no build step, dependencies, or server needed. The only things that require real hosting (`http://`/`https://`, not a bare double-clicked file) are installability and the service worker's offline cache.

## Deploying it

This repo already has a `netlify.toml` pointed at a different app (`chess-availability-calendar/`), so deploy this dashboard as its own Netlify site rather than editing that file:

1. Go to [netlify.com](https://www.netlify.com) and sign in with GitHub (free).
2. **Add new site → Import an existing project → GitHub**, authorize it, and pick this repository.
3. Before deploying, open **Site settings → Build & deploy → Build settings** and set:
   - **Base directory:** `tracking-dashboard`
   - **Publish directory:** `tracking-dashboard` (or `.` relative to the base directory, depending on how Netlify's UI presents it)
   - **Build command:** leave blank — this is a static site with no build step.
4. Deploy. You'll get a URL like `https://your-site-name.netlify.app` in under a minute.
5. Open that URL and use your browser's "Install app" option (or the in-app **Install** button) to add it to your home screen/desktop.

## Data & security notes

- All data (tasks and imported sheets) lives in your browser's `localStorage`, scoped to whatever URL/origin you open the app from. Using it from `file://`, from `localhost`, and from your deployed URL are three different storage buckets — pick one place and stick with it.
- Very large spreadsheets may not fit in `localStorage` (typically a few MB per origin). If a sheet fails to save, you'll get a toast warning; the data still works for that session but won't persist after a refresh.
- Excel parsing uses the bundled [SheetJS](https://sheetjs.com) `xlsx` library (vendored in `vendor/`, not loaded from a CDN, so it also works fully offline). The version available for this project has known, unpatched advisories around parsing maliciously crafted `.xlsx` files (prototype pollution / ReDoS). Only open spreadsheet files you trust; if in doubt, save as `.csv` first (this app's own CSV parser doesn't use that library).
