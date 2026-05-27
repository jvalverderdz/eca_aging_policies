"""
3_6a_prep_country_inputs.py
----------------------------
Reads aging_policies_QA.csv and writes one formatted TXT per country into
temp/country_inputs/.  Each TXT contains, for every question, the top-3
chunks (by rank) so Claude can read them and write summaries.

Run once before summarisation.
"""
import re
import pandas as pd
from pathlib import Path

DATA    = Path("D:/OneDrive/Aging_Update/Projects/Aging Well/Data")
QA_CSV  = DATA / "output" / "aging_policies_QA.csv"
OUT_DIR = DATA / "temp" / "country_inputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

TOP_K = 5   # chunks to keep per question (reduces context load)

GARBAGE_RE = re.compile(
    r"^[\s\.\-_·•◦▪▸►○●\d]+$"          # lines that are only dots/numbers/bullets
    r"|(\.\s*){5,}"                      # runs of 5+ ". "
    r"|(\-\s*){5,}",                     # runs of 5+ "- "
    re.MULTILINE,
)

def is_toc_chunk(text: str) -> bool:
    """Heuristic: chunk looks like a table of contents / index."""
    lines      = [l.strip() for l in text.splitlines() if l.strip()]
    if not lines:
        return True
    dot_lines  = sum(1 for l in lines if re.search(r"\.{4,}", l) or re.search(r"\d+\s*$", l))
    short_pct  = sum(1 for l in lines if len(l) < 40) / max(len(lines), 1)
    return dot_lines / max(len(lines), 1) > 0.4 or short_pct > 0.8

def clean_chunk(text: str) -> str:
    text = re.sub(r"Machine Translated by Google\s*", "", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = GARBAGE_RE.sub("", text)
    return text.strip()


df = pd.read_csv(QA_CSV, encoding="utf-8")
df = df[df["rank"] <= TOP_K].copy()

for country, grp in df.groupby("source"):
    lines = [f"COUNTRY: {country}\n{'='*60}\n"]
    for question, qgrp in grp.groupby("question", sort=False):
        lines.append(f"\nQUESTION: {question}\n{'-'*60}")
        kept = 0
        for _, row in qgrp.sort_values("rank").iterrows():
            chunk = clean_chunk(str(row["text"]))
            if not chunk or is_toc_chunk(chunk):
                continue
            lines.append(f"[chunk_id={row['chunk_id']}]\n{chunk}")
            kept += 1
        if kept == 0:
            lines.append("[No usable chunks found for this question]")

    out_path = OUT_DIR / f"{country}_input.txt"
    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"[{country}] written -> {out_path.name}")

print("\nDone. All country input files written.")
