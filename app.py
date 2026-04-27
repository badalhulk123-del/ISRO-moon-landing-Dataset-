import streamlit as st
import pandas as pd
import plotly.express as px

# Page config
st.set_page_config(
    page_title="ISRO Moon Mission Dashboard",
    layout="wide",
    page_icon="🚀"
)

# Title
st.title("🚀 Chandrayaan-3 Mission Dashboard")
st.markdown("Data Analysis of ISRO Moon Landing")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("mission_data.csv")
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filters")

phase_filter = st.sidebar.multiselect(
    "Select Phase",
    options=df['phase'].unique(),
    default=df['phase'].unique()
)

filtered_df = df[df['phase'].isin(phase_filter)]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Final Altitude (km)", filtered_df['altitude'].iloc[-1])
col2.metric("Final Velocity (m/s)", filtered_df['velocity'].iloc[-1])
col3.metric("Fuel Remaining (%)", filtered_df['fuel_remaining'].iloc[-1])

st.divider()

# Altitude Chart
col1, col2 = st.columns(2)

with col1:
    fig1 = px.line(filtered_df, x='timestamp', y='altitude',
                   title="Altitude vs Time",
                   markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    fig2 = px.line(filtered_df, x='timestamp', y='velocity',
                   title="Velocity vs Time",
                   markers=True, color='phase')
    st.plotly_chart(fig2, use_container_width=True)

# Fuel chart
fig3 = px.area(filtered_df, x='timestamp', y='fuel_remaining',
               title="Fuel Consumption Over Time")
st.plotly_chart(fig3, use_container_width=True)

# Thruster Power
fig4 = px.bar(filtered_df, x='phase', y='thruster_power',
              title="Thruster Power by Phase", color='phase')
st.plotly_chart(fig4, use_container_width=True)

# Correlation Heatmap
st.subheader("📊 Correlation Analysis")

corr = filtered_df.corr(numeric_only=True)

fig5 = px.imshow(corr, text_auto=True, title="Feature Correlation Heatmap")
st.plotly_chart(fig5, use_container_width=True)

# Data Table
st.subheader("📄 Raw Data")
st.dataframe(filtered_df, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit")
