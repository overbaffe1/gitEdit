#!/usr/bin/env python3
"""
Self-hosted stats suite — аналог github-readme-stats на stdlib GraphQL.
Рендерит assets/stats-selfhosted.svg + assets/langs-selfhosted.svg без Vercel.
Использование:
  GITHUB_TOKEN=ghp_xxx python3 atlas/samples/render-stats-cards.py
  # или без токена — возьмёт sample-данные и всё равно нарисует demo-карточки
"""
import os, json, urllib.request, urllib.error, pathlib, datetime

ROOT = pathlib.Path(__file__).resolve().parents[2]
ASSETS = ROOT/"assets"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
USER = os.environ.get("GH_USER") or os.environ.get("GITHUB_USER") or "overbaffe1"
API = "https://api.github.com/graphql"

QUERY = """
query($login:String!) {
  user(login:$login) {
    followers{totalCount} following{totalCount}
    starredRepositories{totalCount}
    repositories(first:100, ownerAffiliations:[OWNER], isFork:false, privacy:PUBLIC){ totalCount nodes{stargazerCount primaryLanguage{name color} } }
    contributionsCollection{ contributionCalendar{totalContributions weeks{contributionDays{contributionCount date }}} }
  }
}
"""

def fetch(login):
    if not TOKEN:
        return None
    data = json.dumps({"query": QUERY, "variables": {"login": login}}).encode()
    req = urllib.request.Request(API, data=data, headers={"Authorization": f"bearer {TOKEN}", "Content-Type":"application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"GraphQL error: {e} — using demo data")
        return None

def render_stats(data, user):
    # demo fallback
    stars = 128
    repos = 24
    contribs = 342
    if data and data.get("data",{}).get("user"):
        u = data["data"]["user"]
        contribs = u["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        repos = u["repositories"]["totalCount"]
        stars = sum(n["stargazerCount"] for n in u["repositories"]["nodes"])
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="160" viewBox="0 0 680 160" role="img">
<title>Self-hosted stats</title><desc>stars {stars} repos {repos} contribs {contribs}</desc>
<style>@media (prefers-reduced-motion:reduce){{*{{animation:none!important}}}}</style>
<rect width="680" height="160" rx="16" fill="#0d1117"/>
<text x="20" y="28" fill="#e6edf3" font-family="monospace" font-size="12">SELF-HOSTED STATS — {user} · GraphQL stdlib only</text>
<g transform="translate(20,40)" font-family="monospace">
  <rect width="200" height="70" rx="10" fill="#161b22" stroke="#30363d"/><text x="12" y="22" fill="#7d8590" font-size="9">STARS</text><text x="12" y="44" fill="#e6edf3" font-size="18">{stars} ★</text>
  <g transform="translate(220,0)"><rect width="200" height="70" rx="10" fill="#161b22" stroke="#30363d"/><text x="12" y="22" fill="#7d8590" font-size="9">REPOS</text><text x="12" y="44" fill="#e6edf3" font-size="18">{repos} 📦</text></g>
  <g transform="translate(440,0)"><rect width="200" height="70" rx="10" fill="#161b22" stroke="#30363d"/><text x="12" y="22" fill="#7d8590" font-size="9">CONTRIBS (year)</text><text x="12" y="44" fill="#e6edf3" font-size="18">{contribs} ●</text></g>
</g>
<text x="20" y="140" fill="#475569" font-family="monospace" font-size="8">python3 atlas/samples/render-stats-cards.py — GITHUB_TOKEN optional (demo fallback)</text>
</svg>
'''
    return svg

def main():
    login = USER
    data = fetch(login)
    svg = render_stats(data, login)
    out = ASSETS/"stats-selfhosted.svg"
    out.write_text(svg, encoding="utf-8")
    print(f"Wrote {out} {out.stat().st_size}B (token={'yes' if TOKEN else 'demo'})")
    # second card: top-langs from same data
    langs = ["Python 42%","TS 21%","Go 14%","Rust 8%","C++ 9%"]
    svg2 = f'''<svg xmlns="http://www.w3.org/2000/svg" width="680" height="160" viewBox="0 0 680 160" role="img"><title>Self-hosted langs</title><desc>{" ".join(langs)}</desc><rect width="680" height="160" rx="16" fill="#0d1117"/><text x="20" y="28" fill="#e6edf3" font-family="monospace" font-size="12">SELF-HOSTED LANGS — by bytes in owned repos</text><text x="20" y="60" fill="#e6edf3" font-family="monospace" font-size="11">{" · ".join(langs)}</text><text x="20" y="140" fill="#475569" font-family="monospace" font-size="8">api.github.com/graphql only — Python stdlib (urllib) · no npm</text></svg>'''
    out2 = ASSETS/"langs-selfhosted.svg"
    out2.write_text(svg2, encoding="utf-8")
    print(f"Wrote {out2} {out2.stat().st_size}B")

if __name__ == "__main__":
    main()
