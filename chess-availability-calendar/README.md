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

Installing (rather than just opening the HTML file) needs the app served over `http://` or `https://` — browsers won't let a page installed from a bare double-clicked file register a service worker or show an install prompt. The easiest free option is GitHub Pages:

1. In the repo settings, enable **GitHub Pages** for this branch (or merge to your default branch first), serving from the `/chess-availability-calendar` folder (or root, adjusting the path).
2. Open the published URL in Chrome, Edge, or Android — you'll see an "Install App" button in the page (and usually one in the browser's address bar too).
3. On iOS Safari, use the Share icon → **Add to Home Screen**.

Once installed, it opens in its own window/icon like a native app and keeps working without an internet connection.

## Just running it locally

Open `index.html` directly in a browser to use every calendar feature immediately — no build step, dependencies, or server needed. The only things that require real hosting are installability and the service worker's offline cache; the app tells you which mode you're in and adjusts its instructions accordingly.

Reminders fire from within the app/browser itself (there's no external push server), so for the 7 PM / 8 AM nudges to actually appear, the app needs to be open (or installed and running in the background) around those times.
