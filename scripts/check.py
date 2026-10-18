#!/usr/bin/env python3
"""Check local HTML, CSS and search-index destinations in a built site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
import json, re, sys
ROOT = Path(__file__).resolve().parents[1] / 'dist'
base = json.loads((ROOT / 'manifest.json').read_text())['start_url']
errors = set()
count = 0

def check(value, source):
    global count
    if not value or value.startswith(('#','data:','mailto:','tel:','javascript:')):
        return
    url = urlsplit(value)
    if value.startswith(base):
        target = ROOT / unquote(urlsplit(value[len(base):]).path)
    elif url.scheme or url.netloc:
        return
    elif value.startswith('/'):
        errors.add(f'{source.relative_to(ROOT)}: unexpected root URL {value}'); return
    else:
        target = source.parent / unquote(url.path)
    count += 1
    if target.is_dir(): target = target / 'index.html'
    if not target.is_file(): errors.add(f'{source.relative_to(ROOT)}: missing {value}')

class Parser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        for key in ('src','href','poster'):
            if key in a: check(a[key], self.source)
        if tag == 'meta' and a.get('http-equiv','').lower() == 'refresh':
            match = re.search(r'url=(.*)', a.get('content',''), re.I)
            if match: check(match[1], self.source)

for f in ROOT.rglob('*'):
    if f.suffix in {'.html','.css','.js','.json','.xml'}:
        text = f.read_text()
        if '__SITE_BASE__' in text or 'bscresearch.github.io/ekip' in text:
            errors.add(f'{f.relative_to(ROOT)}: unreplaced publishing address')
        if f.suffix == '.html':
            parser = Parser(); parser.source = f; parser.feed(text)
        elif f.suffix == '.css':
            for url in re.findall(r'url\([\"\']?([^\)\"\']+)', text): check(url, f)
        elif f.name == 'search-data.json':
            for item in json.loads(text): check(item['href'], f)
        elif f.name == 'search.js':
            for url in re.findall(r"https?[^'\"\s]+\.json", text): check(url, f)
print(f'Checked {count} local references across {len(list(ROOT.rglob("*.html")))} HTML pages.')
for error in sorted(errors): print(error)
sys.exit(bool(errors))
