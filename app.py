import streamlit as st
import pandas as pd
import Levenshtein
from streamlit_lottie import st_lottie
import requests
from io import BytesIO

# Lottie animasiyasını yükləmək üçün funksiyanı yaradın
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# CSV faylının URL-i
url = "https://github.com/Fatulla/AILAB_TASK02_Atalar_Sozlari/blob/main/atalar_sozleri.csv"

try:
    df = pd.read_csv(url, delimiter=',', encoding='utf-8', on_bad_lines='skip')
    st.write(df.head())  # DataFrame-in başını göstəririk
except Exception as e:
    st.error(f"Fayl oxunarkən xəta baş verdi: {e}")

# Başlıq hissəsini düzəldirik
st.markdown("""
    <h1 style="text-align: center; color: #4CAF50;">Bu layihə <span style="color: red;">Fətulla Əliyev</span> tərəfindən <span style="color: red;">AILAB Levenshtein_x</span> tapşırığı üçün hazırlanmışdır</h1>
    <h2 style="text-align: center; color: #4CAF50;">Levenshtein məsafəsi istifadə olunaraq düzgün atalar sözünün tapılması</h2>
""", unsafe_allow_html=True)

# Lottie animasiyasını yükləyirik
lottie_url = "https://assets1.lottiefiles.com/packages/lf20_qnkjwou9.json"  # Lottie animasiya URL-si
lottie_animation = load_lottie_url(lottie_url)

if lottie_animation:
    st_lottie(lottie_animation, speed=1, width=700, height=400, key="animation")

# Axtarış bölməsi
st.markdown("""
    <h3 style="text-align: center; color: #2E8B57;">Axtarış Edin:</h3>
    <p style="text-align: center; color: #555555;">Verilənlər bazasında axtarış edərək ən yaxın atalar sözünü tapın</p>
""", unsafe_allow_html=True)

# Axtarış pəncərəsini böyüdürük
user_input = st.text_input("Atalar sözünüzü daxil edin:", "", max_chars=100)

# Nəticə bölməsi
def find_closest_proverb(user_input, first_column):
    closest_proverb = None
    min_distance = float('inf')

    for proverb in first_column:  # Burada birinci sütunu istifadə edirik
        distance = Levenshtein.distance(user_input, proverb)

        if distance < min_distance:
            min_distance = distance
            closest_proverb = proverb

    return closest_proverb, min_distance

# Əgər istifadəçi daxil edibsə
if user_input:
    closest_proverb, distance = find_closest_proverb(user_input, first_column)

    # Nəticəni göstəririk
    if closest_proverb:
        st.markdown(f"### Ən yaxın atalar sözü:")
        st.write(f"**{closest_proverb}**")
        st.markdown(f"**Levenshtein mesafəsi:** {distance}")
    else:
        st.write("Təəssüf ki, heç bir uyğun atalar sözü tapılmadı.")

# Əlaqə məlumatları: Sol alt küncdə göstərmək
st.markdown("""
    <div style="position: fixed; bottom: 10px; left: 10px; font-size: 12px; color: #555555;">
    <p>Əlaqə üçün: <a href="mailto:aliyevfatulla99@gmail.com">aliyevfatulla99@gmail.com</a></p>
    <p>Telefon: 050-778-08-18</p>
    </div>
""", unsafe_allow_html=True)
