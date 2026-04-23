# PROJECT DECISIONS

## Folder Structure Sign-off
The proposed folder structure is suitable and will be implemented to improve project organization and analysis efficiency.

### Final Structure
```
/corpus/
  /active/
    POJK-22-2023.txt
    POJK-40-2024.txt
    SEOJK-19-2025.txt
  /historical/
    POJK-77-2016.txt
    POJK-31-2020.txt
    POJK-10-2022.txt
    SEOJK-19-2023.txt
  manifest.json
/ground-truth/
  manual-analysis.md  (dari dok 07)
/prompts/
  friction-detection-v1.md
/backend/
  main.py
  ...
/frontend/
  ... (Next.js)
/docs/
  ARCHITECTURE.md
  DEMO_SCRIPT.md
README.md
.gitignore
```

### Rationale
- **Corpus Categorization:** Separating `active` and `historical` regulations allows the system to clearly distinguish between current law and outdated references, which is critical for "friction" and "inconsistency" detection.
- **Separation of Concerns:** Distinct directories for `frontend`, `backend`, and `prompts` ensure a clean development environment and simplify CI/CD pipelines.
- **Ground Truth:** Moving manual analysis to its own folder allows for automated evaluation of the model's performance against human findings.

**Signed off by:** Engineering Review
