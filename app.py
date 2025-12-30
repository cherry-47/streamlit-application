# APP VERSION 8: Visualizations (Bar Chart + Pie Chart) from the same DataFrame
# This whole cell is a complete Streamlit app.
# Copy EVERYTHING in this cell into a file named: app.py
# Then run in your terminal:
#     streamlit run app.py
#
# Tip: Streamlit reruns the script top-to-bottom whenever you change a widget.


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Charts", layout="wide")
st.title("Charts 📈")

# --- Dataset ---
np.random.seed(7)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun"]
stores = ["North", "South", "East", "West"]
fruits = ["Apple", "Banana", "Orange", "Mango"]

rows = []
for m in months:
    for s in stores:
        for f in fruits:
            rows.append({"month": m, "store": s, "fruit": f, "sales": int(np.random.randint(10, 101))})
df = pd.DataFrame(rows)

# --- Filters ---
month_choice = st.selectbox("Month:", ["All"] + months)
store_choices = st.multiselect("Stores:", stores, default=stores)

filtered = df.copy()
if month_choice != "All":
    filtered = filtered[filtered["month"] == month_choice]
filtered = filtered[filtered["store"].isin(store_choices)]

# --- Make a summary table: sales per fruit ---
summary = (
    filtered.groupby("fruit", as_index=False)["sales"]
    .sum()
    .sort_values("sales", ascending=False)
)

st.subheader("Sales by fruit (summary)")
st.dataframe(summary, use_container_width=True)

# --- BAR CHART ---
st.subheader("Bar chart: total sales per fruit")
# Streamlit can directly chart a DataFrame
bar_df = summary.set_index("fruit")  # index becomes x-axis labels
st.bar_chart(bar_df)  # y-axis is sales

# --- PIE CHART ---
st.subheader("Pie chart: sales share per fruit")

fig, ax = plt.subplots()
ax.pie(summary["sales"], labels=summary["fruit"], autopct="%1.1f%%", startangle=90)
ax.axis("equal")  # makes the pie a circle
st.pyplot(fig)
