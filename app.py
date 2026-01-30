import streamlit as st
import math

# 1. Настройка страницы
st.set_page_config(page_title="Produzione Voghera", page_icon="🏭", layout="centered")

# Скрываем лишние меню Streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. Заголовок
st.title("Calcolatore Produzione 🏭")
st.caption("Sistema di calcolo materiale per Agugliatrice")

# 3. Выбор модели
st.write("### 1. Seleziona Modello:")
model_display = st.radio(
    "Modello:",
    ["270/300", "370", "400", "470"],
    horizontal=True,
    label_visibility="collapsed"
)
w = model_display.split('/')[0]

# 4. Поля ввода
col1, col2 = st.columns(2)

with col1:
    st.write("**Quantità Totale (Pz):**")
    total = st.number_input("Pezzi", min_value=0, step=1, label_visibility="collapsed")

with col2:
    st.write("**Lunghezza del pezzo (Metri):**")
    length = st.number_input("Metri", min_value=0.0, step=0.01, format="%.2f", label_visibility="collapsed")

# 5. Кнопка расчета
st.write("") 
if st.button("CALCOLA MATERIALE 🚀", type="primary", use_container_width=True):
    
    if length > 0 and total > 0:
        # Расчет количества матов
        pcs_per_mat = math.floor(40 / length)
        
        if pcs_per_mat > 0:
            mats = math.ceil(total / pcs_per_mat)
            
            # Настройка коэффициентов заправки
            if w == "470": 
                n200, n100 = 3, 5
            elif w == "400": 
                n200, n100 = 2, 5
            elif w == "370": 
                n200, n100 = 2, 4
            else: # 270/300
                n200, n100 = 2, 2
            
            # Базовый расчет рулонов по длине
            rolls200 = math.ceil((mats * 40 * n200) / 181)
            rolls100 = math.ceil((mats * 40 * n100) / 181)
            
            # --- ЛОГИКА ОКРУГЛЕНИЯ ПО КОМПЛЕКТАМ ЗАПРАВКИ ---
            
            if w == "470":
                # Должны закончиться одновременно: пачки по 3 и по 5
                while rolls200 % 3 != 0: rolls200 += 1
                while rolls100 % 5 != 0: rolls100 += 1
                info_text = "Multipli di 3 (H200) e 5 (H100) per caricamento completo."
            
            elif w == "370":
                # Должны закончиться одновременно: пачки по 2 и по 4
                while rolls200 % 2 != 0: rolls200 += 1
                while rolls100 % 4 != 0: rolls100 += 1
                info_text = "Multipli di 2 (H200) e 4 (H100) per caricamento completo."
            
            else:
                # Для 270, 300 и 400: работаем парами (минимум четное)
                if rolls200 % 2 != 0: rolls200 += 1
                if rolls100 % 2 != 0: rolls100 += 1
                info_text = "Arrotondato a numero PARI per evitare scarti (lavoro in coppia)."

            # --- ВЫВОД РЕЗУЛЬТАТА ---
            st.success("✅ Calcolo completato!")
            
            st.markdown("---")
            st.subheader(f"Tappeti necessari (40m): **{mats}**")
            
            st.markdown("### 📦 DA PRENDERE IN MAGAZZINO:")
            
            c1, c2 = st.columns(2)
            c1.metric(label="H200 (Larghi)", value=f"{rolls200} pz")
            c2.metric(label="H100 (Stretti)", value=f"{rolls100} pz")
            
            st.warning(f"ℹ️ {info_text}")
            st.markdown("---")
            
            # Лог
            with open("log_produzione.txt", "a") as f:
                f.write(f"Mod: {w}, Qta: {total}, L: {length} -> H200: {rolls200}, H100: {rolls100}\n")
                
        else:
            st.error("Errore: Il pezzo è più lungo di 40 metri!")
    else:
        st.warning("⚠️ Inserisci numeri validi (maggiori di 0)")
