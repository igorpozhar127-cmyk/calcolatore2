import streamlit as st
import math

# 1. Configurazione della pagina
st.set_page_config(page_title="Produzione Fidenza", page_icon="🏭", layout="centered")

# Nasconde i menu standard di Streamlit
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("Calcolatore Produzione 🏭")
st.caption("Ottimizzazione materiale per Agugliatrice")

# 2. Selezione del Modello
st.write("### 1. Seleziona il Modello:")
model_display = st.radio(
    "Modello:", 
    ["270/300", "370", "400", "470"], 
    horizontal=True, 
    label_visibility="collapsed"
)
w = model_display.split('/')[0]

# 3. Input dati
col1, col2 = st.columns(2)
with col1:
    st.write("**Quantità Totale (Pezzi):**")
    total = st.number_input("Pezzi", min_value=0, step=1, label_visibility="collapsed")
with col2:
    st.write("**Lunghezza del pezzo (Metri):**")
    length = st.number_input("Metri", min_value=0.0, step=0.01, format="%.2f", label_visibility="collapsed")

# 4. Bottone Calcola
st.write("") 
if st.button("CALCOLA MATERIALE 🚀", type="primary", use_container_width=True):
    if length > 0 and total > 0:
        # Calcolo quanti pezzi stanno in un tappeto da 40 metri
        pcs_per_mat = math.floor(40 / length)
        
        if pcs_per_mat > 0:
            # Numero di tappeti da 40m necessari
            mats = math.ceil(total / pcs_per_mat)
            
            # Impostazione coefficienti (strati per la larghezza)
            if w == "470": 
                n200, n100 = 3, 5
            elif w == "400": 
                n200, n100 = 2, 5
            elif w == "370": 
                n200, n100 = 2, 4
            else: # 270/300
                n200, n100 = 2, 2
            
            # Calcolo base rotoli (181m per rotolo)
            rolls200 = math.ceil((mats * 40 * n200) / 181)
            rolls100 = math.ceil((mats * 40 * n100) / 181)
            
            # --- LOGICA ARROTONDAMENTO PER AGUGLIATRICE (TUE REGOLE) ---
            if w == "470":
                # Caricamento completo: multipli di 3 e 5
                while rolls200 % 3 != 0: rolls200 += 1
                while rolls100 % 5 != 0: rolls100 += 1
                msg = "Arrotondato per caricamento completo: 3xH200 e 5xH100"
            
            elif w == "370":
                # Caricamento completo: multipli di 2 e 4
                while rolls200 % 2 != 0: rolls200 += 1
                while rolls100 % 4 != 0: rolls100 += 1
                msg = "Arrotondato per caricamento completo: 2xH200 e 4xH100"
            
            elif w == "400":
                # Caricamento completo: multipli di 2 e 5
                while rolls200 % 2 != 0: rolls200 += 1
                while rolls100 % 5 != 0: rolls100 += 1
                msg = "Arrotondato per caricamento completo: 2xH200 e 5xH100"
                
            else:
                # 270/300: Lavoro in coppia (numeri pari)
                if rolls200 % 2 != 0: rolls200 += 1
                if rolls100 % 2 != 0: rolls100 += 1
                msg = "Arrotondato a numero PARI per lavoro in coppia"

            # --- RISULTATI ---
            st.success("✅ Calcolo completato!")
            
            st.markdown("### 📦 DA PRENDERE IN MAGAZZINO:")
            c1, c2 = st.columns(2)
            c1.metric(label="H200 (Larghi)", value=f"{rolls200} rotoli")
            c2.metric(label="H100 (Stretti)", value=f"{rolls100} rotoli")
            
            st.warning(f"ℹ️ {msg}")
            
            st.markdown("---")
            st.write(f"**Info Linea:** Totale tappeti da produrre: **{mats}**")
            
        else:
            st.error("Errore: Il pezzo è più lungo di 40 metri!")
    else:
        st.warning("⚠️ Inserisci i dati (Pezzi e Metri)")
