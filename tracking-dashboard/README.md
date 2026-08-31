# Mahlet's Tracker

A single-page work dashboard: a live pending-task tracker, a set of firm/case ops trackers (email follow-ups, cyber and engagement-letter reminders, LBA escalations, onboarding, rates, invoices, SharePoint folders), a firms capacity dashboard, and a data-sheet importer for quick CSV/Excel analysis. It's a Progressive Web App (PWA), so it can be installed like a real app and keeps working offline once installed.

Everything — tasks, tracker rows, firm records, and imported data sheets — is saved to your browser's local storage. Nothing is uploaded anywhere; it's entirely private to your device/browser.

## Features

**Overview tab**
- Live counts: total tasks, in progress, overdue, completed this week.
- **Live Task Status** — four big boxes (Not Started/In Progress/Blocked/Done) showing a live count and a peek at the actual tasks in each state.
- "Coming Up" list of your nearest due dates, with overdue items flagged.
- **Reminders Due Soon** — a rollup pulling anything due within 7 days (or overdue) from the Cyber Security, Engagement Letter, and LBA Escalation trackers.
- **Browser notifications** — an opt-in toggle on this card; once enabled, you get a real notification (not just something you have to check for) once a day for any task or cyber/EL/LBA reminder that's due today or overdue.
- Quick summary of which data sheets you've loaded.

**Search everything**
- A search box in the top bar looks across every task and every row in every Firm Tracker at once. Click a result to jump straight to it — the right tab opens, the right tracker is selected, and its own search box is filled in so the match is easy to spot.

**Backup & restore**
- **Backup Data** downloads one JSON file with everything — tasks, every tracker's rows, custom tracker definitions, and firm records — since it's all local-only with no server, this is your copy for safekeeping or moving to another browser/computer.
- **Restore Data** loads a backup file back in (after a confirmation, since it replaces everything currently in the app).

**Tasks tab**
- Add/edit/delete tasks: title, notes, status (Not started / In progress / Blocked / Done), priority (Low/Medium/High/Urgent), due date, and free-form tags.
- Search, filter by status/priority, sort by due date/priority/status/newest, and hide completed tasks.
- **List view** (a flat, sortable list with inline checkboxes) or **Board view** (a 4-column kanban-style layout — drag a card between columns to change its status).
- Overdue tasks are highlighted automatically based on today's date.
- **Recurring tasks** — set a task to repeat daily/weekly/monthly; marking it done automatically creates the next occurrence with the due date advanced.
- **Checklists/subtasks** — add a small checklist to any task (one item per line on the form, or add/remove/check items inline); a progress badge like `2/5` shows on the task.
- Import tasks from:
  - This app's own CSV export (round-trips cleanly).
  - **Trello/Asana/Jira-style CSV exports** — recognizes common column names (Card Name, Summary, List, Section/Column, Due Date, Labels, Priority, etc.) and maps their status/priority values onto this app's own.
  - **A calendar `.ics` export** (Outlook/Google Calendar) — each event becomes a task due on its start date, tagged `calendar`.
- Export tasks back out as CSV.
- **Daily Ops Checklist** — one button seeds three daily-recurring tasks (check failed invoices, rates approval, add matter groups); click again any time without creating duplicates.

**Firm Trackers tab**

A sidebar of purpose-built trackers, grouped by category — click one to see its own editable table (click any cell to edit it in place, no separate edit mode):

