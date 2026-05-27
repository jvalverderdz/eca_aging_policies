"""
3_6c_combine_summaries.py
--------------------------
Reads all per-country summary TXT files from temp/country_summaries/,
parses them, and produces the final wide CSV:
  - 22 rows (one per country)
  - 95 columns: 'country' + for each of 47 questions: answer column + source column

Summary TXT format expected (written by Claude per country):
  COUNTRY: XXX
  ============
  QUESTION: <question text>
  ANSWER: <summary text starting with YES/NO/PARTIALLY>
  SOURCE: chunk_id1, chunk_id2, ...
  ---
  QUESTION: ...
  ...
"""
import re
import pandas as pd
from pathlib import Path

DATA         = Path("D:/OneDrive/Aging_Update/Projects/Aging Well/Data")
SUMMARIES    = DATA / "temp" / "country_summaries"
OUTPUT_CSV   = DATA / "output" / "aging_policies_answers.csv"

QUESTIONS_CSV = DATA / "raw" / "questions.csv"
questions = pd.read_csv(QUESTIONS_CSV)["question"].dropna().str.strip().tolist()

def parse_summary_file(path: Path) -> dict:
    text    = path.read_text(encoding="utf-8")
    country = re.search(r"^COUNTRY:\s*(\w+)", text, re.MULTILINE)
    country = country.group(1).strip() if country else path.stem.split("_")[0]

    record  = {"country": country}

    blocks  = re.split(r"\n---\n", text)
    for block in blocks:
        q_match = re.search(r"QUESTION:\s*(.+?)(?=\nANSWER:)", block, re.DOTALL)
        a_match = re.search(r"ANSWER:\s*(.+?)(?=\nSOURCE:|\Z)", block, re.DOTALL)
        s_match = re.search(r"SOURCE:\s*(.+?)(?=\Z)", block, re.DOTALL)

        if not q_match or not a_match:
            continue

        q = q_match.group(1).strip()
        a = a_match.group(1).strip()
        s = s_match.group(1).strip() if s_match else ""

        record[q]             = a
        record[q + "__src"]   = s

    return record


records = []
for f in sorted(SUMMARIES.glob("*_summary.txt")):
    rec = parse_summary_file(f)
    records.append(rec)
    print(f"Parsed: {f.name}  ({len(rec)} fields)")

df = pd.DataFrame(records)

# Build ordered columns: country, then q/src pairs in question order
cols = ["country"]
for q in questions:
    if q in df.columns:
        cols.append(q)
        src_col = q + "__src"
        cols.append(src_col if src_col in df.columns else q + "__src")

# Add any remaining columns not in questions list
extra = [c for c in df.columns if c not in cols]
cols  = cols + extra

df = df[cols]
df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")
print(f"\nFinal CSV → {OUTPUT_CSV}  ({df.shape[0]} rows × {df.shape[1]} columns)")
