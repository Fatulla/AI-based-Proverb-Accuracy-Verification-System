import streamlit as st
import pandas as pd
import Levenshtein
from streamlit_lottie import st_lottie
import requests

# Lottie animasiyasını yükləmək üçün funksiya
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# CSV faylının URL-i
url = "https://github.com/Fatulla/AI-based-Proverb-Accuracy-Verification-System/raw/main/atalar_sozleri_corrected.csv"

# CSV faylını oxumaq
df = pd.read_csv(url, sep='|', encoding='utf-8-sig')

# Tətbiqin əsas başlığı və təsviri
st.markdown("""
    <h1 style="text-align: center; color: #2E7D32;">Atalar Sözü Axtarış Sistemi</h1>
    <p style="text-align: center; color: #4CAF50; font-size: 18px;">
        Yazılan atalar sözünü Levenshtein məsafəsi ilə yoxlayaraq ən uyğun variantı tapır.
    </p>
    """, unsafe_allow_html=True)

# Lottie animasiyası
lottie_url = "https://assets1.lottiefiles.com/packages/lf20_qnkjwou9.json"
lottie_animation = load_lottie_url(lottie_url)

if lottie_animation:
    st_lottie(lottie_animation, speed=1, width=600, height=300, key="animation")

# Haqqında məlumat bölməsi
with st.expander("Sistem Haqqında", expanded=False):
    st.markdown("""
    <div style="color: #1E88E5; font-size: 16px;">
        <p>Bu sistem, daxil etdiyiniz atalar sözünü verilənlər bazası ilə müqayisə edərək 
        <strong>Levenshtein məsafəsi</strong> alqoritminə əsasən ən yaxın düzgün variantı tapır.</p>
        <p><strong>Necə işləyir?</strong> Siz atalar sözünü yazırsınız, sistem isə onu 
        verilənlər bazasındakı düzgün variantlarla müqayisə edir və ən az fərqli olanı göstərir.</p>
        <p><strong>İstifadəsi:</strong> Sadəcə aşağıdakı xanaya atalar sözünü daxil edin!</p>
    </div>
    """, unsafe_allow_html=True)

# Axtarış bölməsi
st.markdown("""
    <h3 style="text-align: center; color: #2E7D32;">Atalar Sözünüzü Axtarın</h3>
    """, unsafe_allow_html=True)

# Axtarış pəncərəsi
user_input = st.text_input("", placeholder="Atalar sözünü bura yazın...", max_chars=100)

# Ən yaxın atalar sözünü tapmaq üçün funksiya
def find_closest_proverb(user_input, df):
    closest_proverb = None
    min_distance = float('inf')

    for proverb in df['Atalar_sozlari']:
        distance = Levenshtein.distance(user_input, proverb)
        if distance < min_distance:
            min_distance = distance
            closest_proverb = proverb

    return closest_proverb, min_distance

# Nəticələri göstərmək
if user_input:
    closest_proverb, distance = find_closest_proverb(user_input, df)
    
    st.markdown("### Nəticə:")
    if closest_proverb:
        st.success(f"**Tapılan atalar sözü:** {closest_proverb}")
        st.info(f"**Levenshtein məsafəsi:** {distance}")
    else:
        st.warning("Uyğun atalar sözü tapılmadı.")

# Əlaqə məlumatları
st.markdown("""
    <div style="margin-top: 20px; padding: 10px; background-color: #F5F5F5; border-radius: 5px;">
        <h4 style="color: #2E7D32;">Əlaqə Məlumatları</h4>
        <p style="color: #555555;">Əlavə suallarınız üçün:</p>
        <p style="color: #555555;">📧 <a href="mailto:aliyevfatulla99@gmail.com">aliyevfatulla99@gmail.com</a></p>
        <p style="color: #555555;">📞 050-778-08-18</p>
    </div>
    """, unsafe_allow_html=True)
