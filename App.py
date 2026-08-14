import json
import random
import pandas as pd
import streamlit as st

# =============================================================================
# 1. KONFIGURATION & RESPONSIVES, ZENTRIERTES LAYOUT
# =============================================================================
st.set_page_config(
    page_title="Gruppeneinteilung", page_icon="👥", layout="centered"
)

st.markdown(
    """
    <style>
        /* 1. Gesamte Seite gegen horizontales Verrutschen sperren */
        html, body, .main {
            overflow-x: hidden !important;
        }

        /* Hauptcontainer strikt zentrieren & auf 580px begrenzen */
        .main .block-container {
            max-width: 580px !important;
            width: 100% !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-top: 1.5rem !important;
            padding-bottom: 3rem !important;
            padding-left: 0.5rem !important;
            padding-right: 0.5rem !important;
            box-sizing: border-box !important;
        }

        .centered-text { text-align: center !important; }

        /* 2. Vertikale Abstände & Formulare/Buttons vollbreit halten */
        div[data-testid="stVerticalBlock"] {
            gap: 0.5rem !important;
        }

        div[data-testid="stForm"], 
        div[data-testid="stFileUploader"],
        div[data-testid="stSelectbox"],
        div[data-testid="stNumberInput"],
        div[data-testid="stRadio"],
        .element-container button {
            width: 100% !important;
            box-sizing: border-box !important;
        }

        div[data-testid="stForm"] {
            margin-top: 10px !important;
            margin-bottom: 10px !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 10px !important;
            background-color: #ffffff !important;
        }

        /* 3. TABELLEN-CONTAINER: Isolierter horizontaler Scrollbereich & ausreichend Abstand nach unten gegen Abschneiden */
        div[data-testid="stVerticalBlock"]:has(> div > div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(7)),
        div[data-testid="stVerticalBlock"]:has(> div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"]:nth-child(7)) {
            overflow-x: auto !important;
            max-width: 100% !important;
            padding-bottom: 20px !important;
        }

        /* 4. TABELLEN-ZEILEN */
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) {
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
            gap: 0.2rem !important;
            min-width: 500px !important;
        }

        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) > div[data-testid="stColumn"] {
            min-width: 0 !important;
        }

        /* Spaltenbreiten Tabelle */
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) > div[data-testid="stColumn"]:nth-child(1) {
            flex: 0 0 36px !important; max-width: 36px !important; min-width: 36px !important; width: 36px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) > div[data-testid="stColumn"]:nth-child(2) { flex: 1.8 1 0px !important; }
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) > div[data-testid="stColumn"]:nth-child(3) { flex: 1.8 1 0px !important; }
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) > div[data-testid="stColumn"]:nth-child(4),
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) > div[data-testid="stColumn"]:nth-child(5),
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) > div[data-testid="stColumn"]:nth-child(6) { flex: 1.0 1 0px !important; }
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) > div[data-testid="stColumn"]:nth-child(7) {
            flex: 0 0 32px !important; max-width: 32px !important; min-width: 32px !important; width: 32px !important;
        }

        /* Header & Typo */
        .table-header { 
            font-weight: 700; 
            color: #3b3b3b; 
            font-size: 0.8rem; 
            margin: 0 0 10px 0 !important; 
            padding: 0 !important; 
            line-height: 1.2 !important; 
            width: 100%; 
        }
        .th-da   { text-align: center; }
        .th-vn   { text-align: left; }
        .th-nn   { text-align: left; }
        .th-komp { text-align: center; white-space: nowrap !important; word-break: normal !important; }

        .row-vn  { font-weight: 600; font-size: 0.85rem; color: #2d3748; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .row-nn  { font-size: 0.85rem; color: #2d3748; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

        /* Buttons & Checkboxen in Tabelle */
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) div[data-testid="stCheckbox"] {
            display: flex !important; align-items: center !important; justify-content: center !important; height: 28px !important;
        }
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) button {
            height: 28px !important; min-height: 28px !important; width: 100% !important; margin: 10px 0 0 0 !important; padding: 0 1px !important;
            font-size: 0.72rem !important; border-radius: 5px !important; border: 1px solid #e2e8f0 !important; background-color: #f7fafc !important; color: #4a5568 !important;
        }
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) button[kind="primary"],
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) button[data-testid*="primary"] {
            border: 1px solid #ff4b4b !important; background-color: #ff4b4b !important;
        }
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) button[kind="primary"] p,
        div[data-testid="stHorizontalBlock"]:has(> div[data-testid="stColumn"]:nth-child(7)) button[data-testid*="primary"] p {
            color: #ffffff !important; font-weight: 700 !important;
        }

        /* Zusammenfassung Pillen */
        .summary-pill {
            background-color: #f8f9fa; color: #4a5568; border-radius: 5px; padding: 0px; text-align: center;
            font-size: 0.78rem; font-weight: 600; width: 100%; height: 28px; display: flex; align-items: center; justify-content: center;
            margin-top: 4px;
        }
        .sum-number { text-align: center; font-size: 0.82rem; margin-top: 4px; }
        .sum-label  { font-size: 0.82rem; margin-top: 4px; }

        /* Gruppen-Karten */
        .group-card {
            background: #ffffff; border: 1px solid #e2e8f0; border-radius: 8px; padding: 12px; margin-bottom: 10px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05); text-align: center !important;
        }
        .group-card ul { list-style-type: none !important; padding: 0 !important; margin: 6px 0 0 0 !important; text-align: center !important; }
        .group-card li { text-align: center !important; margin-bottom: 3px !important; font-size: 0.9rem; }

        button[kind="primary"][data-testid="baseButton-primary"] {
            background-color: #2e7d32 !important; border-color: #2e7d32 !important;
        }
        button[kind="primary"][data-testid="baseButton-primary"]:hover {
            background-color: #1b5e20 !important; border-color: #1b5e20 !important;
        }
    </style>
""",
    unsafe_allow_html=True,
)

