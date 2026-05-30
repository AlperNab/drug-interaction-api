#!/usr/bin/env python3
"""
drug-interaction-api — list of medications → interaction warnings
Severity scores, mechanism explanations, clinical significance,
monitoring recommendations, alternative suggestions
DISCLAIMER: Educational only — always verify with a pharmacist or physician
"""
import anthropic, json, re, sys

DISCLAIMER = """
⚠️  IMPORTANT DISCLAIMER
This tool is for EDUCATIONAL and INFORMATIONAL purposes only.
ALWAYS consult a licensed pharmacist or physician before making
any medication decisions. Drug interactions can be life-threatening.
Do NOT use this as a substitute for professional medical advice.
"""

SYSTEM = """You are a clinical pharmacist with expertise in drug interactions.
Analyze the provided list of medications for potential interactions.

IMPORTANT: Focus on clinically significant interactions. Include:
- Drug-drug interactions
- Drug-food interactions (if notable)
- Contraindications based on common conditions

Return ONLY valid JSON — no markdown, no explanation.

{
  "medications_analyzed": ["list of normalized drug names"],
  "total_interactions": number,
  "critical_count": number,
  "interactions": [
    {
      "drug_a": "normalized name",
      "drug_b": "normalized name or 'grapefruit juice'",
      "severity": "contraindicated|major|moderate|minor",
      "clinical_significance": "high|medium|low",
      "interaction_type": "pharmacokinetic|pharmacodynamic|combined",
      "mechanism": "plain-English explanation of WHY they interact",
      "effect": "what happens when taken together",
      "symptoms_to_watch": ["symptoms that indicate a problem"],
      "management": "what should be done — separate doses, avoid, monitor, etc.",
      "monitoring": "what labs or vitals to track if combination unavoidable",
      "alternatives": ["safer alternatives to consider"],
      "evidence_level": "established|theoretical|case_report"
    }
  ],
  "food_interactions": [
    {
      "drug": "string",
      "food": "grapefruit|alcohol|dairy|...",
      "effect": "string",
      "severity": "major|moderate|minor"
    }
  ],
  "general_warnings": ["important warnings about this combination overall"],
  "safe_combinations": ["pairs from the list that are generally safe together"],
  "pharmacist_note": "overall clinical summary and recommendation",
  "disclaimer": "Always verify with a licensed pharmacist or prescribing physician."
}"""

SEVERITY_ICON = {
    "contraindicated": "🚫",
    "major": "🔴",
    "moderate": "🟠",
    "minor": "🟡"
}

def check_interactions(medications: list[str]) -> dict:
    """Check drug interactions for a list of medications."""
    client = anthropic.Anthropic()
    med_list = "\n".join(f"- {m}" for m in medications)
    resp = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=4096, system=SYSTEM,
        messages=[{"role":"user","content":f"Check interactions for these medications:\n\n{med_list}"}]
    )
    raw = re.sub(r'^```(?:json)?\s*','',resp.content[0].text.strip(),flags=re.MULTILINE)
    raw = re.sub(r'\s*```$','',raw,flags=re.MULTILINE)
    result = json.loads(raw)
    return result

def print_report(r: dict):
    print(DISCLAIMER)
    total = r.get("total_interactions", 0)
    critical = r.get("critical_count", 0)
    print(f"{'═'*60}")
    print(f"  DRUG INTERACTION CHECK")
    print(f"  Medications: {', '.join(r.get('medications_analyzed',[]))}")
    print(f"  Interactions found: {total} | Critical: {critical}")
    print(f"{'═'*60}")

    interactions = r.get("interactions", [])
    if not interactions:
        print("\n  ✅ No significant interactions detected\n")
    else:
        # Sort by severity
        order = ["contraindicated","major","moderate","minor"]
        sorted_ix = sorted(interactions, key=lambda x: order.index(x.get("severity","minor")))
        for ix in sorted_ix:
            sev = ix.get("severity","minor")
            icon = SEVERITY_ICON.get(sev,"•")
            print(f"\n  {icon} {sev.upper()}: {ix.get('drug_a','')} + {ix.get('drug_b','')}")
            print(f"     Effect: {ix.get('effect','')}")
            print(f"     Why: {ix.get('mechanism','')}")
            print(f"     Management: {ix.get('management','')}")
            if ix.get("monitoring"):
                print(f"     Monitor: {ix.get('monitoring','')}")
            symptoms = ix.get("symptoms_to_watch",[])
            if symptoms:
                print(f"     Watch for: {', '.join(symptoms[:3])}")
            alts = ix.get("alternatives",[])
            if alts:
                print(f"     Alternatives: {', '.join(alts[:2])}")

    food = r.get("food_interactions",[])
    if food:
        print(f"\n{'─'*60}\n  FOOD INTERACTIONS")
        for f in food:
            icon = SEVERITY_ICON.get(f.get("severity","minor"),"•")
            print(f"  {icon} {f.get('drug','')} + {f.get('food','')}: {f.get('effect','')}")

    safe = r.get("safe_combinations",[])
    if safe:
        print(f"\n{'─'*60}\n  GENERALLY SAFE COMBINATIONS")
        for s in safe: print(f"  ✅ {s}")

    note = r.get("pharmacist_note","")
    if note:
        print(f"\n{'─'*60}\n  PHARMACIST NOTE\n  {note}")

    print(f"\n  {r.get('disclaimer','')}")
    print(f"{'═'*60}\n")

if __name__ == "__main__":
    args = sys.argv[1:]
    if not args:
        print("Usage: python -m drug_interaction_api Drug1 Drug2 Drug3 ... [--json]")
        print("Example: python -m drug_interaction_api Warfarin Aspirin Ibuprofen")
        sys.exit(0)

    meds = [a for a in args if not a.startswith("--")]
    if len(meds) < 2:
        print("Please provide at least 2 medications to check interactions")
        sys.exit(1)

    result = check_interactions(meds)

    if "--json" in args:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print_report(result)
