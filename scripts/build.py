#!/usr/bin/env python3
"""Build the recovered static site for a specific hosting URL (standard library only)."""
import argparse
from pathlib import Path
from urllib.parse import urlsplit
import shutil

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--base-url', default='http://localhost:8000/', help='Full public URL, including repository path if any')
args = parser.parse_args()
base = args.base_url.rstrip('/') + '/'
u = urlsplit(base)
if u.scheme not in ('http', 'https') or not u.netloc or u.query or u.fragment or any(c in base for c in '\"\'<>\\'):
    parser.error('--base-url must be an HTTP(S) URL without query, fragment, quotes, or backslashes')
output = ROOT / 'dist'
if output.exists():
    shutil.rmtree(output)
shutil.copytree(ROOT / 'site', output)
for path in output.rglob('*'):
    if path.suffix in {'.html', '.css', '.js', '.json', '.xml', '.svg'}:
        path.write_text(path.read_text(encoding='utf-8').replace('__SITE_BASE__', base), encoding='utf-8')
print(f'Built {output} for {base}')