# =============================================================================
# 2. INITIALISIERUNG & STATE
# =============================================================================
DEFAULT_SCHUELER = [
    {
        "Anwesend": True,
        "Vorname": "stark",
        "Nachname": "1",
        "Leistungsstufe": "stark",
    },
    {
        "Anwesend": True,
        "Vorname": "mittel",
        "Nachname": "1",
        "Leistungsstufe": "mittel",
    },
    {
        "Anwesend": True,
        "Vorname": "schwach",
        "Nachname": "1",
        "Leistungsstufe": "schwach",
    },
    {
        "Anwesend": True,
        "Vorname": "stark",
        "Nachname": "2",
        "Leistungsstufe": "stark",
    },
    {
        "Anwesend": True,
        "Vorname": "mittel",
        "Nachname": "2",
        "Leistungsstufe": "mittel",
    },
    {
        "Anwesend": True,
        "Vorname": "schwach",
        "Nachname": "2",
        "Leistungsstufe": "schwach",
    },
    {
        "Anwesend": True,
        "Vorname": "stark",
        "Nachname": "3",
        "Leistungsstufe": "stark",
    },
    {
        "Anwesend": True,
        "Vorname": "mittel",
        "Nachname": "3",
        "Leistungsstufe": "mittel",
    },
    {
        "Anwesend": True,
        "Vorname": "schwach",
        "Nachname": "3",
        "Leistungsstufe": "schwach",
    },
    {
        "Anwesend": True,
        "Vorname": "stark",
        "Nachname": "4",
        "Leistungsstufe": "stark",
    },
    {
        "Anwesend": True,
        "Vorname": "mittel",
        "Nachname": "4",
        "Leistungsstufe": "mittel",
    },
    {
        "Anwesend": True,
        "Vorname": "schwach",
        "Nachname": "4",
        "Leistungsstufe": "schwach",
    },
]

if "schueler_df" not in st.session_state:
  st.session_state.schueler_df = pd.DataFrame(DEFAULT_SCHUELER)

st.session_state.schueler_df = st.session_state.schueler_df.reset_index(
    drop=True
)

if "show_presentation" not in st.session_state:
  st.session_state.show_presentation = False
if "uploader_key" not in st.session_state:
  st.session_state.uploader_key = 0
if "json_uploader_key" not in st.session_state:
  st.session_state.json_uploader_key = 100

if "size_mode" not in st.session_state:
  st.session_state.size_mode = "Feste Gruppengröße"
if "num_per_group" not in st.session_state:
  st.session_state.num_per_group = 3
if "num_total_groups" not in st.session_state:
  st.session_state.num_total_groups = 3
if "selected_themen" not in st.session_state:
  st.session_state.selected_themen = 3
