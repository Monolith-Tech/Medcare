from sklearn.cluster import KMeans
from sklearn.metrics.pairwise import cosine_similarity
from transformers import pipeline, AutoTokenizer, AutoModel
import numpy as np

# Load transformers models
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-mpnet-base-v2")
model = AutoModel.from_pretrained("sentence-transformers/all-mpnet-base-v2")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

# Function to embed sentences
def embed_sentences(sentences):
    encoded_input = tokenizer(sentences, padding=True, truncation=True, return_tensors='pt')
    with torch.no_grad():
        model_output = model(**encoded_input)
    sentence_embeddings = mean(model_output.last_hidden_state, dim=1).numpy()
    return sentence_embeddings

# Example sentences (replace with your data)
sentences = [
    "The patient complains of severe headache.",
    "The headache has been persistent for the last three days.",
    "No history of migraines.",
    "Patient shows signs of dehydration.",
    "Recommend hydration and rest."
]

# Embed sentences
sentence_embeddings = embed_sentences(sentences)

# Clustering
num_clusters = 2  # Adjust based on your data or use methods to find the optimal number of clusters
clustering_model = KMeans(n_clusters=num_clusters)
clustering_model.fit(sentence_embeddings)
cluster_assignment = clustering_model.labels_

# Summarize each cluster
summaries = []
for cluster_id in range(num_clusters):
    cluster_sentences = [s for s, c in zip(sentences, cluster_assignment) if c == cluster_id]
    cluster_text = ' '.join(cluster_sentences)
    summary = summarizer(cluster_text, max_length=45, min_length=5, do_sample=False)
    summaries.append(summary[0]['summary_text'])

print(summaries)

