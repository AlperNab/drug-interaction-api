# Drug Interaction Api — Standalone Real GUI Implementation

This folder is now its own runnable project app. It does not depend on the root all-project dashboard at runtime.

## Run

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default URL: `http://127.0.0.1:9118`

## What is inside this project folder

- `app/` — FastAPI backend for this project.
- `static/` — elegant browser GUI.
- `plugins/drug-interaction-api.json` — this project’s own feature/customization/input schema.
- `project_config.json` — readable copy of the same project-specific configuration.
- `data/` — local SQLite jobs, uploads, exports.
- `tests/` — verifies this project has a registered real local engine.

## Project-specific scope

- Domain: `Medical / Medication Safety`
- Target user: `Domain operator, business owner, analyst, or team member who needs this workflow executed reliably.`
- Core job: Medication list → interaction warnings
- Suite: `Medical & Research Suite`

## Deep features applied

- interaction matrix
- severity rationale
- patient context modifiers
- mechanism explanation
- monitoring plan
- alternative suggestions
- evidence links

## Customization controls

- `execution_mode` — Execution mode (select)
- `country_database` — country database (select)
- `age_group` — age group (text)
- `pregnancy_renal_hepatic_context` — pregnancy/renal/hepatic context (text)
- `severity_threshold` — severity threshold (slider)
- `output_audience` — output audience (select)
- `local_only_mode` — local-only mode (select)
- `output_format` — output format (select)
- `language` — language (select)
- `privacy_mode` — privacy mode (select)
- `confidence_threshold` — Confidence threshold (slider)

## Input fields

- `medication_list` — Medication list (text) required
- `work_brief` — Work brief / source text / URL / instructions (textarea) required

## External data policy

The local deterministic core is real and executable. Live external systems are not simulated. If Shopify, ATS, ERP, OCR/STT, maps, SERP, market data, medical databases, tax/customs databases, or other live systems are required, this project reports the missing connector/API requirement instead of inventing data.

---

## Final UX/UI Layer

This project now uses the **Evidence & Safety Workbench** pattern.

**UX workflow:** Source intake → evidence extraction → safety review → study/learning output

**Domain components:**
- Medication list panel
- Interaction severity matrix
- Contraindication warnings
- Dose/unit checks
- Clinician review gate

**Quick actions:**
- Normalize medications
- Check interactions
- Flag severe risks
- Prepare review note

**No fake-data policy:** external/live actions require real connectors or API keys. Missing connectors are reported instead of simulated.
