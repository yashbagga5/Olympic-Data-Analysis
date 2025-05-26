import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import os

# Read CSV files using correct filenames with double extension
df = pd.read_csv('./athlete_events.csv')
region_df = pd.read_csv('./noc_regions.csv')

df = preprocessor.preprocess(df,region_df)

st.sidebar.title("🏅 Olympics Analysis")
st.sidebar.image('https://upload.wikimedia.org/wikipedia/commons/thumb/5/5c/Olympic_rings_without_rims.svg/1200px-Olympic_rings_without_rims.svg.png', width=300)
user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal Tally 🏆','Overall Analysis 📊','Country-wise Analysis 🌍','Athlete wise Analysis 👥', 'About ℹ️')
)

if user_menu == 'Medal Tally 🏆':
    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)

    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'Overall' and selected_country == 'Overall':
        st.title("🏆 Overall Tally")
    if selected_year != 'Overall' and selected_country == 'Overall':
        st.title(f"🏆 Medal Tally in {str(selected_year)} Olympics")
    if selected_year == 'Overall' and selected_country != 'Overall':
        st.title(f"🏆 {selected_country} overall performance")
    if selected_year != 'Overall' and selected_country != 'Overall':
        st.title(f"🏆 {selected_country} performance in {str(selected_year)} Olympics")
    st.table(medal_tally)

if user_menu == 'Overall Analysis 📊':
    editions = df['Year'].unique().shape[0] - 1
    cities = df['City'].unique().shape[0]
    sports = df['Sport'].unique().shape[0]
    events = df['Event'].unique().shape[0]
    athletes = df['Name'].unique().shape[0]
    nations = df['region'].unique().shape[0]

    st.title("📊 Top Statistics")
    col1,col2,col3 = st.columns(3)
    with col1:
        st.header("🏛️ Editions")
        st.title(editions)
    with col2:
        st.header("🏙️ Hosts")
        st.title(cities)
    with col3:
        st.header("⚽ Sports")
        st.title(sports)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.header("🎯 Events")
        st.title(events)
    with col2:
        st.header("🌍 Nations")
        st.title(nations)
    with col3:
        st.header("👥 Athletes")
        st.title(athletes)

    nations_over_time = helper.data_over_time(df,'region')
    fig = px.line(nations_over_time, x="Edition", y="region")
    st.title("🌍 Participating Nations over the years")
    st.plotly_chart(fig)

    events_over_time = helper.data_over_time(df, 'Event')
    fig = px.line(events_over_time, x="Edition", y="Event")
    st.title("🎯 Events over the years")
    st.plotly_chart(fig)

    athlete_over_time = helper.data_over_time(df, 'Name')
    fig = px.line(athlete_over_time, x="Edition", y="Name")
    st.title("👥 Athletes over the years")
    st.plotly_chart(fig)

    st.title("📈 No. of Events over time(Every Sport)")
    fig,ax = plt.subplots(figsize=(20,20))
    x = df.drop_duplicates(['Year', 'Sport', 'Event'])
    ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
                annot=True)
    st.pyplot(fig)

    st.title("🏅 Most successful Athletes")
    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0,'Overall')

    selected_sport = st.selectbox('Select a Sport',sport_list)
    x = helper.most_successful(df,selected_sport)
    st.table(x)

if user_menu == 'Country-wise Analysis 🌍':
    st.sidebar.title('Country-wise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a Country',country_list)

    country_df = helper.yearwise_medal_tally(df,selected_country)
    fig = px.line(country_df, x="Year", y="Medal")
    st.title(f"🏆 {selected_country} Medal Tally over the years")
    st.plotly_chart(fig)

    st.title(f"🎯 {selected_country} excels in the following sports")
    pt = helper.country_event_heatmap(df,selected_country)
    fig, ax = plt.subplots(figsize=(20, 20))
    ax = sns.heatmap(pt,annot=True)
    st.pyplot(fig)

    st.title(f"👑 Top 10 athletes of {selected_country}")
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athlete wise Analysis 👥':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])

    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'],show_hist=False, show_rug=False)
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title("📊 Distribution of Age")
    st.plotly_chart(fig)

    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("📈 Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')

    st.title('📏 Height Vs Weight')
    selected_sport = st.selectbox('Select a Sport', sport_list)
    temp_df = helper.weight_v_height(df,selected_sport)
    fig,ax = plt.subplots()
    ax = sns.scatterplot(x=temp_df['Weight'], y=temp_df['Height'], hue=temp_df['Medal'], style=temp_df['Sex'], s=60)
    st.pyplot(fig)

    st.title("👥 Men Vs Women Participation Over the Years")
    final = helper.men_vs_women(df)
    fig = px.line(final, x="Year", y=["Male", "Female"])
    fig.update_layout(autosize=False, width=1000, height=600)
    st.plotly_chart(fig)

if user_menu == 'About ℹ️':
    st.title("ℹ️ About This Project")
    st.markdown("""
    ## 🏅 Olympics Data Analysis Web App

    This dashboard provides interactive visualizations and analysis of Olympic Games data, including medal tallies, country-wise and athlete-wise statistics, and more.

    **Features:**
    - 🏆 Medal tally by year and country
    - 📊 Overall Olympic statistics
    - 🌍 Country-wise and athlete-wise analysis
    - 📈 Visualizations for trends and distributions
    - 👥 Athlete age and gender distribution
    - 📏 Height vs. Weight scatterplots
    - 🎯 Interactive and user-friendly interface

    **Technologies Used:**
    - 🐍 Python 3
    - 🚀 Streamlit (for web dashboard)
    - 📊 Pandas (data manipulation)
    - 📈 Plotly & Seaborn (visualizations)
    - 🎨 Matplotlib (visualizations)

    **Usage Instructions:**
    1. 📥 Clone the repository and install the required dependencies from `requirements.txt`.
    2. 📁 Place the `athlete_events.csv` and `noc_regions.csv` files in the project directory.
    3. 🚀 Run the app using `streamlit run app.py`.
    4. 🎯 Use the sidebar to navigate between different analysis sections.

    **Data Sources:**
    - 📊 [athlete_events.csv](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)
    - 📊 [noc_regions.csv](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results)

    **Future Scope:**
    - 📈 Add more interactive visualizations and dashboards.
    - 🔄 Integrate real-time Olympic data updates.
    - 🤖 Implement machine learning models for medal predictions.
    - 🎯 Expand analysis to include Paralympic Games data.
    - 🔐 Add user authentication and personalized dashboards.
    
    **Author:**  
    - 👤 Name: YASH BAGGA  
    - 📧 Email: yashbagga5@gmail.com  
    - 💻 GitHub: [yashbagga5](https://github.com/yashbagga5)
    """)



