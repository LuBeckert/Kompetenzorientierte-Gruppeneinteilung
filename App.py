import streamlit as st
import pandas as pd
import random

# -----------------------------------------------------------------------------
# 1. KONFIGURATION & CSS
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Gruppen-Generator", page_icon="👥", layout="wide")

st.markdown("""
    <style>
        [data-testid="stMainBlockContainer"] {
            max-width: 800px !important;
            margin-left: auto !important;
            margin-right: auto !important;
            padding-top: 2rem !important;
            padding-bottom: 3rem !important;
        }

        .centered-text {
            text-align: center !important;
        }

        div[data-testid="stVerticalBlock"] > div { 
            gap: 0.15rem !important; 
        }

        div[data-testid="stColumn"] { 
            display: flex !important;
            flex-direction: column !important;
            justify-content: center !important;
            align-items: center !important;
            height: 42px !important;
            padding: 0px 2px !important;
        }

        div[data-testid="stColumn"]:nth-child(2),
        div[data-testid="stColumn"]:nth-child(3) { 
            align-items: flex-start !important; 
            justify-content: center !important;
        }

        .table-header {
            font-weight: 700;
            color: #718096;
            font-size: 0.88rem;
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
            width: 100%;
        }

        div[data-testid="stColumn"]:nth-child(1) div[data-testid="stCheckbox"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            margin: 0 !important;
            padding-top: 6px !important;
            height: 100% !important;
        }
        
        div[data-testid="stCheckbox"] label {
            min-height: unset !important;
            padding: 0 !important;
            margin: 0 !important;
        }

        div[data-testid="stColumn"] button {
            height: 32px !important;
            min-height: 32px !important;
            max-height: 32px !important;
            padding: 0px 8px !important;
            border-radius: 6px !important;
            outline: none !important;
            box-shadow: none !important;
            margin: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        div[data-testid="stColumn"]:nth-child(4) button,
        div[data-testid="stColumn"]:nth-child(5) button,
        div[data-testid="stColumn"]:nth-child(6) button {
            width: 75px !important;
            min-width: 75px !important;
            max-width: 75px !important;
        }

        div[data-testid="stColumn"] button p {
            margin: 0 !important;
            padding: 0 !important;
            line-height: 1 !important;
            font-size: 0.88rem !important;
        }

        div[data-testid="stColumn"]:nth-child(2) button:disabled,
        div[data-testid="stColumn"]:nth-child(3) button:disabled {
            width: 100% !important;
            background-color: transparent !important;
            border: none !important;
            opacity: 1 !important;
            cursor: default !important;
            justify-content: flex-start !important;
        }

        div[data-testid="stColumn"] button:disabled p {
            color: #1a202c !important;
        }

        div[data-testid="stColumn"] button[data-testid="stBaseButton-tertiary"] {
            border: 1px solid #e2e8f0 !important;
            background-color: #f7fafc !important;
        }
        div[data-testid="stColumn"] button[data-testid="stBaseButton-tertiary"] p {
            color: #4a5568 !important;
        }
        div[data-testid="stColumn"] button[data-testid="stBaseButton-tertiary"]:hover {
            background-color: #edf2f7 !important;
        }

        div[data-testid="stColumn"] button[data-testid="stBaseButton-primary"] {
            border: 1px solid #66bb6a !important;
            background-color: #81c784 !important;
        }
        div[data-testid="stColumn"] button[data-testid="stBaseButton-primary"] p {
            color: #1b431e !important;
            font-weight: 700 !important;
        }

        .modus-box div[role="radiogroup"] {
            justify-content: center !important;
        }

        .summary-pill {
            background-color: #f8f9fa;
            color: #4a5568;
            border-radius: 5px;
            padding: 0px;
            text-align: center;
            font-size: 0.8rem;
            font-weight: 600;
            width: 75px !important;
            height: 28px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='centered-text'>👥 Intelligenter Gruppen-Generator</h1>", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# 2. HELPER FUNKTIONEN & CALLBACKS
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

def set_stufe(idx, neue_stufe):
    st.session_state.schueler_df.loc[idx, "Leistungsstufe"] = neue_stufe

def set_anwesend(idx, key):
    st.session_state.schueler_df.loc[idx, "Anwesend"] = st.session_state[key]

# -----------------------------------------------------------------------------
# 3. SESSION STATE INITIALISIERUNG
# -----------------------------------------------------------------------------
if "schueler_df" not in st.session_state:
    st.session_state.schueler_df = pd.DataFrame([
        {"Anwesend": True, "Vorname": "Anna", "Nachname": "Schmidt", "Leistungsstufe": "mittel"},
        {"Anwesend": True, "Vorname": "Ben", "Nachname": "Müller", "Leistungsstufe": "stark"},
        {"Anwesend": True, "Vorname": "Jonas", "Nachname": "Becker", "Leistungsstufe": "stark"},
        {"Anwesend": True, "Vorname": "Jonas", "Nachname": "Meier", "Leistungsstufe": "mittel"},
        {"Anwesend": True, "Vorname": "Emma", "Nachname": "Weber", "Leistungsstufe": "mittel"},
        {"Anwesend": True, "Vorname": "Felix", "Nachname": "Wagner", "Leistungsstufe": "schwach"},
    ])

if "show_presentation" not in st.session_state:
    st.session_state.show_presentation = False

# -----------------------------------------------------------------------------
# 4. PRÄSENTATIONSMODUS
# -----------------------------------------------------------------------------
if st.session_state.show_presentation and "generierte_gruppen" in st.session_state:
    st.button("⚙️ Zurück zur Bearbeitung", on_click=lambda: st.session_state.update({"show_presentation": False}))
    st.markdown("<h2 class='centered-text'>🎯 Gruppeneinteilung</h2>", unsafe_allow_html=True)
    st.write("")

    gruppen = st.session_state.generierte_gruppen
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
    
    uploaded_excel = st.file_uploader("📥 Excel-Liste hochladen (.xlsx, .xls)", type=["xlsx", "xls"])
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
                st.session_state.schueler_df = pd.DataFrame(new_rows)
                st.success(f"✅ {len(new_rows)} Schüler importiert!")
        except Exception as e:
            st.error(f"Fehler beim Einlesen: {e}")

    col_widths = [0.6, 2.2, 2.2, 1.0, 1.0, 1.0]
    
    # TABELLENKOPF
    h1, h2, h3, h4, h5, h6 = st.columns(col_widths)
    h1.markdown("<p class='table-header' style='text-align: center;'>Da?</p>", unsafe_allow_html=True)
    h2.markdown("<p class='table-header' style='text-align: left;'>Vorname</p>", unsafe_allow_html=True)
    h3.markdown("<p class='table-header' style='text-align: left;'>Nachname</p>", unsafe_allow_html=True)
    h4.markdown("<p class='table-header' style='text-align: center;'>schwach</p>", unsafe_allow_html=True)
    h5.markdown("<p class='table-header' style='text-align: center;'>mittel</p>", unsafe_allow_html=True)
    h6.markdown("<p class='table-header' style='text-align: center;'>stark</p>", unsafe_allow_html=True)

    # TABELLENZEILEN
    for idx, row in st.session_state.schueler_df.iterrows():
        c1, c2, c3, c4, c5, c6 = st.columns(col_widths)
        
        # Unique Stable Keys für Buttons & Checkboxen (Eindeutig pro Vor-/Nachname & Index)
        v_name_str = str(row['Vorname'])
        n_name_str = str(row['Nachname'])
        
        cb_key = f"anw_{idx}_{v_name_str}"
        c1.checkbox("", value=bool(row["Anwesend"]), key=cb_key, on_change=set_anwesend, args=(idx, cb_key), label_visibility="collapsed")
        
        c2.button(f"**{v_name_str}**", key=f"vn_{idx}_{v_name_str}", disabled=True)
        c3.button(f"{n_name_str}", key=f"nn_{idx}_{n_name_str}", disabled=True)
        
        aktuelle_stufe = row["Leistungsstufe"]

        # Stufen-Buttons mit explizitem Callback
        c4.button(
            "schwach", 
            key=f"btn_schwach_{idx}_{v_name_str}", 
            type="primary" if aktuelle_stufe == "schwach" else "tertiary",
            on_click=set_stufe,
            args=(idx, "schwach")
        )

        c5.button(
            "mittel", 
            key=f"btn_mittel_{idx}_{v_name_str}", 
            type="primary" if aktuelle_stufe == "mittel" else "tertiary",
            on_click=set_stufe,
            args=(idx, "mittel")
        )

        c6.button(
            "stark", 
            key=f"btn_stark_{idx}_{v_name_str}", 
            type="primary" if aktuelle_stufe == "stark" else "tertiary",
            on_click=set_stufe,
            args=(idx, "stark")
        )

    # AUSWERTUNG & STATISTIK
    anwesende_df = st.session_state.schueler_df[st.session_state.schueler_df["Anwesend"] == True].copy()
    if not anwesende_df.empty:
        vornamen_counts = anwesende_df["Vorname"].str.strip().value_counts()
        doppelte_vornamen = set(vornamen_counts[vornamen_counts > 1].index)
        anwesende_df["AnzeigeName"] = anwesende_df.apply(lambda r: format_student_name(r, doppelte_vornamen), axis=1)
        anwesende_schueler = anwesende_df.to_dict("records")
        
        anzahl_schwach = len(anwesende_df[anwesende_df["Leistungsstufe"] == "schwach"])
        anzahl_mittel = len(anwesende_df[anwesende_df["Leistungsstufe"] == "mittel"])
        anzahl_stark = len(anwesende_df[anwesende_df["Leistungsstufe"] == "stark"])
    else:
        anwesende_schueler = []
        anzahl_schwach = anzahl_mittel = anzahl_stark = 0

    # ABSCHLUSSZEILE (SUMMEN)
    st.markdown("<hr style='margin: 8px 0 8px 0; border: none; border-top: 1px solid #e6e6e6;'>", unsafe_allow_html=True)
    
    s1, s2, s3, s4, s5, s6 = st.columns(col_widths)
    s1.markdown(f"<div class='centered-text'><b>{len(anwesende_schueler)}</b>/{len(st.session_state.schueler_df)}</div>", unsafe_allow_html=True)
    s2.markdown("<div><b>Gesamt</b></div>", unsafe_allow_html=True)
    s3.markdown("", unsafe_allow_html=True)
    s4.markdown(f"<div class='summary-pill'>🔴 {anzahl_schwach}</div>", unsafe_allow_html=True)
    s5.markdown(f"<div class='summary-pill'>🟡 {anzahl_mittel}</div>", unsafe_allow_html=True)
    s6.markdown(f"<div class='summary-pill'>🟢 {anzahl_stark}</div>", unsafe_allow_html=True)

    st.divider()

    # MODUS-AUSWAHL & BUTTON
    st.markdown("<h3 class='centered-text'>⚙️ Zuteilungsmodus & Generierung</h3>", unsafe_allow_html=True)
    st.write("")

    with st.container():
        st.markdown("<div class='modus-box'>", unsafe_allow_html=True)
        modus = st.radio(
            "Wie sollen die Gruppen aufgeteilt werden?",
            options=[
                "3er-Gruppen (Rest als 4er-Gruppe)",
                "3er-Gruppen (Rest als 2er-Gruppen)",
                "2er-Teams nach Leistung (Differenziert: Stark + Schwach)"
            ],
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.write("")
    generate_btn = st.button("🎲 Gruppen generieren & Präsentieren", type="primary", use_container_width=True)

    # GRUPPEN-LOGIK
    def erstelle_3er_mit_4er(schueler_liste):
        random.shuffle(schueler_liste)
        namen = [s["AnzeigeName"] for s in schueler_liste]
        count = len(namen)
        if count == 0: return []
        num_full, remainder = count // 3, count % 3
        teams, idx = [], 0
        for _ in range(num_full):
            teams.append(namen[idx:idx+3])
            idx += 3
        if remainder == 2 and len(teams) >= 2:
            g1, g2 = teams.pop(), teams.pop()
            teams.append(g1 + [namen[idx]])
            teams.append(g2 + [namen[idx+1]])
        elif remainder == 2 and len(teams) == 1:
            teams.append(teams.pop() + [namen[idx], namen[idx+1]])
        elif remainder == 1 and len(teams) > 0:
            teams.append(teams.pop() + [namen[idx]])
        elif remainder > 0 and len(teams) == 0:
            teams.append(namen)
        return teams

    def erstelle_3er_mit_2er(schueler_liste):
        random.shuffle(schueler_liste)
        namen = [s["AnzeigeName"] for s in schueler_liste]
        count = len(namen)
        if count == 0: return []
        num_full, remainder = count // 3, count % 3
        teams, idx = [], 0
        for _ in range(num_full):
            teams.append(namen[idx:idx+3])
            idx += 3
        if remainder == 1 and len(teams) > 0:
            last_group = teams.pop()
            teams.append([last_group[0], last_group[1]])
            teams.append([last_group[2], namen[idx]])
        elif remainder == 2:
            teams.append([namen[idx], namen[idx+1]])
        elif remainder > 0 and len(teams) == 0:
            teams.append(namen)
        return teams

    def erstelle_2er_differenziert(schueler_liste):
        stark = [s["AnzeigeName"] for s in schueler_liste if s["Leistungsstufe"] == "stark"]
        mittel = [s["AnzeigeName"] for s in schueler_liste if s["Leistungsstufe"] == "mittel"]
        schwach = [s["AnzeigeName"] for s in schueler_liste if s["Leistungsstufe"] == "schwach"]
        random.shuffle(stark); random.shuffle(mittel); random.shuffle(schwach)
        teams = []
        while schwach and stark: teams.append([schwach.pop(0), stark.pop(0)])
        while schwach and mittel: teams.append([schwach.pop(0), mittel.pop(0)])
        while mittel and stark: teams.append([mittel.pop(0), stark.pop(0)])
        while len(stark) > 1: teams.append([stark.pop(0), stark.pop(0)])
        while len(mittel) > 1: teams.append([mittel.pop(0), mittel.pop(0)])
        while len(schwach) > 1: teams.append([schwach.pop(0), schwach.pop(0)])
        leftovers = stark + mittel + schwach
        if leftovers:
            if teams: teams[-1].extend(leftovers)
            else: teams.append(leftovers)
        return teams

    if generate_btn:
        if len(anwesende_schueler) == 0:
            st.error("Bitte wähle mindestens einen anwesenden Schüler aus!")
        else:
            if modus == "3er-Gruppen (Rest als 4er-Gruppe)":
                gruppen = erstelle_3er_mit_4er(anwesende_schueler)
            elif modus == "3er-Gruppen (Rest als 2er-Gruppen)":
                gruppen = erstelle_3er_mit_2er(anwesende_schueler)
            else:
                gruppen = erstelle_2er_differenziert(anwesende_schueler)
                
            st.session_state.generierte_gruppen = gruppen
            st.session_state.show_presentation = True
            st.rerun()