- *Firms* — **All Active Firms**, **Casualty Firms**, and **Commercial Firms** are filtered views of the same Active Firms list from the Firms Dashboard tab (not separate data): Casualty/Commercial show only firms with that Line of Business, and adding a firm directly from one of those views auto-fills its Line of Business for you. Edits made here (or on the Firms Dashboard) show up in both places instantly. **Firms Not Through Cyber** is a read-only, auto-computed report — any active firm without a "Confirmed" row in Cyber Security Reminders shows up here automatically, with a **"Log Cyber Reminder →"** button per row that jumps straight to the Cyber Security Reminders tracker with that firm's name pre-filled.
- *Email & Reminders* — Email needing your response (personal/shared inbox), Email needing follow-up, Cyber Security Reminders, Engagement Letter (DocuSign) Reminders, LBA Escalations. Each reminder-style tracker has a due date column that auto-highlights the row red once it's overdue (and clears once you mark it resolved/signed/confirmed/etc.), and a red count badge in the sidebar showing how many rows are overdue.
- *Firm Setup* — Firms Needing T360 Setup (+ attorney code), Onboarding Intake Forms (contacts, W9, conflict waiver, proposed partner/associate/paralegal rates, states active in), Firm Onboarding Stages (EL Signed / Under Cyber Review / Rate Negotiation / Added to System), Firms Needing New EL.
- *Finance* — Invoice Issues, Rate Summary – Casualty, Rate Summary – Commercial (firm, approved, TIN/attorney code, partner/associate/paralegal rates, effective date).
- *Documents* — SharePoint Folder Tracker (which firms have a folder, and what's in it).
- *Timekeepers* — Name, Firm, Level (Partner/Associate/Paralegal), Rate, and Active/Inactive status for every attorney or staff member you bill against.
- *Custom* — click **+ New Custom Tracker** to build your own from scratch (name it, add columns of any type — text/number/date/dropdown), or use **Copy rows & columns in** to fork any existing tracker's current data as a starting point ("a blank tracker to pull in from other trackers").

Most trackers show a small **overview stat row** above the table (total rows, plus a couple of relevant rollups like open matters, average rate, or active count) that updates live as you add, edit, import, or delete rows.

Every tracker supports: search, **click a column header to sort by it**, CSV export, **CSV/Excel import** (matches your file's header row to each tracker's columns by name — `.csv`, `.xlsx`, and `.xls` all work — so you can bulk-load an existing spreadsheet instead of typing row by row), a **firm name autocomplete** wherever a "Firm" field appears (suggests names already in your Active Firms list, so the same firm doesn't end up spelled differently in different trackers), and add/edit/delete rows. Trackers with a status column (like the reminder trackers) also get a **"Hide resolved"** checkbox to keep old completed rows out of view without deleting them. (The auto-computed "Firms Not Through Cyber" report is read-only — no add form, import, or flag rules, since it's derived from other trackers rather than being its own dataset.)

Tables (Firm Trackers and the Firms Dashboard) show the first 150 matching rows and a **"Show more rows"** button for the rest — a large import (thousands of rows) still loads and searches instantly, since the page only ever builds the rows currently on screen instead of all of them at once. Row counts, sorting, search, and Flag Rules all still operate over your *entire* dataset, not just what's currently shown.

**Flag Rules** — click **🚩 Flag Rules** on any tracker (or the Firms Dashboard table) to set up your own conditions: pick a column, pick a condition (Is empty / Is not empty / Equals / Contains / Before / After / Greater than / Less than — the list adapts to the column's type), and any matching row gets a 🚩 marker with a tooltip explaining why, plus a "🚩 N flagged" count next to the row count. For example, on Rate Summary – Casualty: *Effective Date → Is empty* flags every firm missing one, including rows you just brought in with a bulk CSV/Excel import. Rules are per-tracker and stick around — add a few once and they keep applying as new rows come in.

**Firms Dashboard tab**
- **Capacity by Firm** — a true utilization percentage per firm: set a "Capacity Target" (how many open matters that firm is expected to handle) and the bar shows open matters ÷ target, color- and label-coded (✓ Has room / ● Near capacity / ⚠ Over capacity, over 100% possible). Firms without a target set yet fall back to a bar relative to your busiest firm, so the chart is useful immediately even before you've filled in targets.
- **Active Firms** table — loss state, work area, matter group, case type, line of business, director, open matter count, capacity target, and average timekeeper cost, all editable in place.
- **Firm Profile** — a sidebar grouped by loss state, then firm name. Click any firm to see everything about them in one place: their Active Firms record plus every matching row from every Firm Tracker (cyber/EL/LBA reminders, onboarding stage, rates, SharePoint status, and so on), instead of hunting across 13 separate trackers.

**Data Sheets tab**
- Upload a `.csv`, `.xlsx`, or `.xls` file — parsed entirely in your browser (via the bundled SheetJS library). A workbook with multiple sheets prompts you to pick which one(s) to import.
- **Paste Data** — paste rows copied from Excel/Google Sheets directly (tab- or comma-separated, with a header row) without saving a file first.
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

## Known limitations

- Board-view drag-and-drop uses the browser's native HTML5 drag API, which doesn't work on touch screens (phones/tablets) — use List view there instead, where checking the box marks a task done (status changes for other states still require the Edit form on touch devices).
- The `.ics` calendar importer reads `SUMMARY` and `DTSTART` only (no recurrence rules, reminders, or attendees) and takes just the date, dropping any time-of-day.
- Browser notifications only fire while this tab is open in your browser (checked every few minutes) — there's no background push service, so if the tab/browser is fully closed, nothing will notify you until you reopen it (at which point it checks immediately).

## Data & security notes

- All data (tasks, tracker rows, firm records, and imported sheets) lives in your browser, scoped to whatever URL/origin you open the app from. Using it from `file://`, from `localhost`, and from your deployed URL are three different storage buckets — pick one place and stick with it.
- This is a single-user, local-only tool by design — there's no login and no server, so nothing here is visible to anyone else or from any other device/browser. If you ever need the same live data on more than one device, that would require real hosting with a database, which is a different (and larger) project than this.
- Storage is IndexedDB (typically hundreds of MB to a few GB available, tied to your disk space) rather than the much smaller `localStorage` — tested clean importing 100,000 rows into a single tracker. If a browser genuinely doesn't support IndexedDB, saves fall back to `localStorage` and you'll get a toast warning if something is too large to fit there.
- **Everything autosaves as you go** — there's no "Save" button to remember. Every add, edit, delete, or import writes straight to IndexedDB immediately, so closing the tab, closing the browser, or shutting down your laptop normally won't lose anything already on screen. The one thing to know: if you click into a table cell to edit it, type a change, and then close the browser *while that cell is still mid-edit* (before clicking away or pressing Enter), the app now force-commits that pending edit the moment the tab is closed or hidden — so even that in-progress keystroke is captured rather than lost.
- Excel parsing uses the bundled [SheetJS](https://sheetjs.com) `xlsx` library (vendored in `vendor/`, not loaded from a CDN, so it also works fully offline). The version available for this project has known, unpatched advisories around parsing maliciously crafted `.xlsx` files (prototype pollution / ReDoS). Only open spreadsheet files you trust; if in doubt, save as `.csv` first (this app's own CSV parser doesn't use that library).
