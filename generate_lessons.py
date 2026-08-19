#!/usr/bin/env python3
"""
Generate Grade 1 Math Theory – Lessons 1 to 100 (Year 2).
Structure mirrors Year 2/Year 3: 7 sections + bonus + answer key, with
deterministic SVG diagrams and cross-lesson diversity (no repeated diagram types).

Run: python3 generate_lessons.py
"""
import os, math, random
from collections import deque

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# ─── Topics (Grade 1 roadmap, Year-2 style blocks) ───────────────────────────
LESSONS = {
    # 1–10 Counting & Numbers to 20
    1:  ("Counting to 10", "Counting Basics | 90-Minute Lesson"),
    2:  ("Counting to 20", "Numbers to 20 | 90-Minute Lesson"),
    3:  ("One More, One Less", "One More / One Less | 90-Minute Lesson"),
    4:  ("Comparing Within 20", "Compare Within 20 | 90-Minute Lesson"),
    5:  ("Ordering Numbers to 20", "Order Numbers | 90-Minute Lesson"),
    6:  ("Number Lines to 20", "Number Lines | 90-Minute Lesson"),
    7:  ("Ten-Frames", "Ten-Frames | 90-Minute Lesson"),
    8:  ("Making 10", "Bonds to 10 | 90-Minute Lesson"),
    9:  ("Counting Mixed Practice", "Counting Practice | 90-Minute Lesson"),
    10: ("Counting Assessment", "Counting Assessment | 90-Minute Lesson"),
    # 11–20 Addition
    11: ("Adding Within 10", "Addition Within 10 | 90-Minute Lesson"),
    12: ("Adding Within 20", "Addition Within 20 | 90-Minute Lesson"),
    13: ("Part–Whole Addition", "Part–Whole | 90-Minute Lesson"),
    14: ("Adding Three Numbers", "Add Three Numbers | 90-Minute Lesson"),
    15: ("Doubles & Near Doubles", "Doubles | 90-Minute Lesson"),
    16: ("Addition Word Problems", "Addition Stories | 90-Minute Lesson"),
    17: ("Missing Addends", "Missing Addends | 90-Minute Lesson"),
    18: ("Adding on a Number Line", "Add on Number Line | 90-Minute Lesson"),
    19: ("Addition Fluency", "Addition Fluency | 90-Minute Lesson"),
    20: ("Addition Review", "Addition Review | 90-Minute Lesson"),
    # 21–30 Subtraction
    21: ("Subtracting Within 10", "Subtraction Within 10 | 90-Minute Lesson"),
    22: ("Subtracting Within 20", "Subtraction Within 20 | 90-Minute Lesson"),
    23: ("Part–Whole Subtraction", "Take Away Models | 90-Minute Lesson"),
    24: ("Related Facts +/−", "Fact Families | 90-Minute Lesson"),
    25: ("Missing Numbers in Subtraction", "Missing Numbers | 90-Minute Lesson"),
    26: ("Subtraction Word Problems", "Subtraction Stories | 90-Minute Lesson"),
    27: ("Comparing Differences", "Compare Differences | 90-Minute Lesson"),
    28: ("Subtract on a Number Line", "Subtract on Number Line | 90-Minute Lesson"),
    29: ("Subtraction Fluency", "Subtraction Fluency | 90-Minute Lesson"),
    30: ("Subtraction Review", "Subtraction Review | 90-Minute Lesson"),
    # 31–40 Place Value & Numbers to 100
    31: ("Tens and Ones", "Tens & Ones | 90-Minute Lesson"),
    32: ("Numbers to 50", "Numbers to 50 | 90-Minute Lesson"),
    33: ("Numbers to 100", "Numbers to 100 | 90-Minute Lesson"),
    34: ("Expanded Form", "Expanded Form | 90-Minute Lesson"),
    35: ("Digit Values", "Digit Values | 90-Minute Lesson"),
    36: ("Comparing 2-Digit Numbers", "Compare 2-Digit | 90-Minute Lesson"),
    37: ("Ordering to 100", "Order to 100 | 90-Minute Lesson"),
    38: ("10 More, 10 Less", "10 More / 10 Less | 90-Minute Lesson"),
    39: ("Place Value Practice", "Place Value Practice | 90-Minute Lesson"),
    40: ("Place Value Assessment", "Place Value Assessment | 90-Minute Lesson"),
    # 41–50 Mixed +/− within 100
    41: ("Adding Tens", "Adding Tens | 90-Minute Lesson"),
    42: ("Adding 2-Digit + 1-Digit", "2-Digit + 1-Digit | 90-Minute Lesson"),
    43: ("Subtracting Tens", "Subtracting Tens | 90-Minute Lesson"),
    44: ("Subtracting 2-Digit − 1-Digit", "2-Digit − 1-Digit | 90-Minute Lesson"),
    45: ("Mixed +/− Within 50", "Mixed Within 50 | 90-Minute Lesson"),
    46: ("Mixed +/− Within 100", "Mixed Within 100 | 90-Minute Lesson"),
    47: ("Two-Step Stories", "Two-Step Stories | 90-Minute Lesson"),
    48: ("Money: Coins Intro", "Coins | 90-Minute Lesson"),
    49: ("Operations Practice", "Operations Practice | 90-Minute Lesson"),
    50: ("Operations Assessment", "Operations Assessment | 90-Minute Lesson"),
    # 51–60 Measurement & Time
    51: ("Comparing Length", "Compare Length | 90-Minute Lesson"),
    52: ("Measuring in cm", "Length in cm | 90-Minute Lesson"),
    53: ("Telling Time: Hours", "Time to the Hour | 90-Minute Lesson"),
    54: ("Telling Time: Half Hours", "Time to Half Hour | 90-Minute Lesson"),
    55: ("Calendar Days", "Calendar | 90-Minute Lesson"),
    56: ("Mass: Heavier / Lighter", "Mass Compare | 90-Minute Lesson"),
    57: ("Capacity: More / Less", "Capacity Compare | 90-Minute Lesson"),
    58: ("Temperature Read", "Thermometer | 90-Minute Lesson"),
    59: ("Measurement Practice", "Measurement Practice | 90-Minute Lesson"),
    60: ("Measurement Assessment", "Measurement Assessment | 90-Minute Lesson"),
    # 61–70 Geometry
    61: ("2D Shapes", "2D Shapes | 90-Minute Lesson"),
    62: ("Sides & Corners", "Sides & Corners | 90-Minute Lesson"),
    63: ("Sorting Shapes", "Sort Shapes | 90-Minute Lesson"),
    64: ("Symmetry Intro", "Symmetry | 90-Minute Lesson"),
    65: ("Composing Shapes", "Compose Shapes | 90-Minute Lesson"),
    66: ("3D Shapes Intro", "3D Shapes | 90-Minute Lesson"),
    67: ("Shape Patterns", "Shape Patterns | 90-Minute Lesson"),
    68: ("Positions & Directions", "Positions | 90-Minute Lesson"),
    69: ("Geometry Practice", "Geometry Practice | 90-Minute Lesson"),
    70: ("Geometry Review", "Geometry Review | 90-Minute Lesson"),
    # 71–80 Skip Counting & Equal Groups
    71: ("Skip Count by 2s", "Count by 2s | 90-Minute Lesson"),
    72: ("Skip Count by 5s", "Count by 5s | 90-Minute Lesson"),
    73: ("Skip Count by 10s", "Count by 10s | 90-Minute Lesson"),
    74: ("Equal Groups", "Equal Groups | 90-Minute Lesson"),
    75: ("Arrays Intro", "Arrays | 90-Minute Lesson"),
    76: ("Repeated Addition", "Repeated Addition | 90-Minute Lesson"),
    77: ("Sharing Equally", "Sharing | 90-Minute Lesson"),
    78: ("Skip Count 2, 5, 10", "Skip Count 2, 5, 10 | 90-Minute Lesson"),
    79: ("Equal Groups Practice", "Equal Groups Practice | 90-Minute Lesson"),
    80: ("Skip Count & Groups Review", "Groups Review | 90-Minute Lesson"),
    # 81–90 Patterns & Data
    81: ("Number Patterns", "Number Patterns | 90-Minute Lesson"),
    82: ("Colour & Shape Patterns", "Visual Patterns | 90-Minute Lesson"),
    83: ("Tally Charts", "Tally Charts | 90-Minute Lesson"),
    84: ("Pictographs", "Pictographs | 90-Minute Lesson"),
    85: ("Bar Graphs", "Bar Graphs | 90-Minute Lesson"),
    86: ("Reading Simple Tables", "Tables | 90-Minute Lesson"),
    87: ("Data Word Problems", "Data Stories | 90-Minute Lesson"),
    88: ("Growing Patterns", "Growing Patterns | 90-Minute Lesson"),
    89: ("Patterns & Data Practice", "Patterns Practice | 90-Minute Lesson"),
    90: ("Patterns & Data Review", "Data Review | 90-Minute Lesson"),
    # 91–100 Fractions & Spiral
    91: ("Halves", "Halves | 90-Minute Lesson"),
    92: ("Quarters", "Quarters | 90-Minute Lesson"),
    93: ("Halves & Quarters", "Halves & Quarters | 90-Minute Lesson"),
    94: ("Spiral: Numbers & Place Value", "Spiral: Numbers | 90-Minute Lesson"),
    95: ("Spiral: Add & Subtract", "Spiral: + − | 90-Minute Lesson"),
    96: ("Spiral: Shapes & Measure", "Spiral: Shapes & Measure | 90-Minute Lesson"),
    97: ("Spiral: Equal Groups & Patterns", "Spiral: Groups & Patterns | 90-Minute Lesson"),
    98: ("Test-Style Practice A", "Practice Test A | 90-Minute Lesson"),
    99: ("Test-Style Practice B", "Practice Test B | 90-Minute Lesson"),
    100:("End-of-Year Challenge", "End-of-Year Challenge | 90-Minute Lesson"),
}

