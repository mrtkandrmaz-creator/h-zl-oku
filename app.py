"""HızlıOku ⚡ — Duolingo tarzı, kademeli hızlı okuma eğitimi (Streamlit)."""

import json
import math
import random
import re
import time

import streamlit as st

from content import LEVELS, PASSAGES

MAX_HEARTS = 5
PASS_SCORE = 2          # 3 sorudan en az 2 doğru
XP_PER_LEVEL = 100      # her 100 XP = 1 seviye
STAGE_ORDER = ["lesson", "exercise", "quiz", "result"]
STAGE_LABELS = ["Ders", "Egzersiz", "Test", "Sonuç"]

st.set_page_config(page_title="HızlıOku • Hızlı Okuma Akademisi", page_icon="⚡", layout="centered")

CSS = """
<style>
.hero {background: linear-gradient(135deg,#6C5CE7 0%,#00B894 100%); padding: 1.6rem 1rem;
       border-radius: 20px; color: white; text-align: center; margin-bottom: 1.2rem;}
.hero h1 {margin: 0; color: white; font-size: 2.2rem;}
.hero p {margin: .3rem 0 0 0; opacity: .95;}
.node {font-size: 2.4rem; text-align: center; line-height: 1.2;}
.reader {font-size: 1.15rem; line-height: 1.9; padding: 1.2rem 1.4rem; border-radius: 14px;
         background: rgba(128,128,128,.10);}
.flash {font-size: 2.2rem; font-weight: 700; text-align: center; padding: 3rem 1rem;
        border-radius: 16px; background: rgba(108,92,231,.12); min-height: 8rem;}
.hl {background: #FDCB6E; color: #2d3436; border-radius: 6px; padding: 0 4px; font-weight: 600;}
.small-muted {opacity: .7; font-size: .9rem;}
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
        "loaded_sig": None,
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
# Kenar çubuk: istatistikler + ilerleme kaydet/yükle
# ----------------------------------------------------------------------------
def sidebar():
    s = st.session_state
    with st.sidebar:
        st.markdown("## ⚡ HızlıOku")
        level = 1 + s.xp // XP_PER_LEVEL
        st.markdown(f"**Seviye {level}** · {s.xp} XP")
        st.progress((s.xp % XP_PER_LEVEL) / XP_PER_LEVEL)
        st.markdown(f"{'❤️' * s.hearts}{'🖤' * (MAX_HEARTS - s.hearts)}")
        c1, c2 = st.columns(2)
        c1.metric("🔥 Seri", s.streak)
        c2.metric("✅ Kademe", f"{len(set(s.completed))}/{len(LEVELS)}")
        if s.baseline_wpm:
            st.metric("📏 Başlangıç (etkili)", f"{s.baseline_wpm} k/dk")
        if s.final_wpm:
            st.metric("🏆 Final (etkili)", f"{s.final_wpm} k/dk")

        st.divider()
        st.caption("İlerlemeni kaydet ve sonra devam et:")
        data = {
            "xp": s.xp,
            "streak": s.streak,
            "completed": s.completed,
            "baseline_wpm": s.baseline_wpm,
            "final_wpm": s.final_wpm,
        }
        st.download_button("💾 İlerlemeyi indir", json.dumps(data, ensure_ascii=False),
                           file_name="hizliokuma_ilerleme.json", mime="application/json",
                           use_container_width=True)
        up = st.file_uploader("📂 İlerlemeyi yükle", type="json")
        if up is not None:
            sig = f"{up.name}-{up.size}"
            if s.loaded_sig != sig:
                try:
                    d = json.load(up)
                    s.xp = int(d.get("xp", 0))
                    s.streak = int(d.get("streak", 0))
                    s.completed = list(d.get("completed", []))
                    s.baseline_wpm = d.get("baseline_wpm")
                    s.final_wpm = d.get("final_wpm")
                    s.loaded_sig = sig
                    st.rerun()
                except Exception:
                    st.error("Dosya okunamadı.")


# ----------------------------------------------------------------------------
# Harita (kademe listesi)
# ----------------------------------------------------------------------------
def map_view():
    s = st.session_state
    st.markdown(
        "<div class='hero'><h1>⚡ HızlıOku</h1>"
        "<p>Adım adım hızlı okuma — her kademeyi geç, bir sonrakinin kilidini aç!</p></div>",
        unsafe_allow_html=True,
    )
    done = set(s.completed)
    next_idx = next((i for i, l in enumerate(LEVELS) if l["id"] not in done), len(LEVELS))

    if next_idx == len(LEVELS):
        st.success("🎉 Tüm kademeleri tamamladın! Aşağıdan istediğin kademeyi tekrar oynayabilirsin.")
        if s.baseline_wpm and s.final_wpm:
            st.metric("Etkili okuma hızın", f"{s.final_wpm} kelime/dk",
                      delta=f"{s.final_wpm - s.baseline_wpm:+d} (başlangıca göre)")

    for i, lvl in enumerate(LEVELS):
        locked = i > next_idx
        with st.container(border=True):
            c1, c2, c3 = st.columns([1, 6, 3])
            icon = "🔒" if locked else lvl["emoji"]
            c1.markdown(f"<div class='node'>{icon}</div>", unsafe_allow_html=True)
            badge = " ✅" if lvl["id"] in done else ""
            c2.markdown(f"**Kademe {i + 1} · {lvl['title']}**{badge}  \n{lvl['summary']}")
            label = "Tekrar" if lvl["id"] in done else "Başla"
            primary = (i == next_idx)
            if c3.button(label, key=f"start_{lvl['id']}", disabled=locked,
                         use_container_width=True, type="primary" if primary else "secondary"):
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
