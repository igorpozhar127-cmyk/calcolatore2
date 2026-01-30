import streamlit as st
import math

# 1. Настройка страницы
st.set_page_config(page_title="Produzione Voghera", page_icon="🏭", layout="centered")

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
        # Считаем сколько штук лезет в один 40-метровый мат
        pcs_per_mat = math.floor(40 / length)
        
        if pcs_per_mat > 0:
            # Сколько всего матов (Tappeti) нужно прогнать
            mats = math.ceil(total / pcs_per_mat)
            
            # Устанавливаем коэффициенты (сколько полос в ширине)
            if w == "470": n200, n100 = 3, 5
            elif w == "400": n200, n100 = 2, 5
            elif w == "370": n200, n100 = 2, 4
            else: n200, n100 = 2, 2
            
            # Считаем рулоны по метражу (в одном рулоне 181 метр)
            rolls200 = math.ceil((mats * 40 * n200) / 181)
            rolls100 = math.ceil((mats * 40 * n100) / 181)
            
            # --- ПРИМЕНЯЕМ ТВОИ ПРАВИЛА КОМПЛЕКТАЦИИ (AGUGLIATRICE) ---
            if w == "470":
                # Должно делиться на 3 и на 5
                while rolls200 % 3 != 0: rolls200 += 1
                while rolls100 % 5 != 0: rolls100 += 1
                msg = "Округлено до полной заправки: 3xH200 и 5xH100"
            elif w == "370":
                # Должно делиться на 2 и на 4
                while rolls200 % 2 != 0: rolls200 += 1
                while rolls100 % 4 != 0: rolls100 += 1
                msg = "Округлено до полной заправки: 2xH200 и 4xH100"
            elif w == "400":
                # Должно делиться на 2 и на 5
                while rolls200 % 2 != 0: rolls200 += 1
                while rolls100 % 5 != 0: rolls100 += 1
                msg = "Округлено до полной заправки: 2xH200 и 5xH100"
            else:
                # 270/300 — просто четные
                if rolls200 % 2 != 0: rolls200 += 1
                if rolls100 % 2 != 0: rolls100 += 1
                msg = "Округлено до четного числа (работа в паре)"

            # --- ВЫВОД ---
            st.success("✅ Calcolo completato!")
            st.subheader(f"Tappeti totali da fare: {mats}")
            
            st.markdown("### 📦 PORTARE IN AGUGLIATRICE:")
            c1, c2 = st.columns(2)
            c1.metric(label="H200 (Larghi)", value=f"{rolls200} pz")
            c2.metric(label="H100 (Stretti)", value=f"{rolls100} pz")
            
            st.warning(f"ℹ️ {msg}")
        else:
            st.error("Pezzo troppo lungo!")
    else:
        st.warning("Inserisci i dati")
