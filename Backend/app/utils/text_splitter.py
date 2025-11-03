from __future__ import annotations
from typing import List
import re

# Simple sentence-aware chunker with fallback to char chunks

def split_text(text: str, chunk_size: int = 1200, chunk_overlap: int = 200) -> List[str]:
    text = text.strip()
    if not text:
        return []

    # Try sentence split by punctuation
    sentences = re.split(r"(?<=[\.\?\!])\s+", text)
    chunks: List[str] = []
    current = ""

    for s in sentences:
        if len(current) + len(s) + 1 <= chunk_size:
            current = (current + " " + s).strip()
        else:
            if current:
                chunks.append(current)
            # start new chunk with overlap from previous
            if chunk_overlap > 0 and chunks:
                overlap = chunks[-1][-chunk_overlap:]
            else:
                overlap = ""
            current = (overlap + (" " if overlap else "") + s).strip()

    if current:
        chunks.append(current)

    # Ensure max length
    final: List[str] = []
    for c in chunks:
        if len(c) <= chunk_size:
            final.append(c)
        else:
            # hard split
            for i in range(0, len(c), chunk_size - chunk_overlap):
                final.append(c[i : i + (chunk_size - chunk_overlap)])
    return final
