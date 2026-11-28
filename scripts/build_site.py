"""Rebuild the home page, the nav and day-page front matter from scripts/episodes.json.

Add a new day: append it to "episodes", update "next", then run
    python scripts/build_site.py && mkdocs build --strict
"""
import json, re, html, pathlib

ROOT = pathlib.Path(__file__).resolve().parent.parent
D = json.loads((ROOT / "scripts/episodes.json").read_text())
EPS, MODS, NXT = D["episodes"], D["modules"], D["next"]
N = len(EPS)
latest = EPS[-1]
e = html.escape

def url(ep): return f"days/{ep['slug']}/"
def module_of(day): return (day - 1) // 10

# ---------------- home page ----------------
shelf = []
for d in range(1, 101):
    ep = next((x for x in EPS if x["day"] == d), None)
    m = module_of(d)
    if ep:
        cls = "dd-box is-live" + (" is-latest" if ep is latest else "")
        shelf.append(f'<a class="{cls}" href="{url(ep)}" data-day="{d}" style="--i:{d}" '
                     f'title="Day {d}: {e(ep["topic"])}" aria-label="Day {d}: {e(ep["topic"])}"></a>')
    else:
        shelf.append(f'<span class="dd-box" data-day="{d}" style="--i:{d}" title="Day {d}: coming soon"></span>')
    if d % 10 == 0: shelf.append('</span><span class="dd-shelf-group">' if d < 100 else '</span>')

ledger = []
for m, name in enumerate(MODS):
    eps = [x for x in EPS if module_of(x["day"]) == m]
    nxt = NXT if module_of(NXT["day"]) == m else None
    if not eps and not nxt: continue
    lo, hi = m * 10 + 1, m * 10 + 10
    ledger.append(f'<section class="dd-module" data-module="{m}">')
    ledger.append(f'<h3 class="dd-module-name"><span>Days {lo}–{hi}</span> {e(name)}</h3>')
    ledger.append('<ol class="dd-ledger">')
    for ep in eps:
        tags = "".join(f"<span>{e(t)}</span>" for t in ep["tags"])
        hay = e(" ".join([str(ep["day"]), ep["title"], ep["topic"], *ep["tags"]]).lower())
        ledger.append(
            f'<li class="dd-row" data-day="{ep["day"]}" data-search="{hay}"><a href="{url(ep)}">'
            f'<span class="dd-row-day">{ep["day"]}</span>'
            f'<span class="dd-row-main"><span class="dd-row-topic">{e(ep["topic"])}</span>'
            f'<span class="dd-row-title">{e(ep["title"])}</span></span>'
            f'<span class="dd-row-tags">{tags}</span>'
            f'<span class="dd-row-done" aria-label="Read">✓</span></a></li>')
    if nxt:
        ledger.append(
            f'<li class="dd-row is-soon" data-day="{nxt["day"]}" data-search="{e((str(nxt["day"]) + " " + nxt["title"] + " " + nxt["topic"]).lower())}">'
            f'<div><span class="dd-row-day">{nxt["day"]}</span>'
            f'<span class="dd-row-main"><span class="dd-row-topic">{e(nxt["topic"])}</span>'
            f'<span class="dd-row-title">Coming tomorrow: {e(nxt["title"])}</span></span></div></li>')
    ledger.append('</ol></section>')

chips = ['<button class="dd-chip is-on" data-filter="all">All</button>'] + [
    f'<button class="dd-chip" data-filter="{m}">{e(n)}</button>'
    for m, n in enumerate(MODS) if any(module_of(x["day"]) == m for x in EPS)]

roadmap = []
for m, name in enumerate(MODS):
    done = sum(1 for x in EPS if module_of(x["day"]) == m)
    state = "done" if done == 10 else ("now" if done else "later")
    word = {"done": "Complete", "now": f"{done} of 10 out", "later": "Coming up"}[state]
    roadmap.append(f'<li class="is-{state}"><span class="dd-road-range">Days {m*10+1}–{m*10+10}</span>'
                   f'<span class="dd-road-name">{e(name)}</span><span class="dd-road-state">{word}</span></li>')