if "selected_rest" not in st.session_state:
  st.session_state.selected_rest = (
      "Rest gleichmäßig auf bestehende Gruppen aufteilen"
  )


# =============================================================================
# 3. HELPER- & LOGIK-FUNKTIONEN
# =============================================================================
def load_excel_flexible(file):
  raw_df = pd.read_excel(file, header=None)
  header_row_idx = None
  for idx, row in raw_df.iterrows():
    if idx > 15:
      break
    row_values = [str(val).strip().lower() for val in row.dropna().values]
    if any(term in row_values for term in ["nachname", "vorname", "name"]):
      header_row_idx = idx
      break

  if header_row_idx is not None:
    file.seek(0)
    df = pd.read_excel(file, header=header_row_idx)
  else:
    file.seek(0)
    df = pd.read_excel(file)
  return df


def format_student_name(row, duplicate_first_names):
  vorname = str(row["Vorname"]).strip()
  nachname = str(row["Nachname"]).strip()
  if not vorname:
    return nachname
  if not nachname:
    return vorname
  if vorname in duplicate_first_names:
    return f"{vorname} {nachname[0]}."
  return vorname


def get_anwesende_schueler():
  if (
      "schueler_df" not in st.session_state
      or st.session_state.schueler_df.empty
  ):
    return []
  anwesende_df = st.session_state.schueler_df[
      st.session_state.schueler_df["Anwesend"] == True
  ].copy()
  if anwesende_df.empty:
    return []
  vornamen_counts = anwesende_df["Vorname"].str.strip().value_counts()
  doppelte_vornamen = set(vornamen_counts[vornamen_counts > 1].index)
  anwesende_df["AnzeigeName"] = anwesende_df.apply(
      lambda r: format_student_name(r, doppelte_vornamen), axis=1
  )
  return anwesende_df.to_dict("records")


def set_stufe(idx, neue_stufe):
  st.session_state.schueler_df.at[idx, "Leistungsstufe"] = neue_stufe
  st.rerun()


def set_anwesend(idx, key):
  st.session_state.schueler_df.at[idx, "Anwesend"] = st.session_state[key]
  st.rerun()


def delete_student(idx):
  st.session_state.schueler_df = st.session_state.schueler_df.drop(
      idx
  ).reset_index(drop=True)
  st.rerun()


def add_student(vorname, nachname, stufe):
  new_row = pd.DataFrame([{
      "Anwesend": True,
      "Vorname": vorname.strip(),
      "Nachname": nachname.strip(),
      "Leistungsstufe": stufe,
  }])
  st.session_state.schueler_df = pd.concat(
      [st.session_state.schueler_df, new_row], ignore_index=True
  )


