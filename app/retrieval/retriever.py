from pathlib import Path
import re
from collections import Counter
from dataclasses import dataclass

@dataclass
class Chunk:
    source: str
    text: str

def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-zA-Z0-9]+", text.lower())

def load_chunks(directory: str = "data/reference_material") -> list[Chunk]:
    chunks = []
    path = Path(directory)
    if not path.exists():
        return chunks
    for file in sorted(path.glob("*.md")):
        content = file.read_text(encoding="utf-8")
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        for index, paragraph in enumerate(paragraphs, start=1):
            chunks.append(Chunk(f"{file.name}#chunk-{index}", paragraph))
    return chunks

def retrieve(query: str, top_k: int = 5, directory: str = "data/reference_material") -> list[Chunk]:
    """Small transparent lexical retriever for local reference grounding."""
    query_terms = set(_tokens(query))
    scored = []
    for chunk in load_chunks(directory):
        terms = _tokens(chunk.text)
        counts = Counter(terms)
        overlap = sum(counts[t] for t in query_terms)
        if overlap:
            scored.append((overlap / max(len(terms), 1), chunk))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [chunk for _, chunk in scored[:top_k]]
