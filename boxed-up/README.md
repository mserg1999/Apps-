# Boxed Up — Moving Budget Tracker

A fun, editable budget tracker for a move — every couch, deposit, and roll of packing tape in one checklist-style ledger. It's a Progressive Web App (PWA), so it can be installed like a real app — its own icon, its own window, and it keeps working offline once installed.

## Features

- Seven starter categories (Furniture, Kitchen, Household Supplies, Moving Logistics, Move-in Fees, Utilities & Setup, First Week) pre-filled with realistic sample costs — edit or delete anything, or add your own items and categories.
- Check an item off once you've bought it — it gets a strikethrough and rolls into the "packed" tally.
- A move-in date countdown and an optional budget goal that tells you if you're under or over.
- A sticky bottom bar with the running grand total and packed count.
- **Installable app** — add it to your home screen or desktop with its own icon and window, and it keeps working offline once installed (via a service worker).
- **Save Offline Copy** — also saves the whole page as a single self-contained HTML file you can keep or move around without hosting anything.
- Everything is saved to the browser's local storage, so refreshing the page (or reopening the installed app) won't lose your edits.

## Installing it as a real app

Installing (rather than just opening the HTML file) needs the app served over `http://` or `https://` — browsers won't let a page installed from a bare double-clicked file register a service worker or show an install prompt.

**Note:** GitHub Pages only works for free on a *public* repo (a private repo needs GitHub Pro, or an org on GitHub Team/Enterprise). If this repo stays private, use a free static host instead — it deploys straight from the private repo with no plan upgrade:

1. Go to [netlify.com](https://www.netlify.com) and sign in with GitHub (free).
2. **Add new site → Import an existing project → GitHub**, authorize it, and pick this repository.
3. When asked for the Base directory, set it to `boxed-up/` — that folder's own `netlify.toml` (base/publish already set) takes it from there. Pick the branch with the app on it and click **Deploy**.
4. You'll get a URL like `https://your-site-name.netlify.app` in under a minute. Rename it in Site settings → General → "Change site name" if you want something friendlier.
5. Share that URL with anyone moving in with you — see "Getting it onto your home screen" below.

If you'd rather use GitHub Pages, just flip the repo to public first (Settings → General → Danger Zone → Change visibility), then Settings → Pages → Source → deploy from a branch → root. The app will be reachable at `<pages-url>/boxed-up/`.

Once hosted, it opens in its own window/icon like a native app and keeps working without an internet connection.

## Getting it onto your home screen

Once the app has a real URL (from Netlify, GitHub Pages, or any host), open it once, then:

- **iPhone (Safari):** tap the **Share** icon (square with an arrow) → scroll down → **Add to Home Screen** → **Add**.
- **Android (Chrome):** Chrome usually shows an **Install app** banner automatically — tap it. If not, tap the **⋮** menu → **Install app** (or **Add to Home screen**).
- **Desktop (Chrome/Edge):** click the install icon in the address bar, or the **⋮** menu → **Install Boxed Up**.

Either way, an app icon (the little packing box) shows up on your home screen or app list. Tapping it opens the tracker full-screen, no browser bar, and it keeps working offline.

## Just running it locally

Open `index.html` directly in a browser to use every feature immediately — no build step, dependencies, or server needed. The only things that require real hosting are installability and the service worker's offline cache; the app tells you which mode you're in and adjusts its instructions accordingly. Use **Save Offline Copy** any time to grab a portable single-file version.