def generiere_gruppen_dynamisch(
    schueler_liste,
    kategorie,
    size_mode,
    num_per_group,
    num_total_groups,
    rest_strategie,
    num_themen=3,
):
  s_list = schueler_liste.copy()
  n = len(s_list)
  if n == 0:
    return []

  if kategorie == "Gruppenpuzzle":
    random.shuffle(s_list)
    expert_groups = {i: [] for i in range(1, num_themen + 1)}
    for idx, s in enumerate(s_list):
      topic_id = (idx % num_themen) + 1
      expert_groups[topic_id].append(s)

    num_full_groups = n // num_themen
    expert_display = [
        [f"{s['AnzeigeName']}" for s in members]
        for members in expert_groups.values()
    ]

    stammgruppen = []
    rest_schueler = []

    for i in range(num_full_groups):
      group = []
      for topic_id in range(1, num_themen + 1):
        m = expert_groups[topic_id].pop(0)
        group.append(f"{m['AnzeigeName']} (T{topic_id})")
      stammgruppen.append(group)

    for topic_id in range(1, num_themen + 1):
      for m in expert_groups[topic_id]:
        rest_schueler.append(f"{m['AnzeigeName']} (T{topic_id})")

    if "kleinere Gruppe" in rest_strategie and rest_schueler:
      stammgruppen.append(rest_schueler)
    else:
      if stammgruppen:
        for idx, s_name in enumerate(rest_schueler):
          stammgruppen[idx % len(stammgruppen)].append(s_name)
      else:
        if rest_schueler:
          stammgruppen.append(rest_schueler)

    return {
        "typ": "gruppenpuzzle",
        "experten": expert_display,
        "stammgruppen": stammgruppen,
    }

  if size_mode == "Anzahl der Gruppen":
    num_groups = max(1, num_total_groups)
    base = n // num_groups
    extra = n % num_groups
    capacities = [base + (1 if i < extra else 0) for i in range(num_groups)]
  else:
    ziel_groesse = num_per_group
    if "kleinere Gruppe" in rest_strategie:
      capacities = []
      rem = n
      while rem > 0:
        cap = min(ziel_groesse, rem)
        capacities.append(cap)
        rem -= cap
    else:
      num_groups = max(1, round(n / ziel_groesse))
      base = n // num_groups
      extra = n % num_groups
      capacities = [base + (1 if i < extra else 0) for i in range(num_groups)]

  num_groups = len(capacities)
  gruppen = [[] for _ in range(num_groups)]

  if kategorie == "Zufällig":
    random.shuffle(s_list)
    for idx, student in enumerate(s_list):
      for g_idx in range(num_groups):
        if len(gruppen[g_idx]) < capacities[g_idx]:
          gruppen[g_idx].append(student)
          break

  elif kategorie == "Kompetenzorientiert":
    stark = [s for s in s_list if s.get("Leistungsstufe") == "stark"]
    mittel = [s for s in s_list if s.get("Leistungsstufe", "mittel") == "mittel"]
    schwach = [
        s for s in s_list if s.get("Leistungsstufe", "schwach") == "schwach"
    ]

    random.shuffle(stark)
    random.shuffle(mittel)
    random.shuffle(schwach)

    single_indices = [i for i, cap in enumerate(capacities) if cap == 1]
    for idx in single_indices:
      if stark:
        gruppen[idx].append(stark.pop(0))
      elif mittel:
        gruppen[idx].append(mittel.pop(0))
      elif schwach:
        gruppen[idx].append(schwach.pop(0))

    active_indices = [
        i for i, cap in enumerate(capacities) if len(gruppen[i]) < cap
    ]

    for idx in active_indices:
      if stark and len(gruppen[idx]) < capacities[idx]:
        gruppen[idx].append(stark.pop(0))

    for idx in active_indices:
      if schwach and len(gruppen[idx]) < capacities[idx]:
        gruppen[idx].append(schwach.pop(0))

    remaining_pool = stark + mittel + schwach
    random.shuffle(remaining_pool)

    for idx in range(num_groups):
      while len(gruppen[idx]) < capacities[idx] and remaining_pool:
        gruppen[idx].append(remaining_pool.pop(0))

  gruppen = [[s["AnzeigeName"] for s in team] for team in gruppen if len(team) > 0]

  return gruppen


# =============================================================================
# PRÄSENTATIONS-GRID
# =============================================================================
def render_groups_grid(groups_subset, start_index=1, title_prefix="Gruppe"):
  for i in range(0, len(groups_subset), 2):
    cols = st.columns(2)
    for j in range(2):
      group_idx = i + j
      if group_idx < len(groups_subset):
        with cols[j]:
          actual_num = start_index + group_idx
          team_members = groups_subset[group_idx]

          content = (
              f"<div class='group-card'><b>{title_prefix}"
              f" {actual_num}</b><ul>"
          )
          for m in team_members:
            content += f"<li>{m}</li>"
          content += "</ul></div>"
          st.markdown(content, unsafe_allow_html=True)


# =============================================================================
# 4. HEADER & INFO-BEREICH
# =============================================================================
st.markdown(
    "<h2 class='centered-text'>👥 Intelligente Gruppeneinteilung</h2>",
    unsafe_allow_html=True,
)

