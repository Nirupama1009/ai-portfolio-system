"""Similarity Engine Service

Calculates cosine similarity between embedding vectors.
"""

import math
from typing import List, Union, Dict


class SimilarityEngine:
    """Computes similarity scores between embedding vectors."""
    
    @staticmethod
    def calculate_similarity(vector1: Union[List[float], List, Dict[str, float]], vector2: Union[List[float], List, Dict[str, float]]) -> float:
        """Calculate cosine similarity between two embedding vectors.
        
        Uses cosine similarity formula to measure the angle between vectors.
        Returns a value between 0 (completely dissimilar) and 1 (identical).
        
        Args:
            vector1: First embedding vector.
            vector2: Second embedding vector.
            
        Returns:
            Cosine similarity score between 0 and 1.
        """
        # Support dict-based embeddings (token -> weight) for aligned cosine similarity
        if not vector1 or not vector2:
            return 0.0

        # If both are dicts, compute cosine using token intersection
        if isinstance(vector1, dict) and isinstance(vector2, dict):
            # Dot product over common tokens
            common = set(vector1.keys()) & set(vector2.keys())
            if not common:
                return 0.0
            dot_product = sum(vector1[t] * vector2[t] for t in common)
            magnitude1 = math.sqrt(sum(v * v for v in vector1.values()))
            magnitude2 = math.sqrt(sum(v * v for v in vector2.values()))
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            return float(dot_product / (magnitude1 * magnitude2))

        # Fallback to list-based calculation for legacy vectors
        if isinstance(vector1, list) and isinstance(vector2, list):
            length = min(len(vector1), len(vector2))
            dot_product = sum(vector1[index] * vector2[index] for index in range(length))
            magnitude1 = math.sqrt(sum(value * value for value in vector1))
            magnitude2 = math.sqrt(sum(value * value for value in vector2))
            if magnitude1 == 0 or magnitude2 == 0:
                return 0.0
            return float(dot_product / (magnitude1 * magnitude2))

        # If types mismatch, return 0
        return 0.0
    