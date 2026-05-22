"""Embedding Service

Converts text into normalized embedding vectors using TF-IDF approach.
"""

import math
import re
from collections import Counter
from typing import Dict


class EmbeddingService:
    """Generates text embeddings using lightweight TF-IDF approach."""
    
    def get_embedding(self, text: str) -> Dict[str, float]:
        """Convert text into embedding vector.
        
        Uses a simple TF-based approach:
        1. Tokenize text into words
        2. Count word frequencies
        3. Normalize to unit vector
        
        Args:
            text: The text to embed.
            
        Returns:
            Normalized embedding vector (list of floats).
        """
        if not text or not text.strip():
            return {}

        # Tokenize and count
        tokens = re.findall(r"[a-z0-9]+", text.lower())
        counts = Counter(tokens)

        if not counts:
            return {}

        # Build normalized tf vector as a mapping token -> normalized weight
        sq_sum = sum((count * count for count in counts.values()))
        magnitude = math.sqrt(sq_sum) if sq_sum > 0 else 1.0

        return {token: (count / magnitude) for token, count in counts.items()}