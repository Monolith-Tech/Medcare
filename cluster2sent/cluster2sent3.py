import numpy as np
from sklearn.cluster import KMeans
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Initialize the tokenizer and model for embeddings
tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
model = AutoModelForSequenceClassification.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

# Example text data (list of sentences)
sentences = [
    "The patient complains of a headache.",
    "The headache has persisted for three days.",
    "There is no history of migraines.",
    "The patient shows signs of dehydration.",
    "Recommendation includes hydration and rest."
]

# Function to generate embeddings for a list of sentences
def get_embeddings(sentences):
    inputs = tokenizer(sentences, padding=True, truncation=True, return_tensors="pt", max_length=512)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return embeddings

# Generate sentence embeddings
embeddings = get_embeddings(sentences)

# Perform KMeans clustering
kmeans = KMeans(n_clusters=2, random_state=0).fit(embeddings)
labels = kmeans.labels_

# Summarize each cluster using the pipeline
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

clustered_sentences = {i: [] for i in range(kmeans.n_clusters)}
for sentence, label in zip(sentences, labels):
    clustered_sentences[label].append(sentence)

summaries = []
for cluster in clustered_sentences.values():
    cluster_text = ' '.join(cluster)
    summary = summarizer(cluster_text, max_length=130, min_length=30, do_sample=False)
    summaries.append(summary[0]['summary_text'])

for i, summary in enumerate(summaries):
    print(f"Cluster {i+1} Summary: {summary}")
