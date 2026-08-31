# Julie's Wedding Dress Finder

A single-page tool for organizing Julie's wedding dress search: measurements, budget, wedding date, style preferences, reference photos, and the stores worth considering — plus a fast way to launch real searches and a reminder of what to check before buying, since wedding gowns are one of the most return-restricted things you can buy.

## Features

- **Measurements & basics** — bust/waist/hip/height, wedding date, and a budget range (inches or centimeters).
- **Bridal size estimate** — turns those measurements into a starting size against a standard bridal size chart, sized to the largest measurement (the standard bridal-shop rule of thumb, since alterations can take a gown in but rarely let it out). Always double-check against the specific brand's own chart.
- **Style preferences** — silhouette, neckline, sleeves, fabric/detail, and color as quick toggle chips, plus free-text notes for anything else (designers, must-haves, dealbreakers).
- **Reference photos** — drop in inspiration pictures; they're resized and stored right in the browser, with a caption field per photo. Links out to Google Lens / Pinterest for visual (reverse-image) search, since a static page can't run image recognition itself.
- **Stores & return reliability** — a curated list of well-known bridal retailers (Azazie, Anthropologie Weddings/BHLDN, Lulus, Nordstrom, Revolve, ASOS, David's Bridal, Kleinfeld, Etsy sellers) with a plain-language summary of each one's actual return policy and a reliability badge, plus room to add any other store by name/URL.
- **Find Dresses** — builds ready-to-click Google search links scoped to just the stores you picked (`site:store1.com OR site:store2.com ...` plus your style terms and budget), so results come straight from the retailers' current listings.
- **Shopping timeline** — order-by, first-fitting, and final-fitting dates worked backward from the wedding date using typical bridal lead times.
- **Returns checklist** — the things worth confirming before paying: return window, final-sale/custom-order status, fees, condition rules, refund type, and proof-of-condition photos.
- Everything autosaves to the browser's local storage. **Export/Import** buttons move a full profile (including photos) to another device or share it, and **Print shopping brief** gives a clean printable summary to bring to an appointment.

## Why it doesn't silently "scan the internet"

A static page running in your browser can't quietly crawl third-party retailer sites on its own — browsers block cross-site scraping like that (CORS), and it would violate most stores' terms of service anyway. Building a real crawler would mean standing up a server plus paid search/shopping APIs and ongoing maintenance as sites change, which is a different (and much bigger) project than this.

Instead, this app compiles everything you enter into precise, store-scoped search links — including one combined search across every store you picked — so real, current results are one click away, straight from the source.

## Running it

No build step or dependencies — just open `index.html` in a browser.

To host it (for Julie to use from her phone), deploy it as its own Netlify site the same way the other apps in this repo are deployed:

1. On [netlify.com](https://www.netlify.com), **Add new site → Import an existing project → GitHub**, and pick this repository.
2. Under **Site settings → Build & deploy**, set the base/publish directory to `wedding-dress-finder/` (this app doesn't share the root `netlify.toml`, which points at the other app in this repo).
3. Deploy — you'll get a URL like `https://your-site-name.netlify.app`.

## Data & privacy

Everything — measurements, budget, style picks, and reference photos — is stored only in `localStorage` in the browser it was entered in. Nothing is uploaded anywhere. Use **Export profile** to back it up or move it to another browser/device.
