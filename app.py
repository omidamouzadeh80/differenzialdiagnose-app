# app.py
# Insomnie – Entscheidungsunterstützung (Explizite Entscheidungsknoten nach Fig. 1 & Fig. 2)
# Quelle: Heidbreder et al. 2024 (BMC Primary Care). Demo/Schulung – keine medizinische Beratung.

import streamlit as st
from datetime import datetime
import io

st.set_page_config(page_title="Insomnie – Entscheidungsunterstützung", page_icon="🛌", layout="centered")
st.title("🛌 Insomnie – Entscheidungsunterstützung (Demo)")
st.caption("Nur zu Demonstrations-/Schulungszwecken. Keine medizinische Beratung.")

st.sidebar.header("Nutzung")
st.sidebar.markdown("""
Wähle unten, ob du den **akuten** (Fig. 1) oder **chronischen** (Fig. 2) Pfad durchläufst.
Die Fragen sind als **explizite Entscheidungsknoten** mit kurzen Tooltips umgesetzt.
Du kannst das Ergebnis als **CSV** oder **Markdown** exportieren.
""")

FLOW = st.radio("Algorithmus wählen", ["Fig. 1 – Akute Insomnie", "Fig. 2 – Chronische Insomnie"], horizontal=False)

st.divider()

# ========================= Hilfsfunktionen =========================
def yesno(label: str, *, help: str = None, key: str = None):
    return st.radio(label, ["Nein", "Ja"], horizontal=True, key=key or label, help=help) == "Ja"


def bullets(items):
    for it in items:
        st.markdown(f"- {it}")


