from typing import List
from abc import ABC, abstractmethod
import numpy as np
from sentence_transformers import SentenceTransformer


class Embedder(ABC):
    """
    Transform text inputs to embeddings.
    """

    @abstractmethod
    def embed(self, inputs: List[str]) -> np.ndarray:
        """
        Transform a list of N input strings into a numpy array containing embeddings of shape [N, embed_dim]
        """
        pass


class GTEEmbedder(Embedder):
    """
    gte-large is third place on https://huggingface.co/spaces/mteb/leaderboard
    https://huggingface.co/thenlper/gte-large
    """

    def __init__(self, model_type="gte-large"):
        allowed_types = ["gte-large", "gte-base", "gte-small"]
        assert (
            model_type in allowed_types
        ), 'f"Model type must be one of {allowed_types}"'
        self.model = SentenceTransformer(f"thenlper/{model_type}")

    def embed(self, inputs: List[str]) -> np.ndarray:
        return self.model.encode(inputs)
