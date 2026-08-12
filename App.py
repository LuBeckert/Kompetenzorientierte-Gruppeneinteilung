import streamlit as st
import pandas as pd
import random
import json
import math
import extra_streamlit_components as stx

# -----------------------------------------------------------------------------
# 1. KONFIGURATION & CSS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Gruppeneinteilung", page_icon="👥", layout="wide")

st.markdown("""
    <style>
        /* Hauptcontainer */
        [data-testid="stMainBlockContainer"] {
            max-width: 900px !important;
            margin: 0 auto !important;
            align-items: center !important;
            padding-top: 1rem !important;
            padding-bottom: 3rem !important;
        }

        .centered-text { text-align: center !important; }

        /* --------------------------------------------------------------------- */
        /* DROPDOWN-MENÜS: Getrennte vertikale Positionen                       */
        /* --------------------------------------------------------------------- */
        .dropdown-links div[data-testid="stSelectbox"] {
            position: relative;
            top: -10px;
        }

        .dropdown-rechts div[data-testid="stSelectbox"] {
            position: relative;
            top: -10px;
        }

        /* --------------------------------------------------------------------- */
        /* TABELLENZEILEN - PERFEKTE HORIZONTALE FLUCHT                           */
        /* --------------------------------------------------------------------- */
        
        div[data-testid="stHorizontalBlock"] {
            align-items: center !important; 
        }

        div[data-testid="stColumn"] {
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            min-height: 40px !important;
            padding: 0 4px !important;
        }

        div[data-testid="stVerticalBlock"] > div {
            margin-bottom: 0 !important;
        }

        /* ----- SPALTE 1: Checkbox ----- */
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stCheckbox"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            height: 36px !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(1) div[data-testid="stCheckbox"] label {
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* ----- SPALTE 2 & 3: Vorname & Nachname ----- */
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) div[data-testid="stMarkdownContainer"],
        div[data-testid="stHorizontalBlock"] > div:nth-child(3) div[data-testid="stMarkdownContainer"] {
            display: flex !important;
            align-items: center !important;
            height: 36px !important; 
            margin: 0 !important;
            padding: 0 !important;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(2) p,
        div[data-testid="stHorizontalBlock"] > div:nth-child(3) p {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
            font-size: 0.95rem;
            color: #2d3748;
            white-space: nowrap;
        }

        /* ----- SPALTE 4, 5 & 6: Leistungs-Buttons ----- */
        div[data-testid="stHorizontalBlock"] > div:nth-child(n+4):nth-child(-n+6) div[data-testid="stButton"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            height: 36px !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        div[data-testid="stHorizontalBlock"] > div:nth-child(n+4):nth-child(-n+6) button {
            height: 32px !important;
            min-height: 32px !important;
            width: 100% !important;
            margin: 0 !important;
            padding: 0 4px !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border-radius: 6px !important;
            box-sizing: border-box !important;
            border: 1px solid #e2e8f0 !important;
            background-color: #f7fafc !important;
            color: #4a5568 !important;
        }

        div[data-testid="stHorizontalBlock"] > div:nth-child(n+4):nth-child(-n+6) button:hover {
            background-color: #edf2f7 !important;
        }

        div[data-testid="stHorizontalBlock"] > div:nth-child(n+4):nth-child(-n+6) button[kind="primary"],
        div[data-testid="stHorizontalBlock"] > div:nth-child(n+4):nth-child(-n+6) button[data-testid*="primary"] {
            border: 1px solid #ff4b4b !important;
            background-color: #ff4b4b !important;
        }

        div[data-testid="stHorizontalBlock"] > div:nth-child(n+4):nth-child(-n+6) button[kind="primary"] p,
        div[data-testid="stHorizontalBlock"] > div:nth-child(n+4):nth-child(-n+6) button[data-testid*="primary"] p {
            color: #ffffff !important;
            font-weight: 700 !important;
        }

        div[data-testid="stHorizontalBlock"] > div:nth-child(n+4):nth-child(-n+6) button p {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
            font-size: 0.85rem !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            color: inherit !important;
        }

        /* ----- SPALTE 7: Lösch-Button ----- */
        div[data-testid="stHorizontalBlock"] > div:nth-child(7) div[data-testid="stButton"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            height: 36px !important;
            margin: 0 !important;
            padding: 0 !important;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(7) button {
            height: 32px !important;
            min-height: 32px !important;
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            border-radius: 6px !important;
            border: 1px solid #e2e8f0 !important;
            background-color: #f7fafc !important;
        }
        div[data-testid="stHorizontalBlock"] > div:nth-child(7) button:hover {
            background-color: #fee2e2 !important;
            border-color: #f87171 !important;
        }

        .table-header {
            font-weight: 700;
            color: #718096;
            font-size: 0.88rem;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1.2 !important;
            width: 100%;
        }

        .summary-pill {
            background-color: #f8f9fa;
            color: #4a5568;
            border-radius: 5px;
            padding: 0px;
            text-align: center;
            font-size: 0.8rem;
            font-weight: 600;
            width: 100%;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
        }

        div[data-testid="stForm"] {
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            padding: 12px !important;
            margin-top: 1.2rem !important;
            margin-bottom: 1rem !important;
            background-color: #ffffff !important;
        }

        div[data-testid="stExpander"] {
            margin-top: 2rem !important;
            margin-bottom: 2.5rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. COOKIE MANAGER INITIALISIERUNG & LOGIK
# -----------------------------------------------------------------------------
cookie_manager = stx.CookieManager(key="schueler_cookie_mgr")

DEFAULT_SCHUELER = [
    {"Anwesend": True, "Vorname": "Schwach 1", "Nachname": "Schwach 1", "Leistungsstufe": "schwach"},
    {"Anwesend": True, "Vorname": "Schwach 2", "Nachname": "Schwach 2", "Leistungsstufe": "schwach"},
    {"Anwesend": True, "Vorname": "Schwach 3", "Nachname": "Schwach 3", "Leistungsstufe": "schwach"},
    {"Anwesend": True, "Vorname": "Schwach 4", "Nachname": "Schwach 4", "Leistungsstufe": "schwach"},
    {"Anwesend": True, "Vorname": "Mittel 1", "Nachname": "Mittel 1", "Leistungsstufe": "mittel"},
    {"Anwesend": True, "Vorname": "Mittel 2", "Nachname": "Mittel 2", "Leistungsstufe": "mittel"},
    {"Anwesend": True, "Vorname": "Mittel 3", "Nachname": "Mittel 3", "Leistungsstufe": "mittel"},
    {"Anwesend": True, "Vorname": "Stark 1", "Nachname": "Stark 1", "Leistungsstufe": "stark"},
    {"Anwesend": True, "Vorname": "Stark 2", "Nachname": "Stark 2", "Leistungsstufe": "stark"},
    {"Anwesend": True, "Vorname": "Stark 3", "Nachname": "Stark 3", "Leistungsstufe": "stark"},
]

STORAGE_KEY = "gruppen_klassen_liste_cookie"

# Beim ersten Laden kurz auf den CookieManager warten
raw_val = cookie_manager.get(STORAGE_KEY)
if raw_val is None and "cookie_initialized" not in st.session_state:
    st.session_state.cookie_initialized = True
    st.rerun()

def get_all_saved_classes():
    if "saved_classes_cache" in st.session_state:
        return st.session_state.saved_classes_cache

    val = cookie_manager.get(STORAGE_KEY)
    if val:
        try:
            data = json.loads(val) if isinstance(val, str) else val
            res = data if isinstance(data, dict) else {}
            st.session_state.saved_classes_cache = res
            return res
        except Exception:
            return {}
    return {}

if "schueler_df" not in st.session_state:
    st.session_state.schueler_df = pd.DataFrame(DEFAULT_SCHUELER)

st.session_state.schueler_df = st.session_state.schueler_df.reset_index(drop=True)

if "show_presentation" not in st.session_state:
    st.session_state.show_presentation = False
if "uploader_key" not in st.session_state:
    st.session_state.uploader_key = 0
if "current_loaded_class" not in st.session_state:
    st.session_state.current_loaded_class = None

# -----------------------------------------------------------------------------
# 3. HELPER FUNKTIONEN & GRUPPIERUNGS-LOGIK
# -----------------------------------------------------------------------------
def load_excel_flexible(file):
    raw_df = pd.read_excel(file, header=None)
    header_row_idx = None
    for idx, row in raw_df.iterrows():
        if idx > 15: break
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
    if not vorname: return nachname
    if not nachname: return vorname
    if vorname in duplicate_first_names:
        return f"{vorname} {nachname[0]}."
    return vorname

def get_anwesende_schueler():
    if "schueler_df" not in st.session_state or st.session_state.schueler_df.empty:
        return []
    anwesende_df = st.session_state.schueler_df[st.session_state.schueler_df["Anwesend"] == True].copy()
    if anwesende_df.empty:
        return []
    vornamen_counts = anwesende_df["Vorname"].str.strip().value_counts()
    doppelte_vornamen = set(vornamen_counts[vornamen_counts > 1].index)
    anwesende_df["AnzeigeName"] = anwesende_df.apply(lambda r: format_student_name(r, doppelte_vornamen), axis=1)
    return anwesende_df.to_dict("records")

def set_stufe(idx, neue_stufe):
    st.session_state.schueler_df.at[idx, "Leistungsstufe"] = neue_stufe
    st.rerun()

def set_anwesend(idx, key):
    st.session_state.schueler_df.at[idx, "Anwesend"] = st.session_state[key]
    st.rerun()

def delete_student(idx):
    st.session_state.schueler_df = st.session_state.schueler_df.drop(idx).reset_index(drop=True)
    st.rerun()

def add_student(vorname, nachname, stufe):
    new_row = pd.DataFrame([{
        "Anwesend": True,
        "Vorname": vorname.strip(),
        "Nachname": nachname.strip(),
        "Leistungsstufe": stufe
    }])
    st.session_state.schueler_df = pd.concat([st.session_state.schueler_df, new_row], ignore_index=True)

def generiere_gruppen_dynamisch(schueler_liste, kategorie, ziel_groesse, rest_strategie, num_themen=3):
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
        expert_display = [[f"{s['AnzeigeName']}" for s in members] for members in expert_groups.values()]
        
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
                
        if rest_strategie == "Rest als kleinere Gruppe zusammenfassen" and rest_schueler:
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
            "stammgruppen": stammgruppen
        }

    gruppen = []
    
    if kategorie == "Zufällig":
        random.shuffle(s_list)
        if rest_strategie == "Rest als kleinere Gruppe zusammenfassen":
            for i in range(0, n, ziel_groesse):
                chunk = s_list[i:i + ziel_groesse]
                gruppen.append(chunk)
        else:
            num_groups = max(1, round(n / ziel_groesse))
            gruppen = [[] for _ in range(num_groups)]
            for idx, student in enumerate(s_list):
                group_idx = idx % num_groups
                gruppen[group_idx].append(student)
                
    elif kategorie == "Kompetenzorientiert":
        stark = [s for s in s_list if s.get("Leistungsstufe") == "stark"]
        mittel = [s for s in s_list if s.get("Leistungsstufe", "mittel") == "mittel"]
        schwach = [s for s in s_list if s.get("Leistungsstufe", "schwach") == "schwach"]
        
        random.shuffle(stark)
        random.shuffle(mittel)
        random.shuffle(schwach)
        
        if rest_strategie == "Rest als kleinere Gruppe zusammenfassen":
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
        
        single_indices = [i for i, cap in enumerate(capacities) if cap == 1]
        for idx in single_indices:
            if stark:
                gruppen[idx].append(stark.pop(0))
            elif mittel:
                gruppen[idx].append(mittel.pop(0))
            elif schwach:
                gruppen[idx].append(schwach.pop(0))
                
        active_indices = [i for i, cap in enumerate(capacities) if len(gruppen[i]) < cap]
        
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

# -----------------------------------------------------------------------------
# 4. PRÄSENTATIONSMODUS
# -----------------------------------------------------------------------------
st.markdown("<h1 class='centered-text'>👥 Der intelligente Gruppen-Generator</h1>", unsafe_allow_html=True)

with st.expander("ℹ️ Anleitung & Rechtliche Hinweise"):
    st.markdown("""
    ### 🛠️ Kurzanleitung
    1. **Liste der Lernenden erstellen:** Lade eine Excel-Tabelle (.xlsx/.xls) hoch. Das Tool erkennt dabei eigenständig die passenden Spalten für Vor- und Nachnamen, um die Liste automatisch zu erstellen. Alternativ kannst du Lernende auch manuell über das Formular am Tabellenende hinzufügen.
    2. **Anwesenheit & Kompetenz:** 
        - Markiere anwesende Lernende über die Checkbox in der Spalte **„Da?“**.
        - Weise über die Buttons **schwach**, **mittel** oder **stark** das jeweilige Kompetenzniveau zu.
    3. **Klasse speichern (optional):** Klappe den Bereich *„Klasse speichern & laden“* auf, um deine Listen abzuspeichern und später wieder abzurufen.
    4. **Gruppen generieren:** Wähle unten den Zuteilungsmodus und klicke auf **„Gruppen generieren & Präsentieren“**.

    ---
    ### ⚖️ Disclaimer & Datenschutz
    * **Entwicklung & Transparenz:** Dieses Tool wurde von mir (als Nicht-IT-Experten) mithilfe von Künstlicher Intelligenz (KI) entwickelt. Die KI hat mir versichert, dass die Datenschutzstandards eingehalten werden; ich selbst übernehme jedoch **keinerlei Gewähr oder Haftung** für die Richtigkeit, Vollständigkeit oder Datensicherheit.
    * **Datenschutz & DSGVO:** Es findet **keine** zentrale Speicherung von Daten der Lernenden auf externen Servern statt. Alle eingegebenen Daten sowie gespeicherte Klassen werden ausschließlich im Browser gesichert. 
    * **Haftung:** Dieses Tool ist eine reine Arbeitshilfe zur Erleichterung der Gruppeneinteilung. Die Nutzung erfolgt vollständig auf eigene Verantwortung.
    """)

if st.session_state.show_presentation and "generierte_gruppen" in st.session_state:
    col_back, col_reshuffle = st.columns(2)
    with col_back:
        st.button("⚙️ Zurück zur Bearbeitung", on_click=lambda: st.session_state.update({"show_presentation": False}), use_container_width=True)
    with col_reshuffle:
        if st.button("🎲 Neu zusammenwürfeln", type="primary", use_container_width=True):
            current_anwesende = get_anwesende_schueler()
            if current_anwesende:
                kat = st.session_state.get("last_kategorie", "Zufällig")
                groesse = st.session_state.get("last_ziel_groesse", 3)
                strat = st.session_state.get("last_rest_strategie", "Rest gleichmäßig auf bestehende Gruppen aufteilen")
                num_t = st.session_state.get("last_num_themen", 3)
                st.session_state.generierte_gruppen = generiere_gruppen_dynamisch(
                    current_anwesende, kat, groesse, strat, num_t
                )
                st.rerun()

    st.markdown("<h2 class='centered-text' style='margin-top: 1rem;'>🎯 Gruppeneinteilung</h2>", unsafe_allow_html=True)
    st.write("")

    res_data = st.session_state.generierte_gruppen

    if isinstance(res_data, dict) and res_data.get("typ") == "gruppenpuzzle":
        tab_exp, tab_base = st.tabs(["🧩 Expertengruppen", "👥 Stammgruppen"])
        
        with tab_exp:
            cols = st.columns(min(3, len(res_data["experten"])))
            for i, members in enumerate(res_data["experten"], start=1):
                with cols[(i - 1) % len(cols)]:
                    st.markdown(f"### Thema {i}")
                    for m in members:
                        st.write(f"• **{m}**")
                    st.write("")
                    
        with tab_base:
            cols = st.columns(min(3, len(res_data["stammgruppen"])))
            for i, members in enumerate(res_data["stammgruppen"], start=1):
                with cols[(i - 1) % len(cols)]:
                    st.markdown(f"### Stammgruppe {i}")
                    for m in members:
                        st.write(f"• **{m}**")
                    st.write("")
    else:
        gruppen = res_data
        num_cols = min(3, len(gruppen)) if len(gruppen) > 0 else 1
        cols = st.columns(num_cols)
        
        for i, team in enumerate(gruppen, start=1):
            col_idx = (i - 1) % num_cols
            with cols[col_idx]:
                with st.container():
                    st.markdown(f"### Gruppe {i}")
                    for m in team:
                        st.write(f"• **{m}**")
                    st.write("")

# -----------------------------------------------------------------------------
# 5. LEHRERANSICHT
# -----------------------------------------------------------------------------
else:
    st.markdown("<h3 class='centered-text'>📋 Lerngruppe & Anwesenheit</h3>", unsafe_allow_html=True)
    st.write("")
    
    top_col1, top_col2 = st.columns([2.5, 1.5], gap="small")
    with top_col1:
        uploaded_excel = st.file_uploader(
            "Excel-Liste hochladen", 
            type=["xlsx", "xls"], 
            key=f"excel_uploader_{st.session_state.uploader_key}",
            label_visibility="collapsed"
        )
    with top_col2:
        st.markdown("<div style='height: 68px; display: flex; align-items: end;'>", unsafe_allow_html=True)
        if st.button("➕ Neue leere Liste erstellen", use_container_width=True):
            st.session_state.schueler_df = pd.DataFrame(columns=["Anwesend", "Vorname", "Nachname", "Leistungsstufe"])
            st.session_state.current_loaded_class = None
            st.session_state.expander_open = True
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

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
                    v_name = str(row[vorname_col]).strip() if vorname_col and pd.notna(row[vorname_col]) else ""
                    n_name = str(row[nachname_col]).strip() if nachname_col and pd.notna(row[nachname_col]) else ""
                    if v_name.capitalize() in ["Vorname", "Name"] or n_name.capitalize() in ["Nachname", "Name"]:
                        continue
                    if v_name or n_name:
                        stufe = str(row[stufe_col]).strip().lower() if stufe_col and pd.notna(row[stufe_col]) else "mittel"
                        if stufe not in ["stark", "mittel", "schwach"]: stufe = "mittel"
                        new_rows.append({"Anwesend": True, "Vorname": v_name, "Nachname": n_name, "Leistungsstufe": stufe})

            if new_rows:
                st.session_state.schueler_df = pd.DataFrame(new_rows).reset_index(drop=True)
                st.session_state.current_loaded_class = None
                st.session_state.uploader_key += 1
                st.rerun()
        except Exception as e:
            st.error(f"Fehler beim Einlesen: {e}")

    col_widths = [1.0, 2.0, 2.0, 1.5, 1.5, 1.5, 0.6]
    st.write("")

    header_cols = st.columns(col_widths)
    header_cols[0].markdown("<p class='table-header' style='text-align: left; position: relative; top: 0px; color: #3b3b3b;'>Da?</p>", unsafe_allow_html=True)
    header_cols[1].markdown("<p class='table-header' style='text-align: left; position: relative; top: -9px; color: #3b3b3b;'>Vorname</p>", unsafe_allow_html=True)
    header_cols[2].markdown("<p class='table-header' style='text-align: left; position: relative; top: -9px; color: #3b3b3b;'>Nachname</p>", unsafe_allow_html=True)
    header_cols[4].markdown("<p class='table-header' style='text-align: center; position: relative; top: 0px; color: #3b3b3b;'>Kompetenz</p>", unsafe_allow_html=True)

    if not st.session_state.schueler_df.empty:
        for idx, row in st.session_state.schueler_df.iterrows():
            c1, c2, c3, c4, c5, c6, c7 = st.columns(col_widths)
            
            v_name_str = str(row['Vorname'])
            n_name_str = str(row['Nachname'])
            aktuelle_stufe = str(row["Leistungsstufe"]).lower()

            with c1:
                cb_key = f"anw_{idx}_{v_name_str}"
                st.checkbox(
                    "", 
                    value=bool(row["Anwesend"]), 
                    key=cb_key, 
                    on_change=set_anwesend, 
                    args=(idx, cb_key), 
                    label_visibility="collapsed"
                )
            
            with c2:
                st.markdown(f"**{v_name_str}**")
                
            with c3:
                st.markdown(f"{n_name_str}")

            with c4:
                st.button(
                    "schwach", 
                    key=f"btn_schwach_{idx}_{v_name_str}", 
                    type="primary" if aktuelle_stufe == "schwach" else "tertiary",
                    on_click=set_stufe,
                    args=(idx, "schwach")
                )

            with c5:
                st.button(
                    "mittel", 
                    key=f"btn_mittel_{idx}_{v_name_str}", 
                    type="primary" if aktuelle_stufe == "mittel" else "tertiary",
                    on_click=set_stufe,
                    args=(idx, "mittel")
                )

            with c6:
                st.button(
                    "stark", 
                    key=f"btn_stark_{idx}_{v_name_str}", 
                    type="primary" if aktuelle_stufe == "stark" else "tertiary",
                    on_click=set_stufe,
                    args=(idx, "stark")
                )

            with c7:
                st.button(
                    "🗑️", 
                    key=f"btn_del_{idx}_{v_name_str}",
                    on_click=delete_student,
                    args=(idx,)
                )
    else:
        st.info("Die Liste ist aktuell leer. Füge unten einfach erste Lernende hinzu!")

    with st.form("add_student_form", clear_on_submit=True):
        st.markdown("<p style='font-size: 0.85rem; font-weight: 600; color: #718096; margin-bottom: 8px;'>➕ Lernende/n hinzufügen</p>", unsafe_allow_html=True)
        f_col1, f_col2, f_col3, f_col4 = st.columns([2.2, 2.2, 1.8, 2.2])
        new_vname = f_col1.text_input("Vorname", placeholder="Vorname", label_visibility="collapsed")
        new_nname = f_col2.text_input("Nachname", placeholder="Nachname", label_visibility="collapsed")
        new_stufe = f_col3.selectbox("Stufe", options=["mittel", "schwach", "stark"], label_visibility="collapsed")
        btn_add = f_col4.form_submit_button("Hinzufügen", use_container_width=True)
        
        if btn_add:
            if new_vname.strip() or new_nname.strip():
                add_student(new_vname, new_nname, new_stufe)
                st.rerun()

    anwesende_schueler = get_anwesende_schueler()
    
    if not st.session_state.schueler_df.empty:
        anwesende_df_stats = st.session_state.schueler_df[st.session_state.schueler_df["Anwesend"] == True]
        anzahl_schwach = len(anwesende_df_stats[anwesende_df_stats["Leistungsstufe"] == "schwach"])
        anzahl_mittel = len(anwesende_df_stats[anwesende_df_stats["Leistungsstufe"] == "mittel"])
        anzahl_stark = len(anwesende_df_stats[anwesende_df_stats["Leistungsstufe"] == "stark"])
    else:
        anzahl_schwach = anzahl_mittel = anzahl_stark = 0

    st.markdown("<hr style='margin: 12px 0 8px 0; border: none; border-top: 1px solid #e6e6e6;'>", unsafe_allow_html=True)
    
    s1, s2, s3, s4, s5, s6, s7 = st.columns(col_widths)
    s1.markdown(f"<div class='centered-text' style='padding-top: 0px;'><b>{len(anwesende_schueler)}</b>/{len(st.session_state.schueler_df)}</div>", unsafe_allow_html=True)
    s2.markdown("<b>Gesamt</b>", unsafe_allow_html=True)
    s3.markdown("")
    s4.markdown(f"<div class='summary-pill'>🔴 {anzahl_schwach}</div>", unsafe_allow_html=True)
    s5.markdown(f"<div class='summary-pill'>🟡 {anzahl_mittel}</div>", unsafe_allow_html=True)
    s6.markdown(f"<div class='summary-pill'>🟢 {anzahl_stark}</div>", unsafe_allow_html=True)
    s7.markdown("")

    saved_classes = get_all_saved_classes()
    class_names = list(saved_classes.keys())

    expander_title = "💾 Klasse speichern & laden"
    if st.session_state.current_loaded_class:
        expander_title += f" (Geladen: {st.session_state.current_loaded_class})"

    with st.expander(expander_title, expanded=st.session_state.get("expander_open", True)):
        col_left, col_right = st.columns(2, gap="large")
        
        with col_left:
            st.markdown("#### Klasse speichern / aktualisieren")
            if st.session_state.current_loaded_class:
                if st.button(f"✏️ '{st.session_state.current_loaded_class}' aktualisieren", type="primary", use_container_width=True):
                    saved_classes[st.session_state.current_loaded_class] = st.session_state.schueler_df.to_dict(orient="records")
                    st.session_state.saved_classes_cache = saved_classes
                    cookie_manager.set(STORAGE_KEY, json.dumps(saved_classes), max_age=31536000)
                    st.rerun()

            k_name_input = st.text_input("Klassenname eingeben:", placeholder="z. B. Klasse 8a", key="k_name_input")
            if st.button("💾 Als neue Klasse speichern", key="btn_save_class_act", use_container_width=True):
                clean_name = k_name_input.strip()
                if clean_name:
                    saved_classes[clean_name] = st.session_state.schueler_df.to_dict(orient="records")
                    st.session_state.saved_classes_cache = saved_classes
                    st.session_state.current_loaded_class = clean_name
                    cookie_manager.set(STORAGE_KEY, json.dumps(saved_classes), max_age=31536000)
                    st.rerun()

        with col_right:
            st.markdown("#### Gespeicherte Klassen")
            if class_names:
                selected_class = st.selectbox("Klasse auswählen:", options=class_names, key="selected_class_dropdown")
                b_load, b_del = st.columns(2, gap="small")
                with b_load:
                    if st.button("📥 Laden", key="btn_load_class_act", use_container_width=True):
                        st.session_state.schueler_df = pd.DataFrame(saved_classes[selected_class]).reset_index(drop=True)
                        st.session_state.current_loaded_class = selected_class
                        st.rerun()
                with b_del:
                    if st.button("🗑️ Löschen", key="btn_del_class_act", use_container_width=True):
                        if selected_class in saved_classes:
                            del saved_classes[selected_class]
                            st.session_state.current_loaded_class = None
                            st.session_state.saved_classes_cache = saved_classes
                            cookie_manager.set(STORAGE_KEY, json.dumps(saved_classes), max_age=31536000)
                            st.rerun()

    st.divider()

    st.markdown("<h3 class='centered-text'>⚙️ Zuteilungsmodus & Generierung</h3>", unsafe_allow_html=True)
    st.write("")

    kategorie = st.radio(
        "Art der Gruppeneinteilung",
        options=["Zufällig", "Kompetenzorientiert", "Gruppenpuzzle"],
        horizontal=True
    )

    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="dropdown-links">', unsafe_allow_html=True)
        if kategorie == "Gruppenpuzzle":
            ziel_groesse = 3
            num_themen = st.selectbox(
                "Anzahl der Themen (Expertengruppen)",
                options=[2, 3, 4, 5, 6],
                index=1
            )
        else:
            num_themen = 3
            ziel_groesse = st.selectbox(
                "Gewünschte Gruppengröße",
                options=[2, 3, 4, 5],
                format_func=lambda x: f"{x}er-Gruppen"
            )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="dropdown-rechts">', unsafe_allow_html=True)
        rest_strategie = st.selectbox(
            "Umgang mit unvollständigen Resten",
            options=[
                "Rest gleichmäßig auf bestehende Gruppen aufteilen",
                "Rest als kleinere Gruppe zusammenfassen"
            ]
        )
        st.markdown('</div>', unsafe_allow_html=True)

    st.write("")
    generate_btn = st.button("🎲 Gruppen generieren & Präsentieren", type="primary", use_container_width=True)

    if generate_btn:
        if len(anwesende_schueler) == 0:
            st.error("Bitte wähle mindestens einen anwesenden Lernenden aus!")
        else:
            st.session_state.last_kategorie = kategorie
            st.session_state.last_ziel_groesse = ziel_groesse
            st.session_state.last_rest_strategie = rest_strategie
            st.session_state.last_num_themen = num_themen
            st.session_state.generierte_gruppen = generiere_gruppen_dynamisch(
                anwesende_schueler, 
                kategorie, 
                ziel_groesse, 
                rest_strategie,
                num_themen
            )
            st.session_state.show_presentation = True
            st.rerun()