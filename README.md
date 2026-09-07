# NyayaSathi — AI Legal Assistant for Indian SMEs

## Problem Statement
Small business owners in India routinely sign vendor, employment, and lease agreements without full legal review, because professional consultation is expensive. This leads to:
- **Hidden risks** — unfair indemnity clauses, unilateral termination rights, one-sided liability terms.
- **Compliance gaps** — silent violations of the MSME Development Act (e.g. the 45-day payment rule) or the Indian Contract Act 1872.
- **Language barriers** — contracts are drafted in dense legal English, with no accessible explanation in Hindi.

## What This Project Solves
NyayaSathi is a Streamlit app that lets an SME owner upload a contract (PDF/DOCX/TXT) and get back, in plain business language:
- A composite **risk score (0-100)** and clause-by-clause risk rating (Low/Medium/High).
- Plain-English (or Hindi) explanations of each risky clause plus a concrete mitigation suggestion.
- Automatic checks against specific Indian statutes — e.g. Section 27 non-compete validity under the Contract Act, the MSME 45-day payment rule, and the Arbitration & Conciliation Act 1996.
- A downloadable PDF report (with full Hindi/Devanagari font support).
- A local audit trail of every contract analyzed, to spot recurring issues over time.
- A template generator for balanced NDA / vendor / employment agreements SMEs can use as counter-offers.

## Approach
- **Local NLP first:** spaCy (`en_core_web_sm`) extracts dates, organizations, and monetary entities on-device before anything is sent externally.
- **LLM reasoning:** The extracted contract text is sent to a Hugging Face-hosted LLM (`openai/gpt-oss-120b` by default) with a structured prompt that forces a strict JSON response — contract type, risk score, per-clause analysis, and compliance alerts.
- **Bilingual output:** The same prompt pipeline supports English or Hindi output end-to-end, including PDF export via a bundled Noto Sans Devanagari font.
- **Audit trail:** Every analysis is appended to a local JSON log (`data/audit_logs/`) that powers the in-app history tab.

## Tech Stack
Streamlit (UI), Hugging Face Inference API (LLM), spaCy (local NER), PyMuPDF + python-docx (document parsing), fpdf2 (PDF report generation), python-dotenv.

## How to Run
```bash
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
Create a `.env` file in the project root:
```
HF_TOKEN=your_huggingface_token_here
```
Then run:
```bash
streamlit run app.py
```

## Privacy Note
PII extraction (dates, organizations) runs locally via spaCy. Only the contract text needed for analysis is sent to the LLM API, over an encrypted connection.

## Disclaimer
This is an AI-powered assistant for informational purposes only. It does not constitute legal advice and is not a substitute for a qualified legal professional.