# ─── CSS (Year-3 aligned) ────────────────────────────────────────────────────
CSS = """
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      max-width: 880px; margin: 0 auto;
      padding: 32px 24px; color: #1a1a2e;
      font-size: 15px; line-height: 1.75;
    }
    h1 { text-align:center; font-size:1.55em; color:#14532d; margin-bottom:4px; }
    .meta { text-align:center; color:#555; margin-bottom:28px; font-size:.97em; }
    .section-header {
      background:#e8f5e9; border-left:5px solid #14532d;
      padding:7px 14px; margin:28px 0 14px 0;
      font-weight:bold; font-size:1.05em; color:#14532d;
      border-radius:0 6px 6px 0;
    }
    .bonus {
      background:#fff8e1; border-left:5px solid #f9a825;
      padding:7px 14px; margin:28px 0 14px 0;
      font-weight:bold; font-size:1.05em; color:#7a5c00;
      border-radius:0 6px 6px 0;
    }
    .answer-header {
      background:#e6f4ea; border-left:5px solid #2e7d32;
      padding:7px 14px; margin:28px 0 14px 0;
      font-weight:bold; font-size:1.05em; color:#2e7d32;
      border-radius:0 6px 6px 0;
    }
    .question { margin:10px 0 10px 18px; }
    .blank {
      display:inline-block; min-width:54px;
      border-bottom:2px solid #333; margin:0 5px; vertical-align:bottom;
    }
    .wide-blank {
      display:inline-block; min-width:160px;
      border-bottom:2px solid #333; margin:0 5px; vertical-align:bottom;
    }
    .mc-options { display:flex; gap:18px; flex-wrap:wrap; margin:5px 0 3px 0; }
    .mc-opt { padding:3px 14px; border:1.5px solid #a5d6a7; border-radius:4px; background:#f1f8f2; }
    .tf-row { display:inline-flex; gap:18px; margin-left:10px; }
    .tf-opt { padding:2px 12px; border:1.5px solid #a5d6a7; border-radius:4px; background:#f1f8f2; }
    .match-instructions { margin:2px 0 8px 18px; color:#555; font-size:.93em; }
    .matching { display:flex; gap:50px; margin:8px 0 10px 18px; flex-wrap:wrap; }
    .match-col { display:flex; flex-direction:column; gap:8px; }
    .match-item {
      padding:5px 14px; border:1.5px solid #a5d6a7; border-radius:6px;
      background:#f1f8f2; min-width:110px; text-align:center;
    }
    .match-blank {
      display:inline-block; min-width:26px;
      border-bottom:2px solid #333; margin-right:6px; vertical-align:bottom;
    }
    table.answer-key {
      border-collapse:collapse; width:100%;
      margin-top:12px; font-size:.93em;
    }
    table.answer-key th {
      background:#14532d; color:#fff;
      padding:7px 12px; text-align:center;
    }
    table.answer-key td {
      border:1px solid #a5d6a7; padding:6px 12px; text-align:center;
    }
    table.answer-key tr:nth-child(even) td { background:#f0faf2; }
    hr { border:none; border-top:1px solid #c8e6c9; margin:32px 0; }
    .name-line { display:flex; gap:32px; margin-bottom:20px; font-size:.97em; }
    .name-line span { white-space:nowrap; }
    .name-line .line { flex:1; border-bottom:1.5px solid #333; min-width:100px; }
    ol.q-list { padding-left:22px; margin:0; }
    ol.q-list li { margin:10px 0; }
    .answer-section { break-before:page; page-break-before:always; }
    .diagram-wrap { margin: 14px 0 4px 18px; }
    .diagram-caption { font-size:.87em; color:#666; font-style:italic; margin: 2px 0 10px 18px; }
    @media print { hr.before-answer { display:none; } }
"""

PALETTES = [
    ("#e8f5e9", "#14532d"),
    ("#e3f2fd", "#0d47a1"),
    ("#fff3e0", "#e65100"),
    ("#fce4ec", "#880e4f"),
    ("#f3e5f5", "#4a148c"),
    ("#fffde7", "#f57f17"),
]
NAMES = ["Hoa", "Linh", "Nam", "Tuan", "Bao", "Mai", "Lan", "Minh", "Thu", "Phong"]
THINGS = ["pencils", "stickers", "toys", "books", "candies", "marbles", "coins", "apples", "cards", "flowers"]

# Cross-lesson diversity trackers (avoid repeating diagram kinds)
_RECENT_DIAGRAMS = deque(maxlen=4)
_RECENT_MEASURE = deque(maxlen=2)
_RECENT_GEO = deque(maxlen=2)
_RECENT_FRAC = deque(maxlen=2)
_RECENT_DATA = deque(maxlen=2)

def _pick_avoid(rng, options, recent):
    """Prefer options not in recent history; fall back to any."""
    opts = list(options)
    fresh = [o for o in opts if o not in recent]
    choice = rng.choice(fresh if fresh else opts)
    return choice

def lesson_rng(n):
    return random.Random(n * 7919 + 31337)

def tier(n):
    if n <= 33: return 1
    if n <= 66: return 2
    return 3

def max_num(n):
    """Grade 1 ceilings: to 20 early, then 50, then 100."""
    if n <= 20: return 20
    if n <= 40: return 50
    if n <= 70: return 100
    return 100

def mul_max(n):
    """Early equal-groups factors only."""
    if n <= 75: return 5
    if n <= 90: return 5
    return 10

def _pal(rng):
    return rng.choice(PALETTES)

def diagram(svg, caption):
    return (f'<div class="diagram-wrap">{svg}</div>'
            f'<div class="diagram-caption">{caption}</div>')

# ─── SVG helpers (deterministic, Year-3 style) ───────────────────────────────
def svg_clock(hour, minute=0, size=130):
    cx = cy = size / 2
    r = cx - 5
    def pt(deg, rad):
        a = math.radians(deg - 90)
        return cx + rad * math.cos(a), cy + rad * math.sin(a)
    ticks = []
    for i in range(60):
        ox, oy = pt(i * 6, r - 2)
        ix, iy = pt(i * 6, r - (12 if i % 5 == 0 else 7))
        ticks.append(f'<line x1="{ox:.1f}" y1="{oy:.1f}" x2="{ix:.1f}" y2="{iy:.1f}" '
                     f'stroke="#333" stroke-width="{"2.5" if i%5==0 else "1"}"/>')
    nums = []
    for n in range(1, 13):
        tx, ty = pt(n * 30, r - 18)
        nums.append(f'<text x="{tx:.1f}" y="{ty:.1f}" text-anchor="middle" '
                    f'dominant-baseline="central" font-size="11" font-weight="bold" fill="#333">{n}</text>')
    mx, my = pt(minute * 6, r - 18)
    hx, hy = pt((hour % 12 + minute / 60) * 30, r - 30)
    svg = (f'<svg width="{size}" height="{size}" viewBox="0 0 {size} {size}" '
           f'font-family="\'Segoe UI\',Arial,sans-serif">'
           f'<circle cx="{cx}" cy="{cy}" r="{r:.1f}" fill="white" stroke="#333" stroke-width="2.5"/>'
           f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="#333"/>'
           + "".join(ticks) + "".join(nums) +
           f'<line x1="{cx}" y1="{cy}" x2="{mx:.1f}" y2="{my:.1f}" stroke="#555" stroke-width="2.5" stroke-linecap="round"/>'
           f'<line x1="{cx}" y1="{cy}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="#333" stroke-width="4" stroke-linecap="round"/>'
           f'</svg>')
    return svg, f"{hour}:{minute:02d}"

