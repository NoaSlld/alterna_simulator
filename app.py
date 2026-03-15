import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import sys
import os

# ajout du dossier src au path pour les imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.engine import AlternaSourcingEngine
from utils.report import ReportGenerator

# config de la page
st.set_page_config(page_title="Simulateur d'Offres Alterna Énergie", layout="wide")

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stMetric { padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); border: 1px solid #f0f2f6; }
    h1 { font-size: 2.2rem !important; padding-bottom: 1rem; color: #1E1E1E; }
    h2 { font-size: 1.6rem !important; margin-top: 2rem !important; border-bottom: 2px solid #f0f2f6; padding-bottom: 0.5rem; }
    </style>
    """, unsafe_allow_html=True)

st.title("Simulateur d'Offres - Alterna Énergie")
st.markdown("### Simulation de l'impact des variations du marché sur les offres")


# --- SIDEBAR UI ---
st.sidebar.header("Configuration de l'Offre")

with st.sidebar.expander("Coûts Marché & Réglementés", expanded=True):
    val_prix_gros = st.slider("Prix de Gros (€/MWh)", 0, 400, 100, step=5)
    val_turpe = st.slider("Acheminement / TURPE (€/MWh)", 0, 150, 45, step=1)
    val_taxes_fix = st.slider("Taxes (TICFE + CTA) (€/MWh)", 0, 100, 36, step=1)
    val_tva_rate = st.slider("TVA (%)", 0, 30, 20, step=1) / 100.0

with st.sidebar.expander("Stratégie Alterna", expanded=True):
    val_marge_cible = st.slider("Marge Brute Cible (€/MWh)", -50, 100, 25, step=1)
    maintien_prix = st.checkbox("Maintenir le prix final fixe", value=False)
    val_prix_bloque = st.slider("Prix Bloqué (€/MWh TTC)", 150, 400, 247, step=1) if maintien_prix else 247

with st.sidebar.expander("Prix Concurrents (TTC)", expanded=False):
    competitors = {
        "EDF": st.number_input("EDF (€/MWh)", value=251.60),
        "Engie": st.number_input("Engie (€/MWh)", value=225.00),
        "TotalEnergies": st.number_input("TotalEnergies (€/MWh)", value=215.00)
    }


# --- LOGIQUE MÉTIER ---
res = AlternaSourcingEngine.calculate_simulation(
    val_prix_gros, val_turpe, val_taxes_fix, val_tva_rate, 
    val_marge_cible, maintien_prix, val_prix_bloque
)


# --- LAYOUT PRINCIPAL ---
col1, col2 = st.columns([1, 1], gap="large")

# palettes de couleurs premium
color_palette = ['#FF9999', '#66B2FF', '#99FF99', '#FFCC99', '#c2c2f0']
competitor_colors = {
    "Alterna (Simulé)": "#FFCC99", 
    "EDF": "#66B2FF", 
    "Engie": "#99FF99", 
    "TotalEnergies": "#FF9999"
}

with col1:
    st.header("1. Décomposition du Prix")
    labels = ["Énergie", "TURPE", "Taxes", "Marge", "TVA"]
    values = [val_prix_gros, val_turpe, val_taxes_fix, res.nouvelle_marge, res.tva_montant]
    
    fig_pie = go.Figure(data=[go.Pie(
        labels=labels, 
        values=values, 
        hole=.4,
        marker=dict(colors=color_palette)
    )])
    fig_pie.update_layout(legend=dict(orientation="h", y=-0.2), template="plotly_white")
    st.plotly_chart(fig_pie, use_container_width=True)
    
    delta = res.nouvelle_marge - val_marge_cible
    st.metric("Marge Réelle", f"{res.nouvelle_marge:.2f} €/MWh", delta=f"{delta:.2f} €" if maintien_prix else None)
    if res.nouvelle_marge < 0: st.error("⚠️ Vente à perte !")

with col2:
    st.header("2. Benchmark Marché")
    df_bench = pd.DataFrame(AlternaSourcingEngine.get_bench_data(res.prix_vente_final_ttc, competitors))
    
    fig_bench = px.bar(
        df_bench, 
        x="Fournisseur", 
        y="Prix TTC", 
        color="Fournisseur",
        color_discrete_map=competitor_colors
    )
    fig_bench.update_layout(template="plotly_white")
    st.plotly_chart(fig_bench, use_container_width=True)

    st.markdown("**Positionnement :**")
    bench_text_pdf = []
    for name, price in competitors.items():
        diff = res.prix_vente_final_ttc - price
        txt = f"🟢 {-diff:.2f} € moins cher que {name}" if diff < 0 else f"🔴 {diff:.2f} € plus cher que {name}"
        st.write(txt)
        bench_text_pdf.append(txt)

st.markdown("---")
st.header("3. Structure des Coûts HT")
df_stack = pd.DataFrame({
    "Catégorie": ["Structure HT"], 
    "Énergie": [val_prix_gros], 
    "TURPE": [val_turpe], 
    "Taxes": [val_taxes_fix], 
    "Marge": [max(0, res.nouvelle_marge)]
})
fig_stack = px.bar(
    df_stack, 
    y="Catégorie", 
    x=["Énergie", "TURPE", "Taxes", "Marge"], 
    orientation='h', 
    height=200,
    color_discrete_map={
        "Énergie": color_palette[0],
        "TURPE": color_palette[1],
        "Taxes": color_palette[2],
        "Marge": color_palette[3]
    }
)
fig_stack.update_layout(template="plotly_white")
st.plotly_chart(fig_stack, use_container_width=True)


# --- EXPORT ---
if st.sidebar.button("📄 Rapport PDF"):
    with st.spinner("Génération..."):
        try:
            pdf_data = ReportGenerator.generate_pdf(res.params, [fig_pie, fig_bench, fig_stack], bench_text_pdf)
            st.sidebar.download_button("📥 Télécharger", data=pdf_data, file_name="apport_alterna.pdf", mime="application/pdf")
        except Exception as e: st.sidebar.error(f"Erreur : {e}")
