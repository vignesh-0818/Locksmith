import urllib.request
import re
import os
from PIL import Image
import io

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

def scrape_unsplash_photos(query):
    query_slug = query.replace(' ', '-')
    url = f'https://unsplash.com/s/photos/{query_slug}'
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            imgs = re.findall(r'https://images\.unsplash\.com/photo-[a-zA-Z0-9\-]+', html)
            seen = set()
            unique_imgs = []
            for img in imgs:
                # filter out small icons or user avatars if any
                if img not in seen:
                    seen.add(img)
                    unique_imgs.append(img)
            return unique_imgs
    except Exception as e:
        print(f"Error scraping {query}: {e}")
        return []

queries = {
    'emergency_lockout': 'locksmith-door',
    'key_cutting': 'key-machine',
    'lock_rekeying': 'lock-cylinder',
    'deadbolt': 'door-deadbolt',
    'car_key': 'car-key-fob',
    'smart_lock': 'keypad-lock',
    'master_key': 'keys-keyring',
    'commercial_lock': 'security-door-lock',
    'safe_vault': 'bank-vault-safe',
    'broken_key': 'lock-tools',
    'access_control': 'rfid-access-control',
    'door_closer': 'door-closer-hinge'
}

for k, q in queries.items():
    res = scrape_unsplash_photos(q)
    print(f"{k} ({q}) -> {len(res)} URLs found")
    if res:
        print(f"  sample: {res[:2]}")
