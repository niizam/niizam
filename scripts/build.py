"""Generates the animated SVGs used by the profile README.

Run: python scripts/build.py
Star counts are fetched from the GitHub API (falls back to the values below).
"""
import base64
import json
import os
import urllib.request
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
USER = "niizam"

BG = "#0d0b0e"
PANEL = "#141116"
CRIMSON = "#e0315b"
WINE = "#8b1a3a"
TEXT = "#e9e4ea"
MUTED = "#8d8492"
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "Consolas, 'SF Mono', Menlo, 'DejaVu Sans Mono', monospace"

PROJECTS = [
    ("vantage", "Shell", 510, "Lenovo Vantage for Linux."),
    ("Genymotion_A11_libhoudini", "Android", 427, "ARM, ARMv7 and ARM64 translation for Genymotion on Android 11."),
    ("klein", "C++", 0, "Fast CUDA inference for Qwen3.8-27B on a 12 GB GPU, with 262K context and MTP speculative decoding."),
    ("obs-spine-player", "JavaScript", 1, "OBS plugin that plays Spine characters with audio-driven yap mode, emotions and hotkeys."),
    ("humtosong", "Go", 0, "Unofficial Google song recognition API in Go. Audio in, song out."),
    ("openvpn-ksplit", "C++", 0, "Per-app split tunnelling for OpenVPN on Windows 11 using a WFP kernel driver."),
]
LANG_COLORS = {
    "Shell": "#89e051", "Android": "#3ddc84", "C++": "#f34b7d",
    "JavaScript": "#f1e05a", "Go": "#00add8", "Rust": "#dea584",
}


def fetch_stars(repo, default):
    req = urllib.request.Request(f"https://api.github.com/repos/{USER}/{repo}")
    if token := os.environ.get("GITHUB_TOKEN"):
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.load(r)["stargazers_count"]
    except Exception:
        return default


def typed(x, y, text, start, step, size, fill, family, cursor=False, weight="400"):
    """One <text> per prefix, each shown for one step (SMIL, no JS needed)."""
    out = []
    n = len(text)
    for i in range(1, n + 1):
        t0 = start + (i - 1) * step
        hide = "" if i == n else f'<set attributeName="visibility" to="hidden" begin="{t0 + step:.2f}s" fill="freeze"/>'
        label = escape(text[:i])
        if i == n and cursor:
            label += f'<tspan fill="{CRIMSON}">▌<animate attributeName="opacity" values="1;1;0;0" dur="1s" begin="{t0:.2f}s" repeatCount="indefinite"/></tspan>'
        out.append(
            f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{fill}" visibility="hidden" xml:space="preserve">{label}'
            f'<set attributeName="visibility" to="visible" begin="{t0:.2f}s" fill="freeze"/>{hide}</text>'
        )
    return "\n".join(out), start + n * step


def header():
    art = base64.b64encode((ASSETS / "hero.webp").read_bytes()).decode()
    tagline, _ = typed(64, 248, "> I made useless things.", 1.4, 0.06, 22, MUTED, MONO, cursor=True)
    w, h = 1200, 400
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
  <radialGradient id="glow" cx="72%" cy="45%" r="55%">
    <stop offset="0" stop-color="{CRIMSON}" stop-opacity=".45"/>
    <stop offset=".55" stop-color="{WINE}" stop-opacity=".12"/>
    <stop offset="1" stop-color="{BG}" stop-opacity="0"/>
  </radialGradient>
  <linearGradient id="name" x1="0" x2="1">
    <stop offset="0" stop-color="#fff"/>
    <stop offset=".5" stop-color="#ffd4de"/>
    <stop offset="1" stop-color="{CRIMSON}"/>
  </linearGradient>
  <linearGradient id="scan" x1="0" x2="0" y1="0" y2="1">
    <stop offset="0" stop-color="{CRIMSON}" stop-opacity="0"/>
    <stop offset="1" stop-color="{CRIMSON}" stop-opacity=".18"/>
  </linearGradient>
  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
    <path d="M40 0H0V40" fill="none" stroke="#fff" stroke-opacity=".04"/>
  </pattern>
  <pattern id="lines" width="4" height="4" patternUnits="userSpaceOnUse">
    <rect width="4" height="1" fill="#000" opacity=".35"/>
  </pattern>
  <clipPath id="frame"><rect width="{w}" height="{h}" rx="18"/></clipPath>
  <clipPath id="g1"><rect x="0" y="120" width="{w}" height="14"><animate attributeName="y" values="120;150;104;170;132" dur="3s" repeatCount="indefinite" calcMode="discrete"/></rect></clipPath>
  <clipPath id="g2"><rect x="0" y="160" width="{w}" height="10"><animate attributeName="y" values="160;118;176;140;110" dur="2.3s" repeatCount="indefinite" calcMode="discrete"/></rect></clipPath>
