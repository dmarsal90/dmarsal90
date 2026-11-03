"""Rewrite the block between the STATS markers in README.md with public GitHub totals."""
import json
import os
import re
import urllib.request

USER = "dmarsal90"
API = "https://api.github.com"


def get(path):
    req = urllib.request.Request(API + path, headers={
        "Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
    })
    with urllib.request.urlopen(req, timeout=30) as res:
        return json.load(res)


user = get(f"/users/{USER}")
repos, page = [], 1
while True:
    chunk = get(f"/users/{USER}/repos?per_page=100&page={page}&type=owner")
    repos += chunk
    if len(chunk) < 100:
        break
    page += 1
commits = get(f"/search/commits?q=author:{USER}&per_page=1")["total_count"]

block = (
    "<!-- STATS:START -->\n"
    f"**{user['public_repos']}** public repos · "
    f"**{sum(r['stargazers_count'] for r in repos)}** stars · "
    f"**{user['followers']}** followers · "
    f"**{commits}** public commits\n"
    "<!-- STATS:END -->"
)

with open("README.md", encoding="utf-8") as f:
    text = f.read()
new, n = re.subn(r"<!-- STATS:START -->.*?<!-- STATS:END -->", lambda _: block, text, flags=re.S)
if n != 1:
    raise SystemExit("README.md needs exactly one STATS:START/STATS:END block")
with open("README.md", "w", encoding="utf-8") as f:
    f.write(new)