with st.expander("ℹ️ Anleitung, Rechtliches & Datenschutz"):
  st.markdown("""
    ### 🛠️ Kurzanleitung
    1. **Liste der Lernenden erstellen:** 
       - Ziehe eine Excel-Tabelle (`.xlsx`/`.xls`) bequem per **Drag & Drop** in das Upload-Feld (oder erstelle eine leere Liste).
       - Spaltenüberschriften (z. B. *Vorname*, *Nachname*, *Name* etc.) werden dabei **automatisch in allen gängigen Varianten erkannt**.
       - Trage fehlende Lernende bei Bedarf manuell unten nach.
    2. **Anwesenheit & Kompetenz:** 
       - Markiere anwesende Lernende in der Spalte **„Da?“**.
       - Weise über die Buttons **schwach**, **mittel** oder **stark** das jeweilige Niveau zu.
    3. **Speicherung & Sicherung (JSON):** 
       - Speichere deinen aktuellen Klassenstand inkl. Anwesenheit und Kompetenzstufen als `.json`-Datei ab, um sie beim nächsten Mal direkt wieder einzuladen.
    4. **Gruppen generieren:** 
       - Wähle unten den Modus, passe die Parameter an und klicke auf **„Gruppen generieren & Präsentieren“**.

    ---

    ### 🔒 Datenschutz & Datenspeicherung
    * **Keine dauerhafte Speicherung:** Alle eingegebenen Namen, Anwesenheiten und Leistungsstufen werden ausschließlich temporär im Arbeitsspeicher (Session State) deines aktuellen Browser-Tabs verarbeitet. 
    * **Keine Cloud-Speicherung:** Es werden keine personenbezogenen Daten in einer Datenbank gespeichert oder an Dritte übertragen. Sobald du den Browser-Tab schließt, werden die Daten vollständig gelöscht.

    ---

    ### ⚠️ Haftungsausschluss & KI-Hinweis
    * Dieses Tool wurde mithilfe einer Künstlichen Intelligenz (KI) erstellt. 
    * Es wird keinerlei Verantwortung, Garantie oder Haftung für die fehlerfreie Funktion des Codes, die Richtigkeit der Gruppeneinteilungen oder den Datenschutz übernommen. Die Nutzung erfolgt auf eigene Verantwortung.
    """)


# =============================================================================
# 5. ANSICHT 1: PRÄSENTATION
# =============================================================================
if st.session_state.show_presentation and "generierte_gruppen" in st.session_state:

  col_back, col_reshuffle = st.columns(2)
  with col_back:
    st.button(
        "⚙️ Zurück zur Bearbeitung",
        on_click=lambda: st.session_state.update({"show_presentation": False}),
        use_container_width=True,
    )
  with col_reshuffle:
    if st.button(
        "🎲 Neu zusammenwürfeln", type="primary", use_container_width=True
    ):
      current_anwesende = get_anwesende_schueler()
      if current_anwesende:
        kat = st.session_state.get("last_kategorie", "Kompetenzorientiert")
        smode = st.session_state.get("last_size_mode", "Feste Gruppengröße")
        n_per = st.session_state.get("last_num_per_group", 3)
        n_tot = st.session_state.get("last_num_total_groups", 3)
        strat = st.session_state.get(
            "last_rest_strategie",
            "Rest gleichmäßig auf bestehende Gruppen aufteilen",
        )
        num_t = st.session_state.get("last_num_themen", 3)
        st.session_state.generierte_gruppen = generiere_gruppen_dynamisch(
            current_anwesende, kat, smode, n_per, n_tot, strat, num_t
        )
        st.rerun()

  st.markdown(
      "<h3 class='centered-text' style='margin-top: 1.2rem;'>🎯"
      " Gruppeneinteilung</h3>",
      unsafe_allow_html=True,
  )
  st.write("")

  res_data = st.session_state.generierte_gruppen

  if isinstance(res_data, dict) and res_data.get("typ") == "gruppenpuzzle":
    tab_exp, tab_base = st.tabs(["🧩 Expertengruppen", "👥 Stammgruppen"])

    with tab_exp:
      render_groups_grid(
          res_data["experten"], start_index=1, title_prefix="Thema"
      )

    with tab_base:
      render_groups_grid(
          res_data["stammgruppen"], start_index=1, title_prefix="Stammgruppe"
      )
  else:
    render_groups_grid(res_data, start_index=1, title_prefix="Gruppe")