</defs>
<style>
  .float {{ animation: float 6s ease-in-out infinite; }}
  .enter {{ animation: enter 1.1s cubic-bezier(.2,.8,.2,1) both; }}
  .pulse {{ animation: pulse 5s ease-in-out infinite; transform-origin: 860px 180px; }}
  .glitch {{ animation: glitch 4s steps(1) infinite; }}
  .rise {{ animation: rise .9s .3s cubic-bezier(.2,.8,.2,1) both; }}
  .chips {{ animation: rise .9s 3.2s cubic-bezier(.2,.8,.2,1) both; }}
  @keyframes float {{ 0%,100% {{ transform: translateY(0) }} 50% {{ transform: translateY(-10px) }} }}
  @keyframes enter {{ from {{ transform: translateX(80px); opacity: 0 }} to {{ transform: none; opacity: 1 }} }}
  @keyframes pulse {{ 0%,100% {{ opacity: .75; transform: scale(1) }} 50% {{ opacity: 1; transform: scale(1.06) }} }}
  @keyframes glitch {{ 0%,86%,100% {{ opacity: 0 }} 87%,89%,93% {{ opacity: 1 }} 88%,92% {{ opacity: 0 }} }}
  @keyframes rise {{ from {{ transform: translateY(16px); opacity: 0 }} to {{ transform: none; opacity: 1 }} }}
  @media (prefers-reduced-motion: reduce) {{ * {{ animation: none !important }} }}
</style>
<g clip-path="url(#frame)">
  <rect width="{w}" height="{h}" fill="{BG}"/>
  <rect width="{w}" height="{h}" fill="url(#grid)"/>
  <rect class="pulse" width="{w}" height="{h}" fill="url(#glow)"/>
  <!-- rotating ring behind the character -->
  <g transform="translate(860 190)">
    <circle r="165" fill="none" stroke="{CRIMSON}" stroke-opacity=".35" stroke-width="1.5" stroke-dasharray="4 10">
      <animateTransform attributeName="transform" type="rotate" from="0" to="360" dur="40s" repeatCount="indefinite"/>
    </circle>
    <circle r="205" fill="none" stroke="{CRIMSON}" stroke-opacity=".18" stroke-width="1" stroke-dasharray="120 40 8 40">
      <animateTransform attributeName="transform" type="rotate" from="360" to="0" dur="60s" repeatCount="indefinite"/>
    </circle>
  </g>
  <!-- character -->
  <g class="enter"><g class="float">
    <image href="data:image/webp;base64,{art}" x="500" y="12" width="680" height="400"/>
  </g></g>
  <!-- name + glitch slices -->
  <g class="rise">
    <text x="60" y="130" font-family="{MONO}" font-size="16" fill="{CRIMSON}" letter-spacing="4">// HI THERE, I'M</text>
    <text x="58" y="200" font-family="{SANS}" font-size="78" font-weight="800" fill="url(#name)" letter-spacing="-1">lesserfield</text>
    <g class="glitch">
      <text x="64" y="200" font-family="{SANS}" font-size="78" font-weight="800" fill="#ff2a5f" letter-spacing="-1" clip-path="url(#g1)" opacity=".9">lesserfield</text>
      <text x="52" y="200" font-family="{SANS}" font-size="78" font-weight="800" fill="#2af0ff" letter-spacing="-1" clip-path="url(#g2)" opacity=".7">lesserfield</text>
    </g>
  </g>
  {tagline}
  <g class="chips" font-family="{MONO}" font-size="13" fill="{TEXT}">
    {chips(64, 290, ["linux", "reverse engineering", "cuda", "tooling"])}
  </g>
  <!-- scanline sweep + CRT lines -->
  <rect width="{w}" height="90" fill="url(#scan)">
    <animate attributeName="y" from="-90" to="{h}" dur="5s" repeatCount="indefinite"/>
  </rect>
  <rect width="{w}" height="{h}" fill="url(#lines)"/>
  <!-- bottom accent -->
  <rect y="{h - 3}" width="{w}" height="3" fill="{WINE}"/>
  <rect y="{h - 3}" width="240" height="3" fill="{CRIMSON}">
    <animate attributeName="x" values="-240;{w}" dur="4s" repeatCount="indefinite"/>
  </rect>
