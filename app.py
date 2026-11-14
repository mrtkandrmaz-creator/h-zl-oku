"""HızlıOku ⚡ — Duolingo tarzı, kademeli hızlı okuma eğitimi (Streamlit)."""

import math
import random
import re
import time

import streamlit as st
import streamlit.components.v1 as components

from content import LEVELS, PASSAGES

MAX_HEARTS = 5
PASS_SCORE = 2          # 3 sorudan en az 2 doğru
XP_PER_LEVEL = 100      # her 100 XP = 1 seviye
STAGE_ORDER = ["lesson", "exercise", "quiz", "result"]
STAGE_LABELS = ["Ders", "Egzersiz", "Test", "Sonuç"]

st.set_page_config(page_title="HızlıOku • Hızlı Okuma Akademisi", page_icon="⚡", layout="centered")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
html, body, [class*="css"] {font-family: 'Inter', sans-serif;}

/* Üst başlık */
.hero {background: linear-gradient(135deg,#7C5CFF 0%,#22D3EE 100%); padding: 1.8rem 1.4rem;
       border-radius: 24px; color: #fff; margin-bottom: 1rem;
       box-shadow: 0 12px 40px rgba(124,92,255,.35);}
.hero h1 {margin: 0; color: #fff; font-size: 2.1rem; font-weight: 800; letter-spacing: -.5px;}
.hero p {margin: .4rem 0 1rem 0; opacity: .95;}
.track {height: 10px; border-radius: 99px; background: rgba(255,255,255,.28); overflow: hidden;}
.track > div {height: 100%; border-radius: 99px; background: #fff;}
.hero-meta {display: flex; justify-content: space-between; font-size: .85rem; margin-top: .45rem; opacity: .95;}

/* İstatistik kartları */
.stats {display: grid; grid-template-columns: repeat(3, 1fr); gap: .75rem; margin-bottom: 1.1rem;}
.stat {border-radius: 18px; padding: .9rem 1rem; background: rgba(124,92,255,.10);
       border: 1px solid rgba(124,92,255,.25);}
.stat .v {font-size: 1.3rem; font-weight: 800;}
.stat .l {font-size: .74rem; opacity: .7; text-transform: uppercase; letter-spacing: .06em;}

/* Kart (border=True container) */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: 20px; border: 1px solid rgba(124,92,255,.22);
    background: rgba(124,92,255,.06); transition: transform .15s ease, box-shadow .15s ease;}
div[data-testid="stVerticalBlockBorderWrapper"]:has(.lvl):hover {
    transform: translateY(-2px); box-shadow: 0 10px 30px rgba(124,92,255,.22);}

/* Kademe kartı */
.lvl {display: flex; gap: .9rem; align-items: center;}
.lvl.is-locked {opacity: .55;}
.bubble {width: 56px; height: 56px; flex: 0 0 56px; border-radius: 18px; display: flex;
         align-items: center; justify-content: center; font-size: 1.7rem;
         background: linear-gradient(135deg,#7C5CFF,#22D3EE); box-shadow: 0 6px 16px rgba(124,92,255,.35);}
.bubble.done {background: linear-gradient(135deg,#10B981,#22D3EE);}
.bubble.locked {background: rgba(128,128,128,.25); box-shadow: none; filter: grayscale(1);}
.lvl-top {display: flex; align-items: center; gap: .5rem; margin-bottom: .15rem;}
.lvl-no {font-size: .72rem; font-weight: 700; letter-spacing: .08em; opacity: .6;}
.chip {font-size: .68rem; font-weight: 700; padding: .12rem .55rem; border-radius: 99px;}
.chip.next {background: rgba(124,92,255,.22); color: #A99BFF;}
.chip.done {background: rgba(16,185,129,.2); color: #34D399;}
.chip.locked {background: rgba(128,128,128,.2);}
.lvl-title {font-size: 1.08rem; font-weight: 700;}
.lvl-sum {font-size: .88rem; opacity: .72;}

/* Butonlar */
.stButton > button, .stDownloadButton > button {border-radius: 14px; font-weight: 600;
    border: 1px solid rgba(124,92,255,.35); transition: all .15s ease;}
.stButton > button[kind="primary"], .stButton > button[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg,#7C5CFF,#22D3EE); border: none; color: #fff;
    box-shadow: 0 6px 18px rgba(124,92,255,.35);}
.stButton > button[kind="primary"]:hover, .stButton > button[data-testid="stBaseButton-primary"]:hover {
    filter: brightness(1.08); transform: translateY(-1px);}

/* Okuma alanları */
.reader {font-size: 1.15rem; line-height: 1.9; padding: 1.3rem 1.5rem; border-radius: 18px;
         background: rgba(124,92,255,.07); border: 1px solid rgba(124,92,255,.2);
         border-left: 5px solid #7C5CFF;}
.flash {font-size: 2.3rem; font-weight: 800; text-align: center; padding: 3.2rem 1rem;
        border-radius: 22px; min-height: 8rem; border: 1px solid rgba(124,92,255,.3);
        background: linear-gradient(135deg, rgba(124,92,255,.18), rgba(34,211,238,.14));
        box-shadow: 0 0 40px rgba(124,92,255,.2) inset;}
.hl {background: linear-gradient(90deg,#7C5CFF,#22D3EE); color: #fff; border-radius: 8px;
     padding: 1px 6px; font-weight: 700;}

/* Sol panel */
section[data-testid="stSidebar"] {background: linear-gradient(180deg, rgba(124,92,255,.14), rgba(34,211,238,.05));}
.sb-card {border-radius: 20px; padding: .9rem 1rem; margin-bottom: .75rem;
          background: rgba(124,92,255,.12); border: 1px solid rgba(124,92,255,.28);}
.sb-head {display: flex; gap: .75rem; align-items: center; margin-bottom: .65rem;}
.sb-emoji {font-size: 1.9rem; width: 52px; height: 52px; flex: 0 0 52px; border-radius: 16px;
           display: flex; align-items: center; justify-content: center;
           background: linear-gradient(135deg,#FFB86C,#FF7AC6);}
.sb-title {font-weight: 800; font-size: 1.05rem;}
.sb-sub {font-size: .8rem; opacity: .78;}
.sb-bar {height: 10px; border-radius: 99px; background: rgba(255,255,255,.12); overflow: hidden;}
.sb-bar > div {height: 100%; border-radius: 99px; background: linear-gradient(90deg,#FFB86C,#FF7AC6,#7C5CFF);}
.sb-hint {font-size: .72rem; opacity: .65; margin-top: .35rem;}
.sb-row {display: grid; grid-template-columns: 1fr 1fr; gap: .6rem; margin-bottom: .75rem;}
.sb-mini {border-radius: 18px; padding: .7rem .8rem; text-align: center;}
.sb-mini .v {font-size: 1.2rem; font-weight: 800;}
.sb-mini .l {font-size: .7rem; opacity: .8; text-transform: uppercase; letter-spacing: .06em;}
.sb-mini.heart {background: linear-gradient(135deg, rgba(255,92,122,.28), rgba(255,122,198,.14));
                border: 1px solid rgba(255,92,122,.38);}
.sb-mini.fire {background: linear-gradient(135deg, rgba(255,184,108,.30), rgba(255,92,92,.14));
               border: 1px solid rgba(255,184,108,.42);}
.dots {display: flex; gap: .4rem; margin: .55rem 0 .2rem 0;}
.dot {flex: 1; height: 10px; border-radius: 99px; background: rgba(255,255,255,.14);}
.dot.done {background: linear-gradient(90deg,#10B981,#22D3EE);}
.dot.now {background: #7C5CFF; box-shadow: 0 0 10px rgba(124,92,255,.8);}
.sb-speed {font-size: 1.5rem; font-weight: 800; margin-top: .2rem;}
.sb-speed small {font-size: .75rem; opacity: .7; font-weight: 600;}
.sb-tip {background: linear-gradient(135deg, rgba(34,211,238,.16), rgba(124,92,255,.14));
         border-color: rgba(34,211,238,.35);}
</style>
"""


# ----------------------------------------------------------------------------
# Yardımcılar
# ----------------------------------------------------------------------------
def init_state():
    defaults = {
        "xp": 0,
        "hearts": MAX_HEARTS,
        "streak": 0,
        "completed": [],
        "baseline_wpm": None,
        "final_wpm": None,
        "view": "map",
        "level_idx": None,
        "stage": "lesson",
        "read_start": None,
        "ex_done": None,
        "wpm_result": None,
        "last_quiz": None,
        "attempt": 0,
    }
    for k, v in defaults.items():
        st.session_state.setdefault(k, v)


def count_words(text):
    return len(text.split())


def clamp(v, lo, hi):
    return max(lo, min(hi, v))


def default_wpm(factor=0.9, lo=120, hi=500):
    base = st.session_state.baseline_wpm or 200
    return int(clamp(round(base * factor / 10) * 10, lo, hi))


def reset_level_state():
    s = st.session_state
    s.stage = "lesson"
    s.read_start = None
    s.ex_done = None
    s.wpm_result = None
    s.last_quiz = None


def start_level(idx):
    s = st.session_state
    s.view = "level"
    s.level_idx = idx
    s.attempt = 0
    reset_level_state()
    st.rerun()


def go_map():
    st.session_state.view = "map"
    st.rerun()


# ----------------------------------------------------------------------------
# Sol panel: saat, rütbe, can, seri, yolculuk
# ----------------------------------------------------------------------------
CLOCK_HTML = """
<div style="font-family:Inter,system-ui,sans-serif;text-align:center;padding:14px 8px;border-radius:22px;
background:linear-gradient(135deg,#FF7AC6 0%,#7C5CFF 55%,#22D3EE 100%);color:#fff;
box-shadow:0 8px 24px rgba(124,92,255,.35)">
  <div id="g" style="font-size:.8rem;opacity:.95;font-weight:600"></div>
  <div id="t" style="font-size:2.1rem;font-weight:800;letter-spacing:2px;line-height:1.25"></div>
  <div id="d" style="font-size:.78rem;opacity:.95"></div>
</div>
<script>
function tick(){
  const n=new Date(), h=n.getHours();
  const g = h<5 ? 'İyi geceler 🌙' : h<12 ? 'Günaydın ☀️' : h<18 ? 'İyi günler 🌤️' : 'İyi akşamlar 🌆';
  document.getElementById('g').textContent=g;
  document.getElementById('t').textContent=n.toLocaleTimeString('tr-TR',{hour:'2-digit',minute:'2-digit',second:'2-digit'});
  document.getElementById('d').textContent=n.toLocaleDateString('tr-TR',{weekday:'long',day:'numeric',month:'long'});
}
tick(); setInterval(tick,1000);
</script>
<style>body{margin:0;background:transparent}</style>
"""

RANKS = [
    (1, "Çaylak Okur", "🐣"),
    (2, "Meraklı Okur", "📖"),
    (3, "Hızlı Gözler", "👀"),
    (4, "Okuma Ninjası", "🥷"),
    (6, "Işık Hızı", "⚡"),
]

TIPS = [
    "Gözlerini rahat bırak: gerginlik hızı düşürür.",
    "Başlığa ve ilk cümleye göz at, konuyu önceden tahmin et.",
    "Geri dönme isteğine direnmek hızın en büyük sırrı.",
    "Her gün 10 dakika düzenli pratik, haftada bir saatten iyidir.",
    "Kelimeleri tek tek değil, öbek öbek yakalamaya çalış.",
    "Okurken parmağınla ritim tutmak iç sesi azaltır.",
    "İyi uyku, iyi anlamanın yarısıdır.",
    "Hız kadar anlama da önemli: ikisini birlikte ölç.",
]


def rank_for(level):
    name, emoji = RANKS[0][1], RANKS[0][2]
    for min_lvl, n, e in RANKS:
        if level >= min_lvl:
            name, emoji = n, e
    return name, emoji


def sidebar():
    s = st.session_state
    done = set(s.completed)
    total = len(LEVELS)
    next_idx = next((i for i, l in enumerate(LEVELS) if l["id"] not in done), total)
    level = 1 + s.xp // XP_PER_LEVEL
    into = s.xp % XP_PER_LEVEL
    rank, rank_emoji = rank_for(level)

    dots = "".join(
        f"<span class='dot {'done' if l['id'] in done else ('now' if i == next_idx else '')}'></span>"
        for i, l in enumerate(LEVELS)
    )
    tip = TIPS[int(time.time() // 86400) % len(TIPS)]

    with st.sidebar:
        components.html(CLOCK_HTML, height=112)

        st.markdown(
            "<div class='sb-card'>"
            "<div class='sb-head'>"
            f"<div class='sb-emoji'>{rank_emoji}</div>"
            f"<div><div class='sb-title'>{rank}</div>"
            f"<div class='sb-sub'>Seviye {level} · {s.xp} XP</div></div></div>"
            f"<div class='sb-bar'><div style='width:{into}%'></div></div>"
            f"<div class='sb-hint'>Sonraki seviyeye {XP_PER_LEVEL - into} XP kaldı</div>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div class='sb-row'>"
            f"<div class='sb-mini heart'><div class='v'>❤️ {s.hearts}/{MAX_HEARTS}</div><div class='l'>Can</div></div>"
            f"<div class='sb-mini fire'><div class='v'>🔥 {s.streak}</div><div class='l'>Seri</div></div>"
            "</div>",
            unsafe_allow_html=True,
        )

        st.markdown(
            "<div class='sb-card'>"
            f"<div class='sb-sub'>🗺️ Yolculuk · {len(done)}/{total} kademe</div>"
            f"<div class='dots'>{dots}</div></div>",
            unsafe_allow_html=True,
        )

        if s.baseline_wpm:
            final_txt = s.final_wpm if s.final_wpm else "?"
            st.markdown(
                "<div class='sb-card'>"
                "<div class='sb-sub'>⚡ Etkili okuma hızın</div>"
                f"<div class='sb-speed'>{s.baseline_wpm} → {final_txt} <small>kelime/dk</small></div>"
                "</div>",
                unsafe_allow_html=True,
            )

        st.markdown(
            "<div class='sb-card sb-tip'>"
            "<div class='sb-sub'>💡 Günün ipucu</div>"
            f"<div style='margin-top:.25rem;font-size:.9rem'>{tip}</div></div>",
            unsafe_allow_html=True,
        )


# ----------------------------------------------------------------------------
# Harita (kademe listesi)
# ----------------------------------------------------------------------------
def map_view():
    s = st.session_state
    done = set(s.completed)
    total = len(LEVELS)
    pct = int(len(done) / total * 100)
    level = 1 + s.xp // XP_PER_LEVEL
    next_idx = next((i for i, l in enumerate(LEVELS) if l["id"] not in done), total)

    st.markdown(
        "<div class='hero'><h1>⚡ HızlıOku</h1>"
        "<p>Adım adım hızlı okuma. Her kademeyi geç, bir sonrakinin kilidini aç.</p>"
        f"<div class='track'><div style='width:{pct}%'></div></div>"
        f"<div class='hero-meta'><span>{len(done)}/{total} kademe</span><span>%{pct}</span></div></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<div class='stats'>"
        f"<div class='stat'><div class='v'>Sv. {level}</div><div class='l'>{s.xp} XP</div></div>"
        f"<div class='stat'><div class='v'>❤️ {s.hearts}/{MAX_HEARTS}</div><div class='l'>Can</div></div>"
        f"<div class='stat'><div class='v'>🔥 {s.streak}</div><div class='l'>Seri</div></div>"
        "</div>",
        unsafe_allow_html=True,
    )

    if next_idx == total:
        st.success("🎉 Tüm kademeleri tamamladın! İstediğin kademeyi tekrar oynayabilirsin.")
        if s.baseline_wpm and s.final_wpm:
            st.metric("Etkili okuma hızın", f"{s.final_wpm} kelime/dk",
                      delta=f"{s.final_wpm - s.baseline_wpm:+d} (başlangıca göre)")

    chips = {"done": "Tamamlandı", "locked": "Kilitli", "next": "Sıradaki"}
    for i, lvl in enumerate(LEVELS):
        is_done = lvl["id"] in done
        locked = i > next_idx
        state = "done" if is_done else ("locked" if locked else "next")
        icon = "🔒" if locked else lvl["emoji"]
        lock_cls = " is-locked" if locked else ""
        with st.container(border=True):
            c1, c2 = st.columns([7, 3], vertical_alignment="center")
            c1.markdown(
                f"<div class='lvl{lock_cls}'>"
                f"<div class='bubble {state}'>{icon}</div>"
                "<div><div class='lvl-top'>"
                f"<span class='lvl-no'>KADEME {i + 1}</span><span class='chip {state}'>{chips[state]}</span></div>"
                f"<div class='lvl-title'>{lvl['title']}</div>"
                f"<div class='lvl-sum'>{lvl['summary']}</div></div></div>",
                unsafe_allow_html=True,
            )
            label = "Tekrar" if is_done else "Başla"
            if c2.button(label, key=f"start_{lvl['id']}", disabled=locked,
                         use_container_width=True, type="primary" if i == next_idx else "secondary"):
                start_level(i)

    st.caption("⚠️ Not: Hız tek başına anlam taşımaz. Skorun, anlama oranınla çarpılarak hesaplanır.")


# ----------------------------------------------------------------------------
# Egzersizler
# ----------------------------------------------------------------------------
def exercise_footer():
    s = st.session_state
    if s.ex_done:
        st.success("Egzersiz tamam! Şimdi anlama testi zamanı.")
        if st.button("Teste geç →", type="primary", key="to_quiz"):
            s.wpm_result = s.ex_done
            s.stage = "quiz"
            st.rerun()


def exercise_timed(lvl, passage):
    """Metni göster, süre tut, kelime/dk hesapla."""
    s = st.session_state
    st.info(lvl["instruction"])
    if s.read_start is None:
        if st.button("▶️ Hazırım, metni göster", type="primary", key="show_text"):
            s.read_start = time.time()
            st.rerun()
        return
    st.markdown(f"<div class='reader'>{passage['text']}</div>", unsafe_allow_html=True)
    if st.button("✅ Bitirdim", type="primary", key="finish_read"):
        elapsed = max(time.time() - s.read_start, 1.0)
        s.wpm_result = round(count_words(passage["text"]) / elapsed * 60)
        s.read_start = None
        s.stage = "quiz"
        st.rerun()


def highlight_html(words, i):
    parts = [f"<span class='hl'>{w}</span>" if j == i else w for j, w in enumerate(words)]
    return "<div class='reader'>" + " ".join(parts) + "</div>"


def exercise_pacer(lvl, passage):
    s = st.session_state
    st.info(lvl["instruction"])
    wpm = st.slider("Hız (kelime/dk)", 120, 500, default_wpm(), 10, key=f"wpm_{lvl['id']}")
    words = passage["text"].split()
    ph = st.empty()
    if st.button("▶️ Başlat", type="primary", key="go"):
        delay = 60.0 / wpm
        for i in range(len(words)):
            ph.markdown(highlight_html(words, i), unsafe_allow_html=True)
            time.sleep(delay)
        ph.empty()
        s.ex_done = wpm
    exercise_footer()


def flash_html(text):
    return f"<div class='flash'>{text}</div>"


def exercise_chunk(lvl, passage):
    s = st.session_state
    st.info(lvl["instruction"])
    c1, c2 = st.columns(2)
    size = c1.select_slider("Öbek boyutu (kelime)", options=[2, 3, 4], value=2, key=f"size_{lvl['id']}")
    wpm = c2.slider("Hız (kelime/dk)", 150, 600, clamp(default_wpm(1.0), 150, 600), 10, key=f"wpm_{lvl['id']}")
    words = passage["text"].split()
    chunks = [" ".join(words[i:i + size]) for i in range(0, len(words), size)]
    ph = st.empty()
    if st.button("▶️ Başlat", type="primary", key="go"):
        for n in (3, 2, 1):
            ph.markdown(flash_html(str(n)), unsafe_allow_html=True)
            time.sleep(0.7)
        delay = 60.0 / wpm * size
        for ch in chunks:
            ph.markdown(flash_html(ch), unsafe_allow_html=True)
            time.sleep(delay)
        ph.empty()
        s.ex_done = wpm
    exercise_footer()


def exercise_reveal(lvl, passage):
    s = st.session_state
    st.info(lvl["instruction"])
    wpm = st.slider("Hız (kelime/dk)", 150, 600, clamp(default_wpm(1.0), 150, 600), 10, key=f"wpm_{lvl['id']}")
    sentences = [x for x in re.split(r"(?<=[.!?])\s+", passage["text"]) if x.strip()]
    ph = st.empty()
    info = st.empty()
    if st.button("▶️ Başlat", type="primary", key="go"):
        for n in (3, 2, 1):
            ph.markdown(flash_html(str(n)), unsafe_allow_html=True)
            time.sleep(0.7)
        for i, sent in enumerate(sentences):
            ph.markdown(f"<div class='reader'>{sent}</div>", unsafe_allow_html=True)
            info.caption(f"Cümle {i + 1}/{len(sentences)}")
            time.sleep(max(1.2, count_words(sent) / wpm * 60))
        ph.empty()
        info.empty()
        s.ex_done = wpm
    exercise_footer()


def exercise_ramp(lvl, passage):
    s = st.session_state
    st.info(lvl["instruction"])
    base = s.baseline_wpm or 200
    steps = [clamp(round(base * f / 10) * 10, 120, 700) for f in (1.0, 1.15, 1.30)]
    st.caption(f"Hız basamakların: **{steps[0]} → {steps[1]} → {steps[2]}** kelime/dk")
    words = passage["text"].split()
    size = 2
    chunks = [" ".join(words[i:i + size]) for i in range(0, len(words), size)]
    per_phase = math.ceil(len(chunks) / 3)
    ph = st.empty()
    label = st.empty()
    if st.button("▶️ Başlat", type="primary", key="go"):
        for n in (3, 2, 1):
            ph.markdown(flash_html(str(n)), unsafe_allow_html=True)
            time.sleep(0.7)
        for i, ch in enumerate(chunks):
            phase = min(i // per_phase, 2)
            speed = steps[phase]
            label.caption(f"Aşama {phase + 1}/3 · {speed} kelime/dk")
            ph.markdown(flash_html(ch), unsafe_allow_html=True)
            time.sleep(60.0 / speed * size)
        ph.empty()
        label.empty()
        s.ex_done = steps[-1]
    exercise_footer()


EXERCISES = {
    "timed": exercise_timed,
    "pacer": exercise_pacer,
    "chunk": exercise_chunk,
    "reveal": exercise_reveal,
    "ramp": exercise_ramp,
}


# ----------------------------------------------------------------------------
# Test ve sonuç
# ----------------------------------------------------------------------------
def quiz_stage(lvl, passage):
    s = st.session_state
    st.markdown("### 🧠 Anlama testi")
    st.caption("Metin gizlendi. Okuduklarına göre cevapla. Her yanlış cevap 1 can götürür.")
    questions = passage["questions"]
    with st.form(f"quiz_{lvl['id']}_{s.attempt}"):
        answers = []
        for qi, q in enumerate(questions):
            opts = random.Random(q["q"]).sample(q["options"], len(q["options"]))
            answers.append(st.radio(f"{qi + 1}. {q['q']}", opts, index=None,
                                    key=f"q_{lvl['id']}_{s.attempt}_{qi}"))
        submitted = st.form_submit_button("Cevapları gönder", type="primary")
    if not submitted:
        return
    if any(a is None for a in answers):
        st.warning("Lütfen tüm soruları cevapla.")
        return

    total = len(questions)
    score = sum(1 for a, q in zip(answers, questions) if a == q["answer"])
    s.hearts = max(0, s.hearts - (total - score))
    passed = score >= PASS_SCORE
    first = lvl["id"] not in s.completed
    eff = round((s.wpm_result or 0) * score / total)
    gain = 0
    if passed:
        gain = score * 10 + (25 if first else 5)
        s.xp += gain
        s.streak += 1
        if first:
            s.completed.append(lvl["id"])
        if lvl["role"] == "baseline":
            s.baseline_wpm = eff
        elif lvl["role"] == "final":
            s.final_wpm = eff
    else:
        s.streak = 0
    s.last_quiz = {"score": score, "total": total, "passed": passed, "gain": gain, "eff": eff, "first": first}
    s.stage = "result"
    st.rerun()


def result_stage(lvl):
    s = st.session_state
    q = s.last_quiz
    if not q:
        s.stage = "lesson"
        st.rerun()
        return
    measured = lvl["kind"] == "timed"
    c1, c2, c3 = st.columns(3)
    c1.metric("Doğru", f"{q['score']}/{q['total']}")
    c2.metric("Okuma hızı" if measured else "Antrenman hızı", f"{s.wpm_result} k/dk")
    if measured:
        c3.metric("Etkili hız", f"{q['eff']} k/dk")
    else:
        c3.metric("XP", f"+{q['gain']}")

    if q["passed"]:
        st.success(f"🎉 Kademe geçildi! +{q['gain']} XP")
        if q["first"] and lvl["role"] == "final":
            st.balloons()
        if lvl["role"] == "baseline":
            st.info(f"Başlangıç etkili hızın: **{s.baseline_wpm} kelime/dk**. Yolculuğun burada başlıyor!")
        if lvl["role"] == "final" and s.baseline_wpm:
            diff = s.final_wpm - s.baseline_wpm
            st.metric("Başlangıca göre gelişim", f"{s.final_wpm} k/dk", delta=f"{diff:+d}")
            if diff > 0:
                st.success("Harika! Düzenli pratikle bu hızı daha da artırabilirsin. 🚀")
            else:
                st.info("Hız artmadıysa üzülme: anlama oranını koruyarak tekrar dene, ritim ve öbek tekniklerini pekiştir.")
    else:
        st.error(f"Geçmek için en az {PASS_SCORE} doğru gerekiyor. Tekrar deneyebilirsin.")

    b1, b2 = st.columns(2)
    if b1.button("🗺️ Haritaya dön", use_container_width=True):
        go_map()
    if not q["passed"]:
        if b2.button("🔁 Tekrar dene", type="primary", use_container_width=True):
            s.attempt += 1
            reset_level_state()
            s.stage = "exercise"
            st.rerun()
    else:
        nxt = s.level_idx + 1
        if nxt < len(LEVELS) and b2.button("Sonraki kademe →", type="primary", use_container_width=True):
            start_level(nxt)


# ----------------------------------------------------------------------------
# Kademe ekranı
# ----------------------------------------------------------------------------
def level_view():
    s = st.session_state
    lvl = LEVELS[s.level_idx]
    passage = PASSAGES[lvl["passage"]]

    top = st.columns([1, 5])
    if top[0].button("← Harita"):
        go_map()
    top[1].markdown(f"### {lvl['emoji']} Kademe {s.level_idx + 1}: {lvl['title']}")

    stage_i = STAGE_ORDER.index(s.stage)
    st.progress((stage_i + 1) / len(STAGE_ORDER), text=" › ".join(
        f"**{n}**" if i == stage_i else n for i, n in enumerate(STAGE_LABELS)))

    if s.stage != "result" and s.hearts <= 0:
        st.error("💔 Canların bitti! Biraz dinlen, ardından devam et.")
        if st.button("☕ Dinlen ve canları yenile", type="primary"):
            s.hearts = MAX_HEARTS
            s.streak = 0
            st.rerun()
        return

    if s.stage == "lesson":
        with st.container(border=True):
            st.markdown(lvl["lesson"])
        if st.button("Egzersize geç →", type="primary"):
            s.stage = "exercise"
            st.rerun()
    elif s.stage == "exercise":
        EXERCISES[lvl["kind"]](lvl, passage)
    elif s.stage == "quiz":
        quiz_stage(lvl, passage)
    else:
        result_stage(lvl)


def main():
    init_state()
    st.markdown(CSS, unsafe_allow_html=True)
    sidebar()
    if st.session_state.view == "map":
        map_view()
    else:
        level_view()


main()
