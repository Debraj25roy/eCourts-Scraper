# eCourts Scraper (Internship Task)

A beginner-friendly Python project that checks if a given case (CNR) is listed for **today** or **tomorrow** on the eCourts portal.

## 🎯 Features
- Simple command-line interface (CLI)
- Search by **CNR number**
- Choose to check **today’s** or **tomorrow’s** listings
- Saves results to `outputs/result_*.json`
- Handles site errors or captcha gracefully

## ⚙️ Requirements
Python 3.8+

Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 How to Run
```bash
python ecourts_scraper.py --when today
```
OR
```bash
python ecourts_scraper.py --when tomorrow
```

Then follow the prompts to enter the **CNR number**.

## 🧾 Output Example
```json
{
  "query": "MHAB010123452024",
  "when": "today",
  "found": true,
  "listings": [
    {"row": "1 | MHAB01012345 | Civil Case | 14-10-2025 | Court 3"}
  ]
}
```

## ⚠️ Limitations
- The official eCourts website uses JavaScript and captcha.
- This script uses simple HTTP requests, so it may not fetch all listings.
- When blocked, it saves the raw HTML for transparency.


## 👨‍💻 Author
**Debraj Roy** — submitted for internship selection.