</g>
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="18" fill="none" stroke="#fff" stroke-opacity=".08"/>
</svg>'''


def chips(x, y, labels):
    out = []
    for label in labels:
        width = len(label) * 7.6 + 28
        out.append(
            f'<rect x="{x}" y="{y}" width="{width:.0f}" height="30" rx="15" fill="{CRIMSON}" fill-opacity=".1" stroke="{CRIMSON}" stroke-opacity=".5"/>'
            f'<text x="{x + width / 2:.0f}" y="{y + 20}" text-anchor="middle">{escape(label)}</text>'
        )
        x += width + 10
    return "".join(out)


def terminal():
    w, h = 1200, 372
    rows = [
        ("whoami", ["lesserfield. tinkerer, reverser, builder of useless things."]),
        ("cat stack.txt", ["rust · c/c++ · cuda · python · go · javascript · shell"]),
        ("ls ~/projects --pinned", ["vantage/  Genymotion_A11_libhoudini/  klein/  obs-spine-player/  humtosong/"]),
        ("uptime", ["shipping code on github since 2018"]),
    ]
    body, y, t = [], 92, 0.6
    for cmd, outputs in rows:
        body.append(f'<text x="40" y="{y}" font-family="{MONO}" font-size="17" fill="{CRIMSON}" visibility="hidden">~$'
                    f'<set attributeName="visibility" to="visible" begin="{t - 0.2:.2f}s" fill="freeze"/></text>')
        frames, t = typed(72, y, cmd, t, 0.05, 17, TEXT, MONO)
        body.append(frames)
        t += 0.25
        for line in outputs:
            y += 26
            body.append(
                f'<text x="72" y="{y}" font-family="{MONO}" font-size="17" fill="{MUTED}" opacity="0">{escape(line)}'
                f'<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".25s" fill="freeze"/></text>'
            )
            t += 0.15
        y += 34
        t += 0.3
    body.append(f'<text x="40" y="{y}" font-family="{MONO}" font-size="17" fill="{CRIMSON}" opacity="0">~$ <tspan>▌<animate attributeName="opacity" values="1;1;0;0" dur="1s" repeatCount="indefinite"/></tspan>'
                f'<animate attributeName="opacity" to="1" begin="{t:.2f}s" dur=".01s" fill="freeze"/></text>')
    dots = "".join(f'<circle cx="{28 + i * 22}" cy="24" r="6" fill="{c}"/>' for i, c in enumerate(["#ff5f57", "#febc2e", "#28c840"]))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<rect width="{w}" height="{h}" rx="14" fill="{PANEL}"/>
<rect width="{w}" height="48" rx="14" fill="#1b171e"/><rect y="34" width="{w}" height="14" fill="#1b171e"/>
{dots}
<text x="{w / 2}" y="29" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">lesserfield@github: ~</text>
{"".join(body)}
<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="14" fill="none" stroke="#fff" stroke-opacity=".08"/>
</svg>'''