def export_summary_csv(summary: dict) -> bytes:
    # very small hand-made CSV (key;value) for audit/documentation
    lines = ["Feld;Wert"]
    for k, v in summary.items():
        v_str = ", ".join(v) if isinstance(v, (list, tuple)) else str(v)
        lines.append(f"{k};{v_str}")
    return ("
".join(lines)).encode("utf-8")


def export_summary_md(summary: dict, recommendations: list) -> bytes:
    buf = io.StringIO()
    buf.write("# Insomnie – Entscheidungsunterstützung (Zusammenfassung)

")
    buf.write(f"Zeitpunkt: {datetime.now().isoformat(timespec='seconds')}

")
    buf.write("## Eingaben
")
    for k, v in summary.items():
        v_str = ", ".join(v) if isinstance(v, (list, tuple)) else ("Ja" if v is True else ("Nein" if v is False else str(v)))
        buf.write(f"- **{k}:** {v_str}
")
    buf.write("
## Empfehlungen (Demo)
")
    for r in recommendations:
        buf.write(f"- {r}
")
    return buf.getvalue().encode("utf-8")


# ========================= Fig. 1: Akute Insomnie =========================
def run_fig1():
    st.header("Fig. 1 – Akute Insomnie: Entscheidungsfluss (Demo)")

    st.subheader("Knoten A – Symptome & Dauer")
    dauer_lt_3m = yesno(
        "Schlafbeschwerden **< 3 Monate**",
        help="Ab Beginn der aktuellen Episode gerechnet; Übergang zu chronisch ab ≥ 3 Monaten.",
        key="f1_dauer"
    )
    freq_ge_3w = yesno(
        "Häufigkeit **≥ 3 Nächte/Woche**",
        help="Typische DSM-5/ICSD-3 Häufigkeitsschwelle.",
        key="f1_freq"
    )
    day_impair = yesno(
        "**Tagesbeeinträchtigung** vorhanden",
        help="Z. B. Müdigkeit, Leistungseinbußen, Konzentrationsprobleme, Gereiztheit.",
        key="f1_impair"
    )

    st.subheader("Knoten B – Red Flags / unmittelbare Prioritäten")
    redflags = st.multiselect(
        "Red Flags (Mehrfachauswahl)",
        [
            "Akute Suizidalität / schwere depressive Symptomatik",
            "Psychose/Manie-Verdacht",
            "Schwere Substanznutzung (z. B. Alkohol, Sedativa)",
            "Neurologische Alarmzeichen",
        ],
        help="Bei Vorliegen: vorrangige Abklärung/Überweisung vor symptomatischer Therapie.",
        key="f1_redflags"
    )

    st.subheader("Knoten C – Screening auf andere Schlafstörungen")
    other_sleep = st.multiselect(
        "Hinweise auf … (Mehrfachauswahl)",
        [
            "Obstruktive Schlafapnoe (Schnarchen/Atemaussetzer/Tagesschläfrigkeit)",
            "Restless-Legs-Syndrom (Beinbeschwerden/Bewegungsdrang abends)",
            "Zirkadiane Schlaf-Wach-Störung (Schichtarbeit/Phasenverschiebung)",
            "Narkolepsie-/Parasomnie-Verdacht",
        ],
        help="Bei starkem Verdacht frühzeitig gezielt abklären oder überweisen.",
        key="f1_other"
    )

    st.subheader("Knoten D – Schlafhygiene & Verhalten")
    hygiene = st.multiselect(
        "Auffälligkeiten (Mehrfachauswahl)",
        [
            "Unregelmäßige Bett-/Aufstehzeiten",
            "Lange Bettzeit (deutlich > Schlafzeit)",
            "Koffein am späten Nachmittag/Abend",
            "Alkohol/Nikotin am Abend",
            "Intensive Bildschirm-/Gerätenutzung vor dem Schlaf",
        ],
        help="Diese Faktoren gezielt verändern (Stimulus-Kontrolle, Restriktion, Psychoedukation).",
        key="f1_hygiene"
    )

    if st.button("🔎 Auswertung – Fig. 1"):
        st.divider()
        st.subheader("Ergebnis – Fig. 1")

        # Einstufung akut
        if redflags:
            st.error("**Red Flags vorhanden:** Dringliche **Abklärung/Überweisung** priorisieren.")

        akut_kriterien = dauer_lt_3m and freq_ge_3w and day_impair
        if akut_kriterien:
            st.success("Akute/kurzandauernde Insomnie – Kriterien erfüllt")
        else:
            st.warning("Kriterien für akute Insomnie **nicht vollständig** – weitere Abklärung/Verlaufskontrolle.")

        st.markdown("**Empfohlener Pfad (Demo)**")
        recs = []
        if other_sleep:
            recs.append("Gezielte **Abklärung/Überweisung** wegen möglicher anderer Schlafstörung(en).")
        recs.append("Kurzintervention: **Schlafhygiene**, Psychoedukation, **Stimulus-Kontrolle**.")
        recs.append("**Verlaufskontrolle** in 2–4 Wochen; bei Persistenz oder Verschlechterung neu bewerten.")
        if hygiene:
            recs.append("Individuell **Hygienefaktoren** adressieren (siehe oben ausgewählt).")
        recs.append("Pharmakotherapie nur gezielt/kurzzeitig erwägen; Nutzen/Risiken prüfen.")
        bullets(recs)

        # Dokumentation & Export
        summary = {
            "Pfad": "Fig. 1 – Akut",
            "< 3 Monate": dauer_lt_3m,
            "≥ 3 Nächte/Woche": freq_ge_3w,
            "Tagesbeeinträchtigung": day_impair,
            "Red Flags": redflags,
            "Hinweise andere Schlafstörungen": other_sleep,
            "Schlafhygiene-Auffälligkeiten": hygiene,
        }
        st.subheader("Dokumentation & Export")
        csv_bytes = export_summary_csv(summary)
        md_bytes = export_summary_md(summary, recs)
        st.download_button("⬇️ CSV herunterladen", data=csv_bytes, file_name="insomnie_fig1_akut.csv", mime="text/csv")
        st.download_button("⬇️ Markdown herunterladen", data=md_bytes, file_name="insomnie_fig1_akut.md", mime="text/markdown")


# ========================= Fig. 2: Chronische Insomnie =========================
def run_fig2():
    st.header("Fig. 2 – Chronische Insomnie: Entscheidungsfluss (Demo)")

    st.subheader("Knoten 1 – Diagnosekriterien")
    dauer_ge_3m = yesno(
        "Schlafbeschwerden **≥ 3 Monate**",
        help="Chronische Insomnie erfordert in der Regel Dauer ≥ 3 Monate.",
        key="f2_dauer"
    )
    freq_ge_3w = yesno(
        "Häufigkeit **≥ 3 Nächte/Woche**",
        help="Typische DSM-5/ICSD-3 Häufigkeitsschwelle.",
        key="f2_freq"
    )
    day_impair = yesno(
        "**Tagesbeeinträchtigung** vorhanden",
        help="Z. B. Müdigkeit, Leistungseinbußen, Konzentrationsprobleme.",
        key="f2_impair"
    )

    st.subheader("Knoten 2 – Schweregrad (ISI optional)")
    use_isi = yesno(
        "**Insomnia Severity Index (ISI)** liegt vor",
        help="Falls erhoben, kann der ISI die Symptomlast/Verlaufsmessung unterstützen.",
        key="f2_useisi"
    )
    isi = None
    if use_isi:
        isi = st.number_input("ISI-Gesamtwert (0–28)", min_value=0, max_value=28, value=0, step=1, help="Standardauswertung nach Instrument.")

    st.subheader("Knoten 3 – Komorbiditäten & differenzierende Schlafstörungen")
    other_sleep = st.multiselect(
        "Hinweise auf andere Schlafstörung(en) (Mehrfachauswahl)",
        [
            "Obstruktive Schlafapnoe",
            "Restless-Legs-Syndrom",
            "Zirkadiane Störung",
            "Narkolepsie/Parasomnien",
        ],
        help="Bei Hinweisen zuerst abklären/mitbehandeln.",
        key="f2_other"
    )
    relevant_comorbid = st.multiselect(
        "Relevante Komorbiditäten (Mehrfachauswahl)",
        [
            "Depression/Angst",
            "Chronischer Schmerz",
            "Substanzkonsum",
            "Neurologische/Internistische Erkrankung",
        ],
        help="Komorbiditäten können Verlauf/Therapie beeinflussen und sollen mitadressiert werden.",
        key="f2_comorbid"
    )

    st.subheader("Knoten 4 – Zugang & Präferenz")
    cbt_available = yesno(
        "**CBT-I** verfügbar/zugänglich",
        help="Vor Ort, digital oder telemedizinisch.",
        key="f2_cbt"
    )
    patient_prefers_nopsych = yesno(
        "Patient:in bevorzugt **nicht-medikamentöse** Optionen",
        help="Präferenz erfragen und dokumentieren.",
        key="f2_pref"
    )

    st.subheader("Knoten 5 – Red Flags")
    redflags = st.multiselect(
        "Red Flags (Mehrfachauswahl)",
        [
            "Akute Suizidalität / schwere depressive Symptomatik",
            "Psychose/Manie-Verdacht",
            "Schwere Substanznutzung",
            "Neurologische Alarmzeichen",
        ],
        help="Bei Vorliegen: dringliche Abklärung/Überweisung.",
        key="f2_redflags"
    )

    st.subheader("Knoten 6 – Schlafhygiene & Verhalten")
    hygiene = st.multiselect(
        "Auffälligkeiten (Mehrfachauswahl)",
        [
            "Unregelmäßige Bett-/Aufstehzeiten",
            "Lange Bettzeit",
            "Koffein spät",
            "Alkohol/Nikotin abends",
            "Bildschirmnutzung vor dem Schlaf",
        ],
        help="Diese Faktoren im Rahmen der CBT-I-Module gezielt adressieren.",
        key="f2_hygiene"
    )

    if st.button("🔎 Auswertung – Fig. 2"):
        st.divider()
        st.subheader("Ergebnis – Fig. 2")

        if redflags:
            st.error("**Red Flags vorhanden:** Dringliche **Abklärung/Überweisung** vor Therapie priorisieren.")

        chron_kriterien = dauer_ge_3m and freq_ge_3w and day_impair
        if chron_kriterien:
            st.success("**Chronische Insomnie – Kriterien erfüllt (Verdachtsdiagnose)**")
        else:
            st.warning("Kriterien für chronische Insomnie **nicht vollständig** – weitere Abklärung.")

        st.markdown("**Empfohlener Pfad (Demo)**")
        recs = []
        if other_sleep:
            recs.append("Vor/mit Insomniebehandlung: **andere Schlafstörung(en)** abklären/behandeln.")
        if relevant_comorbid:
            recs.append("**Komorbiditäten** parallel adressieren und dokumentieren.")
        if cbt_available:
            recs.append("**CBT-I als First-line** (Stimulus-Kontrolle, Schlafrestriktion, kognitive Strategien, Psychoedukation, Schlafhygiene).")
        else:
            recs.append("Wenn CBT-I nicht verfügbar: **CBT-I-nahe Kurzprogramme**/digitale Angebote; Überweisung erwägen.")
        if not patient_prefers_nopsych:
            recs.append("Bei Präferenz/Aufklärung: **Pharmakotherapie** *zeitlich begrenzt* erwägen; Nutzen/Risiken beachten.")
        if hygiene:
            recs.append("**Schlafhygiene-Faktoren** gezielt verändern (siehe ausgewählte Punkte).")
        if use_isi:
            recs.append(f"**ISI** dokumentiert (Wert: {isi}). Verlauf/Response orientieren.")
        recs.append("**Verlaufskontrolle** und ggf. **Therapieanpassung** (Non-Response → Intensivierung/Alternative).")
        bullets(recs)

        # Dokumentation & Export
        summary = {
            "Pfad": "Fig. 2 – Chronisch",
            "≥ 3 Monate": dauer_ge_3m,
            "≥ 3 Nächte/Woche": freq_ge_3w,
            "Tagesbeeinträchtigung": day_impair,
            "ISI erfasst": use_isi,
            "ISI Wert": isi if use_isi else "",
            "Hinweise andere Schlafstörungen": other_sleep,
            "Komorbiditäten": relevant_comorbid,
            "CBT-I verfügbar": cbt_available,
            "Präferenz nicht-medikamentös": patient_prefers_nopsych,
            "Red Flags": redflags,
            "Schlafhygiene-Auffälligkeiten": hygiene,
        }
        st.subheader("Dokumentation & Export")
        csv_bytes = export_summary_csv(summary)
        md_bytes = export_summary_md(summary, recs)
        st.download_button("⬇️ CSV herunterladen", data=csv_bytes, file_name="insomnie_fig2_chronisch.csv", mime="text/csv")
        st.download_button("⬇️ Markdown herunterladen", data=md_bytes, file_name="insomnie_fig2_chronisch.md", mime="text/markdown")


# ========================= Router =========================
if FLOW.startswith("Fig. 1"):
    run_fig1()
else:
    run_fig2()

st.divider()
st.caption("Quelle: Heidbreder et al., 2024. Diese App ist ein Prototyp und ersetzt keine klinische Beurteilung.")

