import streamlit as st
import json
import os
from datetime import datetime
from fpdf import FPDF  # Make sure you have installed fpdf2 (pip install fpdf2)
from core.parser import ContractParser
from core.nlp_engine import NLPEngine
from core.legal_brain import LegalBrain
from utils.logger import AuditLogger
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("HF_TOKEN")

# --- HELPER FUNCTION: PDF REPORT GENERATION (FIXED FOR HINDI & BYTEARRAY) ---
def generate_pdf_report(analysis, entities):
    pdf = FPDF()
    pdf.add_page()
    
    # Path to your font file as seen in your folder structure
    font_path = "NotoSans-Regular.ttf"
    
    if os.path.exists(font_path):
        # Register the font to support Hindi Devanagari script
        pdf.add_font("HindiFont", "", font_path)
        pdf.set_font("HindiFont", size=12)
        font_name = "HindiFont"
    else:
        # Fallback if font is missing
        pdf.set_font("Helvetica", size=12)
        font_name = "Helvetica"
        st.warning("Font file 'NotoSans-Regular.ttf' not found. Hindi characters will not show in PDF.")

    # Title
    pdf.set_font(font_name, size=16)
    pdf.cell(200, 10, txt="NyayaSathi Legal Analysis Report", ln=True, align='C')
    pdf.ln(10)
    
    # Details
    pdf.set_font(font_name, size=12)
    pdf.cell(200, 10, txt=f"Contract Type: {analysis.get('contract_type', 'N/A')}", ln=True)
    pdf.cell(200, 10, txt=f"Risk Score: {analysis.get('risk_score', '0')}/100", ln=True)
    pdf.ln(5)
    
    pdf.cell(200, 10, txt="Executive Summary:", ln=True)
    pdf.set_font(font_name, size=10)
    pdf.multi_cell(0, 7, txt=analysis.get('summary', ''))
    pdf.ln(5)

    pdf.set_font(font_name, size=11)
    pdf.cell(200, 10, txt="Detailed Clause Analysis:", ln=True)
    pdf.set_font(font_name, size=10)
    
    for clause in analysis.get('clauses', []):
        name = clause.get('name', 'Clause')
        exp = clause.get('explanation', '')
        risk = str(clause.get('risk_level', '')).upper()
        pdf.multi_cell(0, 7, txt=f"• {name} [{risk}]: {exp}")
        pdf.ln(2)
    
    # FIX: Convert fpdf2 bytearray output to standard bytes for Streamlit
    return bytes(pdf.output())

# --- STREAMLIT SETUP ---
st.set_page_config(page_title="NyayaSathi", layout="wide", page_icon="⚖️")

st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

st.title("⚖️ NyayaSathi: SME Legal Assistant")

# --- SIDEBAR ---
with st.sidebar:
    st.header("Hugging Face Setup")
    
    model_id = st.text_input("Model ID", value="openai/gpt-oss-120b") 
    uploaded_file = st.file_uploader("Upload Contract (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'])
    language = st.selectbox("Preferred Output Language", ["English", "Hindi"])
    st.divider()
    st.info("Language selection affects the Summary and Clause Explanations.")

# --- MAIN LOGIC ---
if uploaded_file and api_key:
    if 'last_uploaded_file' not in st.session_state or st.session_state.last_uploaded_file != uploaded_file.name or st.session_state.get('last_lang') != language:
        
        with st.spinner(f"Analyzing in {language}..."):
            # 1. Parsing
            parser = ContractParser()
            raw_text = parser.extract_text(uploaded_file)
            st.session_state.raw_text = raw_text

            # 2. Local NLP
            nlp = NLPEngine()
            st.session_state.local_entities = nlp.get_basic_entities(raw_text)

            # 3. AI Analysis
            brain = LegalBrain(api_key, model_id=model_id)
            analysis = brain.analyze_contract(raw_text, lang=language)
            st.session_state.analysis = analysis
            
            # Save to Audit Log
            AuditLogger.save_log(
                uploaded_file.name, 
                analysis.get('contract_type', 'Unknown'), 
                analysis.get('risk_score', 0), 
                [c.get('name') for c in analysis.get('clauses', []) if c.get('risk_level') == 'high']
            )
        
        st.session_state.last_uploaded_file = uploaded_file.name
        st.session_state.last_lang = language

    # --- TABS INTERFACE ---
    tab1, tab2, tab3 = st.tabs(["📊 Risk Dashboard", "📜 Audit History", "📝 SME Templates"])

    with tab1:
        analysis = st.session_state.analysis
        entities = st.session_state.local_entities

        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Risk Score", f"{analysis.get('risk_score', 0)}/100")
        col_b.metric("Contract Type", analysis.get('contract_type', 'N/A'))
        col_c.write(f"**Identified Entities:**\n{', '.join(set(entities.get('organizations', [])[:3]))}")

        st.divider()
        res_col1, res_col2 = st.columns([2, 1])

        with res_col1:
            st.subheader("Key Findings")
            st.info(f"**Summary ({language}):**\n{analysis.get('summary', 'N/A')}")
            
            st.subheader("Clause Analysis")
            for clause in analysis.get('clauses', []):
                risk_lv = clause.get('risk_level', 'low').lower()
                color = "red" if risk_lv == "high" else "orange" if risk_lv == "medium" else "green"
                with st.expander(f"{clause.get('name', 'Clause')} - :{color}[{risk_lv.upper()}]"):
                    st.write(f"**Explanation:** {clause.get('explanation', 'N/A')}")
                    st.markdown(f"**💡 Suggestion:** {clause.get('mitigation_suggestion', 'N/A')}")

        with res_col2:
            st.subheader("Actions")
            # PDF Generation with Error Handling
            try:
                pdf_bytes = generate_pdf_report(analysis, entities)
                st.download_button(
                    label="📥 Download PDF Report",
                    data=pdf_bytes,
                    file_name=f"Legal_Analysis_{datetime.now().strftime('%d%m%Y')}.pdf",
                    mime="application/pdf"
                )
            except Exception as e:
                st.error(f"Could not generate PDF: {e}")

    with tab2:
        st.subheader("Audit Trail")
        history = AuditLogger.get_logs()
        if history:
            st.dataframe(history, use_container_width=True)
        else:
            st.write("No history found.")

    with tab3:
        st.subheader("Drafting Templates")
        template_type = st.selectbox("Type", ["NDA", "Vendor Contract", "Employment Letter"])
        if st.button("Generate"):
            brain = LegalBrain(api_key, model_id=model_id)
            template = brain.generate_template(template_type)
            st.text_area("Template Draft", template, height=300)

else:
    st.info("Ready to begin. Please provide your HF Token and upload a contract.")