AI Legal Assitant is a sophisticated, AI-powered legal tool designed to empower Indian Small and Medium Enterprises (SMEs). It simplifies complex legal contracts, identifies hidden risks, and provides actionable advice in plain business language, supporting both English and Hindi.

🚀 The Problem

Small business owners in India often sign complex vendor, employment, or lease agreements without full legal review due to high consultation costs. This leads to:

Hidden Risks: Unfair indemnity or unilateral termination clauses.

Compliance Gaps: Violations of the MSME Development Act or Indian Contract Act.

Language Barriers: Difficulty understanding "Legalese" in English or Hindi.

✨ Key Features

Multi-Format Parsing: Support for PDF, DOCX, and Text files using PyMuPDF and python-docx.

Intelligent Risk Scoring: Provides a composite risk score (0-100) and clause-level analysis (Low/Medium/High).

Indian Law Compliance: Specifically checks contracts against:

Indian Contract Act 1872 (e.g., Section 27 Non-compete validity).

MSME Development Act 2006 (e.g., 45-day payment rule).

Arbitration & Conciliation Act 1996.

Multilingual Support: Full analysis and PDF report generation in English and Hindi.

Audit Trail: Automatically builds a local knowledge base of analyzed contracts to identify recurring legal issues.

SME Templates: Generates balanced, "SME-friendly" contract templates for counter-offers.

🛠️ Technical Stack

LLM: DeepSeek-V3 (120B Parameter Model) hosted via Hugging Face Inference.

NLP Preprocessing: spaCy (en_core_web_sm) for local Named Entity Recognition (NER) and segmentation.

Frontend: Streamlit for a professional, responsive dashboard.

Document Handling: PyMuPDF and python-docx.

Export Engine: fpdf2 with Unicode support for Hindi PDF generation.

📂 Project Structure
code
Text
download
content_copy
expand_less
nyayasathi/
├── app.py                # Streamlit UI & Orchestration
├── .env                  # Environment Variables (HF_TOKEN)
├── NotoSans-Regular.ttf  # Unicode font for Hindi support
├── core/
│   ├── parser.py         # Document text extraction
│   ├── nlp_engine.py     # Local NER & NLP processing
│   └── legal_brain.py    # GenAI reasoning & prompt engineering
├── utils/
│   └── logger.py         # Audit logging & Knowledge base logic
└── data/
    └── audit_logs/       # Local JSON history of analyses
⚙️ Installation & Usage



Install Dependencies:

code
Bash
download
content_copy
expand_less
pip install -r requirements.txt
python -m spacy download en_core_web_sm

Setup Environment:
Create a .env file and add your HF_TOKEN=your_token_here.

Run the App:

code
Bash
download
content_copy
expand_less
streamlit run app.py
🛡️ Privacy & Confidentiality

NyayaSathi prioritizes data security. All PII (Personally Identifiable Information) extraction like dates and organizations is handled locally using spaCy. Contract data is transmitted via encrypted API calls to the LLM and is not used for training purposes.

⚠️ Disclaimer

This is an AI-powered assistant designed for informational purposes only. It does not constitute legal advice and is not a replacement for a qualified legal professional.

How to use this for your submission:

Copy the text above.

In VS Code, open your README.md file.

Paste the content and update the GitHub Link and User Name placeholders.

Commit and push to your GitHub.
