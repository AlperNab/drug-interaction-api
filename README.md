# drug-interaction-api

> **List of medications → interaction warnings.** Severity scores, mechanism explanations, monitoring recommendations, safer alternatives. For pharmacists, developers, and healthcare platforms.

[![PyPI](https://img.shields.io/pypi/v/drug-interaction-api?style=flat)](https://pypi.org/project/drug-interaction-api/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

⚠️ **Medical disclaimer:** Educational and informational only. Always verify with a licensed pharmacist or physician. Never use as a substitute for professional medical advice.

## Quickstart

```bash
pip install drug-interaction-api
python -m drug_interaction_api Warfarin Aspirin Ibuprofen
python -m drug_interaction_api Metformin Lisinopril Atorvastatin --json
```

## Example output

```
  🚫 CONTRAINDICATED: Warfarin + Ibuprofen
     Effect: Significantly increased bleeding risk — GI bleeds, bruising
     Why: NSAIDs inhibit platelet function AND displace warfarin from
          plasma proteins, raising free warfarin levels
     Management: Avoid combination. Use acetaminophen for pain instead.
     Monitor: PT/INR if combination unavoidable
     Alternatives: Acetaminophen, topical diclofenac

  🟠 MODERATE: Warfarin + Aspirin
     Effect: Increased anticoagulation and bleeding risk
     Management: Use lowest effective aspirin dose, monitor INR closely
```

## Python API

```python
from drug_interaction_api import check_interactions

result = check_interactions(["Warfarin", "Aspirin", "Metoprolol"])
for ix in result["interactions"]:
    print(f"{ix['severity']}: {ix['drug_a']} + {ix['drug_b']}")
    print(f"  {ix['effect']}")
```

## License
MIT © [Alper Nabil Gabra Zakher](https://github.com/AlperNab)
