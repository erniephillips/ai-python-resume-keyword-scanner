from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the tokenizer and model once at startup
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")
model.eval()  # Set the model to evaluation mode

def get_text_embedding(text):
    """
    Given a text string, returns the average embedding vector using DistilBERT.
    Uses torch.no_grad() for efficient inference.
    """
    inputs = tokenizer(text, return_tensors="pt", truncation=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Get the last hidden state; shape: (batch_size, sequence_length, hidden_size)
    embeddings = outputs.last_hidden_state
    # Average the token embeddings along the sequence length dimension
    avg_embedding = torch.mean(embeddings, dim=1)
    # Move the embedding to CPU (if not already) and convert to a numpy array
    return avg_embedding.detach().cpu().numpy()[0]

def compute_similarity(embedding1, embedding2):
    """
    Compute cosine similarity between two embedding vectors.
    Returns a value between 0 and 1 (1 means very similar).
    """
    # Reshape embeddings to 2D arrays as required by cosine_similarity
    embedding1 = embedding1.reshape(1, -1)
    embedding2 = embedding2.reshape(1, -1)
    similarity = cosine_similarity(embedding1, embedding2)
    return similarity[0][0]
