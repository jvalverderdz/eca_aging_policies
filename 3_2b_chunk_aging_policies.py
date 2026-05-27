"""
3_2b_chunk_aging_policies.py
@author: JValverdeRdz
-----------------------------
Splits each country's consolidated aging-policies-CODE.txt into
~500-char sentence-grouped chunks for multilingual semantic search.

Input:  raw/aging_policies/CODE/aging-policies-CODE.txt  (one file per country,
        produced by 3_0_clean_texts.py)
Output: temp/split_txts_aging/CODE/{docname}_{idx:03d}.txt  (one folder per country)

Requires:
  pip install (none — stdlib only)
"""

import re
from pathlib import Path

PATH         = Path("D:/OneDrive/Aging_Update/Projects/Aging Well/Data")
RAW_POLICIES = PATH / "raw" / "aging_policies"
TEMP         = PATH / "temp"
SPLIT        = TEMP / "split_txts_aging"

CHUNK_MAX_CHARS = 500   # same target size as 3_2_process_texts.py


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

SECTION_RE = re.compile(r"=== (.+?) \[.+?\] ===")


def chunk_all() -> None:
    SPLIT.mkdir(parents=True, exist_ok=True)

    for country_dir in sorted(RAW_POLICIES.iterdir()):
        if not country_dir.is_dir():
            continue
        code         = country_dir.name
        consolidated = country_dir / f"aging-policies-{code}.txt"

        if not consolidated.exists():
            print(f"[{code}] no consolidated file found — skipping (run 3_0 first)")
            continue

        out_dir = SPLIT / code
        out_dir.mkdir(parents=True, exist_ok=True)

        text     = consolidated.read_text(encoding="utf-8", errors="replace")
        sections = _split_by_headers(text)
        total    = 0

        for doc_name, content in sections:
            content = _clean(content)
            chunks  = [c for c in _split_into_chunks(content) if c.strip()]
            for idx, chunk in enumerate(chunks, start=1):
                filename = f"{doc_name}_{idx:03d}.txt"
                (out_dir / filename).write_text(chunk, encoding="utf-8")
            total += len(chunks)

        print(f"[{code}] {len(sections)} docs → {total} chunks → {out_dir}")


def _split_by_headers(text: str) -> list[tuple[str, str]]:
    """Split consolidated text into (doc_name, content) pairs by === header ===."""
    parts    = SECTION_RE.split(text)
    # parts[0] = text before first header (discard)
    # parts[1] = doc_name, parts[2] = content, parts[3] = doc_name, ...
    sections = []
    for i in range(1, len(parts) - 1, 2):
        doc_name = parts[i].strip()
        content  = parts[i + 1].strip()
        if content:
            sections.append((doc_name, content))
    return sections


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _clean(text: str) -> str:
    text = re.sub(r" {2,}", " ", text)                   # collapse double spaces
    text = text.replace("Machine Translated by Google", "")
    text = re.sub(r"\n{2,}", "\n", text)                 # collapse blank lines
    text = re.sub(r"[,]{2,}", "", text)                  # remove repeated commas
    text = re.sub(r"\.\.", ".", text)                    # remove double periods
    return text.strip()


def _split_into_chunks(text: str) -> list[str]:
    # Split on sentence boundaries: period followed by space, newline, or comma
    sentence_re = re.compile(r"\.( |\n|,,)")
    parts       = sentence_re.split(text)

    sentences: list[str] = []
    i = 0
    while i < len(parts):
        segment = parts[i]
        if i + 1 < len(parts):
            segment = segment + "." + parts[i + 1]
            i += 2
        else:
            i += 1
        segment = segment.strip()
        if segment:
            sentences.append(segment)

    # Group sentences into chunks capped at CHUNK_MAX_CHARS
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for sentence in sentences:
        candidate_len = current_len + (1 if current else 0) + len(sentence)
        if current and candidate_len > CHUNK_MAX_CHARS:
            chunks.append(" ".join(current))
            current     = [sentence]
            current_len = len(sentence)
        else:
            current.append(sentence)
            current_len = candidate_len

    if current:
        chunks.append(" ".join(current))

    return chunks


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    chunk_all()
    print("\nDone.")
