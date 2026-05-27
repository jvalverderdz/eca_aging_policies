"""
3_0_clean_texts.py
@author: JValverdeRdz
------------------
This script:
  Step 1 - Extracts every PDF to TXT, mirroring the pdf/ folder structure
           under a sibling txt/ folder:
             CODE/txt/eng/   ← extracted from CODE/pdf/eng/
             CODE/txt/LANG/  ← extracted from CODE/pdf/LANG/

  Step 2 - Consolidates all TXTs per country (all languages) into
             CODE/aging-policies-CODE.txt

Note: translation is no longer needed — multilingual semantic search
(3_3b_search_aging_policies.py) handles cross-lingual retrieval directly.

Requires:
  pip install pdfplumber
"""

import logging
from pathlib import Path

import pdfplumber

# pdfminer (used internally by pdfplumber) emits noisy font warnings for
# Cyrillic / non-Latin PDFs. They are harmless — suppress them.
logging.getLogger("pdfminer").setLevel(logging.ERROR)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PATH         = Path("D:/OneDrive/Aging_Update/Projects/Aging Well/Data")
RAW_POLICIES = PATH / "raw" / "aging_policies"
MIPAA        = PATH / "raw" / "mipaa"


# ---------------------------------------------------------------------------
# Step 1: Extract PDFs to TXT
# ---------------------------------------------------------------------------

def extract_pdfs() -> None:
    for country_dir in sorted(RAW_POLICIES.iterdir()):
        if not country_dir.is_dir():
            continue
        pdf_root = country_dir / "pdf"
        if not pdf_root.exists():
            continue

        code = country_dir.name
        print(f"\n[{code}] extracting PDFs …")

        for lang_dir in sorted(pdf_root.iterdir()):
            if not lang_dir.is_dir():
                continue
            lang    = lang_dir.name
            txt_dir = country_dir / "txt" / lang
            txt_dir.mkdir(parents=True, exist_ok=True)

            for pdf_file in sorted(lang_dir.glob("*.pdf")):
                out_file = txt_dir / (pdf_file.stem + ".txt")
                if out_file.exists():
                    print(f"  [skip]   {lang}/{pdf_file.name}")
                    continue

                text = _pdf_to_text(pdf_file)
                out_file.write_text(text, encoding="utf-8")
                status = "ok" if text.strip() else "empty"
                print(f"  [{status}]     {lang}/{pdf_file.name}")


def _pdf_to_text(pdf_path: Path) -> str:
    pages: list[str] = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
    except Exception as exc:
        print(f"    [warn] {pdf_path.name}: {exc}")
    return "\n\n".join(pages)


# ---------------------------------------------------------------------------
# Step 2: Consolidate all TXTs per country → aging-policies-CODE.txt
# ---------------------------------------------------------------------------

def consolidate() -> None:
    for country_dir in sorted(RAW_POLICIES.iterdir()):
        if not country_dir.is_dir():
            continue
        code     = country_dir.name
        txt_root = country_dir / "txt"
        if not txt_root.exists():
            continue

        sections: list[str] = []
        for lang_dir in sorted(txt_root.iterdir()):
            if not lang_dir.is_dir():
                continue
            lang = lang_dir.name
            for f in sorted(lang_dir.glob("*.txt")):
                content = f.read_text(encoding="utf-8", errors="replace").strip()
                if content:
                    sections.append(f"=== {f.stem} [{lang}] ===\n\n{content}")

        # Append MIPAA report if one exists for this country
        mipaa_file = MIPAA / f"mipaa-report-{code}.txt"
        if mipaa_file.exists():
            content = mipaa_file.read_text(encoding="utf-8", errors="replace").strip()
            if content:
                sections.append(f"=== mipaa-report-{code} [eng] ===\n\n{content}")
                print(f"  [mipaa]  mipaa-report-{code}.txt appended")

        if not sections:
            print(f"\n[{code}] no TXTs found — skipping")
            continue

        out_file = country_dir / f"aging-policies-{code}.txt"
        out_file.write_text("\n\n\n".join(sections), encoding="utf-8")
        print(f"\n[{code}] consolidated {len(sections)} docs → aging-policies-{code}.txt")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("=" * 60)
    print("Step 1 — Extract PDFs to TXT")
    print("=" * 60)
    extract_pdfs()

    print("\n" + "=" * 60)
    print("Step 2 — Consolidate TXTs per country")
    print("=" * 60)
    consolidate()

    print("\nAll done.")
