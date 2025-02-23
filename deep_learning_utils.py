# deep_learning_utils.py

from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load a small, fast model at startup
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def get_text_embedding(text):
    """
    Returns an embedding vector for the given text using a Sentence-Transformers model.
    """
    # The 'encode' method returns a NumPy array if convert_to_numpy=True
    embedding = model.encode(text, convert_to_numpy=True)
    return embedding

def compute_similarity(embedding1, embedding2):
    """
    Compute cosine similarity between two embedding vectors (1 = very similar, 0 = dissimilar).
    """
    embedding1 = embedding1.reshape(1, -1)
    embedding2 = embedding2.reshape(1, -1)
    similarity = cosine_similarity(embedding1, embedding2)
    return float(similarity[0][0])
