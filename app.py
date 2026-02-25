import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import plotly.graph_objects as go

# ==========================================
# 1. KONFIGURACE A STYLY
# ==========================================
st.set_page_config(page_title="Energie Prahy | Interaktivní historie", page_icon="💡", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #f8f9fa; color: #333333; }
    h1, h2, h3 { color: #2c3e50; }
    .timeline-card {
        background: #ffffff; padding: 30px; border-radius: 15px;
        box-shadow: 0 10px 20px rgba(0, 0, 0, 0.05);
        border-left: 8px solid #005b96;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        margin-bottom: 20px;
    }
    .timeline-card:hover { transform: translateY(-5px); box-shadow: 0 15px 25px rgba(0, 0, 0, 0.1); border-left: 8px solid #ffaa00; }
    .era-title { color: #005b96; font-family: 'Segoe UI', sans-serif; font-size: 2em; font-weight: 800; margin-bottom: 5px; }
    .era-dates { color: #e17055; font-weight: 700; font-size: 1.2em; margin-bottom: 15px; }
    .era-text { font-size: 1.1em; line-height: 1.7; color: #555555; text-align: justify; }
    div[data-testid="stMetricValue"] { font-size: 1.5rem; }
</style>
""", unsafe_allow_html=True)

st.title("💡 Krevní oběh metropole: Vývoj pražské energetiky")
st.markdown(
    "Prozkoumejte interaktivní časovou osu. Od prvních Křižíkových obloukovek až po dnešní chytré sítě. **Rolujte dolů a objevujte historii, která pohání naše město.**")
st.write("---")

# ==========================================
# SEKCE I: Počátky elektrifikace (1880–1918)
# ==========================================
col_text1, col_img1 = st.columns([2, 1])

with col_text1:
    st.markdown("""
    <div class="timeline-card">
        <div class="era-title">I. Počátky elektrifikace v Praze</div>
        <div class="era-dates">⏳ cca 1880–1918</div>
        <div class="era-text">
            Počátky elektrifikace v Praze spadají do posledních dvou dekád 19. století a úzce souvisejí s nástupem druhé průmyslové revoluce. Elektrická energie byla zpočátku využívána především pro veřejné osvětlení a demonstrační projekty, které měly technologický i symbolický význam. Klíčovou postavou tohoto období byl <b>František Křižík</b>, který se zasloužil o rozvoj obloukového osvětlení a o zavedení prvních elektrických zařízení v Praze. Elektrifikace však nebyla od počátku koncipována jako jednotný systém. Vznikaly izolované lokální zdroje – malé parní elektrárny zásobující omezené oblasti města stejnosměrným proudem o nízkém napětí.<br><br>
            Z technologického hlediska bylo toto období charakterizováno omezeným dosahem přenosu energie, vysokými ztrátami a absencí standardizace napěťových hladin. Stejnosměrné soustavy, inspirované především koncepcí <b>Thomase Edisona</b>, byly vhodné pro krátké vzdálenosti, avšak jejich technické limity postupně vyvolaly potřebu přechodu ke střídavé soustavě, jejíž princip rozvíjel <b>Nikola Tesla</b>. Praha tak na přelomu století vstoupila do období technologické transformace, kdy se lokální zdroje začaly postupně integrovat a vznikala potřeba centralizovanější infrastruktury.<br><br>
            Elektrifikace města měla nejen technický, ale i urbanistický a ekonomický dopad – umožnila rozvoj elektrických tramvají, prodloužení provozní doby průmyslových podniků a zvýšení bezpečnosti veřejného prostoru díky stabilnějšímu osvětlení. Toto období lze tedy charakterizovat jako fázi experimentální a fragmentované infrastruktury, která vytvořila technologický základ pro pozdější centralizovanou energetickou soustavu 20. století.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_img1:
    st.write("")
    st.image(
        "krizik_o.jpg",
        caption="František Křižík – český Edison", use_container_width=True)

st.markdown("### 1️⃣ Válka proudů: DC vs. AC")
df_acdc = pd.DataFrame({
    "Vlastnost": ["Maximální dosah přenosu", "Možnost transformace napětí", "Typické ztráty", "Vhodnost pro město"],
    "⚡ Stejnosměrná soustava (DC - Křižík)": ["Cca 2 km (omezeno ztrátami)", "Nemožná (zásadní nevýhoda)",
                                              "Vysoké při delším vedení", "Lokální (zdroj musí být v bloku budov)"],
    "🌊 Střídavá soustava (AC - Tesla)": ["Stovky kilometrů (díky VVN)", "Snadná (pomocí transformátorů)",
                                         "Nízké při přenosu velmi vysokého napětí",
                                         "Plošná (jedna velká elektrárna pro město)"]
})
st.table(df_acdc.set_index("Vlastnost"))
st.info(
    "💡 **Didaktické okénko:** Křižík byl zarytým zastáncem stejnosměrného proudu. Proto musely vznikat malé elektrárny přímo v centru (např. na Žižkově). Nakonec ale zvítězila AC technologie, která umožnila postavit velkou Holešovickou elektrárnu bezpečně dál od centra.")

st.markdown("### 2️⃣ Rozvoj prvních zdrojů v Praze")
st.markdown(
    "Posouvejte posuvníkem a sledujte, jak se v čase objevovaly první elektrické instalace na mapě tehdejší Prahy.")
map_data = pd.DataFrame([
    {"name": "První Křižíkovy obloukovky", "lat": 50.087, "lon": 14.430, "year": 1885, "color": [255, 170, 0],
     "info": "Osvětlení nádraží a obchodů"},
    {"name": "První elektrárna Žižkov", "lat": 50.085, "lon": 14.450, "year": 1889, "color": [255, 75, 75],
     "info": "Městská elektrárna (DC)"},
    {"name": "Křižíkova el. dráha (Letná)", "lat": 50.098, "lon": 14.425, "year": 1891, "color": [0, 200, 100],
     "info": "První pražská tramvaj"},
    {"name": "Holešovická elektrárna", "lat": 50.106, "lon": 14.440, "year": 1900, "color": [0, 91, 150],
     "info": "První moderní elektrárna (AC)"}
])
selected_year = st.slider("Vyberte rok (období I.):", 1880, 1905, 1885)
filtered_data = map_data[map_data['year'] <= selected_year]

layer = pdk.Layer('ScatterplotLayer', data=filtered_data, get_position='[lon, lat]', get_color='color', get_radius=250,
                  filled=True, pickable=True)
view_state = pdk.ViewState(latitude=50.095, longitude=14.435, zoom=12.5, pitch=0)
st.pydeck_chart(pdk.Deck(map_provider="carto", map_style="light", initial_view_state=view_state, layers=[layer],
                         tooltip={"html": "<b>{name}</b><br>{info}"}))
st.write("---")

# ==========================================
# SEKCE II: Centralizace (1918–1945)
# ==========================================
col_img2, col_text2 = st.columns([1, 2])

with col_text2:
    st.markdown("""
    <div class="timeline-card">
        <div class="era-title">II. Centralizace a meziválečný rozvoj</div>
        <div class="era-dates">⏳ 1918–1945</div>
        <div class="era-text">
            Období mezi lety 1918–1945 představuje v dějinách pražské energetiky zásadní strukturální zlom. Zatímco před první světovou válkou byla elektrická síť tvořena převážně lokálními a technologicky omezenými zdroji, meziválečné období přineslo proces centralizace výroby a standardizace distribuční soustavy. Elektrická infrastruktura se postupně proměnila z fragmentovaného systému na koordinovanou městskou síť schopnou pokrývat rostoucí průmyslové i obytné potřeby hlavního města.<br><br>
            Klíčovou roli v tomto procesu sehrála výstavba velkokapacitních zdrojů, zejména <b>Holešovická elektrárna</b>, která se stala technologickým symbolem centralizované výroby elektřiny pro Prahu. Zavedení parních turbín s vyšší účinností oproti starším parním strojům umožnilo koncentrovat výrobu do několika velkých zdrojů místo mnoha malých lokálních elektráren. Současně docházelo k postupnému sjednocování napěťových hladin a budování rozvoden, které umožňovaly efektivnější transformaci a distribuci energie do jednotlivých městských částí.<br><br>
            Z technického hlediska bylo toto období charakterizováno růstem instalovaného výkonu, zvyšováním provozních tlaků páry, lepší regulací výroby a vznikem organizovaného dispečerského řízení. Elektrická síť se začala koncipovat jako celek, nikoli jako soubor izolovaných uzlů. Rostoucí elektrifikace domácností, rozvoj průmyslu i expanze elektrické trakce vytvářely tlak na stabilitu a spolehlivost systému, což vedlo k budování záložních kapacit a propojení jednotlivých částí sítě.<br><br>
            Meziválečné období tak představuje fázi technologické konsolidace: elektrická energie se stává standardní součástí městského života a energetická infrastruktura získává podobu, která již nese znaky moderního energetického systému – centralizovaného, regulovaného a výkonově dimenzovaného podle dlouhodobého plánování.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_img2:
    st.write("")
    st.image("hol_trznice.jpg",
             caption="Holešovická Tržnice", use_container_width=True)

st.markdown("### 3️⃣ Vývoj topologie sítě: Od fragmentace k centralizaci")
st.markdown("Přepínejte mezi modely a všimněte si, jak se síť propojila (uzly a spojnice) a jak funguje zálohování.")

network_mode = st.radio("Zvolte model sítě:", ["Kolem roku 1900 (Fragmentace)", "Kolem roku 1935 (Centralizace)"],
                        horizontal=True)
fig = go.Figure()

if "1900" in network_mode:
    edges_x = [2, 1, None, 2, 3, None, 8, 7, None, 8, 9, None, 5, 4, None, 5, 6, None]
    edges_y = [8, 9, None, 8, 7, None, 8, 9, None, 8, 7, None, 2, 1, None, 2, 1, None]
    nodes_x = [2, 8, 5, 1, 3, 7, 9, 4, 6]
    nodes_y = [8, 8, 2, 9, 7, 9, 7, 1, 1]
    node_color = ['red', 'red', 'red', 'blue', 'blue', 'blue', 'blue', 'blue', 'blue']
    node_size = [25, 25, 25, 15, 15, 15, 15, 15, 15]
    node_text = ["Malá el. A", "Malá el. B", "Malá el. C", "Odběr", "Odběr", "Odběr", "Odběr", "Odběr", "Odběr"]
    st.info(
        "💡 **Rok 1900:** Malé lokální zdroje (červené) napájí jen své nejbližší okolí. Zásadní nevýhoda: když má jeden zdroj poruchu, jeho spotřebitelé jsou ve tmě. Nelze si vzájemně vypomoci.")
else:
    edges_x = [5, 3, None, 5, 7, None, 3, 7, None, 0, 3, None, 3, 1, None, 3, 3, None, 3, 5, None, 7, 5, None, 7, 7,
               None, 7, 9, None]
    edges_y = [9, 5, None, 9, 5, None, 5, 5, None, 10, 5, None, 5, 2, None, 5, 2, None, 5, 2, None, 5, 2, None, 5, 2,
               None, 5, 2, None]
    nodes_x = [5, 0, 3, 7, 1, 3, 5, 7, 9]
    nodes_y = [9, 10, 5, 5, 2, 2, 2, 2, 2]
    node_color = ['darkred', 'darkred', 'orange', 'orange', 'blue', 'blue', 'blue', 'blue', 'blue']
    node_size = [40, 35, 25, 25, 15, 15, 15, 15, 15]
    node_text = ["Holešovice (Hlavní)", "Ervěnice (Dálkový)", "Rozvodna Střed", "Rozvodna Jih", "Odběr", "Odběr",
                 "Odběr", "Odběr", "Odběr"]
    st.success(
        "💡 **Rok 1935:** Velké zdroje (tmavě červené) přenáší výkon do uzlových rozvoden (oranžové), které jsou propojené do sítě. Spotřebitelé mají garantovanou zálohu.")

fig.add_trace(go.Scatter(x=edges_x, y=edges_y, mode='lines', line=dict(width=2, color='#888'), hoverinfo='none'))
fig.add_trace(go.Scatter(x=nodes_x, y=nodes_y, mode='markers+text', text=node_text, textposition="bottom center",
                         marker=dict(size=node_size, color=node_color), hoverinfo='none',
                         textfont=dict(size=12, color='black')))
fig.update_layout(height=400, margin=dict(l=0, r=0, t=20, b=20), xaxis=dict(visible=False), yaxis=dict(visible=False),
                  plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 4️⃣ Kouzlo transformátoru: Proč potřebujeme vysoké napětí?")
st.markdown(
    "Při přenosu stejného výkonu vede vyšší napětí k menšímu proudu. A protože ztráty rostou s *druhou mocninou* proudu ($P_{ztráta} = R \cdot I^2$), transformace napětí je absolutně klíčová pro přenos na delší vzdálenosti.")

voltage_options = {"220 V (Lokální, 1890)": 220, "3 kV (Městské linky, 1910)": 3000, "22 kV (Pražská síť, 1925)": 22000,
                   "100 kV (Linka Ervěnice, 1929)": 100000}
selected_v_label = st.select_slider("Zvolte napětí na přenosové lince:", options=list(voltage_options.keys()),
                                    value="22 kV (Pražská síť, 1925)")
selected_v = voltage_options[selected_v_label]

power = 10000000  # 10 MW
current = power / selected_v

if selected_v == 220:
    distance, loss_relative, color = "Max. 1 km", "Extrémní (Kabel by se roztavil)", "inverse"
elif selected_v == 3000:
    distance, loss_relative, color = "Cca 10 km", "Vysoké (vhodné jen po městě)", "normal"
elif selected_v == 22000:
    distance, loss_relative, color = "Cca 50 km", "Nízké (standardní distribuce)", "normal"
else:
    distance, loss_relative, color = "Stovky kilometrů", "Zanedbatelné (propojení regionů)", "normal"

c1, c2, c3 = st.columns(3)
c1.metric("Proud protékající drátem", f"{current:,.0f} Ampér", delta_color=color)
c2.metric("Úroveň tepelných ztrát v síti", loss_relative)
c3.metric("Efektivní dosah přenosu", distance)
st.write("---")

# ==========================================
# SEKCE III: Socialismus (1948–1989)
# ==========================================
col_text3, col_img3 = st.columns([2, 1])

with col_text3:
    st.markdown("""
    <div class="timeline-card">
        <div class="era-title">III. Socialismus a vznik centralizované přenosové soustavy</div>
        <div class="era-dates">⏳ 1948–1989</div>
        <div class="era-text">
            Období po roce 1948 představuje v historii pražské energetické infrastruktury další zásadní transformaci. Zatímco meziválečná centralizace byla především městským a technologickým procesem, poválečný vývoj probíhal v kontextu státního plánování a silné centralizace energetiky na úrovni celého Československa. Energetická infrastruktura Prahy se postupně začlenila do jednotné přenosové soustavy s vysokonapěťovými hladinami 110 kV, 220 kV a později 400 kV.<br><br>
            Rozhodujícím rysem tohoto období byla koncentrace výroby do velkých zdrojů mimo území hlavního města. Praha se z výrobního centra postupně proměnila v převážně odběrovou oblast napojenou na regionální a státní zdroje, včetně jaderných elektráren a velkých tepelných bloků. Budování nadřazené přenosové soustavy umožnilo efektivnější sdílení výkonu, zálohování a vyrovnávání zatížení mezi regiony.<br><br>
            Technologicky se infrastruktura vyznačovala robustností, redundancí a postupným zaváděním dálkového řízení. Rozvodny se staly klíčovými uzly, kde docházelo k transformaci mezi napěťovými hladinami a řízení toků energie. Rozvoj teplárenství a kogeneračních zdrojů přinesl zvýšení energetické účinnosti v městském prostředí, zejména díky kombinované výrobě elektřiny a tepla.<br><br>
            Toto období lze charakterizovat jako fázi maximální centralizace, kdy byla energetická infrastruktura řízena plánovaně, s důrazem na výkonovou bezpečnost a stabilitu, méně však na flexibilitu či tržní efektivitu. Vznikla síť, která strukturálně připomínala hierarchický systém – velké zdroje → přenosová soustava → regionální rozvodny → distribuční síť → konečný odběratel.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_img3:
    st.write("")
    st.image("socialismus.jpg",
             caption="Elektrárna za Socialismu", use_container_width=True)

st.markdown("### 5️⃣ Hierarchický model sítě: Cesta od elektrárny do zásuvky")
st.markdown("Přehled vrstev socialistické energetické kaskády:")

df_hier = pd.DataFrame({
    "Úroveň sítě": ["⚡ Level 1: Velké zdroje", "🗼 Level 2: Přenosová soustava", "🏢 Level 3: Regionální rozvodny",
                    "🔌 Level 4: Distribuční síť"],
    "Role v systému": ["Srdce sítě", "Páteřní dálnice", "Kruhové objezdy", "Kapiláry města"],
    "Typické napětí / Zdroje": ["Mělník, Tušimice, Dukovany", "400 kV (případně 220 kV)", "110 kV",
                                "22 kV / 400 V / 230 V"],
    "Hlavní funkce": ["Masivní výroba energie ze strategických surovin.",
                      "Dálkový transport výkonu napříč státem s minimálními ztrátami.",
                      "Snižování napětí a distribuce energie do jednotlivých čtvrtí Prahy.",
                      "Finální rozvod do ulic, podniků a zásuvek v domácnostech."]
})
st.table(df_hier.set_index("Úroveň sítě"))

st.markdown("### 6️⃣ Robustnost systému: Simulace výpadku")
st.markdown(
    "Socialistická síť kladla obrovský důraz na spolehlivost. Zkuste vypnout hlavní vedení z Mělníka a podívejte se, jak síť zareaguje.")

outage_sim = st.toggle("🔥 Vypnout hlavní vedení z elektrárny Mělník")
fig3 = go.Figure()

nodes_x, nodes_y = [2, 0, 3, 5], [8, 8, 4, 1]
node_texts = ["Zdroj 1: Mělník", "Zdroj 2: Tušimice", "Rozvodna Praha", "Konečný odběratel"]
node_colors = ['#2c3e50', '#2c3e50', '#e17055', '#3498db']

if not outage_sim:
    edges_x, edges_y = [2, 3, None, 0, 3, None, 3, 5, None], [8, 4, None, 8, 4, None, 4, 1, None]
    edge_colors = ['green', 'rgba(128,128,128,0.3)', 'green']
    st.success(
        "✅ **Normální provoz:** Praha je primárně napájena z blízkého zdroje (Mělník). Severočeská elektrárna Tušimice slouží jako záloha a posílá energii jinam.")
else:
    edges_x, edges_y = [2, 3, None, 0, 3, None, 3, 5, None], [8, 4, None, 8, 4, None, 4, 1, None]
    edge_colors = ['red', 'green', 'green']
    node_colors[0] = 'red'
    st.error(
        "🚨 **Výpadek!** Vedení z Mělníka selhalo. Okamžitě přebírá zátěž záložní vedení z Tušimic. Spotřebitel v Praze vůbec nic nepozná.")

for i in range(3):
    fig3.add_trace(go.Scatter(x=[edges_x[i * 3], edges_x[i * 3 + 1]], y=[edges_y[i * 3], edges_y[i * 3 + 1]],
                              mode='lines', line=dict(width=5, color=edge_colors[i], dash='solid' if edge_colors[
                                                                                                         i] != 'rgba(128,128,128,0.3)' else 'dash'),
                              hoverinfo='none'))

fig3.add_trace(go.Scatter(x=nodes_x, y=nodes_y, mode='markers+text', text=node_texts, textposition="top center",
                          marker=dict(size=[40, 40, 30, 20], color=node_colors, line=dict(width=2, color='white')),
                          hoverinfo='none', textfont=dict(size=14, color='black')))
fig3.update_layout(height=400, margin=dict(l=0, r=0, t=20, b=0), xaxis=dict(visible=False), yaxis=dict(visible=False),
                   plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
st.plotly_chart(fig3, use_container_width=True)
st.write("---")

# ==========================================
# SEKCE IV: Liberalizace (1990–2010)
# ==========================================
col_img4, col_text4 = st.columns([1, 2])

with col_text4:
    st.markdown("""
    <div class="timeline-card">
        <div class="era-title">IV. Liberalizace a modernizace energetické infrastruktury</div>
        <div class="era-dates">⏳ 1990–2010</div>
        <div class="era-text">
            Transformace energetického sektoru po roce 1989 představuje strukturální i technologický přelom. Z vertikálně integrovaného a státem řízeného systému se energetika postupně přetváří do modelu založeného na oddělení výroby, přenosu, distribuce a obchodu s elektřinou. Tento proces byl výrazně ovlivněn evropskou legislativou a požadavky na otevření trhu s elektřinou.<br><br>
            V pražském kontextu získává klíčovou roli distribuční společnost <b>PRE distribuce</b>, která spravuje distribuční síť na území hlavního města. Zatímco přenosová soustava je provozována společností <b>ČEPS</b>, distribuce se zaměřuje na provoz a údržbu městských rozvoden, trafostanic a kabelových vedení.<br><br>
            <b>Technologicky je toto období charakterizováno několika zásadními trendy:</b><br>
            • <b>Kabelizace městské sítě</b> – postupný přechod od nadzemního vedení k podzemním kabelům zvyšuje spolehlivost dodávky, snižuje poruchovost a zlepšuje estetický i urbanistický charakter města.<br>
            • <b>Digitalizace řízení</b> – zavádění SCADA systémů, dálkového monitoringu a automatizace umožňuje rychlejší detekci poruch a efektivnější řízení toků energie.<br>
            • <b>Zvyšování kvality dodávky</b> – důraz na parametry jako SAIDI a SAIFI (ukazatele délky a četnosti přerušení dodávky).<br>
            • <b>Modernizace rozvoden</b> – náhrada starších technologií plynem izolovanými rozvodnami (GIS), kompaktnější řešení vhodná pro městské prostředí.<br><br>
            Energetická infrastruktura se v tomto období transformuje z robustního, výkonově orientovaného systému na síť optimalizovanou z hlediska efektivity, spolehlivosti a ekonomiky provozu. Dochází k výraznému posunu v řízení – místo centrálního plánování dominuje regulovaný trh, investiční rozhodování a důraz na nákladovou efektivitu.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_img4:
    st.write("")
    st.image("čez.jpeg",
             caption="ČEZ", use_container_width=True)

st.markdown("### 7️⃣ Rozpad vertikální integrace (Unbundling)")
st.markdown(
    "Zvolte období a podívejte se, jak se změnil trh s elektřinou. Všimněte si rozdílu mezi **fyzickým tokem** (kudy teče proud) a **obchodním tokem** (komu platíte).")

market_era = st.radio("Vyberte uspořádání trhu:",
                      ["Před rokem 1989 (Centrálně řízený monopol)", "Po roce 1995 (Liberalizovaný a oddělený trh)"],
                      horizontal=True)

fig_market = go.Figure()

if "1989" in market_era:
    # Model Monopolu
    fig_market.add_trace(
        go.Scatter(x=[2, 8], y=[2, 2], mode='lines', line=dict(width=5, color='#7f8c8d'), hoverinfo='none'))
    fig_market.add_trace(go.Scatter(
        x=[2, 8], y=[2, 2], mode='markers+text',
        text=["<b>Státní monopol</b><br>(Výroba + Přenos + Distribuce)", "<b>Odběratel</b><br>(Zákazník)"],
        textposition="top center",
        marker=dict(size=[60, 40], color=['#c0392b', '#2980b9'], symbol='square'),
        hoverinfo='none', textfont=dict(size=14, color='black')
    ))
    st.error("🏢 **Jeden státní podnik ovládal vše.** Zákazník si nemohl vybrat, od koho elektřinu koupí.")
else:
    # Model Liberalizovaného trhu
    # Fyzický tok (plná čára)
    fig_market.add_trace(go.Scatter(x=[1, 4, 7, 9.5], y=[3, 3, 3, 3], mode='lines', line=dict(width=5, color='#7f8c8d'),
                                    name='Fyzický tok elektřiny'))
    # Obchodní tok (čárkovaná čára přes Obchodníka)
    fig_market.add_trace(
        go.Scatter(x=[1, 5.25, 9.5], y=[3, 1, 3], mode='lines', line=dict(width=3, color='#f39c12', dash='dash'),
                   name='Finanční tok (Nákup/Prodej)'))

    # Uzly
    nodes_x = [1, 4, 7, 5.25, 9.5]
    nodes_y = [3, 3, 3, 1, 3]
    texts = [
        "<b>Výrobci</b><br>(Konkurence)",
        "<b>Přenos</b><br>(ČEPS - Monopol)",
        "<b>Distribuce</b><br>(PRE - Monopol)",
        "<b>Obchodník</b><br>(Konkurence / Burza)",
        "<b>Odběratel</b><br>(Zákazník)"
    ]
    colors = ['#27ae60', '#e67e22', '#e67e22', '#f1c40f', '#2980b9']

    fig_market.add_trace(go.Scatter(
        x=nodes_x, y=nodes_y, mode='markers+text', text=texts,
        textposition=["top center", "top center", "top center", "bottom center", "top center"],
        marker=dict(size=40, color=colors, symbol='square'),
        hoverinfo='none', textfont=dict(size=13, color='black'), showlegend=True
    ))
    st.success(
        "⚖️ **Oddělený trh (Unbundling).** Dráty (Přenos a Distribuce) zůstávají přirozeným monopolem. Ale energii samotnou si kupujete od Obchodníka, který ji soutěží u Výrobců na burze.")

fig_market.update_layout(
    height=300,
    xaxis=dict(visible=False, range=[0, 11]),
    yaxis=dict(visible=False, range=[0, 5]),
    plot_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=0, r=0, t=10, b=10),
    legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
)
st.plotly_chart(fig_market, use_container_width=True)


# ==========================================
# SEKCE V: Smart Grids (2010 - Současnost)
# ==========================================
col_text5, col_img5 = st.columns([1.5, 1])

with col_text5:
    st.markdown("""
    <div class="timeline-card">
        <div class="era-title">V. Digitalizace a decentralizace: éra Smart Grids</div>
        <div class="era-dates">⏳ 2010–současnost</div>
        <div class="era-text">
            Po roce 2010 vstupuje pražská energetická infrastruktura do fáze kvalitativní proměny. Dochází k postupnému narušení tradičního jednosměrného modelu toku energie (výroba → přenos → distribuce → spotřeba) a k nástupu decentralizovaných zdrojů, zejména fotovoltaických elektráren na střechách budov.<br><br>
            <b>Městská distribuční síť se musí adaptovat na:</b><br>
            • Obousměrné toky energie (prosumer model)<br>
            • Výkyvy výroby z obnovitelných zdrojů<br>
            • Zvyšující se zatížení v důsledku elektromobility<br>
            • Požadavky na flexibilitu a řízení špiček<br><br>
            Smart Grid není pouze technologická inovace, ale systémová změna, která integruje energetiku s informačními a komunikačními technologiemi. Zavádění chytrých měřidel umožňuje detailní monitoring spotřeby a vytváří předpoklady pro dynamické tarify a agregaci flexibility.<br><br>
            Současná infrastruktura je charakterizována jako <b>kyber-fyzický systém</b>, kde jsou fyzické energetické toky řízeny digitální vrstvou dat, algoritmů a dispečerských rozhodnutí. To klade nové nároky na kybernetickou bezpečnost, ochranu dat a odolnost systému vůči externím hrozbám.<br><br>
            Praha tak vstupuje do fáze, kdy energetická infrastruktura přestává být pouze podpůrným technickým systémem a stává se aktivním prvkem městského plánování a udržitelného rozvoje.
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_img5:
    st.write("")
    st.image("FVE.jpg",
             caption="FVE", use_container_width=True)

st.markdown("### 9️⃣ Simulace fotovoltaiky v Praze (tzv. Kachní křivka)")
st.markdown(
    "Vyzkoušejte si, co se stane se spotřebou ze sítě, když si Pražané na střechy nainstalují masivní množství solárních panelů. V poledne hrozí obří přetoky do sítě!")

c_pv1, c_pv2 = st.columns(2)
pv_percent = c_pv1.slider("Podíl domácností s FVE (%)", 0, 100, 10, step=5)
pv_kw = c_pv2.slider("Průměrný výkon jedné FVE instalace (kW)", 2, 10, 5)

total_households = 600000
total_pv_mw = (total_households * (pv_percent / 100) * pv_kw) / 1000

hours = np.arange(24)
base_load = 600 + 200 * np.sin(np.pi * (hours - 6) / 12)
pv_production = np.zeros(24)
pv_production[6:19] = total_pv_mw * np.sin(np.pi * (hours[6:19] - 6) / 12)
net_load = base_load - pv_production

fig_pv = go.Figure()
fig_pv.add_trace(
    go.Scatter(x=hours, y=base_load, mode='lines', name='Běžná spotřeba města', line=dict(color='gray', dash='dash')))
fig_pv.add_trace(
    go.Scatter(x=hours, y=pv_production, mode='lines', name='Výroba ze slunce (FVE)', line=dict(color='#ffcc00')))
fig_pv.add_trace(go.Scatter(x=hours, y=net_load, mode='lines', name='Zbytkové zatížení sítě (Net Load)',
                            line=dict(color='red', width=3)))

fig_pv.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), xaxis_title="Hodina", yaxis_title="Výkon (MW)",
                     legend=dict(yanchor="bottom", y=0.01, xanchor="left", x=0.01))
st.plotly_chart(fig_pv, use_container_width=True)

min_net_load = np.min(net_load)
if min_net_load < 0:
    st.error(
        f"🚨 **Varování pro síť!** V poledne dochází k masivnímu přetoku {abs(min_net_load):.0f} MW zpět do sítě. Hrozí napěťová nestabilita. Jsou potřeba baterie!")
else:
    st.success(
        f"✅ **Síť je stabilní.** Instalovaný výkon FVE v Praze je {total_pv_mw:.0f} MW. Zbytkové zatížení nepadá do mínusu.")

st.markdown("### 🔟 Elektromobilita a Špičková zátěž")
st.markdown(
    "Elektromobily mohou síť zkolabovat, pokud všichni nabíjí po příjezdu z práce. Zapněte 'Řízené nabíjení' (Smart Charging) a podívejte se, jak Smart Grids řeší problém.")

c_ev1, c_ev2, c_ev3 = st.columns([2, 2, 1])
num_evs = c_ev1.slider("Počet EV v Praze", 0, 500000, 50000, step=10000)
simul_pct = c_ev2.slider("Souběžnost (kolik aut se nabíjí naráz) %", 10, 100, 30, step=10)
smart_charge = c_ev3.toggle("🔋 Zapnout řízené nabíjení (Smart Charging)", value=False)

ev_power_mw = num_evs * (simul_pct / 100) * 11 / 1000
ev_load = np.zeros(24)

if not smart_charge:
    ev_load[17:22] = ev_power_mw
    st.warning("⚠️ **Hloupé nabíjení:** Všichni nabíjí v 18:00. Vzniká masivní nová špička, kabely se mohou přehřát.")
else:
    ev_load[0:6] = ev_power_mw / 2
    ev_load[22:24] = ev_power_mw / 2
    st.success(
        "🧠 **Řízené nabíjení:** Auta komunikují se sítí. Nabíjení se odloží na noc, kdy je elektřina levná a síť prázdná.")

total_load_ev = base_load + ev_load

fig_ev = go.Figure()
fig_ev.add_trace(go.Scatter(x=hours, y=base_load, mode='lines', name='Základní spotřeba města', stackgroup='one',
                            line=dict(color='lightgray')))
fig_ev.add_trace(
    go.Scatter(x=hours, y=ev_load, mode='lines', name='Spotřeba EV', stackgroup='one', line=dict(color='#3498db')))
fig_ev.update_layout(height=350, margin=dict(l=20, r=20, t=30, b=20), xaxis_title="Hodina", yaxis_title="Výkon (MW)",
                     legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01))
st.plotly_chart(fig_ev, use_container_width=True)

st.write("---")

# ==========================================
# ZÁVĚR: GRAF SPOTŘEBY
# ==========================================
st.subheader("📈 Závěrem: Jak rostl hlad Prahy po energii (1890–2020)")
years = list(range(1890, 2030, 10))
consumption = [5, 15, 30, 60, 120, 250, 480, 850, 1500, 2200, 3100, 3800, 4000, 3950]
df = pd.DataFrame({"Rok": years, "Spotřeba (GWh)": consumption}).set_index("Rok")
st.line_chart(df, y="Spotřeba (GWh)", color="#e17055")