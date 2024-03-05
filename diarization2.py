from pyAudioAnalysis import audioSegmentation as aS

def speaker_diarization(filename, n_speakers=2, mid_window=2.0, mid_step=0.5, short_window=0.05, short_step=0.025):
    """
    Perform speaker diarization on an audio file with two speakers.

    :param filename: Path to the audio file
    :param n_speakers: Number of speakers to identify (default is 2)
    :param mid_window: Mid-term window size in seconds
    :param mid_step: Mid-term step size in seconds
    :param short_window: Short-term window size in seconds
    :param short_step: Short-term step size in seconds
    :return: None, prints segments and speaker labels
    """
    # Perform diarization using the speakerDiarization function from pyAudioAnalysis
    [flags, classes, accuracy, _] = aS.speaker_diarization(filename, n_speakers, mid_window=mid_window, mid_step=mid_step, short_window=short_window, short_step=short_step, lda_dim=0, plot_res=False)

    # flags: list of speaker flags (0 or 1) for each segment
    # classes: unique labels of speakers (should be 0 and 1 for two speakers)
    # accuracy: accuracy of diarization

    # Print the results
    for i, flag in enumerate(flags):
        segment_start = i * mid_step
        segment_end = segment_start + mid_window
        print(f"Time: {segment_start}-{segment_end} sec, Speaker: {int(flag)}")

# Example usage
filename = 'path/to/your/audiofile.wav'  # Replace this with the path to your audio file
speaker_diarization(filename)
