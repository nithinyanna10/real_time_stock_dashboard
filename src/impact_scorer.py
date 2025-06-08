# src/impact_scorer.py
from transformers import AutoTokenizer, AutoModel
import torch
from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Use a sentence transformer (e.g., MiniLM)
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Sample pre-trained model (simulate; replace with training logic as needed)
clf = RandomForestClassifier()
clf.fit([[0.1]*384, [0.5]*384, [0.9]*384], [0, 1, 2])  # 0: Low, 1: Medium, 2: High impact

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        output = model(**inputs)
    return output.last_hidden_state.mean(dim=1).squeeze().numpy()

def predict_impact(headline):
    emb = get_embedding(headline)
    score = clf.predict([emb])[0]
    label_map = {0: "🟢 Low", 1: "🟡 Medium", 2: "🔴 High"}
    return label_map[score]
