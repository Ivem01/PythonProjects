import streamlit as st
import requests
import pandas as pd

api_key = "22197413c4a7e0410dae4c1f97143184"  

st.set_page_config("Simple Weather App", layout="centered")
st.title("Simple Weather App")

city = st.text_input("Enter city name:", placeholder="Eg: Milan")

if st.button("Check Weather"):
    if city:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == 200:

            st.subheader(f"Weather in {data['name']}, {data['sys']['country']}")

            col1, col2 = st.columns(2)

            with col1 :
                st.metric("Temperature",f"{data['main']['temp']}°C")
                st.metric("Humidity", f"{data['main']['humidity']}%")

            with col2:
                st.metric("Weather", f"{data['weather'][0]['description'].capitalize()}")
                st.metric("Wind Speed", f"{data['wind']['speed']} km/h")

            map_data = pd.DataFrame({'lat': [data['coord']['lat']],'lon': [data['coord']['lon']]})
            
            st.write("### 📍 City Location")
            st.map(map_data)

        else:
            st.error("City not found.")
    else:
        st.error("Please enter the name of the city.")