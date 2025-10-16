# ecourts_scraper.py1

import argparse
import requests
from bs4 import BeautifulSoup
import json, os, time
from datetime import datetime, timedelta

BASE_URL = 'https://services.ecourts.gov.in/ecourtindia_v6/'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def build_date_string(when):
    today = datetime.now()
    target = today if when == 'today' else today + timedelta(days=1)
    return target.strftime('%d-%m-%Y')

def save_raw_html(html, prefix='raw_'):
    os.makedirs('outputs', exist_ok=True)
    fname = os.path.join('outputs', f"{prefix}{int(time.time())}.html")
    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    return fname

def save_output(data):
    os.makedirs('outputs', exist_ok=True)
    fname = os.path.join('outputs', f"result_{int(time.time())}.json")
    with open(fname, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    return fname

def fetch_case_by_cnr(cnr, when):
    result = {'query': cnr, 'when': when, 'found': False, 'listings': []}
    date_str = build_date_string(when)

    url = f"{BASE_URL}?p=casestatus%2Findex&cnr={cnr}"
    try:
        res = requests.get(url, headers=HEADERS, timeout=15)
        if res.status_code == 200:
            soup = BeautifulSoup(res.text, 'html.parser')
            text = soup.get_text().lower()
            if 'captcha' in text or 'javascript' in text:
                result['message'] = 'Site requires captcha or JavaScript — saved HTML.'
                result['html_file'] = save_raw_html(res.text)
                return result

            for tr in soup.find_all('tr'):
                if cnr.lower() in tr.get_text().lower() or date_str in tr.get_text():
                    cols = [c.get_text(strip=True) for c in tr.find_all(['td','th'])]
                    result['found'] = True
                    result['listings'].append({'row': ' | '.join(cols)})

            pdfs = [a['href'] for a in soup.find_all('a', href=True) if '.pdf' in a['href'].lower()]
            if pdfs:
                result['pdf_links'] = pdfs

    except Exception as e:
        result['error'] = str(e)

    result['message'] = result.get('message', 'Search complete.')
    return result

def main():
    parser = argparse.ArgumentParser(description='Simple eCourts Scraper')
    parser.add_argument('--when', choices=['today','tomorrow'], default='today', help='Check listings for today or tomorrow')
    args = parser.parse_args()

    print('\n🧾 eCourts Scraper — Internship Project')
    print('Checking for:', args.when, build_date_string(args.when))

    mode = input('\nSearch by (1) CNR or (2) Case number? Enter 1 or 2: ').strip()

    if mode == '1':
        cnr = input('Enter CNR Number: ').strip()
        result = fetch_case_by_cnr(cnr, args.when)
        out_file = save_output(result)
        print(f'\nSaved output to {out_file}')
    else:
        print('\nCase number mode not fully implemented (for simplicity). Try CNR mode.')

    print('\n✅ Done. This project is a simple demonstration — no complex automation used.')

if __name__ == '__main__':
    main()
