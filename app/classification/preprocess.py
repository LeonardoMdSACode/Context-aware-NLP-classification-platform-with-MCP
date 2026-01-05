import re
from typing import List


def clean_text(text: str) -> str:
    """
    Minimal preprocessing: normalize whitespace, remove control chars.
    """
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[\x00-\x1f]+", "", text)
    return text


def tokenize(text: str) -> List[str]:
    """
    Simple whitespace tokenizer.
    """
    text = clean_text(text)
    return text.split()
