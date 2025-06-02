import streamlit as st
import pandas as pd
import plotly.express as px

if "df" in st.session_state:
    df = st.session_state["df"]

st.title("Diamant-Verktyget")



num_columns = df.select_dtypes(include='number').columns.tolist()

y_axis = st.selectbox("Välj Y-axel", num_columns, index = num_columns.index('carat') if 'carat' in num_columns else 0)
x_axis = st.selectbox("Välj X axel", num_columns, index = num_columns.index('price') if 'price' in num_columns else 1)

color_choice = st.selectbox("Färgval", df.columns.to_list(), index = df.columns.get_loc('cut') if 'cut' in df.columns else 0)

fig = px.scatter(
    df,
    x = x_axis,
    y = y_axis,
    color = color_choice,
    hover_data=["cut", "color", "clarity", "carat", "price"],
    title=f"{y_axis} vs {x_axis} färgad efter {color_choice}"
)

st.plotly_chart(fig, use_container_width=True)