import streamlit as st
import math

# 1. Настройка страницы
st.set_page_config(page_title="Produzione Fidenza", page_icon="🏭", layout="centered")

# Скрываем лишнее
hide_st_style = """<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}</style>"""
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("Calcolatore Produzione 🏭")

# 2. Выбор модели
st.write("### 1. Seleziona Modello:")
model_display = st.radio("Modello:", ["270/300", "370", "400", "470"], horizontal=True, label_visibility="collapsed")
w = model_display.split('/')[0]

# 3. Поля ввода
col1, col2 = st.columns(2)
with col1:
    st.write("**Quantità Totale (Pz):**")
    total = st.number_input("Pezzi", min_value=0, step=1, label_visibility="collapsed")
with col2:
    st.write("**Lunghezza del pezzo (Metri):**")
    length = st.number_input("Metri", min_value=0.0, step=0.01, format="%.2f", label_visibility="collapsed")

if st.button("CALCOLA MATERIALE 🚀", type="primary", use_container_width=True):
    if length > 0 and total > 0:
        pcs_per_mat = math.floor(40 / length)
        
        if pcs_per_mat > 0:
            mats = math.ceil(total / pcs_per_mat)
            
            # Коэффициенты заправки
            if w == "470": n200, n100 = 3, 5
            elif w == "400": n200, n100 = 2, 5
            elif w == "370": n200, n100 = 2, 4
            else: n200, n100 = 2, 2
            
            # Базовый расчет рулонов
            rolls200 = math.ceil((mats * 40 * n200) / 181)
            rolls100 = math.ceil((mats * 40 * n100) / 181)
            
            # --- ЛОГИКА КРАТНОСТИ (ТВОИ ПРАВИЛА) ---
            if w == "470":
                while rolls200 % 3 != 0: rolls200 += 1
                while rolls100 % 5 != 0: rolls100 += 1
                msg = "Округлено: заправка по 3 (H200) и 5 (H100)"
            elif w == "370":
                while rolls200 % 2 != 0: rolls200 += 1
                while rolls100 % 4 != 0: rolls100 += 1
                msg = "Округлено: заправка по 2 (H200) и 4 (H100)"
            elif w == "400":
                while rolls200 % 2 != 0: rolls200 += 1
                while rolls100 % 5 != 0: rolls100 += 1
                msg = "Округлено: заправка по 2 (H200) и 5 (H100)"
            else:
                if rolls200 % 2 != 0: rolls200 += 1
                if rolls100 % 2 != 0: rolls100 += 1
                msg = "Округлено до четного (работа парами)"

            # --- ВЫВОД РЕЗУЛЬТАТОВ ---
            st.success("✅ Calcolo completato!")
            
            # Сначала самое важное - рулоны
            st.markdown("### 📦 ПРИВЕЗТИ СО СКЛАДА:")
            c1, c2 = st.columns(2)
            # Делаем цифры рулонов крупными и понятными
            c1.metric(label="H200 (Larghi)", value=f"{rolls200} шт")
            c2.metric(label="H100 (Stretti)", value=f"{rolls100} шт")
            
            st.warning(f"ℹ️ {msg}")
            
            # А информацию про коврики прячем вниз
            st.markdown("---")
            st.write(f"Инфо для линии: всего выйдет **{mats}** коврика(ов) по 40м.")
            
        else:
            st.error("Pezzo troppo lungo!")
    else:
        st.warning("Введи данные")
