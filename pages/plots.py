import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.title("Plot Page")


if "df" in st.session_state:
    df = st.session_state["df"]


df = df[np.abs(df['depth_error']) < 0.5]

if df.empty:
    st.error("No diamonds satisfy the adjusted depth condition.")
    st.stop()

st.markdown("---")


total_rows = len(df)

cuts_qty = df['cut'].value_counts().reset_index()
cuts_qty.columns = ['cut', 'count']
fig1 = px.pie(cuts_qty, names='cut', values='count', title=f'Proportion of Diamonds by Cut (Total: {total_rows})')
st.plotly_chart(fig1)

st.markdown("---")


mean_by_cut = df.groupby('cut')['price'].mean().reset_index().sort_values('price')
fig2 = px.bar(mean_by_cut, x='cut', y='price', title="Mean Price by Cut", color='price', color_continuous_scale='Blues')
st.plotly_chart(fig2)


select_cut = st.selectbox("Select cut", df['cut'].unique())
filtered_cut = df[df['cut'] == select_cut]
avg_price = filtered_cut['price'].mean()
st.write(f"Average price for selected cut: ${avg_price:.2f}")

st.markdown("---")

st.subheader("Price range per cut")
fig_box = px.box(df, x='cut', y='price', color='cut',
                 title="Boxplot of Diamonds price range",
                 labels= {'cut':'Cut', 'price':'Price'})

st.plotly_chart(fig_box)


fig3 = px.scatter(df, x='carat', y='price', color='cut',
                  title="Price vs Carat",
                  labels={'carat': 'Carat', 'price': 'Price'},
                  opacity=0.6)
st.plotly_chart(fig3)

st.write("""
Diagrammet visar att priset ökar tydligt med karatvikten. Vid högre karat ses större spridning i pris, vilket tyder på att även slipning, färg och klarhet påverkar priset – särskilt för större diamanter.
""")

#st.markdown("---")
#fig3,ax3 = plt.subplots()
#ax3.scatter(df[])


