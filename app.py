import streamlit as st
import pandas as pd
import Levenshtein
from streamlit_lottie import st_lottie
import requests
from io import BytesIO

# Lottie animasiyasını yükləmək üçün funksiya
def load_lottie_url(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Default CSV faylının URL-i
default_url = "https://github.com/Fatulla/AI-based-Proverb-Accuracy-Verification-System/raw/main/atalar_sozleri_corrected.csv"

# Tətbiqin əsas başlığı və təsviri
st.markdown("""
    <h1 style="text-align: center; color: #D32F2F;">Atalar Sözü Axtarış Sistemi</h1>
    <p style="text-align: center; color: #4CAF50; font-size: 18px; font-weight: bold;">
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
        <p><strong>Necə işləyir?</strong> Siz atalar sözünü yazırsınız, axtar düyməsini sıxırsınız, 
        sistem isə onu verilənlər bazasındakı düzgün variantlarla müqayisə edir və ən az fərqli olanı göstərir.</p>
        <p><strong>İstifadəsi:</strong> Aşağıdakı xanaya atalar sözünü daxil edin və axtarışa başlayın.</p>
    </div>
    """, unsafe_allow_html=True)

# Verilənlər bazasını oxumaq
try:
    df = pd.read_csv(default_url, sep='|', encoding='utf-8-sig')
except Exception as e:
    st.error(f"Verilənlər bazasını oxumaq mümkün olmadı: {e}")
    df = pd.DataFrame()

# Axtarış bölməsi
st.markdown("""
    <h3 style="text-align: center; color: #2E7D32; font-family: 'Arial', sans-serif; font-weight: bold; margin-bottom: 20px;">
        Atalar Sözünüzü Axtarın
    </h3>
    """, unsafe_allow_html=True)

# Axtarış pəncərəsi və düymə
user_input = st.text_input(
    "",
    placeholder="Atalar sözünü bura yazın...",
    max_chars=100,
    key="proverb_input"
)

# Axtarış düyməsi
if st.button("Axtar"):
    # Ən yaxın atalar sözünü tapmaq üçün funksiya
    def find_closest_proverb(user_input, df):
        if not user_input or df.empty:
            return None, None
        closest_proverb = None
        min_distance = float('inf')

        for proverb in df['Atalar_sozlari']:
            distance = Levenshtein.distance(user_input.lower(), proverb.lower())
            if distance < min_distance:
                min_distance = distance
                closest_proverb = proverb

        return closest_proverb, min_distance

    # Nəticələri göstərmək
    if user_input and not df.empty:
        closest_proverb, distance = find_closest_proverb(user_input, df)
        
        st.markdown("### Nəticə:")
        if closest_proverb:
            st.success(f"**Tapılan atalar sözü:** {closest_proverb}")
            st.info(f"**Levenshtein məsafəsi:** {distance}")
        else:
            st.warning("Uyğun atalar sözü tapılmadı.")
    elif not user_input:
        st.info("Atalar sözünü daxil edin.")
    elif df.empty:
        st.warning("Verilənlər bazası yüklənməyib.")

# Əlaqə məlumatları
st.markdown("""
    <div style="margin-top: 20px; padding: 10px; background-color: #F5F5F5; border-radius: 5px;">
        <h4 style="color: #2E7D32;">Əlaqə Məlumatları</h4>
        <p style="color: #555555;">Əlavə suallarınız üçün:</p>
        <p style="color: #555555;">📧 <a href="mailto:aliyevfatulla99@gmail.com">aliyevfatulla99@gmail.com</a></p>
        <p style="color: #555555;">📞 050-778-08-18</p>
    </div>
    """, unsafe_allow_html=True)

# Verilənlər bazasını endirmək üçün düymə
st.markdown("---")  # Ayrıcı xətt
response = requests.get(default_url)
if response.status_code == 200:
    csv_data = BytesIO(response.content)
    st.download_button(
        label="Verilənlər bazasını endir",
        data=csv_data,
        file_name="atalar_sozleri_corrected.csv",
        mime="text/csv"
    )
