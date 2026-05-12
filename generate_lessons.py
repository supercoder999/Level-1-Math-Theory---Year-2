#!/usr/bin/env python3
"""
Generate Grade 1 Math Theory – Lessons 2 to 100.

Question format variety per section (rotates every 4 lessons):
  fill-in-blank | multiple choice | true/false | matching / picture

Section rotation by lesson range:
  Lessons  1-40 : Comparing Numbers & Order | Shapes & Measurement | Telling Time
  Lessons 41-70 : Comparing Numbers & Order | Place Value           | Number Patterns
  Lessons 71-100: Multiplication             | Place Value           | Number Patterns

Run: python3 generate_lessons.py
"""
import os, math, random

OUTDIR = os.path.dirname(os.path.abspath(__file__))

# ─── CSS ─────────────────────────────────────────────────────────────────────
CSS = """
    body {
      font-family: 'Segoe UI', Arial, sans-serif;
      max-width: 860px;
      margin: 0 auto;
      padding: 32px 24px;
      color: #1a1a2e;
      font-size: 15px;
      line-height: 1.7;
    }
    h1 { text-align:center; font-size:1.55em; color:#0d4f8c; margin-bottom:4px; }
    .meta { text-align:center; color:#555; margin-bottom:28px; font-size:.97em; }
    .section-header {
      background:#e8f0fb; border-left:5px solid #0d4f8c;
      padding:7px 14px; margin:28px 0 14px 0;
      font-weight:bold; font-size:1.05em; color:#0d4f8c;
      border-radius:0 6px 6px 0;
    }
    .question { margin:10px 0 10px 18px; }
    .blank {
      display:inline-block; min-width:48px;
      border-bottom:2px solid #333; margin:0 5px; vertical-align:bottom;
    }
    .wide-blank {
      display:inline-block; min-width:140px;
      border-bottom:2px solid #333; margin:0 5px; vertical-align:bottom;
    }
    .visual-row {
      display:flex; gap:40px; flex-wrap:wrap;
      align-items:flex-start; margin:12px 0 12px 18px;
    }
    .visual-item { text-align:center; font-size:.9em; color:#444; }
    .visual-item svg { display:block; margin:0 auto 6px auto; }
    /* Multiple choice */
    .mc-options { display:flex; gap:18px; flex-wrap:wrap; margin:5px 0 3px 0; }
    .mc-opt { padding:3px 12px; border:1.5px solid #bcd; border-radius:4px; background:#f7f9ff; }
    /* True / False */
    .tf-row { display:inline-flex; gap:18px; margin-left:10px; }
    .tf-opt { padding:2px 12px; border:1.5px solid #bcd; border-radius:4px; background:#f7f9ff; }
    /* Matching */
    .match-instructions { margin:2px 0 8px 18px; color:#555; font-size:.93em; }
    .matching { display:flex; gap:50px; margin:8px 0 10px 18px; flex-wrap:wrap; }
    .match-col { display:flex; flex-direction:column; gap:8px; }
    .match-item {
      padding:5px 14px; border:1.5px solid #bcd; border-radius:6px;
      background:#f7f9ff; min-width:100px; text-align:center;
    }
    .match-blank {
      display:inline-block; min-width:26px;
      border-bottom:2px solid #333; margin-right:6px; vertical-align:bottom;
    }
    /* Dot picture */
    .dot-picture { margin:6px 0 4px 18px; }
    /* Answer key */
    table.answer-key {
      border-collapse:collapse; width:100%;
      margin-top:12px; font-size:.93em;
    }
    table.answer-key th {
      background:#0d4f8c; color:#fff;
      padding:7px 12px; text-align:center;
    }
    table.answer-key td {
      border:1px solid #bcd; padding:6px 12px; text-align:center;
    }
    table.answer-key tr:nth-child(even) td { background:#f0f5ff; }
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
    hr { border:none; border-top:1px solid #dce3ef; margin:32px 0; }
    .name-line { display:flex; gap:32px; margin-bottom:20px; font-size:.97em; }
    .name-line span { white-space:nowrap; }
    .name-line .line { flex:1; border-bottom:1.5px solid #333; min-width:100px; }
    ol.q-list { padding-left:22px; margin:0; }
    ol.q-list li { margin:9px 0; }
    .answer-section { break-before:page; page-break-before:always; }
    @media print { hr.before-answer { display:none; } }
"""

# ─── SVG helpers ──────────────────────────────────────────────────────────────
def clock_svg(hour, minute=0):
    cx, cy, r = 65, 65, 60
    h_rad = math.radians((hour % 12) * 30 + minute * 0.5)
    hx = cx + 32 * math.sin(h_rad); hy = cy - 32 * math.cos(h_rad)
    m_rad = math.radians(minute * 6)
    mx = cx + 44 * math.sin(m_rad); my = cy - 44 * math.cos(m_rad)
    ticks = ""
    for i in range(12):
        a = math.radians(i * 30)
        x1 = cx + (r-10)*math.sin(a); y1 = cy - (r-10)*math.cos(a)
        x2 = cx + r*math.sin(a);      y2 = cy - r*math.cos(a)
        ticks += f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="#0d4f8c" stroke-width="2"/>'
    nums = ""
    for i, lbl in {0:"12",1:"1",2:"2",3:"3",4:"4",5:"5",6:"6",7:"7",8:"8",9:"9",10:"10",11:"11"}.items():
        a = math.radians(i*30)
        nx = cx + (r-18)*math.sin(a); ny = cy - (r-18)*math.cos(a) + 4
        nums += f'<text x="{nx:.1f}" y="{ny:.1f}" font-size="10" text-anchor="middle" fill="#1a1a2e">{lbl}</text>'
    fmt_str = f"{hour}:{minute:02d}"
    return (f'<svg width="130" height="130" viewBox="0 0 130 130">'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="white" stroke="#0d4f8c" stroke-width="4"/>'
            f'{ticks}{nums}'
            f'<line x1="{cx}" y1="{cy}" x2="{hx:.1f}" y2="{hy:.1f}" stroke="#0d4f8c" stroke-width="5" stroke-linecap="round"/>'
            f'<line x1="{cx}" y1="{cy}" x2="{mx:.1f}" y2="{my:.1f}" stroke="#c0392b" stroke-width="3" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="{cy}" r="4" fill="#1a1a2e"/></svg>'), fmt_str


