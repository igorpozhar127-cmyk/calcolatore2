import streamlit as st
import math

# 1. Configurazione della pagina
st.set_page_config(page_title="Voghera", page_icon="🏭", layout="centered")

# Nasconde i menu standard di Streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

# 2. Titolo
st.title("Calcolatore Produzione 🏭")
st.caption("Sistema di calcolo materiale per Agugliatrice")

# 3. Selezione del Modello
st.write("### 1. Seleziona Modello:")
model_display = st.radio(
    "Modello:",
    ["270/300", "370", "400", "470", "1000"],
    horizontal=True,
    label_visibility="collapsed"
)
w = model_display.split('/')[0]

# 4. Input dati
col1, col2 = st.columns(2)

with col1:
    st.write("**Quantità Totale (Pz):**")
    total = st.number_input("Pezzi", min_value=0, step=1, label_visibility="collapsed")

with col2:
    st.write("**Lunghezza del pezzo (Metri):**")
    length = st.number_input("Metri", min_value=0.0, step=0.01, format="%.2f", label_visibility="collapsed")

# 5. Bottone di calcolo
st.write("") 
if st.button("CALCOLA MATERIALE 🚀", type="primary", use_container_width=True):
    
    if length > 0 and total > 0:
        # --- LOGICA LUNGHEZZA TAPPETO ---
        # Определяем длину: 27.9 для 1000, иначе 40
        max_len = 27.9 if w == "1000" else 40.0
        
        # Calcolo numero di pezzi per tappeto
        pcs_per_mat = math.floor(max_len / length)
        
        if pcs_per_mat > 0:
            mats = math.ceil(total / pcs_per_mat)
            
            # Impostazione coefficienti di carico
            if w == "1000":
                n200, n100 = 5, 12
            elif w == "470": 
                n200, n100 = 3, 5
            elif w == "400": 
                n200, n100 = 2, 5
            elif w == "370": 
                n200, n100 = 2, 4
            else: # 270/300
                n200, n100 = 2, 2
            
            # Calcolo base rotoli necessari (181m per rotolo)
            rolls200 = math.ceil((mats * max_len * n200) / 181)
            rolls100 = math.ceil((mats * max_len * n100) / 181)
            
            # --- LOGICA DI ARROTONDAMENTO ---
            if w == "1000":
                while rolls200 % 5 != 0: rolls200 += 1
                while rolls100 % 12 != 0: rolls100 += 1
                info_text = f"Arrotondato per carico completo: 5xH200 e 12xH100."
            
            elif w == "470":
                while rolls200 % 3 != 0: rolls200 += 1
                while rolls100 % 5 != 0: rolls100 += 1
                info_text = "Arrotondato per carico completo: 3xH200 e 5xH100."
            
            elif w == "370":
                while rolls200 % 2 != 0: rolls200 += 1
                while rolls100 % 4 != 0: rolls100 += 1
                info_text = "Arrotondato per carico completo: 2xH200 e 4xH100."
            
            else:
                if rolls200 % 2 != 0: rolls200 += 1
                if rolls100 % 2 != 0: rolls100 += 1
                info_text = "Arrotondato a numero PARI (lavoro in coppia)."

            # --- RISULTATI ---
            st.success("✅ Calcolo completato!")
            
            st.markdown("---")
            # ВОТ ЗДЕСЬ ИСПРАВЛЕНО: теперь подставляется max_len (27.9 или 40)
            st.subheader(f"Tappeti necessari ({max_len}m): **{mats}**")
            
            st.markdown("### 📦 DA PRENDERE IN MAGAZZINO:")
            
            c1, c2 = st.columns(2)
            c1.metric(label="H200 (Larghi)", value=f"{rolls200} rotoli")
            c2.metric(label="H100 (Stretti)", value=f"{rolls100} rotoli")
            
            st.warning(f"ℹ️ {info_text}")
            st.markdown("---")
            
            # Log
            with open("log_produzione.txt", "a") as f:
                f.write(f"Mod: {w}, Qta: {total}, L: {length}, Tappeto: {max_len}m -> H200: {rolls200}, H100: {rolls100}\n")
                
        else:
            st.error(f"Errore: Il pezzo è più lungo di {max_len} metri!")
    else:
        st.warning("⚠️ Inserisci numeri validi (maggiori di 0)")
