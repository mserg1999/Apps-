# Outside Counsel Directory

A searchable directory of outside counsel / claims panel law firms, in a single `index.html` file with no dependencies.

## What it tracks
- Law firm name
- TIN (masked by default — click **Show** to reveal, **Copy** to copy)
- States served
- Primary, billing, and IT contacts (name, title, email, phone)

## Features
- **Search** by firm name or state, using either the code (`TX`) or the name (`Texas`), plus a state dropdown filter. Click any state tag on a card to see every firm in that state. Press `/` to jump to search.
- **Add / edit / delete** firms. TIN is auto-formatted (`12-3456789`) and checked for duplicates.
- **Export CSV** of the current search results (opens in Excel).
- **Backup / Restore** the whole directory as a JSON file.

## Data storage
Data is saved in the browser's local storage, so each person and browser has its own copy. Use **Backup** / **Restore** to move or share it. The four firms that appear on first open are fictional samples; delete them before you add real data.

## Running it
Open `index.html` in any browser, or host the folder on any static host (Netlify, GitHub Pages, etc.).
