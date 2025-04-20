import streamlit as st
import pandas as pd
import numpy as np

st.title('Uber pickups in NYC')


#streamlit run "C:/Users/arpap/Documents/Arpapat/DADS NIDA/DADS 5001 Tools/streamlit/uber_pickups.py"

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
         'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

@st.cache_data
def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

# Create a text element and let the reader know the data is loading.
data_load_state = st.text('Loading data...')
# Load 10,000 rows of data into the dataframe.
data = load_data(10000)
# Notify the reader that the data was successfully loaded.
data_load_state.text('Loading data...done!')

#data

#st.subheader('Raw data')
#st.write(data)

if st.checkbox('Show raw data'):
    st.subheader('Raw data')
    st.write(data)

st.subheader('Number of pickups by hour')
hist_values = np.histogram(
    data[DATE_COLUMN].dt.hour, bins=24, range=(0,24))[0]
st.bar_chart(hist_values)

st.subheader('Map of all pickups')
st.map(data)


#hour_to_filter = 17
hour_to_filter = st.slider('hour', 0, 23, 17)  # min: 0h, max: 23h, default: 17h
filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
st.subheader(f'Map of all pickups at {hour_to_filter}:00')
st.map(filtered_data)


st.header("Exercise")

import pydeck as pdk
st.subheader ('1. Convert 2D map to 3D map using PyDeck')
st.subheader('3D Map of all pickups')
st.pydeck_chart(
    pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=40.76,
            longitude=-74,
            zoom=9,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                "HexagonLayer",
                data=data,
                get_position="[lon, lat]",
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                "ScatterplotLayer",
                data=data,
                get_position="[lon, lat]",
                get_color="[200, 30, 0, 160]",
                get_radius=200,
            ),
        ],
    )
)


st.subheader('2. Use Date input')
import datetime

d = st.date_input("When is your next Uber ride scheduled?", value=None)
st.write("Your next scheduled Uber ride is:", d)


st.subheader('3. Use SelectBox')

option = st.selectbox(
    "At what time is your next Uber scheduled?",
    ("00.01-06.00", "06.01-12.00", "12.01-18.00", "18.01-00.00"),
    index=None,
    placeholder="Select time...",
)
st.write("The time you selected:", option)


#conda install plotly
st.subheader('4. Use plotly')
import plotly.express as px

data['hour'] = data[DATE_COLUMN].dt.hour
fig = px.histogram(data, x='hour', nbins=24, title="Pickups by Hour")
st.plotly_chart(fig)

st.subheader('5. Click a button to increase the number X in the following message, "This page has run X times"')
if "counter" not in st.session_state:
    st.session_state.counter = 0

st.session_state.counter += 1

st.header(f"This page has run {st.session_state.counter} times.")
st.button("Run it again")