def dot_grid_svg(count, per_row=5):
    rows_n = max(1, (count + per_row - 1) // per_row)
    w = per_row * 28 + 8;  h = rows_n * 28 + 8
    dots = ""
    for i in range(count):
        cx = 18 + (i % per_row) * 28
        cy = 18 + (i // per_row) * 28
        dots += f'<circle cx="{cx}" cy="{cy}" r="10" fill="#0d4f8c" opacity="0.85"/>'
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}">{dots}</svg>'


# ─── Shape data ───────────────────────────────────────────────────────────────
SHAPES = {
    "Circle":    '<svg width="80" height="80" viewBox="0 0 80 80"><circle cx="40" cy="40" r="34" fill="#cce4f7" stroke="#0d4f8c" stroke-width="3"/></svg>',
    "Square":    '<svg width="80" height="80" viewBox="0 0 80 80"><rect x="10" y="10" width="60" height="60" fill="#cce4f7" stroke="#0d4f8c" stroke-width="3"/></svg>',
    "Triangle":  '<svg width="80" height="80" viewBox="0 0 80 80"><polygon points="40,6 76,74 4,74" fill="#cce4f7" stroke="#0d4f8c" stroke-width="3"/></svg>',
    "Rectangle": '<svg width="110" height="70" viewBox="0 0 110 70"><rect x="6" y="8" width="98" height="54" fill="#cce4f7" stroke="#0d4f8c" stroke-width="3"/></svg>',
    "Pentagon":  '<svg width="80" height="80" viewBox="0 0 80 80"><polygon points="40,5 75,28 62,70 18,70 5,28" fill="#cce4f7" stroke="#0d4f8c" stroke-width="3"/></svg>',
    "Hexagon":   '<svg width="80" height="80" viewBox="0 0 80 80"><polygon points="40,4 72,22 72,58 40,76 8,58 8,22" fill="#cce4f7" stroke="#0d4f8c" stroke-width="3"/></svg>',
    "Oval":      '<svg width="110" height="70" viewBox="0 0 110 70"><ellipse cx="55" cy="35" rx="46" ry="26" fill="#cce4f7" stroke="#0d4f8c" stroke-width="3"/></svg>',
    "Diamond":   '<svg width="80" height="80" viewBox="0 0 80 80"><polygon points="40,4 76,40 40,76 4,40" fill="#cce4f7" stroke="#0d4f8c" stroke-width="3"/></svg>',
}
SHAPE_SIDES = {"Circle":0,"Square":4,"Triangle":3,"Rectangle":4,"Pentagon":5,"Hexagon":6,"Oval":0,"Diamond":4}

# ─── Word problem templates ───────────────────────────────────────────────────
WP_TEMPLATES = [
    lambda a,b: (f"Minh has <strong>{a} apples</strong>. He gets <strong>{b} more</strong>. How many does he have now?", a+b, "apples"),
    lambda a,b: (f"There are <strong>{a+b} birds</strong> on a tree. <strong>{b} fly away</strong>. How many are left?", a, "birds"),
    lambda a,b: (f"Lan has <strong>{a} stickers</strong>. She gives <strong>{b}</strong> to her friend. How many does she have left?", a-b, "stickers"),
    lambda a,b: (f"A basket has <strong>{a} oranges</strong> and <strong>{b} bananas</strong>. How many fruits in total?", a+b, "fruits"),
    lambda a,b: (f"There are <strong>{a} red flowers</strong> and <strong>{b} yellow flowers</strong>. How many flowers altogether?", a+b, "flowers"),
    lambda a,b: (f"A shop has <strong>{a+b} candies</strong>. It sells <strong>{b}</strong>. How many remain?", a, "candies"),
    lambda a,b: (f"Hoa collects <strong>{a} shells</strong> on Monday and <strong>{b} shells</strong> on Tuesday. How many in total?", a+b, "shells"),
    lambda a,b: (f"There are <strong>{a+b} children</strong> in the playground. <strong>{b} go home</strong>. How many are left?", a, "children"),
    lambda a,b: (f"Tuan has <strong>{a} toy cars</strong>. He buys <strong>{b} more</strong>. How many cars does he have?", a+b, "cars"),
    lambda a,b: (f"A box has <strong>{a+b} crayons</strong>. <strong>{b} are broken</strong>. How many good crayons are there?", a, "crayons"),
    lambda a,b: (f"Nam sees <strong>{a} cats</strong> and <strong>{b} dogs</strong> in the park. How many animals in total?", a+b, "animals"),
    lambda a,b: (f"There are <strong>{a} fish</strong> in a tank. <strong>{b} more</strong> are added. How many fish now?", a+b, "fish"),
    lambda a,b: (f"A bag has <strong>{a+b} marbles</strong>. <strong>{b} are lost</strong>. How many are left?", a, "marbles"),
    lambda a,b: (f"Mai bakes <strong>{a} cupcakes</strong> in the morning and <strong>{b}</strong> in the afternoon. How many cupcakes total?", a+b, "cupcakes"),
    lambda a,b: (f"There are <strong>{a} books</strong> on the shelf. <strong>{b} are taken out</strong>. How many books remain?", a-b, "books"),
    lambda a,b: (f"A class has <strong>{a} boys</strong> and <strong>{b} girls</strong>. How many students in total?", a+b, "students"),
    lambda a,b: (f"Bao has <strong>{a} coins</strong>. He spends <strong>{b}</strong>. How many coins are left?", a-b, "coins"),
    lambda a,b: (f"There are <strong>{a+b} butterflies</strong>. <strong>{b} fly away</strong>. How many stay?", a, "butterflies"),
    lambda a,b: (f"Linh has <strong>{a} pencils</strong>. Her teacher gives her <strong>{b} more</strong>. How many does she have now?", a+b, "pencils"),
    lambda a,b: (f"There are <strong>{a} chairs</strong> in the room. <strong>{b} more</strong> are brought in. How many chairs now?", a+b, "chairs"),
]

NUM_WORDS = {
    0:"zero",1:"one",2:"two",3:"three",4:"four",5:"five",6:"six",7:"seven",
    8:"eight",9:"nine",10:"ten",11:"eleven",12:"twelve",13:"thirteen",
    14:"fourteen",15:"fifteen",16:"sixteen",17:"seventeen",18:"eighteen",
    19:"nineteen",20:"twenty",
}

# ─── Format rotation ──────────────────────────────────────────────────────────
_FMT_CYCLES = {
    'counting':    ['picture','fill',  'mc',   'tf'],
    'addition':    ['fill',   'mc',   'match', 'tf'],
    'subtraction': ['fill',   'mc',   'match', 'tf'],
    'comparing':   ['fill',   'mc',   'tf',    'fill'],
    'word':        ['fill',   'mc',   'fill',  'mc'],
    'shapes':      ['fill',   'mc',   'match', 'fill'],
    'time':        ['fill',   'mc',   'fill',  'mc'],
    'place':       ['fill',   'mc',   'tf',    'fill'],
    'patterns':    ['fill',   'mc',   'tf',    'match'],
    'multiply':    ['fill',   'mc',   'match', 'tf'],
}
_FMT_OFFSETS = {
    'counting':0,'addition':1,'subtraction':2,'comparing':3,
    'word':0,'shapes':1,'time':2,'place':1,'patterns':2,'multiply':3,
}

def section_fmt(n, key):
    opts = _FMT_CYCLES[key]
    return opts[(n + _FMT_OFFSETS.get(key,0)) % len(opts)]


# ─── Question format helpers ──────────────────────────────────────────────────
def mc_options_html(rng, correct, lo=0, spread=4, text_options=None):
    """Build MC options HTML, return (html, correct_label)."""
    labels = ['A','B','C','D']
    if text_options:
        pool = list(text_options)
    else:
        wrongs = set(); tried = {correct}
        for _ in range(60):
            if len(wrongs) >= 3: break
            d = rng.randint(1, spread)
            for cand in [correct+d, correct-d]:
                if cand not in tried and cand >= lo:
                    wrongs.add(cand); tried.add(cand)
        extra = 1
        while len(wrongs) < 3:
            cand = correct + extra
            if cand not in tried: wrongs.add(cand)
            extra += 1
        pool = [(correct, True)] + [(w, False) for w in list(wrongs)[:3]]
    rng.shuffle(pool)
    correct_label = None
    html = '<div class="mc-options">'
    for i,(val,is_cor) in enumerate(pool[:4]):
        lbl = labels[i]
        if is_cor: correct_label = lbl
        html += f'<span class="mc-opt">{lbl}) {val}</span>'
    html += '</div>'
    return html, correct_label


def tf_html(statement, is_true):
    opts = '<span class="tf-row"><span class="tf-opt">True</span><span class="tf-opt">False</span></span>'
    return f'{statement} &nbsp;{opts}', "True" if is_true else "False"


def match_html(rng, pairs, instruction="Match each item to its answer (write A, B, C, or D):"):
    labels = ['A','B','C','D'][:len(pairs)]
    right_vals = [p[1] for p in pairs]
    shuffled = right_vals[:]
    rng.shuffle(shuffled)
    right_labeled = list(zip(labels, shuffled))
    left_col  = ''.join(f'<div class="match-item"><span class="match-blank"></span>{i+1}. &nbsp;{p[0]}</div>' for i,p in enumerate(pairs))
    right_col = ''.join(f'<div class="match-item">{lbl}. &nbsp;{val}</div>' for lbl,val in right_labeled)
    html = (f'<p class="match-instructions">{instruction}</p>'
            f'<div class="matching"><div class="match-col">{left_col}</div>'
            f'<div class="match-col">{right_col}</div></div>')
    answers = []
    for i,(_,val) in enumerate(pairs):
        for lbl,sv in right_labeled:
            if sv == val:
                answers.append((str(i+1), lbl))
                break
    return html, answers


def _unique_add_pairs(rng, max_a, max_b, count=4):
    pairs=[]; used=set()
    for _ in range(200):
        if len(pairs)>=count: break
        a=rng.randint(1,max_a); b=rng.randint(1,max_b); s=a+b
        if s not in used: used.add(s); pairs.append((a,b,s))
    return pairs[:count]


def _unique_sub_pairs(rng, max_a, count=4):
    pairs=[]; used=set()
    for _ in range(200):
        if len(pairs)>=count: break
        a=rng.randint(3,max_a); b=rng.randint(1,a-1); r=a-b
        if r not in used and r>0: used.add(r); pairs.append((a,b,r))
    return pairs[:count]


# ─── Section 1: Counting & Number Recognition ────────────────────────────────
def sec1_counting(n, rng, fmt='fill'):
    max_n = min(10 + n*2, 100)
    html = '<ol class="q-list">'
    answers = []

    if fmt == 'picture':
        for qi in range(1, 4):
            count = rng.randint(3, min(20, max_n))
            svg = dot_grid_svg(count)
            opt_html, lbl = mc_options_html(rng, count, lo=1, spread=3)
            html += (f'<li class="question">How many dots?<br>'
                     f'<div class="dot-picture">{svg}</div>{opt_html}</li>')
            answers.append((str(qi), f"{lbl}) {count}"))
        skip = rng.choice([2,5,10]); start = rng.randint(1,3)*skip
        seq = [start+i*skip for i in range(5)]
        opt_html, lbl = mc_options_html(rng, seq[4], lo=0, spread=skip)
        html += (f'<li class="question">Count by {skip}s. What is next?&nbsp; '
                 f'{seq[0]}, {seq[1]}, {seq[2]}, {seq[3]}, ___<br>{opt_html}</li>')
        answers.append(("4", f"{lbl}) {seq[4]}"))
        a = rng.randint(2, min(20,max_n)-1)
        q_html, ans = tf_html(f"The number <strong>{a+1}</strong> comes after <strong>{a}</strong>.", True)
        html += f'<li class="question">{q_html}</li>'
        answers.append(("5", ans))

    elif fmt == 'mc':
        dots_n = rng.randint(3, min(15,max_n))
        opt_html,lbl = mc_options_html(rng, dots_n, lo=1, spread=3)
        html += f'<li class="question">Count the dots:&nbsp; {"● "*dots_n}<br>{opt_html}</li>'
        answers.append(("1", f"{lbl}) {dots_n}"))
        num = rng.randint(5, max(6,min(max_n,30)))
        opt_html,lbl = mc_options_html(rng, num, lo=1, spread=2)
        html += (f'<li class="question">What number is missing?&nbsp; '
                 f'{num-2}, {num-1}, ___, {num+1}<br>{opt_html}</li>')
        answers.append(("2", f"{lbl}) {num}"))
        mid = rng.randint(3, max(4,min(max_n,40)-1))
        opt_html,lbl = mc_options_html(rng, mid-1, lo=0, spread=2)
        html += (f'<li class="question">What number comes <strong>before</strong> '
                 f'<strong>{mid}</strong>?<br>{opt_html}</li>')
        answers.append(("3", f"{lbl}) {mid-1}"))
        skip=rng.choice([2,5,10]); start=rng.randint(1,3)*skip
        seq=[start+i*skip for i in range(4)]
        opt_html,lbl = mc_options_html(rng, seq[3], lo=0, spread=skip)
        html += (f'<li class="question">Count by {skip}s. What comes next?&nbsp; '
                 f'{seq[0]}, {seq[1]}, {seq[2]}, ___<br>{opt_html}</li>')
        answers.append(("4", f"{lbl}) {seq[3]}"))
        nw = rng.randint(1, min(20,max_n)); word = NUM_WORDS.get(nw,str(nw))
        wrongs_w = [NUM_WORDS.get(nw+d,str(nw+d)) for d in [1,-1,2] if (nw+d) in NUM_WORDS and (nw+d)!=nw]
        text_pool = [(word,True)]+[(w,False) for w in wrongs_w[:3]]
        opt_html,lbl = mc_options_html(rng, None, text_options=text_pool)
        html += f'<li class="question">Which word matches <strong>{nw}</strong>?<br>{opt_html}</li>'
        answers.append(("5", f"{lbl}) {word}"))

    elif fmt == 'tf':
        stmts=[]
        a = rng.randint(2,min(18,max_n)-1)
        stmts.append((f"<strong>{a+1}</strong> is greater than <strong>{a}</strong>.", True))
        b = rng.randint(5,min(20,max_n)); wrong_next=b+rng.choice([-1,1,2])
        stmts.append((f"The number after <strong>{b-1}</strong> is <strong>{wrong_next}</strong>.", wrong_next==b))
        odd = rng.choice([1,3,5,7,9,11,13])
        stmts.append((f"<strong>{odd}</strong> is an even number.", False))
        even = rng.choice([2,4,6,8,10,12])
        stmts.append((f"<strong>{even}</strong> is an even number.", True))
        nw = rng.randint(1,min(15,max_n)); word=NUM_WORDS.get(nw,str(nw))
        use_wrong = rng.random()<0.5
        shown = NUM_WORDS.get(nw+(1 if use_wrong else 0), word)
        stmts.append((f"<strong>{nw}</strong> in words is \"{shown}\".", not use_wrong))
        rng.shuffle(stmts)
        for qi,(stmt,is_true) in enumerate(stmts[:5],1):
            q_html,ans = tf_html(stmt,is_true)
            html += f'<li class="question">{q_html}</li>'
            answers.append((str(qi), ans))

    else:  # fill
        dots_n = rng.randint(3,min(15,max_n))
        html += (f'<li class="question">Count and write the number:&nbsp; {"● "*dots_n}<br>'
                 f'Answer: <span class="blank"></span></li>')
        answers.append(("1", str(dots_n)))
        start=rng.randint(1,max(2,max_n-9)); seq=list(range(start,start+10))
        hidden=sorted(rng.sample(range(10),3))
        parts=[("___" if i in hidden else str(v)) for i,v in enumerate(seq)]
        html += f'<li class="question">Fill in the missing numbers: {", ".join(parts)}</li>'
        answers.append(("2", ", ".join(str(seq[i]) for i in hidden)))
        mid=rng.randint(2,max(3,min(max_n,50)-1))
        html += (f'<li class="question">Write the number <strong>before</strong> and <strong>after</strong>: '
                 f'<span class="blank"></span> , {mid} , <span class="blank"></span></li>')
        answers.append(("3", f"{mid-1} and {mid+1}"))
        skip=rng.choice([2,5,10]); s_start=rng.randint(1,3)*skip
        s_seq=[s_start+i*skip for i in range(6)]; s_hidden=[1,3,5]
        s_parts=[("___" if i in s_hidden else str(v)) for i,v in enumerate(s_seq)]
        html += f'<li class="question">Count by {skip}s. Fill in the blanks: {", ".join(s_parts)}</li>'
        answers.append(("4", ", ".join(str(s_seq[i]) for i in s_hidden)))
        nw=rng.randint(1,min(20,max_n)); word=NUM_WORDS.get(nw,str(nw))
        html += (f'<li class="question">Write the number in words: <strong>{nw}</strong> = '
                 f'<span class="wide-blank"></span></li>')
        answers.append(("5", word))

    html += '</ol>'
    return html, answers


# ─── Section 2: Addition ─────────────────────────────────────────────────────
def sec2_addition(n, rng, fmt='fill'):
    max_a=min(5+n,50); max_b=min(5+n,30)
    html='<ol class="q-list">'; answers=[]

    if fmt == 'mc':
        for i in range(1,6):
            a=rng.randint(1,max_a); b=rng.randint(1,max_b); s=a+b
            opt_html,lbl = mc_options_html(rng,s,lo=1,spread=4)
            html += f'<li class="question">{a} + {b} = ?<br>{opt_html}</li>'
            answers.append((str(i),f"{lbl}) {s}"))
        c=rng.randint(2,max_a); d=rng.randint(1,max_b)
        html += f'<li class="question">Fill in the blank: {c} + <span class="blank"></span> = {c+d}</li>'
        answers.append(("6",str(d)))

    elif fmt == 'match':
        pairs=_unique_add_pairs(rng,max_a,max_b,4)
        m_html,m_ans=match_html(rng,[(f"{a} + {b}",s) for a,b,s in pairs])
        html += f'<li class="question">{m_html}</li>'
        for num,lbl in m_ans:
            a,b,s=pairs[int(num)-1]; answers.append((num,f"{lbl} ({s})"))
        for i in range(5,7):
            a=rng.randint(1,max_a); b=rng.randint(1,max_b)
            html += f'<li class="question">{a} + {b} = <span class="blank"></span></li>'
            answers.append((str(i),str(a+b)))

    elif fmt == 'tf':
        stmts=[]; corrects=0
        for _ in range(20):
            if len(stmts)>=6: break
            a=rng.randint(1,min(max_a,15)); b=rng.randint(1,min(max_b,10)); s=a+b
            if corrects<3 or rng.random()<0.5:
                stmts.append((f"{a} + {b} = <strong>{s}</strong>",True)); corrects+=1
            else:
                w=s+rng.choice([-2,-1,1,2,3])
                if w>0: stmts.append((f"{a} + {b} = <strong>{w}</strong>",False))
        rng.shuffle(stmts)
        for qi,(stmt,is_true) in enumerate(stmts[:6],1):
            q_html,ans=tf_html(stmt,is_true)
            html += f'<li class="question">{q_html}</li>'
            answers.append((str(qi),ans))

    else:  # fill
        for i in range(1,6):
            a=rng.randint(1,max_a); b=rng.randint(1,max_b)
            html += f'<li class="question">{a} + {b} = <span class="blank"></span></li>'
            answers.append((str(i),str(a+b)))
        c=rng.randint(2,max_a); d=rng.randint(1,max_b)
        html += f'<li class="question">Fill in the blank: {c} + <span class="blank"></span> = {c+d}</li>'
        answers.append(("6",str(d)))

    html += '</ol>'
    return html, answers


# ─── Section 3: Subtraction ──────────────────────────────────────────────────
def sec3_subtraction(n, rng, fmt='fill'):
    max_a=min(8+n,60)
    html='<ol class="q-list">'; answers=[]

    if fmt == 'mc':
        for i in range(1,6):
            a=rng.randint(3,max_a); b=rng.randint(1,a-1); r=a-b
            opt_html,lbl=mc_options_html(rng,r,lo=0,spread=4)
            html += f'<li class="question">{a} − {b} = ?<br>{opt_html}</li>'
            answers.append((str(i),f"{lbl}) {r}"))
        a=rng.randint(5,max_a); b=rng.randint(1,a-1)
        html += f'<li class="question">Fill in the blank: {a} − <span class="blank"></span> = {a-b}</li>'
        answers.append(("6",str(b)))

    elif fmt == 'match':
        pairs=_unique_sub_pairs(rng,max_a,4)
        m_html,m_ans=match_html(rng,[(f"{a} − {b}",r) for a,b,r in pairs])
        html += f'<li class="question">{m_html}</li>'
        for num,lbl in m_ans:
            a,b,r=pairs[int(num)-1]; answers.append((num,f"{lbl} ({r})"))
        for i in range(5,7):
            a=rng.randint(3,max_a); b=rng.randint(1,a-1)
            html += f'<li class="question">{a} − {b} = <span class="blank"></span></li>'
            answers.append((str(i),str(a-b)))

    elif fmt == 'tf':
        stmts=[]; corrects=0
        for _ in range(20):
            if len(stmts)>=6: break
            a=rng.randint(3,min(max_a,20)); b=rng.randint(1,a-1); r=a-b
            if corrects<3 or rng.random()<0.5:
                stmts.append((f"{a} − {b} = <strong>{r}</strong>",True)); corrects+=1
            else:
                w=r+rng.choice([-2,-1,1,2])
                if w>=0: stmts.append((f"{a} − {b} = <strong>{w}</strong>",False))
        rng.shuffle(stmts)
        for qi,(stmt,is_true) in enumerate(stmts[:6],1):
            q_html,ans=tf_html(stmt,is_true)
            html += f'<li class="question">{q_html}</li>'
            answers.append((str(qi),ans))

    else:  # fill
        for i in range(1,6):
            a=rng.randint(3,max_a); b=rng.randint(1,a-1)
            html += f'<li class="question">{a} − {b} = <span class="blank"></span></li>'
            answers.append((str(i),str(a-b)))
        a=rng.randint(5,max_a); b=rng.randint(1,a-1)
        html += f'<li class="question">Fill in the blank: {a} − <span class="blank"></span> = {a-b}</li>'
        answers.append(("6",str(b)))

    html += '</ol>'
    return html, answers


# ─── Section 4a: Comparing Numbers & Order ───────────────────────────────────
def sec4_comparing(n, rng, fmt='fill'):
    max_n=min(10+n*2,100)
    html='<ol class="q-list">'; answers=[]

    if fmt == 'mc':
        for i in range(1,4):
            x=rng.randint(1,max_n); y=rng.randint(1,max_n)
            correct_sym = ">" if x>y else ("<" if x<y else "=")
            text_pool=[(s, s==correct_sym) for s in [">","<","=","≠"]]
            opt_html,lbl=mc_options_html(rng,None,text_options=text_pool)
            html += (f'<li class="question">Which symbol belongs in the blank?&nbsp; '
                     f'{x} ___ {y}<br>{opt_html}</li>')
            answers.append((str(i),f"{lbl}) {correct_sym}"))
        pool4=[rng.randint(1,max_n) for _ in range(5)]; greatest=max(pool4)
        opt_html,lbl=mc_options_html(rng,greatest,lo=1,spread=5)
        html += (f'<li class="question">Which is the greatest?&nbsp; '
                 f'{", ".join(map(str,pool4))}<br>{opt_html}</li>')
        answers.append(("4",f"{lbl}) {greatest}"))
        num5=rng.randint(1,min(20,max_n)); correct5="even" if num5%2==0 else "odd"
        text5=[("even",num5%2==0),("odd",num5%2!=0),("neither",False),("both",False)]
        opt_html,lbl=mc_options_html(rng,None,text_options=text5)
        html += f'<li class="question">Is <strong>{num5}</strong> even or odd?<br>{opt_html}</li>'
        answers.append(("5",f"{lbl}) {correct5}"))

    elif fmt == 'tf':
        stmts=[]
        for _ in range(20):
            if len(stmts)>=5: break
            x=rng.randint(1,min(max_n,30)); y=rng.randint(1,min(max_n,30))
            ch=rng.randint(0,2)
            if ch==0: stmts.append((f"<strong>{x}</strong> &gt; <strong>{y}</strong>",x>y))
            elif ch==1: stmts.append((f"<strong>{x}</strong> &lt; <strong>{y}</strong>",x<y))
            else:
                num=rng.randint(2,min(max_n,20))
                stmts.append((f"<strong>{num}</strong> is an even number.", num%2==0))
        rng.shuffle(stmts)
        for qi,(stmt,is_true) in enumerate(stmts[:5],1):
            q_html,ans=tf_html(stmt,is_true)
            html += f'<li class="question">{q_html}</li>'
            answers.append((str(qi),ans))

    else:  # fill
        pairs=[(rng.randint(1,max_n),rng.randint(1,max_n)) for _ in range(3)]
        cmp_html="Fill in &gt;, &lt;, or =:<br>"
        for i,(x,y) in enumerate(pairs):
            lbl=chr(ord('a')+i); sym=(">" if x>y else ("<" if x<y else "="))
            cmp_html+=f"&nbsp;&nbsp;{lbl}) {x} <span class='blank'></span> {y}<br>"
            answers.append((f"1{lbl}",sym))
        html += f'<li class="question">{cmp_html}</li>'
        nums=list({rng.randint(1,max_n) for _ in range(10)})[:5]
        while len(nums)<5: nums.append(rng.randint(1,max_n))
        html += (f'<li class="question">Order from <strong>smallest to largest</strong>: '
                 f'{", ".join(map(str,nums))}<br><span class="wide-blank"></span></li>')
        answers.append(("2",", ".join(map(str,sorted(nums)))))
        pool=[rng.randint(1,max_n) for _ in range(5)]
        html += (f'<li class="question">Which number is greatest: '
                 f'{", ".join(map(str,pool))}? <span class="blank"></span></li>')
        answers.append(("3",str(max(pool))))
        pool2=sorted(rng.sample(range(1,min(31,max_n+1)),6))
        evens=[x for x in pool2 if x%2==0]
        html += (f'<li class="question">Circle the <strong>even</strong> numbers:&nbsp; '
                 f'{" &nbsp; ".join(map(str,pool2))}</li>')
        answers.append(("4",", ".join(map(str,evens)) if evens else "none"))

    html += '</ol>'
    return html, answers


# ─── Section 5: Word Problems ─────────────────────────────────────────────────
def sec5_word_problems(n, rng, fmt='fill'):
    max_a=min(5+n,40); html='<ol class="q-list">'; answers=[]; used=set()
    for i in range(5):
        for _ in range(50):
            tidx=rng.randint(0,len(WP_TEMPLATES)-1)
            if tidx not in used: used.add(tidx); break
        tmpl=WP_TEMPLATES[tidx]
        a=rng.randint(3,max_a); b=rng.randint(1,min(a-1,max_a//2))
        try:
            qtext,ans_val,unit=tmpl(a,b)
            if isinstance(ans_val,int) and ans_val<=0: qtext,ans_val,unit=tmpl(b+4,b)
        except Exception: qtext,ans_val,unit=WP_TEMPLATES[0](a,b)
        if fmt=='mc' and isinstance(ans_val,int):
            opt_html,lbl=mc_options_html(rng,ans_val,lo=0,spread=3)
            html += f'<li class="question">{qtext}<br>{opt_html}</li>'
            answers.append((str(i+1),f"{lbl}) {ans_val} {unit}"))
        else:
            html += f'<li class="question">{qtext}<br>Answer: <span class="blank"></span> {unit}</li>'
            answers.append((str(i+1),f"{ans_val} {unit}"))
    html += '</ol>'
    return html, answers


# ─── Section 6a: Shapes & Measurement ────────────────────────────────────────
def sec6_shapes(n, rng, fmt='fill'):
    shape_names=list(SHAPES.keys()); chosen=rng.sample(shape_names,4)
    html='<ol class="q-list">'; answers=[]

    if fmt == 'match':
        shuffled_names=chosen[:]; rng.shuffle(shuffled_names)
        right_labeled=list(zip(['A','B','C','D'],shuffled_names))
        left_col=''.join(f'<div class="match-item"><span class="match-blank"></span>{i+1}. &nbsp;{SHAPES[s]}</div>' for i,s in enumerate(chosen))
        right_col=''.join(f'<div class="match-item">{lbl}. {name}</div>' for lbl,name in right_labeled)
        instr='<p class="match-instructions">Match each shape to its name:</p>'
        html += (f'<li class="question">{instr}'
                 f'<div class="matching"><div class="match-col">{left_col}</div>'
                 f'<div class="match-col">{right_col}</div></div></li>')
        for i,s in enumerate(chosen):
            for lbl,name in right_labeled:
                if name==s: answers.append((str(i+1),f"{lbl}) {s}")); break

    elif fmt == 'mc':
        html += '<li class="question">Name each shape:</li></ol>'
        html += '<div class="visual-row">'
        for s in chosen: html += f'<div class="visual-item">{SHAPES[s]}<br>Shape: <span class="blank"></span></div>'
        html += '</div>'
        answers.append(("Shapes",", ".join(chosen)))
        html += '<ol class="q-list" start="2">'
        s_sides=[c for c in chosen if SHAPE_SIDES[c]>0]
        s=rng.choice(s_sides) if s_sides else chosen[0]; sides=SHAPE_SIDES[s]
        if sides>0:
            opt_html,lbl=mc_options_html(rng,sides,lo=0,spread=2)
            html += f'<li class="question">How many sides does a <strong>{s}</strong> have?<br>{opt_html}</li>'
            answers.append(("Q2",f"{lbl}) {sides}"))
        else:
            html += f'<li class="question">Does a <strong>{s}</strong> have straight sides? <span class="blank"></span></li>'
            answers.append(("Q2","No"))

    else:  # fill
        html += '<li class="question">Name each shape:</li></ol>'
        html += '<div class="visual-row">'
        for s in chosen: html += f'<div class="visual-item">{SHAPES[s]}<br>Shape: <span class="blank"></span></div>'
        html += '</div>'
        answers.append(("Shapes",", ".join(chosen)))
        html += '<ol class="q-list" start="2">'
        s_sides=[c for c in chosen if SHAPE_SIDES[c]>0]
        s=rng.choice(s_sides) if s_sides else chosen[0]
        html += f'<li class="question">How many sides does a <strong>{s}</strong> have? <span class="blank"></span></li>'
        answers.append(("Q2",str(SHAPE_SIDES[s])))

    l1=rng.randint(12,60); l2=rng.randint(1,l1-1)
    obj1=rng.choice(["pencil","ruler","straw","ribbon","rope","stick"])
    obj2=rng.choice(["crayon","pen","chopstick","string","wire","twig"])
    html += f'<li class="question">Which is longer? Circle:&nbsp; A {obj1} ({l1} cm) &nbsp;or&nbsp; A {obj2} ({l2} cm)?</li>'
    answers.append(("Q3",f"{obj1} ({l1} cm)"))
    w1=rng.randint(2,10); g2=rng.randint(100,w1*1000-100)
    obj3=rng.choice(["watermelon","pumpkin","bag of rice","rock","book"])
    obj4=rng.choice(["apple","orange","banana","egg","eraser"])
    html += f'<li class="question">Which is heavier? Circle:&nbsp; A {obj3} ({w1} kg) &nbsp;or&nbsp; A {obj4} ({g2} g)?</li>'
    answers.append(("Q4",f"{obj3} ({w1} kg)"))
    html += '</ol>'
    return html, answers


# ─── Section 6b: Place Value (Lessons 31+) ───────────────────────────────────
def sec_place_value(n, rng, fmt='fill'):
    max_num=min(10+n*2,99); html='<ol class="q-list">'; answers=[]

    if fmt == 'mc':
        for i in range(1,4):
            num=rng.randint(11,max_num); tens=num//10; ones=num%10
            opt_html,lbl=mc_options_html(rng,tens,lo=0,spread=2)
            html += (f'<li class="question">How many <strong>tens</strong> are in <strong>{num}</strong>?<br>'
                     f'{opt_html}</li>')
            answers.append((str(i),f"{lbl}) {tens}"))
        for i in range(4,6):
            t=rng.randint(1,9); o=rng.randint(0,9); num=t*10+o
            opt_html,lbl=mc_options_html(rng,num,lo=10,spread=5)
            html += f'<li class="question"><strong>{t} tens</strong> and <strong>{o} ones</strong> = ?<br>{opt_html}</li>'
            answers.append((str(i),f"{lbl}) {num}"))

    elif fmt == 'tf':
        stmts=[]
        for _ in range(20):
            if len(stmts)>=5: break
            num=rng.randint(11,max_num); tens=num//10; ones=num%10
            use_wrong=rng.random()<0.5
            shown_tens=tens+(rng.choice([-1,1]) if use_wrong else 0)
            if shown_tens>0:
                stmts.append((
                    f"<strong>{num}</strong> has <strong>{shown_tens} tens</strong> and <strong>{ones} ones</strong>.",
                    not use_wrong
                ))
        rng.shuffle(stmts)
        for qi,(stmt,is_true) in enumerate(stmts[:5],1):
            q_html,ans=tf_html(stmt,is_true)
            html += f'<li class="question">{q_html}</li>'
            answers.append((str(qi),ans))

    else:  # fill
        for i in range(1,4):
            num=rng.randint(11,max_num); tens=num//10; ones=num%10
            html += (f'<li class="question"><strong>{num}</strong> = '
                     f'<span class="blank"></span> tens and <span class="blank"></span> ones</li>')
            answers.append((str(i),f"{tens} tens, {ones} ones"))
        for i in range(4,6):
            t=rng.randint(1,9); o=rng.randint(0,9); num=t*10+o
            html += f'<li class="question"><strong>{t} tens</strong> and <strong>{o} ones</strong> = <span class="blank"></span></li>'
            answers.append((str(i),str(num)))

    html += '</ol>'
    return html, answers


# ─── Section 7a: Telling Time (Lessons 1-40) ─────────────────────────────────
def sec7_time(n, rng, fmt='fill'):
    if n<20: allowed=[0]
    elif n<40: allowed=[0,30]
    else: allowed=[0,15,30,45]
    clock_times=[]; used=set()
    for _ in range(100):
        if len(clock_times)>=3: break
        h=rng.randint(1,12); m=rng.choice(allowed)
        if (h,m) not in used: used.add((h,m)); clock_times.append((h,m))

    answers=[]; labels_clk=["A","B","C"]
    if fmt == 'mc':
        html='<ol class="q-list"><li class="question">What time does each clock show?</li></ol>'
        html += '<div class="visual-row">'
        for i,(h,m) in enumerate(clock_times):
            svg,fmt_str=clock_svg(h,m)
            wrong_h=(h%12)+1
            pool=[(fmt_str,True),(f"{wrong_h}:{m:02d}",False),
                  (f"{h}:{(m+30)%60:02d}",False),(f"{(h%12)+2}:{m:02d}",False)]
            rng.shuffle(pool)
            correct_lbl=None
            opts='<div class="mc-options">'
            for j,(val,is_c) in enumerate(pool[:4]):
                lbl=['A','B','C','D'][j]
                if is_c: correct_lbl=lbl
                opts += f'<span class="mc-opt">{lbl}) {val}</span>'
            opts += '</div>'
            html += f'<div class="visual-item">{svg}<strong>Clock {labels_clk[i]}:</strong><br>{opts}</div>'
            answers.append((f"Clock {labels_clk[i]}",f"{correct_lbl}) {fmt_str}"))
        html += '</div>'
        start_h=rng.randint(6,10); add_h=rng.randint(1,4)
        opt_html,lbl=mc_options_html(rng,start_h+add_h,lo=1,spread=2)
        html += (f'<ol class="q-list" start="2"><li class="question">School starts at <strong>{start_h}:00</strong>. '
                 f'After <strong>{add_h} hour{"s" if add_h>1 else ""}</strong>, what time is it?<br>'
                 f'{opt_html}</li></ol>')
        answers.append(("Q2",f"{lbl}) {start_h+add_h}:00"))
    else:  # fill
        html='<ol class="q-list"><li class="question">Write the time shown on each clock:</li></ol>'
        html += '<div class="visual-row">'
        for i,(h,m) in enumerate(clock_times):
            svg,fmt_str=clock_svg(h,m)
            html += f'<div class="visual-item">{svg}<strong>Clock {labels_clk[i]}:</strong> <span class="blank"></span></div>'
            answers.append((f"Clock {labels_clk[i]}",fmt_str))
        html += '</div>'
        start_h=rng.randint(6,10); add_h=rng.randint(1,4)
        html += (f'<ol class="q-list" start="2"><li class="question">School starts at <strong>{start_h}:00</strong>. '
                 f'After <strong>{add_h} hour{"s" if add_h>1 else ""}</strong>, what time is it? '
                 f'<span class="blank"></span></li></ol>')
        answers.append(("Q2",f"{start_h+add_h}:00"))
    return html, answers


# ─── Section 7b: Number Patterns (Lessons 41+) ───────────────────────────────
def sec_patterns(n, rng, fmt='fill'):
    html='<ol class="q-list">'; answers=[]
    step_choices=[1,2,3,5] if n<=60 else [2,3,4,5,10]

    def make_seq(start,step,length=6): return [start+i*step for i in range(length)]

    if fmt == 'mc':
        for i in range(1,6):
            step=rng.choice(step_choices); start=rng.randint(1,10)
            seq=make_seq(start,step,5); nxt=seq[-1]+step
            opt_html,lbl=mc_options_html(rng,nxt,lo=0,spread=step+1)
            html += (f'<li class="question">What comes next?&nbsp; '
                     f'{", ".join(map(str,seq))}, ___<br>{opt_html}</li>')
            answers.append((str(i),f"{lbl}) {nxt}"))

    elif fmt == 'tf':
        stmts=[]
        for _ in range(20):
            if len(stmts)>=5: break
            step=rng.choice(step_choices); start=rng.randint(1,8)
            seq=make_seq(start,step,5); use_wrong=rng.random()<0.5
            shown_nxt=seq[-1]+(step+(rng.choice([-1,1,2]) if use_wrong else 0))
            seq_str=", ".join(map(str,seq))
            stmts.append((f"The next number in <strong>{seq_str}</strong> is <strong>{shown_nxt}</strong>.", not use_wrong))
        rng.shuffle(stmts)
        for qi,(stmt,is_true) in enumerate(stmts[:5],1):
            q_html,ans=tf_html(stmt,is_true)
            html += f'<li class="question">{q_html}</li>'
            answers.append((str(qi),ans))

    elif fmt == 'match':
        pattern_rules=[]; used_steps=set()
        for _ in range(50):
            if len(pattern_rules)>=4: break
            step=rng.choice(step_choices)
            if step in used_steps: continue
            used_steps.add(step); start=rng.randint(1,5)
            seq=make_seq(start,step,4)
            pattern_rules.append((", ".join(map(str,seq))+" ...", f"Add {step} each time"))
        if len(pattern_rules)>=4:
            m_html,m_ans=match_html(rng,pattern_rules[:4],"Match each pattern to its rule:")
            html += f'<li class="question">{m_html}</li>'
            for num,lbl in m_ans:
                _,rule=pattern_rules[int(num)-1]; answers.append((num,f"{lbl}) {rule}"))
        step=rng.choice(step_choices); start=rng.randint(1,8)
        seq=make_seq(start,step,6); hidden_i=rng.randint(1,4)
        parts=[("___" if i==hidden_i else str(v)) for i,v in enumerate(seq)]
        html += f'<li class="question">Fill in the missing number:&nbsp; {", ".join(parts)}</li>'
        answers.append(("5",str(seq[hidden_i])))

    else:  # fill
        for i in range(1,6):
            step=rng.choice(step_choices); start=rng.randint(1,10)
            seq=make_seq(start,step,6); hidden_i=rng.randint(1,4)
            parts=[("___" if j==hidden_i else str(v)) for j,v in enumerate(seq)]
            html += f'<li class="question">Fill in the missing number:&nbsp; {", ".join(parts)}</li>'
            answers.append((str(i),str(seq[hidden_i])))

    html += '</ol>'
    return html, answers


# ─── Section 4b: Multiplication (Lessons 71+) ────────────────────────────────
def sec_multiplication(n, rng, fmt='fill'):
    if n<=80: tables=[2,3]
    elif n<=90: tables=[2,3,4]
    else: tables=[2,3,4,5]
    html='<ol class="q-list">'; answers=[]

    if fmt == 'mc':
        for i in range(1,6):
            t=rng.choice(tables); b=rng.randint(1,10); product=t*b
            opt_html,lbl=mc_options_html(rng,product,lo=0,spread=t)
            html += f'<li class="question">{t} × {b} = ?<br>{opt_html}</li>'
            answers.append((str(i),f"{lbl}) {product}"))
        t=rng.choice(tables); b=rng.randint(2,5); product=t*b
        html += (f'<li class="question">Fill in: {" + ".join([str(t)]*b)} = '
                 f'{t} × <span class="blank"></span> = <span class="blank"></span></li>')
        answers.append(("6",f"{b}, {product}"))

    elif fmt == 'match':
        prods=[]; used_p=set()
        for _ in range(100):
            if len(prods)>=4: break
            t=rng.choice(tables); b=rng.randint(1,8); p=t*b
            if p not in used_p: used_p.add(p); prods.append((t,b,p))
        m_html,m_ans=match_html(rng,[(f"{t} × {b}",p) for t,b,p in prods])
        html += f'<li class="question">{m_html}</li>'
        for num,lbl in m_ans:
            t,b,p=prods[int(num)-1]; answers.append((num,f"{lbl} ({p})"))
        for i in range(5,7):
            t=rng.choice(tables); b=rng.randint(1,10)
            html += f'<li class="question">{t} × {b} = <span class="blank"></span></li>'
            answers.append((str(i),str(t*b)))

    elif fmt == 'tf':
        stmts=[]; corrects=0
        for _ in range(30):
            if len(stmts)>=6: break
            t=rng.choice(tables); b=rng.randint(1,8); p=t*b
            if corrects<3 or rng.random()<0.5:
                stmts.append((f"{t} × {b} = <strong>{p}</strong>",True)); corrects+=1
            else:
                w=p+rng.choice([-t,t,t*2,-1,1])
                if w>0: stmts.append((f"{t} × {b} = <strong>{w}</strong>",False))
        rng.shuffle(stmts)
        for qi,(stmt,is_true) in enumerate(stmts[:6],1):
            q_html,ans=tf_html(stmt,is_true)
            html += f'<li class="question">{q_html}</li>'
            answers.append((str(qi),ans))

    else:  # fill
        for i in range(1,6):
            t=rng.choice(tables); b=rng.randint(1,10)
            html += f'<li class="question">{t} × {b} = <span class="blank"></span></li>'
            answers.append((str(i),str(t*b)))
        t=rng.choice(tables); b=rng.randint(2,5); product=t*b
        html += (f'<li class="question">Fill in: {" + ".join([str(t)]*b)} = '
                 f'{t} × <span class="blank"></span> = <span class="blank"></span></li>')
        answers.append(("6",f"{b}, {product}"))

    html += '</ol>'
    return html, answers


# ─── Bonus ────────────────────────────────────────────────────────────────────
def sec_bonus(n, rng):
    max_n=min(5+n,40)
    a=rng.randint(2,max_n); b=rng.randint(1,max_n); c=rng.randint(1,min(a+b-1,max_n))
    ans1=a+b-c
    while ans1<=0: c-=1; ans1=a+b-c
    x=rng.randint(3,max_n); give=rng.randint(1,x-1); get=rng.randint(1,max_n//2)
    step=rng.choice([1,2,3,5]); sp=rng.randint(1,6)
    seq_p=[sp+i*step for i in range(6)]; hidden_i=rng.randint(1,4)
    parts_p=[("___" if i==hidden_i else str(v)) for i,v in enumerate(seq_p)]
    html = f"""<ol class="q-list">
  <li class="question">{a} + {b} − {c} = <span class='blank'></span></li>
  <li class="question">Tuan has <strong>{x}</strong> stickers. Gives <strong>{give}</strong> to a friend, then receives <strong>{get}</strong> from his sister. How many does he have now? <span class='blank'></span></li>
  <li class="question">Fill in the blank: {", ".join(parts_p)} <span class='blank'></span></li>
</ol>"""
    return html, [("1",str(ans1)),("2",str(x-give+get)),("3",str(seq_p[hidden_i]))]


# ─── Answer key table ─────────────────────────────────────────────────────────
def build_answer_table(sections):
    rows='<tr><th>#</th><th>Answer</th><th>#</th><th>Answer</th><th>#</th><th>Answer</th></tr>\n'
    for label,pairs in sections:
        rows+=(f'<tr><td colspan="6" style="background:#dce8f5;font-weight:bold;'
               f'text-align:left;padding-left:12px;">{label}</td></tr>\n')
        for i in range(0,len(pairs),3):
            chunk=pairs[i:i+3]
            while len(chunk)<3: chunk.append(("",""))
            cells="".join(f"<td>{q}</td><td>{a}</td>" for q,a in chunk)
            rows+=f"<tr>{cells}</tr>\n"
    return f'<table class="answer-key">{rows}</table>'


# ─── Main lesson builder ──────────────────────────────────────────────────────
def build_lesson(n):
    rng=random.Random(n*9973+31337)

    if n<=40:
        s4_key,s4_label,s4_fn = 'comparing','Comparing Numbers &amp; Order',sec4_comparing
        s6_key,s6_label,s6_fn = 'shapes',   'Shapes &amp; Measurement',    sec6_shapes
        s7_key,s7_label,s7_fn = 'time',     'Telling Time',                sec7_time
    elif n<=70:
        s4_key,s4_label,s4_fn = 'comparing','Comparing Numbers &amp; Order',sec4_comparing
        s6_key,s6_label,s6_fn = 'place',    'Place Value',                  sec_place_value
        s7_key,s7_label,s7_fn = 'patterns', 'Number Patterns',              sec_patterns
    else:
        s4_key,s4_label,s4_fn = 'multiply', 'Multiplication',               sec_multiplication
        s6_key,s6_label,s6_fn = 'place',    'Place Value',                  sec_place_value
        s7_key,s7_label,s7_fn = 'patterns', 'Number Patterns',              sec_patterns

    f1=section_fmt(n,'counting'); f2=section_fmt(n,'addition')
    f3=section_fmt(n,'subtraction'); f4=section_fmt(n,s4_key)
    f5=section_fmt(n,'word'); f6=section_fmt(n,s6_key); f7=section_fmt(n,s7_key)

    s1_html,s1_ans = sec1_counting(n,rng,f1)
    s2_html,s2_ans = sec2_addition(n,rng,f2)
    s3_html,s3_ans = sec3_subtraction(n,rng,f3)
    s4_html,s4_ans = s4_fn(n,rng,f4)
    s5_html,s5_ans = sec5_word_problems(n,rng,f5)
    s6_html,s6_ans = s6_fn(n,rng,f6)
    s7_html,s7_ans = s7_fn(n,rng,f7)
    sb_html,sb_ans = sec_bonus(n,rng)

    fmt_badge={'fill':'✏️ Fill-in','mc':'🔘 Multiple Choice','tf':'✅ True/False',
               'match':'🔗 Matching','picture':'🖼️ Picture'}
    section_labels=['Counting &amp; Number Recognition','Addition','Subtraction',
                    s4_label,'Word Problems',s6_label,s7_label]
    sections_content=[s1_html,s2_html,s3_html,s4_html,s5_html,s6_html,s7_html]
    time_alloc=[10,15,15,10,20,10,10]
    fmts=[f1,f2,f3,f4,f5,f6,f7]

    body_html=(f'<h1>🧠 Grade 1 Math – 90 Minute Test (Lesson {n})</h1>\n'
               f'<div class="meta">Total: 40 points &nbsp;|&nbsp; Time: 90 minutes</div>\n'
               f'<div class="name-line">\n  <span>Name:</span><span class="line"></span>\n'
               f'  <span>Date:</span><span class="line"></span>\n</div>\n')

    for i,(lbl,content,t,fmt) in enumerate(zip(section_labels,sections_content,time_alloc,fmts)):
        badge=fmt_badge.get(fmt,'')
        body_html+=(f'<div class="section-header">⏱ Section {i+1}: {lbl} ({t} mins) '
                    f'&nbsp;<small style="font-weight:normal;opacity:.8">{badge}</small></div>\n{content}\n')

    body_html+=f'<div class="bonus">⏱ Bonus Challenge (5 mins)</div>\n{sb_html}\n'

    ans_sections=[
        ('Section 1: Counting &amp; Number Recognition',s1_ans),
        ('Section 2: Addition',s2_ans),
        ('Section 3: Subtraction',s3_ans),
        (f'Section 4: {s4_label}',s4_ans),
        ('Section 5: Word Problems',s5_ans),
        (f'Section 6: {s6_label}',s6_ans),
        (f'Section 7: {s7_label}',s7_ans),
        ('Bonus Challenge',sb_ans),
    ]
    ans_table=build_answer_table(ans_sections)
    body_html+=(f'<hr class="before-answer"/>\n<div class="answer-section">\n'
                f'<div class="answer-header">✅ Answer Key — Lesson {n} (Grade 1, 90 Minute Test)</div>\n'
                f'{ans_table}\n</div>')

    return (f'<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            f'  <meta charset="UTF-8" />\n'
            f'  <meta name="viewport" content="width=device-width, initial-scale=1.0" />\n'
            f'  <title>Grade 1 Math – 90 Minute Test (Lesson {n})</title>\n'
            f'  <style>{CSS}</style>\n</head>\n<body>\n{body_html}\n</body>\n</html>')


# ─── Run ─────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    for n in range(2, 101):
        html = build_lesson(n)
        path = os.path.join(OUTDIR, f"Lesson {n} - Grade 1 Math Theory.html")
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  ✓ Lesson {n}")
    print(f"\nDone. 99 lessons saved to:\n  {OUTDIR}")
