import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Page config

st.set_page_config(page_title="Sri Lanka Accommodation Dashboard", layout="wide")

# --------------------------------
# Load Data

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'cleaned_accommodation.csv')

@st.cache_data
def load_data():
    df = pd.read_csv(file_path)
    return df

df = load_data()

# --------------------------------
# Tabs

tab1, tab2 = st.tabs(["📊 Dashboard", "📘 About App"])

#TAB 1 ----------------------
with tab1:
    # Sidebar
    st.sidebar.title("🔎 Filter Options")
    districts = st.sidebar.multiselect("Select District(s)", df['district'].unique(), default=None)
    types = st.sidebar.multiselect("Select Accommodation Type(s)", df['type'].unique(), default=None)
    ratings = st.sidebar.multiselect("Select Star Ratings", df['grade'].unique(), default=None)

    # Filter Logic
    filtered_df = df.copy()
    if districts:
        filtered_df = filtered_df[filtered_df['district'].isin(districts)]
    if types:
        filtered_df = filtered_df[filtered_df['type'].isin(types)]
    if ratings:
        filtered_df = filtered_df[filtered_df['grade'].isin(ratings)]

    # Title
    st.title("Sri Lanka Accommodation Analysis Dashboard")
    st.markdown("This dashboard helps visualize accommodation distribution, types, and capacity across districts in Sri Lanka.")

    # Key Metrics
    st.subheader("📊 Key Stats")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Accommodations", filtered_df.shape[0])
    col2.metric("Total Rooms", int(filtered_df['rooms'].sum()))
    col3.metric("Districts Covered", filtered_df['district'].nunique())

    # Visual 1: Rooms by District
    st.subheader("🏙️ Total Rooms by District")
    rooms_by_district = filtered_df.groupby("district")["rooms"].sum().sort_values(ascending=False).reset_index()
    fig1 = px.bar(rooms_by_district, x="district", y="rooms", color="district",
                  labels={"rooms": "Number of Rooms"},
                  title="Total Number of Rooms by District",
                  hover_data=["rooms"])
    st.plotly_chart(fig1, use_container_width=True)

    # Visual 2: Accommodation Type Distribution
    st.subheader("🛏️ Accommodation Type Distribution")
    type_dist = filtered_df['type'].value_counts().reset_index()
    type_dist.columns = ['Accommodation Type', 'Count']
    fig2 = px.pie(type_dist, names='Accommodation Type', values='Count',
                  title='Accommodation Type Share', hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

    # Visual 3: Star Rating Breakdown
    st.subheader("⭐ Star Rating Breakdown")
    rating_dist = filtered_df['grade'].value_counts().sort_index().reset_index()
    rating_dist.columns = ['grade', 'Count']
    fig3 = px.bar(rating_dist, x='grade', y='Count', color='grade',
                  title='Star Rating Distribution of Accommodations',
                  hover_data=["Count"])
    st.plotly_chart(fig3, use_container_width=True)

    # Visual 4: Map View
    st.subheader("📍 Accommodation Locations Map")
    st.map(filtered_df[['latitude', 'longitude']])

    # Visual 5: Accommodation Count by District
    st.subheader("🏢 Number of Accommodations by District")
    count_by_district = filtered_df['district'].value_counts().reset_index()
    count_by_district.columns = ['District', 'Number of Accommodations']
    fig5 = px.bar(count_by_district, x='District', y='Number of Accommodations',
                  color='District', title='Total Accommodations by District')
    st.plotly_chart(fig5, use_container_width=True)

    # Visual 6: Line Chart - Average Room Capacity by Star Rating
    st.subheader("📈 Average Room Capacity by Star Rating")
    room_trend = (
        filtered_df.groupby('grade')['rooms']
        .mean()
        .reset_index()
        .sort_values(by='grade')
    )
    star_order = ['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'UNRATED']
    room_trend['grade'] = pd.Categorical(room_trend['grade'], categories=star_order, ordered=True)
    room_trend = room_trend.sort_values('grade')
    fig8 = px.line(room_trend, x='grade', y='rooms',
                   markers=True, title='Average Room Capacity by Star Rating',
                   labels={'rooms': 'Average Number of Rooms', 'grade': 'Star Rating'})
    st.plotly_chart(fig8, use_container_width=True)

    # Data Table
    st.subheader("📋 Accommodation Details Table")
    st.dataframe(
        filtered_df[['hotel_id', 'name', 'type', 'grade', 'rooms', 'district', 'address']],
        use_container_width=True
    )

    # Download Button
    st.download_button("📥 Download Filtered Data", filtered_df.to_csv(index=False), "filtered_data.csv")

    # Footer
    st.markdown("---")
    st.markdown("Made by Dinuki Lejinarathna | Data Science Project Lifecycle | University of Westminster")

# TAB 2----------------
with tab2:
    st.title("📘 About the Sri Lanka Accommodation Dashboard")

    st.markdown("""
    Welcome to the **Sri Lanka Accommodation Analysis Dashboard**! 🇱🇰  
    This interactive web app provides insights into registered accommodations across Sri Lanka using a cleaned dataset.

    ---

    ### 🎯 Purpose of the App

    This dashboard is designed to help:
    - **Travel planners** understand accommodation distribution.
    - **Policy makers** assess infrastructure density by district.
    - **Tourism analysts** explore star ratings and accommodation types.
    - **Researchers & Students** visualize accommodation trends geographically.

    ---

    ### 🛠️ How It Works

    **1. Filters:**  
    Use the **sidebar** to filter accommodations by:
    - **District**
    - **Type of Accommodation**
    - **Star Rating**

    **2. Visualizations:**  
    The main dashboard displays:
    - Total rooms by district
    - Accommodation type share
    - Star rating breakdown
    - A geolocation map of accommodations
    - District-wise counts
    - Average room size by star rating
    - Filtered data in table format

    **3. Download:**  
    You can export the filtered dataset using the **Download button**.

    ---

    ### 📂 Data Source

    The dataset includes:
    - Hotel ID, Name, Type, Grade (Star Rating), Room Count
    - District, Address, Latitude, and Longitude

    ---

    ### 👨‍🎓 Project Details

    **Developed by:** *Dinuki Lejinarathna*  
    **Module:** *Data Science Project Lifecycle*  
    **University:** *University of Westminster*

    Explore and enjoy! 🌍✨
    """)

