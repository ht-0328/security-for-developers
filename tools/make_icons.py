# Lucide（線のアイコン）と Simple Icons（ブランドロゴ）から、AWS アイコン風の
# 「分類ごとの色付きチップ + 白い図柄」の 64x64 SVG を生成する。
# 使い方: python -I make_icons.py <lucide/icons> <simple-icons/package> <出力先>
import json, re, sys
from pathlib import Path

lucide_dir, si_dir, out_dir = (Path(a) for a in sys.argv[1:4])

# 分類 → 色（ライトモードの CSS トークンと合わせる）
CATEGORY_COLOR = {
    "threat": "#dd344c",   # 攻撃・脅威（赤）
    "defense": "#2e8540",  # 守り・対策（緑）
    "asset": "#2463c6",    # データ・部品・システム（青）
    "people": "#7a3fe0",   # 人・権限・組織（紫）
    "ops": "#e07a00",      # 運用・プロセス・学び（橙）
}

# 分類ごとに使うアイコン。"a|b" は a が無ければ b を使う（版によって名前が違うため）
ICONS = {
    "threat": """bug skull bomb syringe fish triangle-alert|alert-triangle octagon-alert|alert-octagon shield-off shield-alert
                 zap crosshair lock-open|unlock eye door-open mail-warning user-x file-warning wifi-off flame footprints
                 venetian-mask swords ban circle-x|x-circle message-square-warning|message-square-x unplug
                 key-square hand-coins biohazard radiation cloud-off server-off database-zap""",
    "defense": """shield shield-check lock lock-keyhole key key-round fingerprint scan scan-face filter
                  circle-check|check-circle badge-check eye-off file-lock shield-ellipsis siren radar shield-half
                  square-check|check-square list-checks scan-search scan-line brick-wall|fence door-closed umbrella
                  life-buoy construction shield-plus scan-eye|scan-face vault|safe server-cog funnel|filter
                  lock-keyhole-open|unlock-keyhole shield-user|shield square-asterisk|asterisk
                  square-check-big|check-square-2 circle-check-big|check-circle-2 file-check-2|file-check""",
    "asset": """database server hard-drive package package-check package-search boxes box file-code code terminal
                globe cloud cookie file-text folder-lock folder cpu container git-branch git-pull-request
                git-commit-horizontal|git-commit layers network router wifi monitor smartphone laptop app-window
                braces binary file-json link mail message-square image upload download hash cable plug
                hard-drive-download archive table-2|table key-square|key form-input|text-cursor-input
                square-code|code-2 file-code-2|file-code text-cursor-input|text-cursor arrow-left-right|arrow-right-left
                send server-crash|server-off file-digit|file-text""",
    "people": """user users user-check user-cog id-card|contact badge building building-2 briefcase user-round
                 user-plus user-minus contact handshake crown graduation-cap person-standing glasses store
                 landmark scale gavel user-round-check|user-check users-round|users shield-user|user-check
                 user-lock|user-cog user-pen|user-cog baby smile frown""",
    "ops": """clipboard-list clipboard-check bell bell-ring activity search history refresh-cw rotate-ccw calendar
              calendar-clock book-open timer workflow flag archive-restore chart-bar|bar-chart chart-line|line-chart
              settings wrench hammer flask-conical test-tube puzzle route map compass lightbulb megaphone
              phone-call notebook-pen pen-line scroll-text file-check file-search stethoscope heart-pulse
              trending-up gauge repeat rocket bot brain sparkles newspaper alarm-clock circle-help|help-circle
              info book-marked library bookmark eye target list-todo|list-checks square-pen|edit shield-question|circle-help
              git-compare-arrows|git-compare clock message-circle-question|message-circle phone life-buoy
              file-clock bug-play|bug bug-off search-check|search""",
}

# ブランドロゴ（Simple Icons のスラッグ）
BRANDS = """github githubactions npm pypi python nodedotjs docker kubernetes owasp letsencrypt dependabot renovate
            snyk trivy cloudflare googlecloud auth0 okta keycloak firebase gnubash git gitlab bitbucket
            openjdk kotlin typescript javascript postgresql mysql sqlite redis nginx linux android apple
            googlechrome curl openssl vault terraform jenkins 1password bitwarden yubico burpsuite wireshark
            kalilinux discord dotenv"""

def inner_svg(text):
    """<svg ...> と </svg> の間（図柄の本体）だけを取り出す"""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    m = re.search(r"<svg\b[^>]*>(.*)</svg>", text, flags=re.S)
    return m.group(1).strip() if m else None

def pick(lucide_dir, spec):
    for name in spec.split("|"):
        p = lucide_dir / f"{name}.svg"
        if p.exists():
            return name, p
    return None, None

out_dir.mkdir(parents=True, exist_ok=True)
missing = []
made = 0
for cat, names in ICONS.items():
    d = out_dir / cat
    d.mkdir(exist_ok=True)
    color = CATEGORY_COLOR[cat]
    for spec in names.split():
        name, p = pick(lucide_dir, spec)
        if not p:
            missing.append(f"{cat}:{spec}")
            continue
        body = inner_svg(p.read_text(encoding="utf-8"))
        # 24 単位の図柄を 38 単位に拡大し、中央（13,13 から）に置く。線は白
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><title>{name}</title>'
               f'<rect width="64" height="64" fill="{color}"/>'
               f'<g transform="translate(13 13) scale(1.5833)" fill="none" stroke="#fff" stroke-width="2" '
               f'stroke-linecap="round" stroke-linejoin="round">{body}</g></svg>\n')
        # 出力名は先頭の候補名で統一する（版が変わっても本文のパスが変わらないように）
        (d / f"{spec.split('|')[0]}.svg").write_bytes(svg.encode("utf-8"))
        made += 1

# ブランドロゴ：白いチップにブランド色の図柄
data = json.load((si_dir / "data" / "simple-icons.json").open(encoding="utf-8"))
by_slug = {i["slug"]: i for i in data}
bd = out_dir / "brand"
bd.mkdir(exist_ok=True)
for slug in BRANDS.split():
    p = si_dir / "icons" / f"{slug}.svg"
    if not p.exists() or slug not in by_slug:
        missing.append(f"brand:{slug}")
        continue
    body = inner_svg(p.read_text(encoding="utf-8"))
    body = re.sub(r"<title>.*?</title>", "", body, flags=re.S)
    hexc = by_slug[slug]["hex"]
    # 真っ黒・真っ白に近いロゴは、ダークモードでも見えるように濃い灰色にそろえる
    r, g, b = int(hexc[0:2], 16), int(hexc[2:4], 16), int(hexc[4:6], 16)
    if r + g + b < 60: hexc = "24292f"
    if r + g + b > 700: hexc = "6b7280"
    title = by_slug[slug]["title"].replace("&", "&amp;").replace("<", "&lt;")
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><title>{title}</title>'
           f'<rect width="64" height="64" fill="#ffffff"/>'
           f'<g transform="translate(14 14) scale(1.5)" fill="#{hexc}">{body}</g></svg>\n')
    (bd / f"{slug}.svg").write_bytes(svg.encode("utf-8"))
    made += 1

print("made", made)
print("missing", len(missing), missing)
