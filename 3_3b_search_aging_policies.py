"""
3_3b_search_aging_policies.py
@author: JValverdeRdz
------------------------------
Multilingual semantic search over aging_policies chunks.

English questions are compared against native-language policy chunks using
paraphrase-multilingual-MiniLM-L12-v2 — a lightweight model (117MB, 50 languages)
that maps questions and text into a shared vector space, enabling cross-lingual
retrieval without translation. CPU-friendly (~1–2h for 22 countries).

Input:  temp/split_txts_aging/CODE_LANG/chunk_*.txt
        raw/questions.csv  (column: "question")
Output: output/aging_policies_QA.csv

Requires:
  pip install sentence-transformers pandas numpy
"""
from __future__ import annotations

import os
os.environ["HF_HOME"] = "D:/huggingface_cache"

from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

PATH       = Path("D:/OneDrive/Aging_Update/Projects/Aging Well/Data")
TEMP       = PATH / "temp"
CHUNKS_DIR = TEMP / "split_txts_aging"
OUTPUT     = PATH / "output"
QUESTIONS_CSV = PATH / "raw" / "questions.csv"
RESULTS_CSV   = OUTPUT / "aging_policies_QA.csv"

# paraphrase-multilingual-MiniLM-L12-v2: 50 languages, ~117MB, CPU-friendly.
# Upgrade to "intfloat/multilingual-e5-large" if a GPU is available (better quality).
MODEL_NAME = "paraphrase-multilingual-MiniLM-L12-v2"

TOP_K = 10   # top chunks to retrieve per question per document


# ---------------------------------------------------------------------------
# Load chunks grouped by source folder (CODE_LANG)
# ---------------------------------------------------------------------------

def load_chunks(chunks_dir: Path) -> dict[str, list[dict]]:
    corpus: dict[str, list[dict]] = {}

    for folder in sorted(chunks_dir.iterdir()):
        if not folder.is_dir():
            continue
        records = []
        for chunk_file in sorted(folder.iterdir()):
            text = chunk_file.read_text(encoding="utf-8", errors="replace").strip()
            if text and ".........." not in text:
                records.append({"chunk_id": chunk_file.name, "text": text})
        if records:
            corpus[folder.name] = records
            print(f"[load_chunks] '{folder.name}': {len(records)} chunks")

    print(f"[load_chunks] Total sources: {len(corpus)}\n")
    return corpus


# ---------------------------------------------------------------------------
# Load questions
# ---------------------------------------------------------------------------

def load_questions(questions_csv: Path) -> list[str]:
    df        = pd.read_csv(questions_csv, encoding="utf-8")
    questions = df["question"].dropna().str.strip().tolist()
    questions = [q for q in questions if q]
    print(f"[load_questions] {len(questions)} questions loaded.\n")
    return questions


# ---------------------------------------------------------------------------
# Embed chunks for one source
# ---------------------------------------------------------------------------

def embed_chunks(records: list[dict], model: SentenceTransformer, source_name: str) -> pd.DataFrame:
    texts      = [r["text"] for r in records]
    embeddings = model.encode(texts, normalize_embeddings=True, show_progress_bar=True)

    rows = [
        {"source": source_name, "chunk_id": r["chunk_id"],
         "text": r["text"], "embedding": embeddings[i]}
        for i, r in enumerate(records)
    ]
    df = pd.DataFrame(rows)
    print(f"[embed_chunks] '{source_name}': {len(df)} embeddings computed.")
    return df


# ---------------------------------------------------------------------------
# Semantic search + export
# ---------------------------------------------------------------------------

def semantic_search_and_export(
    corpus: dict[str, list[dict]],
    questions: list[str],
    model: SentenceTransformer,
    results_path: Path,
    top_k: int = TOP_K,
) -> None:

    print("[semantic_search] Encoding questions …")
    question_embeddings = model.encode(
        questions,
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    print(f"[semantic_search] {len(questions)} question vectors ready.\n")

    all_rows: list[dict] = []

    for source_name, records in corpus.items():
        print(f"[semantic_search] Processing: '{source_name}' …")
        chunks_df        = embed_chunks(records, model, source_name)
        chunk_embeddings = np.array(chunks_df["embedding"].tolist())

        for q_idx, question in enumerate(questions):
            scores      = chunk_embeddings @ question_embeddings[q_idx]
            top_indices = np.argsort(scores)[::-1][:min(top_k, len(chunks_df))]

            for rank, idx in enumerate(top_indices, start=1):
                row = chunks_df.iloc[idx]
                all_rows.append({
                    "source":   source_name,
                    "question": question,
                    "rank":     rank,
                    "chunk_id": row["chunk_id"],
                    "score":    round(float(scores[idx]), 6),
                    "text":     row["text"],
                })

    results_path.parent.mkdir(parents=True, exist_ok=True)
    out_df = pd.DataFrame(all_rows, columns=["source", "question", "rank", "chunk_id", "score", "text"])
    out_df.to_csv(results_path, index=False, encoding="utf-8")
    print(f"\n[done] {len(out_df)} rows → {results_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print(f"[main] Loading model: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)

    corpus    = load_chunks(CHUNKS_DIR)
    questions = load_questions(QUESTIONS_CSV)

    semantic_search_and_export(
        corpus=corpus,
        questions=questions,
        model=model,
        results_path=RESULTS_CSV,
        top_k=TOP_K,
    )
