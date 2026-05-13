import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.title("Brooklyn Bridge Pedestrian Dashboard")
st.subheader("Explore hourly, daily, and weekly pedestrian traffic patterns")


df = pd.read_csv("brooklyn_bridge_pedestrians.csv")

df = df.rename(columns={
    "Pedestrians": "pedestrians",
    "Towards Manhattan": "to_manhattan",
    "Towards Brooklyn": "to_brooklyn"
})

df["hour_beginning"] = pd.to_datetime(df["hour_beginning"])
df = df.sort_values("hour_beginning")
df = df.set_index("hour_beginning")


st.sidebar.header("Dashboard Controls")

view = st.sidebar.radio(
    "Choose traffic view",
    ["Hourly", "Daily", "Weekly"]
)

weather_options = ["All"] + sorted(df["weather_summary"].dropna().unique())

selected_weather = st.sidebar.selectbox(
    "Choose weather",
    weather_options
)

if selected_weather != "All":
    df = df[df["weather_summary"] == selected_weather]


traffic_df = df[["pedestrians", "to_manhattan", "to_brooklyn"]]

if view == "Daily":
    traffic_df = traffic_df.resample("D").sum()
elif view == "Weekly":
    traffic_df = traffic_df.resample("W").sum()


col1, col2 = st.columns(2)

with col1:
    st.metric("Total Pedestrians", f"{traffic_df['pedestrians'].sum():,.0f}")

with col2:
    st.metric("Average Pedestrians", f"{traffic_df['pedestrians'].mean():,.0f}")


fig, ax = plt.subplots(figsize=(12, 5))

ax.plot(
    traffic_df.index,
    traffic_df["pedestrians"],
    color="steelblue",
    label="Total pedestrians"
)

ax.plot(
    traffic_df.index,
    traffic_df["to_manhattan"],
    color="gold",
    label="To Manhattan"
)

ax.plot(
    traffic_df.index,
    traffic_df["to_brooklyn"],
    color="lightpink",
    label="To Brooklyn"
)

ax.set_title(view + " Pedestrian Traffic on the Brooklyn Bridge")
ax.set_xlabel("Date")
ax.set_ylabel("Pedestrian Count")
ax.legend()

plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)


st.write("Dataset preview")
st.dataframe(df.head())
