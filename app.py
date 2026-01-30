import streamlit as st
import math

# 1. Настройка страницы (чтобы выглядело как приложение)
st.set_page_config(page_title="Produzione Voghera", page_icon="🏭", layout="centered")

# Скрываем лишние меню Streamlit, чтобы было чисто
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
st.caption("Sistema di calcolo materiale")

# 3. Выбор модели (крупные кнопки)
st.write("### 1. Seleziona Modello:")
model_display = st.radio(
    "Modello:",
    ["270/300", "370", "400", "470"],
    horizontal=True,
    label_visibility="collapsed"
)
# Берем только цифру до слеша, как в твоем коде для ПК
w = model_display.split('/')[0]

# 4. Поля ввода (оптимизировано для мобильных)
col1, col2 = st.columns(2)

with col1:
    st.write("**Quantità Totale (Pz):**")
    total = st.number_input("Pezzi", min_value=0, step=1, label_visibility="collapsed")

with col2:
    st.write("**Lunghezza del pezzo (Metri):**")
    # step=0.01 позволяет вводить запятую (например, 1.25)
    length = st.number_input("Metri", min_value=0.0, step=0.01, format="%.2f", label_visibility="collapsed")

# 5. Кнопка расчета (во всю ширину)
st.write("") # отступ
if st.button("CALCOLA MATERIALE 🚀", type="primary", use_container_width=True):
    
    # Проверка на ошибки (как try/except в твоем коде)
    if length > 0 and total > 0:
        # --- ТВОЯ ЛОГИКА ИЗ TKINTER ---
        pcs_per_mat = math.floor(40 / length)
        
        if pcs_per_mat > 0:
            mats = math.ceil(total / pcs_per_mat)
            
            # Логика коэффициентов
            if w == "470": 
                n200, n100 = 3, 5
            elif w == "400": 
                n200, n100 = 2, 5
            elif w == "370": 
                n200, n100 = 2, 4
            else: # 270/300
                n200, n100 = 2, 2
            
            # Расчет рулонов H200
            rolls200 = math.ceil((mats * 40 * n200) / 181)
            # Твоя проверка на четность
            if n200 == 2 and rolls200 % 2 != 0:
                rolls200 += 1
            
            # Расчет рулонов H100
            rolls100 = math.ceil((mats * 40 * n100) / 181)
            
            # --- ВЫВОД РЕЗУЛЬТАТА ---
            st.success("✅ Calcolo completato!")
            
            # Основной блок с результатами
            st.markdown("---")
            st.subheader(f"Tappeti necessari (40m): **{mats}**")
            
            st.markdown("### 📦 DA PRENDERE IN MAGAZZINO:")
            
            # Красивые плашки с цифрами
            c1, c2 = st.columns(2)
            c1.metric(label="H200 (Larghi)", value=f"{rolls200} pz")
            c2.metric(label="H100 (Stretti)", value=f"{rolls100} pz")
            
            st.markdown("---")
            
            # Сохранение в лог (скрытое)
            with open("log_produzione.txt", "a") as f:
                f.write(f"Mod: {w}, Qta: {total}, L: {length} -> H200: {rolls200}, H100: {rolls100}\n")
                
        else:
            st.error("Errore: Il pezzo è più lungo di 40 metri!")
    else:
        st.warning("⚠️ Inserisci numeri validi (maggiori di 0)")