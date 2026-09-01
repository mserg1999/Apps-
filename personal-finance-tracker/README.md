# 🌸 Bloom Budget — Personal Finance Tracker

A fun, pastel (lavender 💜 / yellow 💛 / baby pink 🩷) personal finance app for tracking spending, planning savings goals with deadlines, and staying on top of short-term bills and long-term debt like federal and private student loans. It's a Progressive Web App (PWA), so it can be installed like a real app and keeps working offline.

## Features

- **Dashboard** with live stat cards (balance, monthly income, monthly spending, savings rate) that update instantly whenever you add or remove a transaction.
- **Transactions** — log income and expenses across categories: Rent, WiFi, Utilities, Phone Bill, Subscriptions, Food, Entertainment, Shopping, Household Supplies, Transportation, Student Loans (Federal & Private), and more. Filter by type, category, or month.
- **Savings Goals** — set a target amount and a deadline, pick a fun emoji, then add or withdraw funds and watch the progress bar, "days left," and "$/month needed to hit your goal" update live. Goals that fall behind pace get flagged; hitting 100% triggers a confetti celebration 🎉.
- **Bills & Loans** — track short-term recurring bills (rent, subscriptions, utilities, etc.) with due-date chips and one-tap "Mark as Paid," plus long-term debt (federal/private student loans or other debt) with payoff progress bars and an estimated payoff date based on your monthly payment.
- **Insights** — fun facts about your habits, a category spending leaderboard, and a month-over-month spending comparison.
- Pastel, rounded, emoji-forward UI designed to feel encouraging rather than stressful.
- **Installable app** — add it to your home screen or desktop with its own icon and window, and it keeps working offline once installed (via a service worker).
- Everything is saved to the browser's local storage — nothing leaves your device. Use Settings (⚙️) to set a starting balance, export a JSON backup, import one back in, or reset all data.

## Installing it as a real app

Installing (rather than just opening the HTML file) needs the app served over `http://` or `https://` — browsers won't let a page installed from a bare double-clicked file register a service worker or show an install prompt.

1. Go to [netlify.com](https://www.netlify.com) and sign in with GitHub (free).
2. **Add new site → Import an existing project → GitHub**, authorize it, and pick this repository.
3. Netlify reads the included `netlify.toml`, so the base/publish directory is already set to `personal-finance-tracker/` — just pick the branch with this app on it and click **Deploy**.
4. You'll get a URL like `https://your-site-name.netlify.app` in under a minute. Rename it in Site settings → General → "Change site name" if you want something friendlier.

If you'd rather use GitHub Pages, flip the repo to public first (Settings → General → Danger Zone → Change visibility), then Settings → Pages → Source → deploy from a branch → root. The app will be reachable at `<pages-url>/personal-finance-tracker/`.

## Getting it onto your home screen

Once the app has a real URL (from Netlify, GitHub Pages, or any host), open it once, then:

- **iPhone (Safari):** tap the **Share** icon (square with an arrow) → scroll down → **Add to Home Screen** → **Add**.
- **Android (Chrome):** Chrome usually shows an **Install app** banner automatically — tap it. If not, tap the **⋮** menu → **Install app** (or **Add to Home screen**).

Either way, the piggy-bank icon shows up on your home screen. Tapping it opens the app full-screen, no browser bar, and it keeps working offline.

## Just running it locally

Open `index.html` directly in a browser to use every feature immediately — no build step, dependencies, or server needed. The only things that require real hosting are installability and the service worker's offline cache.

## Your data

All transactions, goals, bills, and loans are stored only in your browser's local storage on that device/browser. There's no account, no server, and no syncing. Use the **Export Data** button in Settings regularly if you want a backup, and **Import Data** to restore it (or move it to another browser/device).
