import json
import os
from langchain_core.prompts import ChatPromptTemplate

class PromptManager:
    """Manages structural banking prompt templates for FinGuard AI's evaluation loops."""
    
    def __init__(self, manifest_path: str = "prompts.json"):
        self.manifest_path = manifest_path
        self.prompts = self._load_manifest()

    def _load_manifest(self) -> dict:
        if not os.path.exists(self.manifest_path):
            raise FileNotFoundError(f"Prompt configuration manifest not found at: {self.manifest_path}")
        with open(self.manifest_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def get_default_prediction_prompt(self, raw_financial_text: str, stress_basis_points: int = 200) -> str:
        """Formats the RTF + TCI + CoT default risk evaluation template."""
        config = self.prompts["default_prediction_engine"]
        
        # Compile via LangChain structural abstraction
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", config["system_template"]),
            ("human", config["human_template"])
        ])
        
        # Format variables for ingestion
        formatted_messages = prompt_template.format_messages(
            raw_financial_text=raw_financial_text,
            stress_basis_points=stress_basis_points
        )
        
        # Returns raw text representation for LLM pipelines or LangSmith prompt logs
        return "\n\n".join([msg.content for msg in formatted_messages])

    def get_reverse_audit_prompt(self, generated_memo: dict, raw_financial_text: str) -> str:
        """Formats the adversarial mistake finding and fraud audit framework."""
        config = self.prompts["reverse_engineering_audit"]
        
        prompt_template = ChatPromptTemplate.from_messages([
            ("system", config["system_template"]),
            ("human", config["human_template"])
        ])
        
        formatted_messages = prompt_template.format_messages(
            generated_memo=json.dumps(generated_memo, indent=2),
            raw_financial_text=raw_financial_text
        )
        
        return "\n\n".join([msg.content for msg in formatted_messages])

# Quick execution sanity check
if __name__ == "__main__":
    # Initialize the prompt manager framework
    manager = PromptManager()
    
    sample_text = "Net Operating Income: INR 50,00,000. Current Liabilities: INR 20,00,000."
    
    print("=================== 1. DEFAULT ENGINE PROMPT MULTI-STAGE TRACE ===================")
    prediction_prompt = manager.get_default_prediction_prompt(sample_text, stress_basis_points=250)
    print(prediction_prompt)
    
    print("\n=================== 2. REVERSE AUDIT PROMPT ADVERSARIAL TRACE ===================")
    mock_memo = {"baseline_dscr": 2.5, "default_risk_tier": "Low"}
    audit_prompt = manager.get_reverse_audit_prompt(mock_memo, sample_text)
    print(audit_prompt)