# =============================================================================
# 6. ANSICHT 2: LEHRER / BEARBEITEN
# =============================================================================
else:
  st.markdown(
      "<h3 class='centered-text'>📋 Lerngruppe & Anwesenheit</h3>",
      unsafe_allow_html=True,
  )
  st.write("")

  # 1. EXCEL-UPLOAD & NEUE LISTE ERSTELLEN
  st.write("**Excel-Liste hochladen (per Drag & Drop oder Klick):**")
  uploaded_excel = st.file_uploader(
      "Excel-Liste hochladen",
      type=["xlsx", "xls"],
      key=f"excel_uploader_{st.session_state.uploader_key}",
      label_visibility="collapsed",
  )

  if st.button("➕ Neue leere Liste erstellen", use_container_width=True):
    st.session_state.schueler_df = pd.DataFrame(
        columns=["Anwesend", "Vorname", "Nachname", "Leistungsstufe"]
    )
    st.rerun()

  if uploaded_excel is not None:
    try:
      excel_df = load_excel_flexible(uploaded_excel)
      cols_clean = {str(c).strip().capitalize(): c for c in excel_df.columns}
      new_rows = []
      nachname_col = cols_clean.get("Nachname") or cols_clean.get("Name")
      vorname_col = cols_clean.get("Vorname")
      stufe_col = cols_clean.get("Leistungsstufe")

      if nachname_col or vorname_col:
        for _, row in excel_df.iterrows():
          v_name = (
              str(row[vorname_col]).strip()
              if vorname_col and pd.notna(row[vorname_col])
              else ""
          )
          n_name = (
              str(row[nachname_col]).strip()
              if nachname_col and pd.notna(row[nachname_col])
              else ""
          )
          if v_name.capitalize() in [
              "Vorname",
              "Name",
          ] or n_name.capitalize() in ["Nachname", "Name"]:
            continue
          if v_name or n_name:
            stufe = (
                str(row[stufe_col]).strip().lower()
                if stufe_col and pd.notna(row[stufe_col])
                else "mittel"
            )
            if stufe not in ["stark", "mittel", "schwach"]:
              stufe = "mittel"
            new_rows.append({
                "Anwesend": True,
                "Vorname": v_name,
                "Nachname": n_name,
                "Leistungsstufe": stufe,
            })

      if new_rows:
        st.session_state.schueler_df = pd.DataFrame(new_rows).reset_index(
            drop=True
        )
        st.session_state.uploader_key += 1
        st.rerun()
    except Exception as e:
      st.error(f"Fehler beim Einlesen: {e}")

  st.write("")

  # 2. TABELLE
  with st.container():
    col_widths = [0.6, 1.8, 1.8, 1.0, 1.0, 1.0, 0.5]

    header_cols = st.columns(col_widths)
    header_cols[0].markdown(
        "<p class='table-header th-da'>Da?</p>", unsafe_allow_html=True
    )
    header_cols[1].markdown(
        "<p class='table-header th-vn'>Vorname</p>", unsafe_allow_html=True
    )
    header_cols[2].markdown(
        "<p class='table-header th-nn'>Nachname</p>", unsafe_allow_html=True
    )
    header_cols[4].markdown(
        "<p class='table-header th-komp'>Kompetenz</p>", unsafe_allow_html=True
    )

    if not st.session_state.schueler_df.empty:
      for idx, row in st.session_state.schueler_df.iterrows():
        c1, c2, c3, c4, c5, c6, c7 = st.columns(col_widths)

        v_name_str = str(row["Vorname"])
        n_name_str = str(row["Nachname"])
        aktuelle_stufe = str(row["Leistungsstufe"]).lower()

        with c1:
          cb_key = f"anw_{idx}_{v_name_str}_{n_name_str}"
          st.checkbox(
              "",
              value=bool(row["Anwesend"]),
              key=cb_key,
              on_change=set_anwesend,
              args=(idx, cb_key),
              label_visibility="collapsed",
          )

        with c2:
          st.markdown(
              f"<div class='row-vn'>{v_name_str}</div>", unsafe_allow_html=True
          )

        with c3:
          st.markdown(
              f"<div class='row-nn'>{n_name_str}</div>", unsafe_allow_html=True
          )

        with c4:
          st.button(
              "schwach",
              key=f"btn_schwach_{idx}_{v_name_str}_{n_name_str}",
              type="primary" if aktuelle_stufe == "schwach" else "tertiary",
              on_click=set_stufe,
              args=(idx, "schwach"),
          )

        with c5:
          st.button(
              "mittel",
              key=f"btn_mittel_{idx}_{v_name_str}_{n_name_str}",
              type="primary" if aktuelle_stufe == "mittel" else "tertiary",
              on_click=set_stufe,
              args=(idx, "mittel"),
          )

        with c6:
          st.button(
              "stark",
              key=f"btn_stark_{idx}_{v_name_str}_{n_name_str}",
              type="primary" if aktuelle_stufe == "stark" else "tertiary",
              on_click=set_stufe,
              args=(idx, "stark"),
          )

        with c7:
          st.button(
              "🗑️",
              key=f"btn_del_{idx}_{v_name_str}_{n_name_str}",
              on_click=delete_student,
              args=(idx,),
          )
    else:
      st.info(
          "Die Liste ist aktuell leer. Füge unten einfach erste Lernende hinzu!"
      )

    anwesende_schueler = get_anwesende_schueler()

    if not st.session_state.schueler_df.empty:
      anwesende_df_stats = st.session_state.schueler_df[
          st.session_state.schueler_df["Anwesend"] == True
      ]
      anzahl_schwach = len(
          anwesende_df_stats[
              anwesende_df_stats["Leistungsstufe"] == "schwach"
          ]
      )
      anzahl_mittel = len(
          anwesende_df_stats[anwesende_df_stats["Leistungsstufe"] == "mittel"]
      )
      anzahl_stark = len(
          anwesende_df_stats[anwesende_df_stats["Leistungsstufe"] == "stark"]
      )
    else:
      anzahl_schwach = anzahl_mittel = anzahl_stark = 0

    s1, s2, s3, s4, s5, s6, s7 = st.columns(col_widths)
    s1.markdown(
        f"<div class='sum-number'><b>{len(anwesende_schueler)}</b>/{len(st.session_state.schueler_df)}</div>",
        unsafe_allow_html=True,
    )
    s2.markdown(
        "<div class='sum-label'><b>Gesamt</b></div>", unsafe_allow_html=True
    )
    s3.markdown("")
    s4.markdown(
        f"<div class='summary-pill'>🔴 {anzahl_schwach}</div>",
        unsafe_allow_html=True,
    )
    s5.markdown(
        f"<div class='summary-pill'>🟡 {anzahl_mittel}</div>",
        unsafe_allow_html=True,
    )
    s6.markdown(
        f"<div class='summary-pill'>🟢 {anzahl_stark}</div>",
        unsafe_allow_html=True,
    )
    s7.markdown("")

  # 3. MANUELLES HINZUFÜGEN
  with st.form("add_student_form", clear_on_submit=True):
    st.markdown(
        "<p style='font-size: 0.85rem; font-weight: 600; color: #718096;"
        " margin-bottom: 8px;'>➕ Lernende/n hinzufügen</p>",
        unsafe_allow_html=True,
    )
    f_col1, f_col2, f_col3, f_col4 = st.columns([1.8, 1.8, 1.1, 1.3])
    new_vname = f_col1.text_input(
        "Vorname", placeholder="Vorname", label_visibility="collapsed"
    )
    new_nname = f_col2.text_input(
        "Nachname", placeholder="Nachname", label_visibility="collapsed"
    )
    new_stufe = f_col3.selectbox(
        "Stufe",
        options=["mittel", "schwach", "stark"],
        label_visibility="collapsed",
    )
    btn_add = f_col4.form_submit_button("Hinzufügen", use_container_width=True)

    if btn_add:
      if new_vname.strip() or new_nname.strip():
        add_student(new_vname, new_nname, new_stufe)
        st.rerun()

  st.write("")

  # =========================================================================
  # 4. EINGEKLAPPTE LISTENVERWALTUNG (JSON)
  # =========================================================================
  with st.expander("💾 Klassenliste speichern & laden (JSON)"):
    st.markdown("""
        Hier kannst du den aktuellen Zustand deiner Klasse inklusive **Anwesenheiten** und **Kompetenzstufen** sichern oder eine gespeicherte Liste wiederherstellen.
        * **Download:** Lädt deine aktuelle Tabelle als `.json`-Datei auf deinen Computer herunter.
        * **Upload:** Ziehe eine gespeicherte `.json`-Datei per **Drag & Drop** in das Feld unten, um die Liste sofort wieder einzuladen.
        """)
    st.write("")

    # JSON Download
    current_data = st.session_state.schueler_df.to_dict("records")
    json_string = json.dumps(current_data, ensure_ascii=False, indent=2)

    st.download_button(
        label="📥 Aktuelle Liste als JSON herunterladen",
        data=json_string,
        file_name="lerngruppe.json",
        mime="application/json",
        use_container_width=True,
    )

    st.write("")
    st.markdown("**JSON-Datei hochladen (per Drag & Drop oder Klick):**")

    uploaded_json = st.file_uploader(
        "JSON-Datei hochladen",
        type=["json"],
        key=f"json_uploader_{st.session_state.json_uploader_key}",
        label_visibility="collapsed",
    )

    if uploaded_json is not None:
      try:
        loaded_data = json.load(uploaded_json)
        if isinstance(loaded_data, list):
          st.session_state.schueler_df = pd.DataFrame(loaded_data)
          st.session_state.json_uploader_key += 1
          st.success("Liste erfolgreich aus JSON aktualisiert!")
          st.rerun()
        else:
          st.error(
              "Ungültiges Format: Die JSON-Datei muss eine Liste von Personen"
              " enthalten."
          )
      except Exception as e:
        st.error(f"Fehler beim Laden der JSON-Datei: {e}")

  # =========================================================================
  # 5. DAUERHAFT SICHTBARER ZUTEILUNGSMODUS
  # =========================================================================
  st.markdown(
      "<h3 class='centered-text' style='margin-top: 1rem;'>⚙️ Zuteilungsmodus &"
      " Generierung</h3>",
      unsafe_allow_html=True,
  )
  st.write("")

  st.markdown("**Art der Gruppeneinteilung**")
  kategorie = st.radio(
      "Art der Gruppeneinteilung",
      options=["Kompetenzorientiert", "Zufällig", "Gruppenpuzzle"],
      index=0,
      horizontal=True,
      label_visibility="collapsed",
  )

  st.write("")

  if kategorie == "Gruppenpuzzle":
    st.markdown("**Anzahl der Themen (Expertengruppen)**")
    num_themen = st.number_input(
        "Anzahl Themen",
        min_value=2,
        max_value=6,
        value=st.session_state.selected_themen,
        step=1,
        key="selected_themen",
        label_visibility="collapsed",
    )
    size_mode = "Feste Gruppengröße"
    num_per_group = 3
    num_total_groups = 3
  else:
    num_themen = 3
    st.markdown("**Gruppengröße / Einteilung**")
    size_mode = st.radio(
        "Einteilungs-Methode",
        options=["Feste Gruppengröße", "Anzahl der Gruppen"],
        key="size_mode",
        horizontal=True,
        label_visibility="collapsed",
    )

    if size_mode == "Feste Gruppengröße":
      st.markdown(
          "<p style='font-size: 0.85rem; font-weight: 600; color: #4a5568;"
          " margin-top: 4px;'>Personen pro Gruppe:</p>",
          unsafe_allow_html=True,
      )
      num_per_group = st.number_input(
          "Personen pro Gruppe",
          min_value=2,
          max_value=10,
          value=st.session_state.num_per_group,
          step=1,
          key="num_per_group",
          label_visibility="collapsed",
      )
      num_total_groups = 3
    else:
      st.markdown(
          "<p style='font-size: 0.85rem; font-weight: 600; color: #4a5568;"
          " margin-top: 4px;'>Lerngruppe aufteilen in (Anzahl Gruppen):</p>",
          unsafe_allow_html=True,
      )
      num_total_groups = st.number_input(
          "Anzahl Gruppen",
          min_value=2,
          max_value=10,
          value=st.session_state.num_total_groups,
          step=1,
          key="num_total_groups",
          label_visibility="collapsed",
      )
      num_per_group = 3

  st.write("")

  st.markdown("**Umgang mit Resten**")
  rest_strategie = st.radio(
      "Strategie für Reste wählen",
      options=[
          "Rest gleichmäßig auf bestehende Gruppen aufteilen",
          "Rest als kleinere Gruppe zusammenfassen",
      ],
      key="selected_rest",
      label_visibility="collapsed",
  )

  st.write("")
  generate_btn = st.button(
      "🎲 Gruppen generieren & Präsentieren",
      type="primary",
      use_container_width=True,
  )

  if generate_btn:
    if len(anwesende_schueler) == 0:
      st.error("Bitte wähle mindestens einen anwesenden Lernenden aus!")
    else:
      st.session_state.last_kategorie = kategorie
      st.session_state.last_size_mode = size_mode
      st.session_state.last_num_per_group = num_per_group
      st.session_state.last_num_total_groups = num_total_groups
      st.session_state.last_rest_strategie = rest_strategie
      st.session_state.last_num_themen = num_themen
      st.session_state.generierte_gruppen = generiere_gruppen_dynamisch(
          anwesende_schueler,
          kategorie,
          size_mode,
          num_per_group,
          num_total_groups,
          rest_strategie,
          num_themen,
      )
      st.session_state.show_presentation = True
      st.rerun()