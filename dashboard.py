import streamlit as st
import pandas as pd
import plotly.express as px


# --------------------------------
# Page config
# --------------------------------
st.set_page_config(page_title="Sri Lanka Accommodation Dashboard", layout="wide")

# --------------------------------
# Load Data
# --------------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("D:\streamlit\DSPL_individual\cleaned_accommodation.csv")
    return df

df = load_data()

# --------------------------------
# Sidebar Filters
# --------------------------------
st.sidebar.title("🔎 Filter Options")

# District filter
districts = st.sidebar.multiselect("Select District(s)", df['district'].unique(), default=None)

# Type filter
types = st.sidebar.multiselect("Select Accommodation Type(s)", df['type'].unique(), default=None)

# Star Rating filter
ratings = st.sidebar.multiselect("Select Star Ratings", df['grade'].unique(), default=None)

# Filter logic
filtered_df = df.copy()
if districts:
    filtered_df = filtered_df[filtered_df['district'].isin(districts)]
if types:
    filtered_df = filtered_df[filtered_df['type'].isin(types)]
if ratings:
    filtered_df = filtered_df[filtered_df['grade'].isin(ratings)]

# --------------------------------
# Dashboard Title
# --------------------------------
st.title("Sri Lanka Accommodation Analysis Dashboard")
st.markdown("This dashboard helps visualize accommodation distribution, types, and capacity across districts in Sri Lanka.")

# --------------------------------
# Key Metrics
# --------------------------------
st.subheader("📊 Key Stats")

col1, col2, col3 = st.columns(3)

col1.metric("Total Accommodations", filtered_df.shape[0])
col2.metric("Total Rooms", int(filtered_df['rooms'].sum()))
col3.metric("Districts Covered", filtered_df['district'].nunique())

#--------------------------------------------------------------------

## Visual 1: Rooms by District

st.subheader("🏙️ Total Rooms by District")
rooms_by_district = filtered_df.groupby("district")["rooms"].sum().sort_values(ascending=False).reset_index()

fig1 = px.bar(rooms_by_district, x="district", y="rooms", color="district",
              labels={"rooms": "Number of Rooms"},
              title="Total Number of Rooms by District")
st.plotly_chart(fig1, use_container_width=True)

#--------------------------------------------------------------
# Visual 2: Accommodation Type Distribution

st.subheader("🛏️ Accommodation Type Distribution")
type_dist = filtered_df['type'].value_counts().reset_index()
type_dist.columns = ['Accommodation Type', 'Count']

fig2 = px.pie(type_dist, names='Accommodation Type', values='Count',
              title='Accommodation Type Share', hole=0.4)
st.plotly_chart(fig2, use_container_width=True)

#-------------------------------------------------------------
# Visual 3: Star Rating Distribution

st.subheader("⭐ Star Rating Breakdown")

rating_dist = df['grade'].value_counts().sort_index().reset_index()
rating_dist.columns = ['grade', 'Count']

fig3 = px.bar(rating_dist, x='grade', y='Count', color='grade',
              title='Star Rating Distribution of Accommodations')
st.plotly_chart(fig3, use_container_width=True)

#-------------------------------------------------------------------
# Visual 4: Map View

st.subheader("📍 Accommodation Locations Map")
st.map(filtered_df[['latitude', 'longitude']])

#-------------------------------------------------------------------
# Table View

st.subheader("📋 Accommodation Details Table")
st.dataframe(
    filtered_df[['hotel_id', 'name', 'type', 'grade', 'rooms', 'district', 'address']],
    use_container_width=True
)