index = f'''---
hide: [navigation, toc, footer]
title: Data engineering, explained like a shop
---

<div class="dd-awning" aria-hidden="true"></div>

<div class="dd-hero">
<div class="dd-hero-text">
<h1>Data engineering, explained like a shop.</h1>
<p class="dd-lede">Every app you use, from food delivery to UPI, runs on data pipelines. Each day you get one real problem data engineers face, told as a short story about Raju's shop, then the proper fix with code you can run.</p>
<div class="dd-buttons">
<a class="md-button md-button--primary" href="days/day-01-late-arriving-data/">Start from Day 1</a>
<a class="md-button" href="#episodes">Browse all episodes</a>
</div>
</div>
<a class="dd-today" href="{url(latest)}">
<span class="dd-today-label">New today · Day {latest["day"]}</span>
<span class="dd-today-title">{e(latest["title"])}</span>
<span class="dd-today-topic">{e(latest["topic"])}</span>
<span class="dd-today-cta">Read the notes and run the code</span>
</a>
</div>

<div class="dd-shelf-wrap">
<p class="dd-shelf-caption"><strong>{N} of 100</strong> days out<span class="dd-read-count" hidden></span>. Each box is a day; tap one to open it.</p>
<div class="dd-shelf"><span class="dd-shelf-group">{"".join(shelf)}</div>
<div class="dd-shelf-legend"><span><i class="is-live"></i>Published</span><span><i class="is-read"></i>You've read it</span><span><i></i>Coming up</span></div>
</div>

<ol class="dd-steps">
<li><strong>Watch the 60-second story</strong> on Instagram or YouTube. A shop, a problem, no jargon.</li>
<li><strong>Read the real version</strong> here: why it happens, each fix, trade-offs and interview questions.</li>
<li><strong>Run the code</strong> on a tiny dataset and watch the numbers change on your laptop.</li>
</ol>

<h2 id="episodes">Episodes</h2>

<div class="dd-finder">
<label class="dd-search"><span class="dd-sr">Search episodes</span>
<input type="search" placeholder="Search a topic, like shuffle, CDC or partitions" autocomplete="off"></label>
<div class="dd-chips" role="group" aria-label="Filter by module">{"".join(chips)}</div>
</div>
<p class="dd-empty" hidden>No episode matches that yet. Try a broader word, or browse all.</p>

<div class="dd-ledger-wrap">
{chr(10).join(ledger)}
</div>

<h2>The 100-day path</h2>

<ol class="dd-road">
{chr(10).join(roadmap)}
</ol>

<h2>Who it's for</h2>

<ul class="dd-who">
<li><strong>Students</strong> deciding whether data engineering is for them.</li>
<li><strong>Career switchers</strong> who want the ideas before the tools.</li>
<li><strong>Interview prep</strong>: every day ends with real interview questions.</li>
<li><strong>Anyone curious</strong> how the apps on their phone keep their numbers right.</li>
</ul>

<div class="dd-about">
<p><strong>Made by Preetam</strong>, a senior data engineer in Mumbai with 5+ years of building data pipelines for large financial companies. Follow along on <a href="https://instagram.com/datadukaan">Instagram</a> and <a href="https://youtube.com/@datadukaan">YouTube</a>. All code is on <a href="https://github.com/datadukaan/datadukaan.github.io">GitHub</a>.</p>
<p class="dd-small">Examples are generic teaching material and don't reflect any employer's systems.</p>
</div>
'''
(ROOT / "docs/index.md").write_text(index)

# ---------------- nav ----------------
nav = ["nav:", "  - Home: index.md"]
for m, name in enumerate(MODS):
    eps = [x for x in EPS if module_of(x["day"]) == m]
    if not eps: continue
    nav.append(f'  - "{name}":')
    for ep in eps:
        nav.append(f'    - "Day {ep["day"]}: {ep["topic"]}": days/{ep["slug"]}.md')
y = (ROOT / "mkdocs.yml").read_text()
y = re.sub(r"(?ms)^nav:\n.*?(?=^extra:)", "\n".join(nav) + "\n", y)
y = re.sub(r"(?m)^  latest: .*$", f'  latest: {{day: {latest["day"]}, topic: {json.dumps(latest["topic"])}, url: "{url(latest)}"}}', y)
(ROOT / "mkdocs.yml").write_text(y)

# ---------------- day front matter ----------------
for ep in EPS:
    p = ROOT / "docs/days" / f"{ep['slug']}.md"
    t = p.read_text()
    fm = f"---\nday: {ep['day']}\nmodule: {json.dumps(MODS[module_of(ep['day'])])}\ntopic: {json.dumps(ep['topic'], ensure_ascii=False)}\n---\n"
    if t.startswith("---\nday:"):
        t = re.sub(r"(?s)\A---\n.*?\n---\n", fm, t, count=1)
    else:
        t = fm + t
    p.write_text(t)
print(f"home + nav + front matter for {N} days; next: Day {NXT['day']}")
