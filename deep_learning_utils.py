from transformers import AutoTokenizer, AutoModel
import torch

# Load the model and tokenizer once at startup
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")

def get_text_embedding(text):
    """
    Given a text string, returns the average embedding vector using DistilBERT.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    outputs = model(**inputs)
    # The last_hidden_state has shape: (batch_size, sequence_length, hidden_size)
    embeddings = outputs.last_hidden_state
    # Average the token embeddings (across sequence length)
    avg_embedding = torch.mean(embeddings, dim=1)
    return avg_embedding.detach().numpy()[0]

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def compute_similarity(embedding1, embedding2):
    """
    Compute cosine similarity between two embedding vectors.
    Returns a value between 0 and 1 (1 means very similar).
    """
    embedding1 = embedding1.reshape(1, -1)
    embedding2 = embedding2.reshape(1, -1)
    similarity = cosine_similarity(embedding1, embedding2)
    return similarity[0][0]
