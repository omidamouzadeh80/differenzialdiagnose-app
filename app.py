# app.py
import streamlit as st
from math import exp

st.set_page_config(page_title="Differenzialdiagnose – Demo", page_icon="🩺", layout="centered")
st.title("🩺 Differenzialdiagnose – Demo (Prototyp)")

st.caption("👩‍⚕️ Hinweis: Nur zu Demonstrationszwecken. Keine medizinische Beratung.")

# --- Definitions: Diagnosen & Feature-Gewichte (sehr vereinfacht!) ---
DIAGNOSES = {
    "Influenza": {
        "Fieber": 2.0, "Husten": 1.2, "Myalgien": 1.4, "Kopfschmerzen": 0.8, "Schneller Beginn (<48h)": 1.5
    },
    "COVID-19": {
        "Fieber": 1.6, "Husten": 1.4, "Atemnot": 1.2, "Geruchs-/Geschmacksverlust": 2.0, "Kontakt zu COVID-Fall": 2.2
    },
    "Pneumonie": {
        "Fieber": 1.4, "Husten": 1.0, "Atemnot": 2.0, "Brustschmerz": 1.6, "Sauerstoffsättigung < 94%": 2.4
    },
    "Migräne": {
        "Kopfschmerzen": 2.2, "Photophobie": 1.6, "Übelkeit/Erbrechen": 1.4, "Pulsierend einseitig": 1.8, "Trigger (Stress/Schlafmangel)": 0.8
    },
    "Appendizitis": {
        "Bauchschmerzen (rechts unten)": 2.4, "Fieber": 1.0, "Übelkeit/Erbrechen": 1.2, "Loslassschmerz": 2.0, "Appetitlosigkeit": 1.0
    }
}

FEATURES = sorted({f for d in DIAGNOSES.values() for f in d.keys()})

st.subheader("1) Symptome/Risikofaktoren auswählen")
sel = st.multiselect("Wähle alles Zutreffende:", FEATURES)

st.subheader("2) Zusätzliche Angaben (optional)")
rapid = st.checkbox("Schneller Beginn (<48h)")
contact_covid = st.checkbox("Kontakt zu COVID-Fall")
spo2_low = st.checkbox("Sauerstoffsättigung < 94%")

# Map optionale Kurzlabels auf Features
extra = []
if rapid: extra.append("Schneller Beginn (<48h)")
if contact_covid: extra.append("Kontakt zu COVID-Fall")
if spo2_low: extra.append("Sauerstoffsättigung < 94%")
selected_features = set(sel) | set(extra)

def score_diag(diag_name):
    weights = DIAGNOSES[diag_name]
    return sum(weights.get(f, 0.0) for f in selected_features)

def softmax(scores):
    # numerisch stabil
    mx = max(scores) if scores else 0.0
    exps = [exp(s - mx) for s in scores]
    total = sum(exps) or 1.0
    return [e/total for e in exps]

if st.button("🔎 Analyse starten"):
    labels = list(DIAGNOSES.keys())
    raw_scores = [score_diag(d) for d in labels]
    probs = softmax(raw_scores)

    # Sortiert ausgeben
    ranked = sorted(zip(labels, raw_scores, probs), key=lambda x: x[2], reverse=True)

    st.subheader("Ergebnis (Demo-Scores → normalisierte Anteile)")
    for name, score, p in ranked:
        st.write(f"**{name}** — Score: `{score:.2f}` — Anteil: **{p*100:.1f}%**")
        st.progress(min(1.0, p))

    st.info("Diese Ausgabe ist rein illustrativ. Für echte Anwendungen: validierte Regeln/Modelle, "
            "klinische Kontextdaten, Kalibrierung & Evaluation einplanen.")
else:
    st.caption("Wähle Merkmale und klicke auf „Analyse starten“.")
