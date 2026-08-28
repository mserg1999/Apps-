# Chess Lesson Availability Calendar

A fun, chess-themed availability picker for Doug to mark the days and times he's free to teach Mahlet how to play chess. It's a Progressive Web App (PWA), so it can be installed like a real app — its own icon, its own window, and it keeps working offline.

## Features

- Interactive month calendar with a chessboard look — click a date to open its time slots.
- Click or drag across time slots (7 AM–9 PM, 30-minute blocks) to mark yourself available, "Mark whole day free," or clear a day in one click.
- Live summary of everything that's been scheduled, with one-click removal per day.
- **Lesson reminders** — exactly two nudges per lesson: 7:00 PM the night before, and 8:00 AM the day of. No account, no outside calendar — just this app.
- **Installable app** — add it to your home screen or desktop with its own icon and window, and it keeps working offline once installed (via a service worker).
- **Save Offline Copy** — also saves the whole page as a single self-contained HTML file you can keep or move around without hosting anything.
- Everything is saved to the browser's local storage, so refreshing the page (or reopening the installed app) won't lose your picks.

## Installing it as a real app

Installing (rather than just opening the HTML file) needs the app served over `http://` or `https://` — browsers won't let a page installed from a bare double-clicked file register a service worker or show an install prompt.

**Note:** GitHub Pages only works for free on a *public* repo (a private repo needs GitHub Pro, or an org on GitHub Team/Enterprise). If this repo stays private, use a free static host instead — it deploys straight from the private repo with no plan upgrade:

1. Go to [netlify.com](https://www.netlify.com) and sign in with GitHub (free).
2. **Add new site → Import an existing project → GitHub**, authorize it, and pick this repository.
3. Netlify reads the included `netlify.toml`, so the base/publish directory is already set to `chess-availability-calendar/` — just pick the branch with the app on it and click **Deploy**.
4. You'll get a URL like `https://your-site-name.netlify.app` in under a minute. Rename it in Site settings → General → "Change site name" if you want something friendlier.
5. Share that URL with Doug (text, email, whatever) — see "Getting it onto Doug's home screen" below.

If you'd rather use GitHub Pages, just flip the repo to public first (Settings → General → Danger Zone → Change visibility), then Settings → Pages → Source → deploy from a branch → root. The app will be reachable at `<pages-url>/chess-availability-calendar/`.

Once hosted, it opens in its own window/icon like a native app and keeps working without an internet connection.

## Getting it onto Doug's home screen

Once the app has a real URL (from Netlify, GitHub Pages, or any host), send that link to Doug. He opens it once, then:

- **iPhone (Safari):** tap the **Share** icon (square with an arrow) → scroll down → **Add to Home Screen** → **Add**.
- **Android (Chrome):** Chrome usually shows an **Install app** banner automatically — tap it. If not, tap the **⋮** menu → **Install app** (or **Add to Home screen**).

Either way, an app icon (the green chess knight) shows up on his home screen. Tapping it opens the calendar full-screen, no browser bar, and it keeps working offline. The first time he opens it, have him tap **Turn On Reminders** and allow notifications so the night-before/day-of nudges work.

## Just running it locally

Open `index.html` directly in a browser to use every calendar feature immediately — no build step, dependencies, or server needed. The only things that require real hosting are installability and the service worker's offline cache; the app tells you which mode you're in and adjusts its instructions accordingly.

Reminders fire from within the app/browser itself (there's no external push server), so for the 7 PM / 8 AM nudges to actually appear, the app needs to be open (or installed and running in the background) around those times.
