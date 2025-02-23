from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.metrics.pairwise import cosine_similarity
import spacy

# Load model and tokenizer once (this may take a few seconds during the first run)
tokenizer = AutoTokenizer.from_pretrained("distilbert-base-uncased")
model = AutoModel.from_pretrained("distilbert-base-uncased")

# Load spaCy model for keyword extraction (ensure you have downloaded 'en_core_web_sm')
nlp = spacy.load("en_core_web_sm")


def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    with torch.no_grad():
        outputs = model(**inputs)
    # Average the token embeddings to obtain a sentence embedding.
    embeddings = outputs.last_hidden_state.mean(dim=1)
    return embeddings.numpy()[0]


def compute_similarity(text1, text2):
    emb1 = get_embedding(text1)
    emb2 = get_embedding(text2)
    sim = cosine_similarity([emb1], [emb2])[0][0]
    return float(sim * 100)  # Return as a native Python float percentage


def find_missing_keywords(resume_text, job_text, threshold=0.7):
    """
    Extracts candidate keywords (noun chunks up to 3 words) from the job description using spaCy,
    then checks if they are semantically present in the resume using DistilBERT embeddings.
    If a keyword's similarity to the resume embedding is below the threshold, it's considered missing.
    """
    # Extract candidate keywords from job_text using spaCy noun chunks
    doc = nlp(job_text)
    candidate_keywords = list(set([
        chunk.text.lower()
        for chunk in doc.noun_chunks
        if len(chunk.text.split()) <= 3
    ]))

    missing = []
    # Compute embedding for the entire resume text once
    resume_embedding = get_embedding(resume_text)

    for keyword in candidate_keywords:
        keyword_embedding = get_embedding(keyword)
        sim = cosine_similarity([keyword_embedding], [resume_embedding])[0][0]
        if sim < threshold:
            missing.append(keyword)

    return missing
