# Speaker Diarisation

from pyAudioAnalysis import (
    audioBasicIO,
    MidTermFeatures,
    ShortTermFeatures
)
from sklearn.cluster import KMeans
import numpy as np

def speaker_diarization(filename, mid_window, mid_step, short_window, short_step, n_speakers):
    # Load audio file
    [sampling_rate, signal] = audioBasicIO.read_audio_file(filename)
    
    # Mid-term feature extraction
    [mt_features, _, _] = MidTermFeatures.mid_feature_extraction(
        signal, sampling_rate, 
        mid_window * sampling_rate,
        mid_step * sampling_rate,
        round(sampling_rate * short_window),
        round(sampling_rate * short_step)
    )

    # Feature normalization
    mt_features_norm = MidTermFeatures.normalize_features([mt_features.T])[0].T

    # K-means clustering
    kmeans = KMeans(n_clusters=n_speakers)
    kmeans.fit(mt_features_norm.T)
    labels = kmeans.labels_

    # Segmenting the audio signal into clusters (assuming each cluster corresponds to a speaker)
    segments = np.zeros((len(labels), 2))
    for i, label in enumerate(labels):
        segments[i, 0] = i * mid_step
        segments[i, 1] = i * mid_step + mid_window

    return labels, segments

# Parameters
filename = 'demo_session.mp3'  # Path to the audio file
mid_window = 2.0  # Mid-term window size in seconds
mid_step = 0.5  # Mid-term step size in seconds
short_window = 0.05  # Short-term window size in seconds
short_step = 0.025  # Short-term step size in seconds
n_speakers = 2  # Number of speakers (clusters) to identify

labels, segments = speaker_diarization(filename, mid_window, mid_step, short_window, short_step, n_speakers)

print(labels)  # Prints the cluster labels of each segment
print(segments)  # Prints the start and end times of each segment
