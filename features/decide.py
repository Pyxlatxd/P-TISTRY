# features/decide.py
from docx import Document
from groq import Groq
from features.api import GROQ_API_KEY  # your API key

client = Groq(api_key=GROQ_API_KEY)

def decide_statistical_treatment(doc: Document):
    """
    Analyze the full document and let LLaMA decide the appropriate statistical treatment.
    Returns the AI's decision as a Python dict, without modifying the doc.
    """
    # --- Gather full text ---
    full_text = "\n\n".join([p.text for p in doc.paragraphs if p.text.strip()])
    if not full_text.strip():
        return None

    # --- Prepare prompt ---
    prompt = f"""
You are an expert APA research assistant.
Analyze the following full research document and decide the most appropriate statistical treatment(s)
based on research design, data type, and hypotheses.
Provide your own reasoning and return a JSON object only, like:
{{"treatment": "One-Way ANOVA", "reason": "There are three groups and one dependent variable"}}

Document:
{full_text}
"""

    try:
        # --- Query LLaMA ---
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an APA research assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=3000,
            temperature=0
        )

        raw = completion.choices[0].message.get("content") \
              if isinstance(completion.choices[0].message, dict) \
              else completion.choices[0].message.content

        # --- Parse JSON ---
        try:
            decision = json.loads(raw.strip())
        except Exception as e:
            print(f"❌ JSON parse error: {e}")
            print(f"Raw output (first 500 chars): {raw[:500]}")
            decision = {"error": "Could not parse LLaMA output", "raw_output": raw.strip()}

        return decision

    except Exception as e:
        print(f"[Statistical Decision Error] {e}")
        return {"error": str(e)}
