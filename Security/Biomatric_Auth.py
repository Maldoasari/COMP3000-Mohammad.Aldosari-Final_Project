import librosa
from scipy.spatial import distance
def Voice_Auth(O_Sample, N_Sample):
# Load audio files
 audio1, sr1 = librosa.load("user_audio2.wav")
 audio2, sr2 = librosa.load("user_audio.wav")

# Extract MFCC
 mfcc1 = librosa.feature.mfcc(y=audio1, sr=sr1)
 mfcc2 = librosa.feature.mfcc(y=audio2, sr=sr2)

# Flatten the MFCC arrays
 mfcc1_flat = mfcc1.flatten()
 mfcc2_flat = mfcc2.flatten()

# Calculate cosine similarity between the two flattened MFCC arrays
 similarity = 1 - distance.cosine(mfcc1_flat, mfcc2_flat)

# Set a similarity threshold to determine if they are the same person
 threshold = 0.9714  # You can adjust this threshold based on your needs

 if similarity >= threshold:
    print(similarity)
    print("The audio files are likely from the same person.")
    return True
 else:
    print(similarity)
    print("The audio files are likely from different people.")
    return False
