import streamlit as st
import google.generativeai as genai
import requests
from bs4 import BeautifulSoup

# 1. Conectar la IA
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
# Forzamos el modelo exacto que pide Google
modelo = genai.GenerativeModel('gemini-3.8-flash')

st.set_page_config(page_title="Generador Viral IA", page_icon="🚀")
st.title("🚀 Generador de Contenido Viral con IA")
st.write("Convierte cualquier artículo o noticia en una estrategia completa de redes sociales en segundos.")

url = st.text_input("Pega aquí el enlace de la noticia o artículo:")

if st.button("Generar Estrategia"):
    if url.startswith("http"):
        with st.spinner("Procesando texto con Gemini 3.8 Flash..."):
            try:
                # --- FASE 1: SCRAPING ---
                headers = {"User-Agent": "Mozilla/5.0"}
                respuesta = requests.get(url, headers=headers, timeout=10)
                soup = BeautifulSoup(respuesta.text, "html.parser")
                parrafos = soup.find_all('p')
                texto_limpio = " ".join([p.text for p in parrafos])[:6000] 
                
                # --- FASE 2: IA ---
                instruccion = f"""
                Actúa como experto en marketing digital. Lee este texto y genera:
                1. Un resumen ejecutivo (3 viñetas).
                2. Un post profesional para LinkedIn (con hashtags).
                3. Un hilo corto para Twitter/X.
                
                Texto: {texto_limpio}
                """
                respuesta_ia = modelo.generate_content(instruccion)
                
                # --- FASE 3: RESULTADOS ---
                st.success("¡Contenido generado con éxito!")
                st.markdown(respuesta_ia.text)
                
            except Exception as e:
                st.error(f"Error detallado: {e}")
    else:
        st.warning("Introduce un enlace válido que empiece por http:// o https://")