def svg_number_line(lo, hi, mark, width=420):
    pad = 24
    span = hi - lo
    def x(v):
        return pad + (v - lo) / span * (width - 2 * pad)
    ticks = []
    step = max(1, span // 10)
    for v in range(lo, hi + 1, step):
        xx = x(v)
        ticks.append(f'<line x1="{xx:.0f}" y1="18" x2="{xx:.0f}" y2="32" stroke="#333" stroke-width="2"/>')
        ticks.append(f'<text x="{xx:.0f}" y="48" text-anchor="middle" font-size="11" fill="#333">{v}</text>')
    mx = x(mark)
    return (f'<svg width="{width}" height="58" viewBox="0 0 {width} 58" '
            f'font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<line x1="{pad}" y1="25" x2="{width-pad}" y2="25" stroke="#333" stroke-width="2"/>'
            + "".join(ticks) +
            f'<circle cx="{mx:.0f}" cy="25" r="6" fill="#c0392b"/>'
            f'</svg>')

def svg_place_value(num):
    h, t, o = num // 100, (num % 100) // 10, num % 10
    leaves = []
    if num >= 100:
        parts = [("Hundreds", h, h * 100), ("Tens", t, t * 10), ("Ones", o, o)]
        xs = [40, 200, 360]
        W = 480
    else:
        parts = [("Tens", t if num >= 10 else 0, (t if num >= 10 else 0) * 10), ("Ones", o, o)]
        if num < 10:
            parts = [("Ones", o, o)]
            xs = [180]
            W = 360
        else:
            xs = [80, 280]
            W = 440
    leaf_svg = ""
    for (label, d, val), x in zip(parts, xs):
        leaf_svg += (f'<rect x="{x}" y="78" width="120" height="40" rx="6" fill="#e8f5e9" stroke="#14532d"/>'
                     f'<text x="{x+60}" y="96" text-anchor="middle" font-size="12" font-weight="bold" fill="#14532d">{d} {label}</text>'
                     f'<text x="{x+60}" y="111" text-anchor="middle" font-size="11" fill="#555">= {val}</text>'
                     f'<line x1="{W//2}" y1="44" x2="{x+60}" y2="78" stroke="#14532d" stroke-width="1.8"/>')
    return (f'<svg width="{W}" height="130" viewBox="0 0 {W} 130" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<rect x="{(W-160)//2}" y="6" width="160" height="38" rx="7" fill="#14532d"/>'
            f'<text x="{W//2}" y="30" text-anchor="middle" font-size="16" font-weight="bold" fill="#fff">{num}</text>'
            + leaf_svg + '</svg>')

def svg_ten_frame(filled, total=10):
    fill, stroke = "#e8f5e9", "#14532d"
    cells = ""
    for i in range(total):
        r, c = divmod(i, 5)
        x, y = 8 + c * 36, 8 + r * 36
        cells += f'<rect x="{x}" y="{y}" width="32" height="32" fill="white" stroke="{stroke}" stroke-width="2"/>'
        if i < filled:
            cells += f'<circle cx="{x+16}" cy="{y+16}" r="10" fill="{stroke}"/>'
    return (f'<svg width="190" height="84" viewBox="0 0 190 84" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'{cells}</svg>')

def svg_array(rows, cols, rng):
    fill, stroke = _pal(rng)
    cs = 22
    cells = ""
    for r in range(rows):
        for c in range(cols):
            cells += (f'<rect x="{6+c*cs}" y="{6+r*cs}" width="{cs-4}" height="{cs-4}" rx="3" '
                      f'fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
    W, H = cols * cs + 8, rows * cs + 8
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'{cells}</svg>')

def svg_equal_groups(groups, per, rng):
    fill, stroke = _pal(rng)
    boxes = ""
    for g in range(groups):
        x0 = 8 + g * 70
        dots = "".join(
            f'<circle cx="{x0+18+(i%3)*16}" cy="{28+(i//3)*16}" r="6" fill="{stroke}"/>'
            for i in range(per)
        )
        boxes += (f'<rect x="{x0}" y="8" width="62" height="{20+((per-1)//3+1)*16}" rx="6" '
                  f'fill="{fill}" stroke="{stroke}" stroke-width="2"/>{dots}')
    W = groups * 70 + 10
    H = 28 + ((per - 1) // 3 + 1) * 16
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'{boxes}</svg>')

def svg_part_whole(whole, part_a, part_b, rng, hide="b"):
    fill, stroke = _pal(rng)
    a_lbl = str(part_a) if hide != "a" else "?"
    b_lbl = str(part_b) if hide != "b" else "?"
    w_lbl = str(whole) if hide != "w" else "?"
    return (f'<svg width="280" height="110" viewBox="0 0 280 110" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<rect x="60" y="8" width="160" height="40" rx="6" fill="#14532d"/>'
            f'<text x="140" y="34" text-anchor="middle" fill="#fff" font-size="16" font-weight="bold">{w_lbl}</text>'
            f'<rect x="20" y="62" width="110" height="38" rx="6" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<text x="75" y="87" text-anchor="middle" fill="{stroke}" font-size="15" font-weight="bold">{a_lbl}</text>'
            f'<rect x="150" y="62" width="110" height="38" rx="6" fill="#fff8e1" stroke="#f9a825" stroke-width="2"/>'
            f'<text x="205" y="87" text-anchor="middle" fill="#7a5c00" font-size="15" font-weight="bold">{b_lbl}</text>'
            f'</svg>')

def svg_rect(w_u, h_u, rng):
    fill, stroke = _pal(rng)
    s = 12
    W, H = w_u * s + 24, h_u * s + 28
    return (f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<rect x="12" y="8" width="{w_u*s}" height="{h_u*s}" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<text x="{12+w_u*s//2}" y="{H-4}" text-anchor="middle" font-size="11" fill="{stroke}">{w_u} cm</text>'
            f'<text x="8" y="{8+h_u*s//2}" text-anchor="middle" font-size="11" fill="{stroke}" '
            f'transform="rotate(-90,8,{8+h_u*s//2})">{h_u} cm</text></svg>')

def svg_grid_area(cols, rows, shaded, rng):
    fill, stroke = _pal(rng)
    cs = 22
    cells = ""
    for r in range(rows):
        for c in range(cols):
            idx = r * cols + c
            col = stroke if idx in shaded else fill
            cells += (f'<rect x="{2+c*cs}" y="{2+r*cs}" width="{cs-2}" height="{cs-2}" '
                      f'fill="{col}" stroke="{stroke}" stroke-width="1"/>')
    return f'<svg width="{cols*cs+4}" height="{rows*cs+4}" viewBox="0 0 {cols*cs+4} {rows*cs+4}">{cells}</svg>'

def svg_frac_bar(numer, denom, rng):
    fill, stroke = _pal(rng)
    W, H = 200, 32
    seg = W // denom
    rects = "".join(
        f'<rect x="{i*seg}" y="0" width="{seg}" height="{H}" '
        f'fill="{stroke if i < numer else fill}" stroke="white" stroke-width="1"/>'
        for i in range(denom)
    )
    return f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">{rects}</svg>'

def svg_frac_pie(numer, denom, rng):
    fill, stroke = _pal(rng)
    cx, cy, r = 50, 50, 40
    slices = ""
    for i in range(denom):
        a1 = math.radians(i * 360 / denom - 90)
        a2 = math.radians((i + 1) * 360 / denom - 90)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        col = stroke if i < numer else fill
        large = 1 if 360 / denom > 180 else 0
        slices += (f'<path d="M{cx},{cy} L{x1:.1f},{y1:.1f} A{r},{r} 0 {large},1 {x2:.1f},{y2:.1f} Z" '
                   f'fill="{col}" stroke="white" stroke-width="1"/>')
    return f'<svg width="100" height="100" viewBox="0 0 100 100">{slices}</svg>'

def svg_frac_numberline(numer, denom):
    W = 280
    ticks = ""
    for i in range(denom + 1):
        x = 20 + i * (W - 40) / denom
        ticks += f'<line x1="{x:.0f}" y1="22" x2="{x:.0f}" y2="34" stroke="#333" stroke-width="1.5"/>'
        ticks += f'<text x="{x:.0f}" y="50" text-anchor="middle" font-size="10" fill="#333">{i}/{denom}</text>'
    tx = 20 + numer * (W - 40) / denom
    return (f'<svg width="{W}" height="58" viewBox="0 0 {W} 58" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<line x1="16" y1="28" x2="{W-16}" y2="28" stroke="#333" stroke-width="2"/>'
            f'{ticks}<circle cx="{tx:.0f}" cy="28" r="6" fill="#c0392b"/></svg>')

SHAPE_META = {
    "Circle": (0, 0), "Square": (4, 4), "Triangle": (3, 0),
    "Rectangle": (4, 2), "Pentagon": (5, 5), "Hexagon": (6, 6), "Diamond": (4, 2),
}

def svg_shape(name, rng, symmetry=False):
    fill, stroke = _pal(rng)
    bodies = {
        "Circle": f'<circle cx="40" cy="40" r="32" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
        "Square": f'<rect x="10" y="10" width="60" height="60" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
        "Triangle": f'<polygon points="40,6 74,72 6,72" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
        "Rectangle": f'<rect x="6" y="14" width="98" height="48" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
        "Pentagon": f'<polygon points="40,5 75,28 62,70 18,70 5,28" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
        "Hexagon": f'<polygon points="40,4 72,22 72,58 40,76 8,58 8,22" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
        "Diamond": f'<polygon points="40,4 76,40 40,76 4,40" fill="{fill}" stroke="{stroke}" stroke-width="3"/>',
    }
    overlay = ""
    if symmetry and name == "Square":
        overlay = (f'<line x1="10" y1="40" x2="70" y2="40" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="4,3"/>'
                   f'<line x1="40" y1="10" x2="40" y2="70" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="4,3"/>')
    elif symmetry and name == "Rectangle":
        overlay = (f'<line x1="6" y1="38" x2="104" y2="38" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="4,3"/>'
                   f'<line x1="55" y1="14" x2="55" y2="62" stroke="#c0392b" stroke-width="1.5" stroke-dasharray="4,3"/>')
    w, h = ("110", "70") if name == "Rectangle" else ("80", "80")
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{bodies[name]}{overlay}</svg>'

def svg_angle(kind, rng):
    fill, stroke = _pal(rng)
    deg = {"right": 90, "acute": 45, "obtuse": 125}[kind]
    rad = math.radians(deg)
    x2 = 80 + 50 * math.cos(math.pi - rad)
    y2 = 80 - 50 * math.sin(math.pi - rad)
    return (f'<svg width="110" height="95" viewBox="0 0 110 95" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<line x1="20" y1="80" x2="80" y2="80" stroke="{stroke}" stroke-width="3"/>'
            f'<line x1="80" y1="80" x2="{x2:.0f}" y2="{y2:.0f}" stroke="{stroke}" stroke-width="3"/>'
            f'<path d="M60,80 A20,20 0 0,0 {80+20*math.cos(math.pi-rad):.0f},{80-20*math.sin(math.pi-rad):.0f}" '
            f'fill="none" stroke="#c0392b" stroke-width="2"/>'
            f'</svg>')

def svg_bar_graph(items, rng):
    """items: list of (label, value)"""
    fill, stroke = _pal(rng)
    max_v = max(v for _, v in items) or 1
    bar_w, gap, base_y, max_h = 36, 18, 120, 90
    bars = ""
    for i, (lab, val) in enumerate(items):
        h = int(val / max_v * max_h)
        x = 40 + i * (bar_w + gap)
        bars += (f'<rect x="{x}" y="{base_y-h}" width="{bar_w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
                 f'<text x="{x+bar_w/2}" y="{base_y-h-6}" text-anchor="middle" font-size="11" fill="{stroke}">{val}</text>'
                 f'<text x="{x+bar_w/2}" y="{base_y+16}" text-anchor="middle" font-size="11" fill="#333">{lab}</text>')
    W = 40 + len(items) * (bar_w + gap) + 20
    return (f'<svg width="{W}" height="150" viewBox="0 0 {W} 150" font-family="\'Segoe UI\',Arial,sans-serif">'
            f'<line x1="30" y1="20" x2="30" y2="{base_y}" stroke="#333" stroke-width="2"/>'
            f'<line x1="30" y1="{base_y}" x2="{W-10}" y2="{base_y}" stroke="#333" stroke-width="2"/>'
            f'{bars}</svg>')

def svg_pictograph(items, rng):
    fill, stroke = _pal(rng)
    rows = ""
    for i, (lab, count) in enumerate(items):
        icons = "".join(
            f'<circle cx="{70+j*20}" cy="{18+i*30}" r="7" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'
            for j in range(count)
        )
        rows += f'<text x="4" y="{22+i*30}" font-size="12" fill="#333">{lab}</text>{icons}'
    W = max(70 + max(c for _, c in items) * 20 + 20, 160)
    return f'<svg width="{W}" height="{len(items)*30+10}" viewBox="0 0 {W} {len(items)*30+10}">{rows}</svg>'

def svg_ruler(length_cm, rng):
    fill, stroke = _pal(rng)
    px = 16
    W = length_cm * px + 30
    marks = ""
    for i in range(length_cm + 1):
        x = 15 + i * px
        h = 12 if i % 5 == 0 else 7
        marks += f'<line x1="{x}" y1="18" x2="{x}" y2="{18+h}" stroke="{stroke}" stroke-width="1.5"/>'
        if i % 5 == 0:
            marks += f'<text x="{x}" y="46" text-anchor="middle" font-size="10" fill="{stroke}">{i}</text>'
    return (f'<svg width="{W}" height="52" viewBox="0 0 {W} 52">'
            f'<rect x="10" y="16" width="{length_cm*px+10}" height="14" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'{marks}</svg>')

def svg_thermometer(temp, rng):
    fill, stroke = _pal(rng)
    y = 90 - min(temp, 40) * 1.4
    return (f'<svg width="55" height="110" viewBox="0 0 55 110">'
            f'<rect x="22" y="12" width="10" height="70" rx="5" fill="#eee" stroke="{stroke}" stroke-width="2"/>'
            f'<circle cx="27" cy="90" r="12" fill="{fill}" stroke="{stroke}" stroke-width="2"/>'
            f'<rect x="24" y="{y:.0f}" width="6" height="{90-y:.0f}" fill="#c0392b"/>'
            f'<text x="42" y="55" font-size="11" fill="{stroke}">{temp}°C</text></svg>')

# ─── MC / TF helpers ─────────────────────────────────────────────────────────
def mc_html(rng, correct, lo=0, spread=10, text_options=None):
    labels = ['A', 'B', 'C', 'D']
    if text_options:
        pool = list(text_options)
        rng.shuffle(pool)
        correct_label = None
        html = '<div class="mc-options">'
        for i, (val, is_cor) in enumerate(pool[:4]):
            lbl = labels[i]
            if is_cor:
                correct_label = lbl
            html += f'<span class="mc-opt">{lbl}) {val}</span>'
        html += '</div>'
        return html, correct_label
    wrongs, tried = set(), {correct}
    for _ in range(80):
        if len(wrongs) >= 3:
            break
        d = rng.randint(1, max(1, spread))
        for cand in (correct + d, correct - d):
            if cand not in tried and cand >= lo:
                wrongs.add(cand)
                tried.add(cand)
    extra = 1
    while len(wrongs) < 3:
        cand = correct + extra
        if cand not in tried:
            wrongs.add(cand)
        extra += 1
    pool = [(correct, True)] + [(w, False) for w in list(wrongs)[:3]]
    rng.shuffle(pool)
    correct_label = None
    html = '<div class="mc-options">'
    for i, (val, is_cor) in enumerate(pool[:4]):
        lbl = labels[i]
        if is_cor:
            correct_label = lbl
        html += f'<span class="mc-opt">{lbl}) {val}</span>'
    html += '</div>'
    return html, correct_label

def tf_html(statement, is_true):
    opts = '<span class="tf-row"><span class="tf-opt">True</span><span class="tf-opt">False</span></span>'
    return f'{statement} &nbsp;{opts}', "True" if is_true else "False"

def q_li(text):
    return f'<li class="question">{text}</li>'

# ─── Topic block helpers ─────────────────────────────────────────────────────
def topic_block(n):
    if n <= 10: return "count"
    if n <= 20: return "add"
    if n <= 30: return "sub"
    if n <= 40: return "place"
    if n <= 50: return "ops"
    if n <= 60: return "measure"
    if n <= 70: return "geo"
    if n <= 80: return "groups"
    if n <= 90: return "data"
    return "review"

# ─── Section builders ────────────────────────────────────────────────────────
def sec_topic(n, rng, which):
    """Sections 1–2: topic-focused with diagrams (Grade 1)."""
    block = topic_block(n)
    topic, _ = LESSONS[n]
    html = '<ol class="q-list">'
    answers = []
    hi = max_num(n)
    used_diag = []

    def add(q, ans, diag=None, caption=None, kind=None):
        nonlocal html
        answers.append((str(len(answers) + 1), ans))
        body = q
        if diag:
            body += "<br>" + diagram(diag, caption or "")
            used_diag.append(kind or caption or "diag")
        html += q_li(body)

    if block == "count":
        filled = rng.randint(3, 10)
        add(f'How many counters are in the ten-frame? <span class="blank"></span>',
            str(filled), svg_ten_frame(filled), "Ten-frame", "tenframe")
        lo, hi_nl = 0, 20
        mark = rng.randint(2, 18)
        add(f'What number is marked? <span class="blank"></span>',
            str(mark), svg_number_line(lo, hi_nl, mark), f"Number line {lo}–{hi_nl}", "numberline")
        a = rng.randint(1, 18)
        add(f'What is <strong>1 more</strong> than {a}? <span class="blank"></span>', str(a + 1))
        b = rng.randint(2, 20)
        add(f'What is <strong>1 less</strong> than {b}? <span class="blank"></span>', str(b - 1))
        x, y = rng.randint(1, 20), rng.randint(1, 20)
        while x == y:
            y = rng.randint(1, 20)
        sym = ">" if x > y else "<"
        add(f'Fill in &gt; or &lt;: {x} <span class="blank"></span> {y}', sym)

    elif block == "add":
        a = rng.randint(2, min(9, hi // 2 + 2))
        b = rng.randint(1, min(9, hi - a))
        whole = a + b
        hide = rng.choice(["a", "b", "w"])
        ans = {"a": a, "b": b, "w": whole}[hide]
        add(f'Find the missing number in the part–whole model. <span class="blank"></span>',
            str(ans), svg_part_whole(whole, a, b, rng, hide=hide), "Part–whole model", "partwhole")
        x, y = rng.randint(1, 9), rng.randint(1, 9)
        add(f'{x} + {y} = <span class="blank"></span>', str(x + y))
        x, y = rng.randint(3, 10), rng.randint(2, 9)
        opt, lbl = mc_html(rng, x + y, lo=1, spread=5)
        add(f'{x} + {y} = ?{opt}', f"{lbl}) {x+y}")
        bond = rng.randint(3, 9)
        other = 10 - bond
        add(f'Complete the bond to 10: {bond} + <span class="blank"></span> = 10', str(other))
        stmt_ok = rng.random() < 0.5
        x, y = rng.randint(2, 8), rng.randint(2, 8)
        shown = x + y if stmt_ok else x + y + rng.choice([-1, 1, 2])
        qh, ans = tf_html(f"<strong>{x} + {y} = {shown}</strong>", shown == x + y)
        add(qh, ans)

    elif block == "sub":
        whole = rng.randint(8, min(20, hi))
        a = rng.randint(2, whole - 1)
        b = whole - a
        hide = rng.choice(["a", "b", "w"])
        ans = {"a": a, "b": b, "w": whole}[hide]
        add(f'Find the missing number. <span class="blank"></span>',
            str(ans), svg_part_whole(whole, a, b, rng, hide=hide), "Part–whole model", "partwhole")
        x = rng.randint(6, min(20, hi)); y = rng.randint(1, x - 1)
        add(f'{x} − {y} = <span class="blank"></span>', str(x - y))
        x = rng.randint(8, 18); y = rng.randint(2, 8)
        opt, lbl = mc_html(rng, x - y, lo=0, spread=4)
        add(f'{x} − {y} = ?{opt}', f"{lbl}) {x-y}")
        # fact family
        p, q = rng.randint(2, 8), rng.randint(2, 8)
        add(f'Complete the fact family: {p} + {q} = {p+q}, so {p+q} − {p} = <span class="blank"></span>',
            str(q))
        stmt_ok = rng.random() < 0.5
        x = rng.randint(10, 18); y = rng.randint(2, 8)
        shown = x - y if stmt_ok else x - y + rng.choice([-1, 1, 2])
        qh, ans = tf_html(f"<strong>{x} − {y} = {shown}</strong>", shown == x - y)
        add(qh, ans)

    elif block == "place":
        num = rng.randint(11, hi)
        add(f'What is the value of the digit <strong>{(num//10)%10}</strong> in <strong>{num}</strong>? '
            f'<span class="blank"></span>',
            str(((num // 10) % 10) * 10),
            svg_place_value(num), f"Place value of {num}", "placevalue")
        a, b = rng.randint(10, hi), rng.randint(10, hi)
        while a == b:
            b = rng.randint(10, hi)
        sym = ">" if a > b else "<"
        add(f'Fill in &gt; or &lt;: {a} <span class="blank"></span> {b}', sym)
        lo, hi_nl = 0, min(100, ((hi // 10) + 1) * 10)
        mark = rng.randint(lo + 5, hi_nl - 5)
        add(f'What number is marked on the number line? <span class="blank"></span>',
            str(mark), svg_number_line(lo, hi_nl, mark), f"Number line {lo}–{hi_nl}", "numberline")
        filled = rng.randint(3, 9)
        add(f'How many counters are in the ten-frame? <span class="blank"></span>',
            str(filled), svg_ten_frame(filled), "Ten-frame", "tenframe")
        num2 = rng.randint(11, hi)
        add(f'<strong>{num2}</strong> = <span class="blank"></span> tens and <span class="blank"></span> ones',
            f"{num2//10} tens, {num2%10} ones")

    elif block == "ops":
        a = rng.randint(10, min(40, hi)); b = rng.randint(5, 20)
        add(f'{a} + {b} = <span class="blank"></span>',
            str(a + b), svg_part_whole(a + b, a, b, rng, hide="w"), "Part–whole", "partwhole")
        x = rng.randint(20, min(80, hi)); y = rng.randint(5, 20)
        if x <= y: x = y + 10
        add(f'{x} − {y} = <span class="blank"></span>', str(x - y))
        tens = rng.randint(2, 8) * 10
        add(f'{tens} + 10 = <span class="blank"></span>', str(tens + 10))
        x, y = rng.randint(12, 30), rng.randint(8, 20)
        opt, lbl = mc_html(rng, x + y, lo=1, spread=8)
        add(f'{x} + {y} = ?{opt}', f"{lbl}) {x+y}")
        coins = rng.choice([5, 10, 20, 50])
        add(f'A coin shows <strong>{coins}</strong>. Write the value: <span class="blank"></span>',
            str(coins))

    elif block == "measure":
        length = rng.randint(3, 10)
        add(f'How long is the object? <span class="blank"></span> cm',
            f"{length} cm", svg_ruler(length, rng), "Ruler", "ruler")
        h, m = rng.randint(1, 12), rng.choice([0, 30])
        clock, ts = svg_clock(h, m)
        add(f'What time does the clock show? <span class="blank"></span>',
            ts, clock, f"Clock showing {ts}", "clock")
        a, b = rng.randint(3, 9), rng.randint(3, 9)
        longer = f"{a} cm" if a > b else (f"{b} cm" if b > a else "equal")
        add(f'Which is longer: <strong>{a} cm</strong> or <strong>{b} cm</strong>? <span class="blank"></span>', longer)
        temp = rng.randint(15, 32)
        add(f'What temperature is shown? <span class="blank"></span> °C',
            f"{temp} °C", svg_thermometer(temp, rng), "Thermometer", "thermo")
        add(f'How many days are in <strong>1</strong> week? <span class="blank"></span>', "7")

    elif block == "geo":
        # Avoid sides+vertices duplicate; rotate question kinds
        sname = rng.choice(list(SHAPE_META))
        add(f'Name this shape: <span class="blank"></span>',
            sname, svg_shape(sname, rng), sname, "shape-name")
        s2 = rng.choice([s for s in SHAPE_META if s != "Circle"])
        ask = _pick_avoid(rng, ["sides", "symmetry"], _RECENT_GEO)
        if ask == "sides":
            add(f'How many sides does a <strong>{s2}</strong> have? <span class="blank"></span>',
                str(SHAPE_META[s2][0]), svg_shape(s2, rng), s2, "shape-sides")
        else:
            sq = rng.choice(["Square", "Rectangle"])
            add(f'Count the dashed symmetry lines: <span class="blank"></span>',
                str(SHAPE_META[sq][1]), svg_shape(sq, rng, symmetry=True), f"{sq} symmetry", "symmetry")
        _RECENT_GEO.append(ask)
        cols, rows = rng.randint(2, 4), rng.randint(2, 3)
        shaded = set(rng.sample(range(cols * rows), rng.randint(2, cols * rows - 1)))
        add(f'Each square = 1. How many are shaded? <span class="blank"></span>',
            str(len(shaded)), svg_grid_area(cols, rows, shaded, rng), "Area grid", "grid")
        facts = [
            ("A triangle has 3 sides.", True),
            ("A square has 5 sides.", False),
            ("A circle has corners.", False),
            ("A rectangle has 4 sides.", True),
        ]
        stmt, ok = rng.choice(facts)
        qh, ans = tf_html(stmt, ok)
        add(qh, ans)
        add(f'A <strong>hexagon</strong> has how many sides? <span class="blank"></span>', "6")

    elif block == "groups":
        filled = rng.randint(4, 10)
        add(f'How many counters? <span class="blank"></span>',
            str(filled), svg_ten_frame(filled), "Ten-frame", "tenframe")
        g, p = rng.randint(2, 4), rng.randint(2, 5)
        add(f'<strong>{g}</strong> boxes with <strong>{p}</strong> in each. How many in all? '
            f'<span class="blank"></span>',
            str(g * p), svg_equal_groups(g, p, rng), f"{g} boxes of {p}", "boxes")
        skip = rng.choice([2, 5, 10])
        start = skip
        seq = [start + i * skip for i in range(5)]
        add(f'Count by {skip}s: {", ".join(map(str, seq[:4]))}, <span class="blank"></span>',
            str(seq[4]))
        a = rng.choice([2, 5, 10])
        add(f'{a} + {a} + {a} = <span class="blank"></span>',
            str(a + a + a))
        total = rng.choice([8, 10, 12]); share = rng.choice([d for d in (2, 4) if total % d == 0])
        add(f'Put <strong>{total}</strong> into <strong>{share}</strong> equal piles. Each pile has? '
            f'<span class="blank"></span>', str(total // share))

    elif block == "data":
        items = [("Mon", rng.randint(2, 8)), ("Tue", rng.randint(2, 8)),
                 ("Wed", rng.randint(2, 8)), ("Thu", rng.randint(2, 8))]
        dtype = _pick_avoid(rng, ["bar", "picto"], _RECENT_DATA)
        if dtype == "bar":
            target = rng.choice(items)
            add(f'How many on <strong>{target[0]}</strong>? <span class="blank"></span>',
                str(target[1]), svg_bar_graph(items, rng), "Bar graph", "bar")
        else:
            fruits = [("Apples", rng.randint(2, 5)), ("Pears", rng.randint(2, 5)),
                      ("Oranges", rng.randint(2, 5))]
            fi = rng.randint(0, 2)
            add(f'Each ● = 1. How many <strong>{fruits[fi][0]}</strong>? <span class="blank"></span>',
                str(fruits[fi][1]), svg_pictograph(fruits, rng), "Pictograph", "picto")
            items = fruits
        _RECENT_DATA.append(dtype)
        add(f'Which has the most? <span class="blank"></span>',
            max(items, key=lambda x: x[1])[0])
        skip = rng.choice([2, 3, 5, 10])
        start = skip
        seq = [start + i * skip for i in range(5)]
        add(f'Rule: add {skip}. Missing: {seq[0]}, {seq[1]}, ___, {seq[3]}, {seq[4]} → '
            f'<span class="blank"></span>', str(seq[2]))
        add(f'Total for the first two? <span class="blank"></span>',
            str(items[0][1] + items[1][1]))
        colors = ["red", "blue", "green", "yellow"]
        pat = [rng.choice(colors) for _ in range(3)]
        add(f'Colour pattern: {", ".join(pat)}, <span class="blank"></span> … What comes next?',
            pat[0])

    else:  # review / fractions spiral
        num = rng.randint(12, hi)
        add(f'<strong>{num}</strong> has <span class="blank"></span> tens and <span class="blank"></span> ones',
            f"{num//10} tens, {num%10} ones", svg_place_value(num), f"{num}", "placevalue")
        x, y = rng.randint(5, 15), rng.randint(3, 12)
        add(f'{x} + {y} = <span class="blank"></span>', str(x + y))
        denom, numer = rng.choice([2, 4]), None
        numer = rng.randint(1, denom - 1)
        style = _pick_avoid(rng, ["pie", "bar"], _RECENT_FRAC)
        svg = svg_frac_pie(numer, denom, rng) if style == "pie" else svg_frac_bar(numer, denom, rng)
        add(f'Shaded fraction: <span class="blank"></span>',
            f"{numer}/{denom}", svg, "Fraction", style)
        _RECENT_FRAC.append(style)
        h, m = rng.randint(1, 12), rng.choice([0, 30])
        clock, ts = svg_clock(h, m)
        add(f'Time shown: <span class="blank"></span>', ts, clock, "Clock", "clock")
        sname = rng.choice(["Square", "Triangle", "Circle", "Rectangle"])
        add(f'Name this shape: <span class="blank"></span>',
            sname, svg_shape(sname, rng), sname, "shape")

    while len(answers) < 5:
        a, b = rng.randint(2, 12), rng.randint(1, 8)
        add(f'{a} + {b} = <span class="blank"></span>', str(a + b))
    # keep only first 5 if somehow more
    answers = answers[:5]
    # rebuild html if truncated — answers already appended in order; ok if ==5
    html += '</ol>'
    title = f"Section {which}: {topic} (15 mins)"
    _RECENT_DIAGRAMS.extend(used_diag[-3:])
    return title, html, answers


def sec_addsub(n, rng):
    """Section 3: Addition & Subtraction (or early equal groups in later tiers)."""
    html = '<ol class="q-list">'
    answers = []
    hi = max_num(n)
    if n >= 71:
        g, p = rng.randint(2, 4), rng.randint(2, 5)
        html += q_li(f'{g} boxes with {p} in each. How many in all? <span class="blank"></span><br>'
                     + diagram(svg_equal_groups(g, p, rng), f"{g} boxes of {p}"))
        answers.append(("1", str(g * p)))
        html += q_li(f'{p} + {p} + {p} = <span class="blank"></span>')
        answers.append(("2", str(p * 3)))
        skip = rng.choice([2, 5, 10])
        seq = [skip * i for i in range(1, 6)]
        html += q_li(f'Count by {skip}s: {seq[0]}, {seq[1]}, ___, {seq[3]}, {seq[4]} → '
                     f'<span class="blank"></span>')
        answers.append(("3", str(seq[2])))
        a = rng.choice([2, 5, 10])
        html += q_li(f'{a} + {a} = <span class="blank"></span>')
        answers.append(("4", str(a + a)))
        total = rng.choice([10, 12, 8])
        html += q_li(f'Put {total} into 2 piles the same size. Each pile has? <span class="blank"></span>')
        answers.append(("5", str(total // 2)))
        html += '</ol>'
        return "Section 3: Groups &amp; Skip Counting (15 mins)", html, answers

    # Grade 1 add/sub focus
    a = rng.randint(3, min(12, hi // 2 + 4))
    b = rng.randint(2, min(10, hi - a))
    html += q_li(f'Find the missing part.<br>'
                 + diagram(svg_part_whole(a + b, a, b, rng, hide="b"), "Part–whole")
                 + 'Missing = <span class="blank"></span>')
    answers.append(("1", str(b)))
    for i in range(2, 4):
        x, y = rng.randint(1, min(15, hi)), rng.randint(1, min(10, hi))
        html += q_li(f'{x} + {y} = <span class="blank"></span>')
        answers.append((str(i), str(x + y)))
    for i in range(4, 6):
        x = rng.randint(6, min(20, hi)); y = rng.randint(1, x - 1)
        html += q_li(f'{x} − {y} = <span class="blank"></span>')
        answers.append((str(i), str(x - y)))
    html += '</ol>'
    return "Section 3: Addition &amp; Subtraction (15 mins)", html, answers


def sec_word(n, rng):
    hi = max_num(n)
    html = '<ol class="q-list">'
    answers = []
    name = rng.choice(NAMES)
    thing = rng.choice(THINGS)
    a = rng.randint(3, min(15, hi // 2 + 5))
    b = rng.randint(2, min(12, hi - a if hi > a else 10))
    html += q_li(f'<strong>{name}</strong> has <strong>{a} {thing}</strong> and gets '
                 f'<strong>{b} more</strong>. How many in total?<br>'
                 + diagram(svg_part_whole(a + b, a, b, rng, hide="w"), "Part–whole for the story")
                 + f'Answer: <span class="blank"></span> {thing}')
    answers.append(("1", str(a + b)))

    if n >= 71:
        g, p = rng.randint(2, 4), rng.randint(2, 5)
        html += q_li(f'<strong>{g} boxes</strong> each hold <strong>{p} {thing}</strong>. Total?<br>'
                     + diagram(svg_equal_groups(g, p, rng), "Same-size boxes")
                     + f'Answer: <span class="blank"></span>')
        answers.append(("2", str(g * p)))
    else:
        name2 = rng.choice(NAMES)
        have = rng.randint(8, min(20, hi))
        give = rng.randint(2, have - 1)
        html += q_li(f'<strong>{name2}</strong> has <strong>{have} {thing}</strong> and gives away '
                     f'<strong>{give}</strong>. How many left?<br>'
                     + diagram(svg_part_whole(have, have - give, give, rng, hide="a"), "Take-away model")
                     + f'Answer: <span class="blank"></span>')
        answers.append(("2", str(have - give)))

    name3 = rng.choice(NAMES)
    x = rng.randint(5, min(18, hi)); y = rng.randint(3, min(12, hi))
    html += q_li(f'<strong>{name3}</strong> finds <strong>{x}</strong> then <strong>{y}</strong> more {thing}. '
                 f'Total? <span class="blank"></span>')
    answers.append(("3", str(x + y)))

    # compare story
    red, blue = rng.randint(3, 12), rng.randint(3, 12)
    while red == blue:
        blue = rng.randint(3, 12)
    more = "red" if red > blue else "blue"
    html += q_li(f'There are <strong>{red} red</strong> and <strong>{blue} blue</strong> balloons. '
                 f'Which colour has more? <span class="blank"></span>')
    answers.append(("4", more))

    # MC word
    start = rng.randint(6, 14); lose = rng.randint(1, start - 1)
    opt, lbl = mc_html(rng, start - lose, lo=0, spread=4)
    html += q_li(f'A jar has {start} sweets. {lose} are eaten. How many left?{opt}')
    answers.append(("5", f"{lbl}) {start - lose}"))
    html += '</ol>'
    return "Section 4: Word Problems (15 mins)", html, answers


def sec_measure(n, rng):
    t = tier(n)
    html = '<ol class="q-list">'
    answers = []
    facts = [
        ("minutes in 1 hour", lambda a: 60, (1, 1)),
        ("days in {a} week(s)", lambda a: a * 7, (1, 3)),
        ("cm in {a} m", lambda a: a * 100, (1, 3)),
    ]
    fact = rng.choice(facts)
    a_val = rng.randint(*fact[2])
    ans = fact[1](a_val)
    html += q_li(f'How many {fact[0].format(a=a_val)}? <span class="blank"></span>')
    answers.append(("1", str(ans)))

    # simple elapsed (hours only for Grade 1)
    sh = rng.randint(7, 14)
    add_h = rng.randint(1, 3)
    html += q_li(f'Start at <strong>{sh}:00</strong>. After <strong>{add_h} hour(s)</strong>, '
                 f'the time is? <span class="blank"></span>')
    answers.append(("2", f"{(sh + add_h) % 24}:00"))

    a, b = rng.randint(4, 12), rng.randint(4, 12)
    longer = f"{a} cm" if a > b else (f"{b} cm" if b > a else "equal")
    html += q_li(f'Longer: <strong>{a} cm</strong> or <strong>{b} cm</strong>? <span class="blank"></span>')
    answers.append(("3", longer))

    # Rotate measure diagram across lessons
    choice = _pick_avoid(rng,
                         ["clock", "ruler", "thermo"] if t >= 2 else ["clock", "ruler"],
                         _RECENT_MEASURE)
    _RECENT_MEASURE.append(choice)
    if choice == "clock":
        h, m = rng.randint(1, 12), rng.choice([0, 30])
        clock, ts = svg_clock(h, m)
        html += q_li(f'What time does the clock show?<br>'
                     + diagram(clock, f"Clock showing {ts}")
                     + 'Answer: <span class="blank"></span>')
        answers.append(("4", ts))
    elif choice == "ruler":
        length = rng.randint(3, 10)
        html += q_li(f'Read the ruler length:<br>'
                     + diagram(svg_ruler(length, rng), "Ruler in cm")
                     + 'Length = <span class="blank"></span> cm')
        answers.append(("4", f"{length} cm"))
    else:
        temp = rng.randint(12, 35)
        html += q_li(f'Read the thermometer:<br>'
                     + diagram(svg_thermometer(temp, rng), "Thermometer")
                     + 'Temperature = <span class="blank"></span> °C')
        answers.append(("4", f"{temp} °C"))

    w, h = rng.randint(2, 6), rng.randint(2, 5)
    longer = f"{w} cm" if w != h else "equal"
    if w < h:
        longer = f"{h} cm"
    html += q_li(f'Which is longer: <strong>{w} cm</strong> or <strong>{h} cm</strong>?<br>'
                 + diagram(svg_rect(w, h, rng), "Compare lengths")
                 + '<span class="blank"></span>')
    answers.append(("5", longer))
    html += '</ol>'
    return "Section 5: Measurement &amp; Time (10 mins)", html, answers


def sec_geo_data(n, rng):
    html = '<ol class="q-list">'
    answers = []
    sname = rng.choice(list(SHAPE_META))
    html += q_li(f'Name this shape:<br>'
                 + diagram(svg_shape(sname, rng), sname)
                 + '<span class="blank"></span>')
    answers.append(("1", sname))

    # Never ask both sides and vertices of same shape (same answer for polygons)
    s2 = rng.choice([s for s in SHAPE_META if s != "Circle"])
    geo_ask = _pick_avoid(rng, ["sides", "symmetry", "grid"], _RECENT_GEO)
    if geo_ask == "sides":
        html += q_li(f'How many sides does a <strong>{s2}</strong> have?<br>'
                     + diagram(svg_shape(s2, rng), s2)
                     + '<span class="blank"></span>')
        answers.append(("2", str(SHAPE_META[s2][0])))
    elif geo_ask == "symmetry":
        sq = rng.choice(["Square", "Rectangle"])
        html += q_li(f'Lines of symmetry on this <strong>{sq}</strong>?<br>'
                     + diagram(svg_shape(sq, rng, symmetry=True), sq)
                     + '<span class="blank"></span>')
        answers.append(("2", str(SHAPE_META[sq][1])))
    else:
        cols, rows = rng.randint(2, 4), rng.randint(2, 3)
        shaded = set(rng.sample(range(cols * rows), rng.randint(2, cols * rows - 1)))
        html += q_li(f'Each square = 1. How many are shaded?<br>'
                     + diagram(svg_grid_area(cols, rows, shaded, rng), "Area grid")
                     + '<span class="blank"></span>')
        answers.append(("2", str(len(shaded))))
    _RECENT_GEO.append(geo_ask)

    # Q3: complementary geo (different from Q2)
    if geo_ask != "grid":
        cols, rows = rng.randint(2, 4), rng.randint(2, 3)
        shaded = set(rng.sample(range(cols * rows), rng.randint(2, cols * rows - 1)))
        html += q_li(f'How many coloured squares?<br>'
                     + diagram(svg_grid_area(cols, rows, shaded, rng), "Colour grid")
                     + 'Coloured = <span class="blank"></span>')
        answers.append(("3", str(len(shaded))))
    else:
        facts = [
            ("A triangle has 3 sides.", True),
            ("A square has 5 sides.", False),
            ("A hexagon has 6 sides.", True),
            ("A circle has 4 vertices.", False),
        ]
        stmt, ok = rng.choice(facts)
        qh, ans = tf_html(stmt, ok)
        html += q_li(qh)
        answers.append(("3", ans))

    # Data diagram — rotate bar vs pictograph
    dtype = _pick_avoid(rng, ["bar", "picto"], _RECENT_DATA)
    _RECENT_DATA.append(dtype)
    if dtype == "bar":
        labs = ["Red", "Blue", "Green"]
        items = [(labs[i], rng.randint(2, 8)) for i in range(3)]
        best = max(items, key=lambda x: x[1])[0]
        html += q_li(f'Which colour has the most?<br>'
                     + diagram(svg_bar_graph(items, rng), "Bar graph")
                     + '<span class="blank"></span>')
        answers.append(("4", best))
    else:
        fruits = [("Apples", rng.randint(2, 5)), ("Pears", rng.randint(2, 5)), ("Bananas", rng.randint(2, 5))]
        html += q_li(f'Each ● = 1. How many Apples?<br>'
                     + diagram(svg_pictograph(fruits, rng), "Pictograph")
                     + '<span class="blank"></span>')
        answers.append(("4", str(fruits[0][1])))

    facts = [
        ("A triangle has 3 sides.", True),
        ("A square has 5 sides.", False),
        ("A hexagon has 6 sides.", True),
        ("A circle has 4 vertices.", False),
    ]
    stmt, ok = rng.choice(facts)
    qh, ans = tf_html(stmt, ok)
    html += q_li(qh)
    answers.append(("5", ans))
    html += '</ol>'
    return "Section 6: Geometry &amp; Data (10 mins)", html, answers


def sec_fractions(n, rng):
    """Section 7: Halves & quarters (Grade 1) with rotating diagram styles."""
    html = '<ol class="q-list">'
    answers = []
    denoms = [2, 4] if n < 91 else [2, 3, 4]

    # Rotate pie / bar / numberline so consecutive lessons differ
    styles = ["pie", "bar", "numberline"]
    order = []
    for _ in range(3):
        s = _pick_avoid(rng, [x for x in styles if x not in order], _RECENT_FRAC)
        order.append(s)
    _RECENT_FRAC.extend(order[:2])

    for i, style in enumerate(order, 1):
        d = rng.choice(denoms)
        num = rng.randint(1, d - 1)
        if style == "pie":
            html += q_li(f'What fraction of the circle is shaded?<br>'
                         + diagram(svg_frac_pie(num, d, rng), "Fraction circle")
                         + '<span class="blank"></span>')
        elif style == "bar":
            html += q_li(f'What fraction of the bar is shaded?<br>'
                         + diagram(svg_frac_bar(num, d, rng), "Fraction bar")
                         + '<span class="blank"></span>')
        else:
            d = rng.choice([2, 4])
            num = rng.randint(1, d - 1)
            html += q_li(f'What fraction is marked on the number line?<br>'
                         + diagram(svg_frac_numberline(num, d), "Fraction number line")
                         + '<span class="blank"></span>')
        answers.append((str(i), f"{num}/{d}"))

    # unshaded
    d4 = rng.choice([2, 4])
    num4 = rng.randint(1, d4 - 1)
    html += q_li(f'What fraction is <em>NOT</em> shaded?<br>'
                 + diagram(svg_frac_bar(num4, d4, rng), "Fraction bar")
                 + '<span class="blank"></span>')
    answers.append(("4", f"{d4-num4}/{d4}"))

    if rng.random() < 0.5:
        html += q_li(f'Which is greater: <strong>1/2</strong> or <strong>1/4</strong>? <span class="blank"></span>')
        answers.append(("5", "1/2"))
    else:
        opt, lbl = mc_html(rng, None, text_options=[
            ("1/2", True), ("1/3", False), ("1/4", False), ("2/2", False)])
        html += q_li(f'Which fraction means one half?{opt}')
        answers.append(("5", f"{lbl}) 1/2"))
    html += '</ol>'
    return "Section 7: Fractions — Halves &amp; Quarters (15 mins)", html, answers


def sec_bonus(n, rng):
    html = '<ol class="q-list">'
    answers = []
    a, b, c = rng.randint(5, 20), rng.randint(2, 10), rng.randint(1, 8)
    html += q_li(f'{a} + {b} − {c} = <span class="blank"></span>')
    answers.append(("B1", str(a + b - c)))
    skip = rng.choice([2, 5, 10])
    seq = [skip * i for i in range(1, 6)]
    html += q_li(f'Find the missing number: {seq[0]}, {seq[1]}, {seq[2]}, ___, {seq[4]} → '
                 f'<span class="blank"></span>')
    answers.append(("B2", str(seq[3])))
    filled = rng.randint(4, 10)
    html += q_li(f'Challenge: how many counters?<br>'
                 + diagram(svg_ten_frame(filled), "Ten-frame")
                 + '<span class="blank"></span>')
    answers.append(("B3", str(filled)))
    html += '</ol>'
    return "Bonus Challenge (5 mins)", html, answers


# ─── Page builder ────────────────────────────────────────────────────────────
def build_lesson(n, rng):
    topic, subtitle = LESSONS[n]
    sections = []
    all_answers = []

    for which in (1, 2):
        title, html, ans = sec_topic(n, rng, which)
        # differentiate sec2 slightly by re-seeding offset
        if which == 2:
            rng2 = random.Random(n * 7919 + 31337 + 777)
            title, html, ans = sec_topic(n, rng2, which)
            title = f"Section 2: {topic} — Practice (15 mins)"
        sections.append((title, html))
        all_answers.append((title, ans))

    for fn in (sec_addsub, sec_word, sec_measure, sec_geo_data, sec_fractions, sec_bonus):
        title, html, ans = fn(n, rng)
        sections.append((title, html))
        all_answers.append((title, ans))

    body = ""
    for title, html in sections:
        cls = "bonus" if title.startswith("Bonus") else "section-header"
        icon = "⭐ " if cls == "bonus" else "⏱ "
        body += f'<div class="{cls}">{icon}{title}</div>\n{html}\n'

    ak_rows = ""
    for sec_title, sec_ans in all_answers:
        short = sec_title.split(":")[0].replace("Section ", "S").replace("Bonus Challenge (5 mins)", "Bonus")
        if "—" in sec_title:
            short = "S2"
        for q, a in sec_ans:
            ak_rows += f'<tr><td>{short}</td><td>{q}</td><td style="text-align:left">{a}</td></tr>\n'

    answer_section = f"""
<hr class="before-answer">
<div class="answer-section">
  <div class="answer-header">✅ Answer Key — Lesson {n}</div>
  <table class="answer-key">
    <thead><tr><th>Section</th><th>Q#</th><th>Answer</th></tr></thead>
    <tbody>{ak_rows}</tbody>
  </table>
</div>
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lesson {n} – Grade 1 Math Theory</title>
  <style>{CSS}</style>
</head>
<body>
  <h1>🧠 Grade 1 Math Theory – Lesson {n}</h1>
  <div class="meta">{subtitle} &nbsp;|&nbsp; Level: Year 2</div>
  <div class="name-line">
    <span>Name:</span><span class="line"></span>
    <span>Date:</span><span class="line"></span>
  </div>
  <hr>
{body}
{answer_section}
</body>
</html>"""

def main():
    for n in range(1, 101):
        rng = lesson_rng(n)
        html = build_lesson(n, rng)
        path = os.path.join(OUTDIR, f"Lesson {n} - Grade 1 Math Theory.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✓ Lesson {n}: {LESSONS[n][0]}")
    print(f"\nDone. 100 Year-1 lessons saved to:\n  {OUTDIR}")

if __name__ == "__main__":
    main()