def wrap(text, limit):
    lines, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + 1 > limit and cur:
            lines.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}".strip()
    lines.append(cur)
    return lines[:2]


def card(i, name, lang, stars, desc):
    w, h = 590, 150
    color = LANG_COLORS.get(lang, MUTED)
    title = name if len(name) <= 28 else name[:26] + "…"
    desc_lines = "".join(
        f'<text x="28" y="{80 + n * 22}" font-family="{SANS}" font-size="15" fill="{MUTED}">{escape(line)}</text>'
        for n, line in enumerate(wrap(desc, 66))
    )
    star_text = f'★ {stars}' if stars else ""
    delay = i * 0.6
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}">
<defs>
  <linearGradient id="b" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{w}" y2="0">
    <stop offset="0" stop-color="{CRIMSON}" stop-opacity="0"/>
    <stop offset=".5" stop-color="{CRIMSON}"/>
    <stop offset="1" stop-color="{CRIMSON}" stop-opacity="0"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-{w};{w}" dur="3.5s" begin="{delay}s" repeatCount="indefinite"/>
  </linearGradient>
</defs>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="{PANEL}" stroke="#fff" stroke-opacity=".08"/>
<rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="none" stroke="url(#b)" stroke-width="1.5"/>
<rect x="0" y="22" width="4" height="30" rx="2" fill="{CRIMSON}"/>
<text x="28" y="46" font-family="{SANS}" font-size="21" font-weight="700" fill="{TEXT}">{escape(title)}</text>
{desc_lines}
<circle cx="34" cy="{h - 24}" r="6" fill="{color}"/>
<text x="48" y="{h - 19}" font-family="{SANS}" font-size="14" fill="{MUTED}">{escape(lang)}</text>
<text x="{w - 28}" y="{h - 19}" text-anchor="end" font-family="{SANS}" font-size="14" font-weight="600" fill="{CRIMSON}">{star_text}</text>
</svg>'''


def divider():
    w = 1200
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} 24" width="{w}" height="24">
<defs><linearGradient id="d" x1="0" x2="1"><stop offset="0" stop-color="{CRIMSON}" stop-opacity="0"/><stop offset=".5" stop-color="{CRIMSON}"/><stop offset="1" stop-color="{CRIMSON}" stop-opacity="0"/></linearGradient></defs>
<rect y="11" width="{w}" height="2" fill="{CRIMSON}" opacity=".2"/>
<rect y="11" width="300" height="2" fill="url(#d)"><animate attributeName="x" values="-300;{w}" dur="3s" repeatCount="indefinite"/></rect>
<rect x="{w / 2 - 6}" y="6" width="12" height="12" fill="{BG}" stroke="{CRIMSON}" stroke-width="2" transform="rotate(45 {w / 2} 12)">
  <animate attributeName="stroke-opacity" values="1;.3;1" dur="2s" repeatCount="indefinite"/>
</rect>
</svg>'''


def main():
    (ASSETS / "header.svg").write_text(header(), encoding="utf-8")
    (ASSETS / "terminal.svg").write_text(terminal(), encoding="utf-8")
    (ASSETS / "divider.svg").write_text(divider(), encoding="utf-8")
    (ASSETS / "cards").mkdir(exist_ok=True)
    for i, (name, lang, stars, desc) in enumerate(PROJECTS):
        svg = card(i, name, lang, fetch_stars(name, stars), desc)
        (ASSETS / "cards" / f"{name}.svg").write_text(svg, encoding="utf-8")


if __name__ == "__main__":
    main()
