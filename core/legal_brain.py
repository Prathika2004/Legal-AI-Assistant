import json
from huggingface_hub import InferenceClient

class LegalBrain:
    def __init__(self, api_key, model_id="openai/gpt-oss-120b"): 
        # INITIALIZATION: This creates the client attribute
        self.client = InferenceClient(api_key=api_key)
        self.model_id = model_id

    def analyze_contract(self, contract_text, lang="English"):
        # STRONGER language instruction
        language_instruction = f"IMPORTANT: You must write all verbal descriptions, summaries, and explanations in {lang}."
        if lang == "Hindi":
            language_instruction += " (Use Devanagari script for Hindi)."

        system_prompt = f"""
        {language_instruction}
        You are a senior Indian Legal Expert. Analyze the contract and return ONLY a JSON object.
        
        JSON Structure:
        {{
          "contract_type": "string",
          "risk_score": 0-100,
          "summary": "Detailed summary in {lang}",
          "clauses": [{{
            "name": "Clause Name", 
            "explanation": "Simple explanation in {lang}", 
            "risk_level": "low/medium/high", 
            "mitigation_suggestion": "Advice in {lang}"
          }}],
          "compliance_alerts": ["Alerts in {lang}"]
        }}
        """

        user_prompt = f"Contract Text to analyze:\n{contract_text[:10000]}"

        # Using the Chat Completion API
        try:
            response = self.client.chat_completion(
                model=self.model_id,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=4000,
                temperature=0.1 
            )
            
            content = response.choices[0].message.content
            
            # Clean JSON if model returns markdown
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0].strip()
            elif "```" in content:
                content = content.split("```")[1].split("```")[0].strip()
                
            return json.loads(content)
        except Exception as e:
            # Fallback error structure if the LLM fails
            return {
                "contract_type": "Error",
                "risk_score": 0,
                "summary": f"LLM Error: {str(e)}",
                "clauses": [],
                "compliance_alerts": []
            }

    def generate_template(self, template_type):
        prompt = f"Draft a professional Indian law compliant {template_type} agreement for an SME. Use simple business language."
        
        try:
            response = self.client.chat_completion(
                model=self.model_id,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=3000
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating template: {str(e)}"