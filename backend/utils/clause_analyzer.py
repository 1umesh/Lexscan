import os
import json
import re
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    google_api_key=api_key,
    temperature=0.2,
)

SYSTEM_PROMPT = """You are an expert legal contract analyst. Analyze the provided contract text and return a detailed structured JSON analysis.

Return ONLY valid JSON (no markdown, no backticks, no preamble). The JSON must follow this exact schema:

{
  "contract_type": "string (e.g. Employment, NDA, Service Agreement, Lease, Partnership)",
  "overall_risk_level": "LOW | MEDIUM | HIGH | CRITICAL",
  "executive_summary": "string (2-3 sentence summary of the contract and its key concerns)",
  "risk_score": number from 0-100,
  "parties_involved": ["string array of party names/roles found in contract"],
  "key_dates": [
    {"label": "string", "date": "string"}
  ],
  "dangerous_clauses": [
    {
      "id": "string (dc_1, dc_2, ...)",
      "title": "string (short clause title)",
      "original_text": "string (exact excerpt from contract, max 200 chars)",
      "risk_level": "MEDIUM | HIGH | CRITICAL",
      "risk_explanation": "string (why this is dangerous for the user)",
      "category": "string (e.g. Liability, Termination, IP Rights, Payment, Confidentiality, Dispute Resolution)"
    }
  ],
  "suggested_improvements": [
    {
      "id": "string (si_1, si_2, ...)",
      "title": "string",
      "original_text": "string (the problematic original excerpt, max 200 chars)",
      "improved_text": "string (the suggested replacement language)",
      "reason": "string (why this improvement matters)"
    }
  ],
  "missing_clauses": [
    {
      "id": "string (mc_1, mc_2, ...)",
      "clause_name": "string",
      "why_needed": "string (why this clause is important)",
      "suggested_text": "string (a sample clause text to add, max 300 chars)"
    }
  ],
  "positive_aspects": [
    "string (things the contract does well)"
  ],
  "negotiation_tips": [
    "string (specific negotiation leverage points for the user)"
  ]
}

Be thorough and specific. Identify real issues, not generic ones. Base everything strictly on the contract text provided."""


async def analyze_contract(raw_text: str) -> dict:
    # Trim to avoid token overload — take first ~12000 chars
    trimmed = raw_text[:12000]

    prompt = f"{SYSTEM_PROMPT}\n\n---CONTRACT TEXT START---\n{trimmed}\n---CONTRACT TEXT END---"

    response = llm.invoke([HumanMessage(content=prompt)])
    content = response.content.strip()

    # Strip markdown code fences if present
    content = re.sub(r"^```(?:json)?\s*", "", content)
    content = re.sub(r"\s*```$", "", content)

    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Try to extract JSON object from response
        match = re.search(r"\{[\s\S]*\}", content)
        if match:
            return json.loads(match.group())
        raise ValueError("AI did not return valid JSON. Raw response: " + content[:300])
