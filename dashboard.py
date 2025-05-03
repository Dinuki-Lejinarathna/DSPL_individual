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

rating_dist = filtered_df['grade'].value_counts().sort_index().reset_index()
rating_dist.columns = ['grade', 'Count']

fig3 = px.bar(rating_dist, x='grade', y='Count', color='grade',
              title='Star Rating Distribution of Accommodations')
st.plotly_chart(fig3, use_container_width=True)

#-------------------------------------------------------------------
# Visual 4: Map View

st.subheader("📍 Accommodation Locations Map")
st.map(filtered_df[['latitude', 'longitude']])

#-------------------------------------------------------------------

# Visual 5: Accommodation Count by District
# --------------------------------
st.subheader("🏢 Number of Accommodations by District")
count_by_district = filtered_df['district'].value_counts().reset_index()
count_by_district.columns = ['District', 'Number of Accommodations']

fig5 = px.bar(count_by_district, x='District', y='Number of Accommodations',
              color='District', title='Total Accommodations by District')
st.plotly_chart(fig5, use_container_width=True)

#----------------------------------------------------------------------------

# Visual 6: Line Chart - Average Room Capacity by Star Rating

st.subheader("📈 Average Room Capacity by Star Rating")

# Group by star rating and calculate average rooms
room_trend = (
    filtered_df.groupby('grade')['rooms']
    .mean()
    .reset_index()
    .sort_values(by='grade')
)

# Ensure proper order for plotting
star_order = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'UNRATED']
room_trend['grade'] = pd.Categorical(room_trend['grade'], categories=star_order, ordered=True)
room_trend = room_trend.sort_values('grade')

fig8 = px.line(room_trend, x='grade', y='rooms',
               markers=True, title='Average Room Capacity by Star Rating',
               labels={'rooms': 'Average Number of Rooms', 'grade': 'star rating'})

st.plotly_chart(fig8, use_container_width=True)

# Table View

st.subheader("📋 Accommodation Details Table")
st.dataframe(
    filtered_df[['hotel_id', 'name', 'type', 'grade', 'rooms', 'district', 'address']],
    use_container_width=True
)

# Footer
# --------------------------------
st.markdown("---")
st.markdown("Made by Dinuki Lejinarathna | Data Science Project Lifecycle | University of Westminster")
