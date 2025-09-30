import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
import os
# 🔹 Fundo personalizado
st.markdown(
    """
    <style>
    body {
        background: linear-gradient(136deg, #4B0082, #8A2BE2); /* Roxo → Violeta */
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <h1 style='font-family: "Brush Script MT", cursive; color: #4B0082; text-align: center; font-size:120px;'>
        Juana Prognostica
    </h1>
    """,
    unsafe_allow_html=True
)

# Configuração inicial
st.set_page_config(page_title="Mapa do Clima", layout="wide")
st.title("🌍 Mapa do Clima!")

# API Key do OpenWeather (adicione nos secrets do Streamlit ou como variável de ambiente)
API_KEY = os.getenv("OPENWEATHER_API_KEY")

if not API_KEY:
    st.warning("⚠️ Configure sua chave da API do OpenWeatherMap em `OPENWEATHER_API_KEY`.")
    st.stop()

# Criar mapa (centralizado no Brasil)
m = folium.Map(location=[-14.2350, -51.9253], zoom_start=4)

# Instruções
st.markdown("👉 Clique em qualquer cidade no mapa para ver a previsão do tempo")

# Exibir mapa
map_data = st_folium(m, width=700, height=500)

# Se o usuário clicar no mapa
if map_data and map_data["last_clicked"]:
    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    # Chamada API OpenWeather
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?"
        f"lat={lat}&lon={lon}&appid={API_KEY}&units=metric&lang=pt_br"
    )
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        cidade = data.get("name", "Desconhecida")
        temp = data["main"]["temp"]
        sensacao = data["main"]["feels_like"]
        clima = data["weather"][0]["description"].capitalize()

        st.subheader(f"📍 {cidade} ({lat:.2f}, {lon:.2f})")
        st.metric("🌡️ Temperatura", f"{temp:.1f} °C")
        st.metric("🥵 Sensação térmica", f"{sensacao:.1f} °C")
        st.write(f"☁️ Condição: {clima}")
    else:
        st.error("Erro ao buscar dados da previsão. Verifique sua chave da API.")

# Rodar localmente:
# streamlit run app.py





