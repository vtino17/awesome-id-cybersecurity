from pathlib import Path
import re
from urllib.parse import urlsplit


text = Path("README.md").read_text(encoding="utf-8")
links = re.findall(r"\[[^\]]+\]\(([^)]+)\)", text)
external = [link for link in links if not link.startswith("#") and "://" in link]

assert external, "catalog must contain external resources"
for link in external:
    parsed = urlsplit(link)
    assert parsed.scheme == "https", f"external link must use HTTPS: {link}"
    assert parsed.hostname, f"external link has no hostname: {link}"

assert "nc -e" not in text, "catalog must not embed reverse-shell commands"
assert "google.com/search" not in text, "catalog must link to authoritative resources"
assert "Rp " not in text and "$400" not in text, "catalog must not freeze volatile prices"

print(f"validated {len(external)} external catalog links")
