import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="Excel Extractor")

st.title("📊 Excel Data Extractor")
st.write("Column G එකේ '1' හෝ '2' වලින් පටන් ගන්නා, දිග 12ක් වන දත්ත Column M වෙත ලබාගැනීම.")

uploaded_file = st.file_uploader("ඔයාගේ Excel file එක මෙතනට Upload කරන්න", type=['xlsx'])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    
    # Logic එක apply කිරීම
    def extract_logic(value):
        val_str = str(value).strip()
        if (val_str.startswith('1') or val_str.startswith('2')) and len(val_str) == 12:
            return val_str
        return None

    if 'G' in df.columns:
        df['M'] = df['G'].apply(extract_logic)
        st.success("වැඩේ සාර්ථකයි! පහතින් Download කරගන්න.")
        st.dataframe(df.head()) # Preview එකක් පෙන්වන්න

        # Download button එක හැදීම
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)
        
        st.download_button(
            label="Download Updated Excel",
            data=output.getvalue(),
            file_name="updated_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    else:
        st.error("Error: ඔයාගේ Excel එකේ 'G' කියලා Column එකක් නැහැ!")