import streamlit as st
import pandas as pd
import plotly.express as px

# Load data from CSV file
def load_data():
    df = pd.read_csv('charts.csv')  # Update the path if needed
    return df

df = load_data()

# Define pages using st.subpage
page = st.sidebar.selectbox("Choose a Page", ["Dashboard", "Artist Stats", "Compare Artists"])

if page == "Dashboard":
    # Streamlit app for the Dashboard page
    st.title('Music Chart Dashboard')

    # Sidebar widgets for filtering
    st.sidebar.subheader('Filter Data')
    selected_artist = st.sidebar.selectbox('Select Artist:', df['artist'].unique())
    if selected_artist != 'All':
        filtered_data = df[df['artist'] == selected_artist]
    else:
        filtered_data = df

    selected_song = st.sidebar.selectbox('Select Song:', filtered_data['song'].unique())
    if selected_song != 'All':
        filtered_data = filtered_data[filtered_data['song'] == selected_song]

    # Display filtered data
    st.sidebar.write('Displaying data for', selected_artist, 'and', selected_song)
    st.sidebar.dataframe(filtered_data)

    # Line Chart
    st.subheader('Line Chart: Rank Over Time')
    line_chart = px.line(filtered_data, x='date', y='rank', color='song', title='Rank Over Time')
    st.plotly_chart(line_chart)

    # Donut Chart
    st.subheader('Donut Chart: Peak Rank Distribution')
    peak_rank_distribution = filtered_data['peak-rank'].value_counts().reset_index()
    peak_rank_distribution.columns = ['Peak Rank', 'Count']
    donut_chart = px.pie(peak_rank_distribution, names='Peak Rank', values='Count', hole=0.5, title='Peak Rank Distribution')
    st.plotly_chart(donut_chart)

elif page == "Artist Stats":
    # Streamlit app for the Artist Stats page
    st.title('Artist Stats')

    st.subheader('Select an Artist:')
    selected_artist = st.selectbox('Choose an Artist:', df['artist'].unique())

    artist_stats = df[df['artist'] == selected_artist]
    num_songs = len(artist_stats['song'].unique())
    total_weeks_on_board = [artist_stats['song'].unique()]['weeks-on-board'].sum()

    st.write(f"**Artist:** {selected_artist}")
    st.write(f"**Number of Songs:** {num_songs}")
    # st.write(f"**Total Weeks on Billboard:** {total_weeks_on_board}")

elif page == "Compare Artists":
    # Streamlit app for the Compare Artists page
    st.title('Compare Artists')

    st.subheader('Select a Year:')
    selected_year = st.selectbox('Choose a Year:', df['date'].str[0:4].unique())

    top_artists_by_year = df[df['date'].str.startswith(selected_year)]
    top_artists = top_artists_by_year.groupby('artist')['rank'].mean().reset_index().sort_values(by='rank')

    st.subheader(f'Top Artists in {selected_year}')
    bar_chart = px.bar(top_artists,
                        x='rank',
                        y='artist', 
                        orientation='h', 
                        title=f'Top Artists in {selected_year}',
                        height=700)
    st.plotly_chart(bar_chart)
