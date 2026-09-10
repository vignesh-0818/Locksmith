import urllib.request
import io
import os
import hashlib
from PIL import Image

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

# All existing hashes in assets/images/
existing_hashes = set()
for root, dirs, files in os.walk('assets/images'):
    for f in files:
        path = os.path.join(root, f)
        with open(path, 'rb') as fp:
            existing_hashes.add(hashlib.sha256(fp.read()).hexdigest())

print(f"Total existing image hashes: {len(existing_hashes)}")

candidate_list = [
    # (category, filename, url)
    ('services', 'emergency-lockout-new.jpg', 'https://images.unsplash.com/photo-1590856029826-c7a73142bbf1?auto=format&fit=crop&w=800&h=533&q=80'),
    ('services', 'key-cutting-new.jpg', 'https://images.unsplash.com/photo-1589829545856-d10d557cf95f?auto=format&fit=crop&w=800&h=533&q=80'),
    ('services', 'lock-rekeying-new.jpg', 'https://images.unsplash.com/photo-1581092160607-ee22621dd758?auto=format&fit=crop&w=800&h=533&q=80'),
    ('services', 'deadbolt-installation-new.jpg', 'https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&w=800&h=533&q=80'),
    ('services', 'automotive-key-programming-new.jpg', 'https://images.unsplash.com/photo-1617814076367-b759c7d7e738?auto=format&fit=crop&w=800&h=533&q=80'),
    ('services', 'smart-lock-installation-new.jpg', 'https://images.unsplash.com/photo-1557597774-9d273605dfa9?auto=format&fit=crop&w=800&h=533&q=80'),
    ('services', 'commercial-master-key-new.jpg', 'https://images.unsplash.com/photo-1563245372-f21724e3856d?auto=format&fit=crop&w=800&h=533&q=80'),
    ('services', 'commercial-security-new.jpg', 'https://images.unsplash.com/photo-1486406146926-c627a92ad1ab?auto=format&fit=crop&w=800&h=533&q=80'),
    ('services', 'safe-opening-new.jpg', 'https://images.unsplash.com/photo-1563013544-824ae1b704d3?auto=format&fit=crop&w=800&h=533&q=80'),
    ('services', 'broken-key-extraction-new.jpg', 'https://images.unsplash.com/photo-1581092580497-e0d23cbdf1dc?auto=format&fit=crop&w=800&h=533&q=80'),
    ('services', 'access-control-new.jpg', 'https://images.unsplash.com/photo-1563986768609-322da13575f3?auto=format&fit=crop&w=800&h=533&q=80'),
    ('services', 'door-hardware-repair-new.jpg', 'https://images.unsplash.com/photo-1534349762230-e0cadf78f5da?auto=format&fit=crop&w=800&h=533&q=80'),

    ('blog', 'blog-deadbolt-guide.jpg', 'https://images.unsplash.com/photo-1544816155-12df9643f363?auto=format&fit=crop&w=800&h=533&q=80'),
    ('blog', 'blog-locked-out-tips.jpg', 'https://images.unsplash.com/photo-1516455590571-18256e5bb9ff?auto=format&fit=crop&w=800&h=533&q=80'),
    ('blog', 'blog-smart-vs-deadbolt.jpg', 'https://images.unsplash.com/photo-1558002038-94473b64c76b?auto=format&fit=crop&w=800&h=533&q=80'),
    ('blog', 'blog-rekey-vs-replace.jpg', 'https://images.unsplash.com/photo-1616401784845-180882ba9ba8?auto=format&fit=crop&w=800&h=533&q=80'),
    ('blog', 'blog-car-key-programming.jpg', 'https://images.unsplash.com/photo-1541899481282-d53bffe3c35d?auto=format&fit=crop&w=800&h=533&q=80'),
    ('blog', 'blog-commercial-master-keys.jpg', 'https://images.unsplash.com/photo-1533090161767-e6ffed986c88?auto=format&fit=crop&w=800&h=533&q=80')
]

os.makedirs('assets/images/services', exist_ok=True)
os.makedirs('assets/images/blog', exist_ok=True)

downloaded = []
for folder, fname, url in candidate_list:
    target_path = os.path.join('assets/images', folder, fname)
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=12) as resp:
            data = resp.read()
            h = hashlib.sha256(data).hexdigest()
            is_dup_existing = h in existing_hashes
            img = Image.open(io.BytesIO(data))
            img.save(target_path, 'JPEG', quality=85)
            print(f"Downloaded {target_path}: {img.size}, bytes={len(data)}, dup_of_existing={is_dup_existing}")
            downloaded.append((target_path, is_dup_existing, h))
    except Exception as e:
        print(f"FAILED {target_path}: {e}")

print(f"\nTotal downloaded: {len(downloaded)} / {len(candidate_list)}")
