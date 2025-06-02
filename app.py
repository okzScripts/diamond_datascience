import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Oskar Diamond Trading", layout="wide")
st.title("💎 Oskar Diamond Trading Inc Ltd. - för Guldfynd")

if "df" in st.session_state:
    df_clean = st.session_state["df"]
    st.success("✅ Tidigare uppladdad data har laddats in")
else:
    uploaded_file = st.file_uploader("📂 Ladda upp en CSV med diamantdata", type=["csv"])

    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
        except Exception as e:
            st.error(f"Ett fel uppstod vid inläsning av data:\n{e}")
        else:
            df_clean = df.dropna(subset=['x', 'y', 'z', 'depth'])
            df_clean['depth_calc'] = 200 * (df_clean['z'] / (df_clean['x'] + df_clean['y']))
            tolerance = 0.5
            df_clean = df_clean[(df_clean['depth'] - df_clean['depth_calc']).abs() <= tolerance]
            df_clean = df_clean.dropna(subset=['cut', 'color', 'clarity'])
            st.session_state["df"] = df_clean
            st.success("✅ Data uppladdad och rensad")
    else:
        st.info("👈 Ladda upp en CSV-fil för att börja")
        st.stop()

col1, col2 = st.columns([1, 2])
with col1:
    st.success("✅ Data uppladdad och rensad")
    st.metric("Antal rader i originaldata", len(df))
    st.metric("Rader kvar efter rensning", len(df_clean))

with col2:
    st.dataframe(df_clean.head(50), use_container_width=True)

    st.divider()

st.divider()
st.subheader("📊 Djupjämförelse")
fig, ax = plt.subplots(figsize=(10, 4))
ax.hist(df_clean["depth"] - df_clean["depth_calc"], bins=40, color="#4e79a7", edgecolor='white')
ax.set_title("Skillnad mellan 'depth' och beräknad 'depth_calc'")
ax.set_xlabel("Depth - Depth_calc")
ax.set_ylabel("Antal")
st.pyplot(fig)
