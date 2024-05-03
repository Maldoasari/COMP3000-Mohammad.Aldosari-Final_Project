import csv
import random
import os, wave, webrtcvad, librosa, scipy
from pydub import AudioSegment
import speech_recognition as sr
import numpy as np

def IsSpeech(filename):
    # Resample the audio
    resampled_audio = resample_wav_file(filename=filename)
    resampled_audio.export('Database/bin/resampled_aud', format="wav")
    
    # Initialize VAD
    vad = webrtcvad.Vad(2)
    
    with wave.open('Database/bin/resampled_aud', 'rb') as wf:
        sample_rate = wf.getframerate()
        if sample_rate not in (8000, 16000, 32000, 48000):
            raise ValueError(f"Unsupported sample rate: {sample_rate}")

        # Calculate the number of audio frames per chunk (e.g., 20 ms)
        frames_per_chunk = int(sample_rate * 0.02)  
        bytes_per_chunk = frames_per_chunk * 2  
        audio_frames = []

        # Read and process each chunk
        audio_chunk = wf.readframes(frames_per_chunk)
        while len(audio_chunk) == bytes_per_chunk:
            # Check for speech in the chunk
            if vad.is_speech(audio_chunk, sample_rate):
                audio_frames.append(audio_chunk)
            audio_chunk = wf.readframes(frames_per_chunk)
        
        # Combine voice detected chunks
        combined_audio = b''.join(audio_frames)
        with wave.open("Database/bin/vad_combined_audio.wav", 'wb') as out_wf:
            out_wf.setnchannels(1)
            out_wf.setsampwidth(wf.getsampwidth())
            out_wf.setframerate(sample_rate)
            out_wf.writeframes(combined_audio)
    audio = AudioSegment.from_file("Database/bin/vad_combined_audio.wav", format="wav")
    if len(audio) <= 0:
        return False
    # Check for background noise on the combined audio
    elif isit_background_noise("Database/bin/vad_combined_audio.wav"):
        return False
    else:  
    # Convert frames to AudioData for recognition
    # Load your audio file
     recognizer = sr.Recognizer()
     with sr.AudioFile(filename) as source:
    # Record the audio file as an audio data object
      audio_data = recognizer.record(source)
      recognized_text = recognizer.recognize_google(audio_data)
     try:
        if len(recognized_text) > 0:
            return recognized_text
        else:
            return None
     except sr.UnknownValueError:
        return 500
     except sr.RequestError:
        return "API unavailable."
csv_file = 'Voice_Assistant/shortjokes.csv'   
with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        jokes = [row['Joke'] for row in reader]
        
def get_random_joke():
    random.shuffle(jokes)
    return random.choice(jokes)


def resample_wav_file(filename, target_sample_rate=16000):
    audio = AudioSegment.from_wav(filename)
    resampled_audio = audio.set_frame_rate(target_sample_rate)
    return resampled_audio
def delete_recording(filename1, filename2, filename3, filename4, filename5):
    try:
        os.remove(filename1)
        os.remove(filename2)
        os.remove(filename3)
        os.remove(filename4)
        os.remove(filename5)
    except FileNotFoundError:
        print(f"File not found!")
    except Exception as e:
        print(f"Error occurred: {e}")

def save_audio_as_wav(audio_data, filename):
     if audio_data is not None:
        with open(filename, "wb") as file:
            file.write(audio_data.get_wav_data())
     else:
        print("No audio data received.")

def isit_background_noise(filename, threshold=-45): #40 for quitness - 45 for voice commands. 45 is perfect by far for detecting quitness and voice commands
    # Load the audio file
    y, sr = librosa.load(filename, sr=None)
    frame_length = 510 
    
    # Pre-processing steps
    y = normalize_audio(y)
    y = high_pass_filter(y, sr)
    y = remove_silence(y, sr)
    
    # Compute short-time energy
    energy = np.array([sum(abs(y[i:i+frame_length]**2))
                       for i in range(0, len(y), frame_length)])
    
    # Convert energy to dB
    energy_db = librosa.amplitude_to_db(energy, ref=np.max)
    
    # If the average energy is below the threshold, it might be noise
    return np.mean(energy_db) < threshold


def normalize_audio(audio):
    audio = audio / np.max(np.abs(audio))
    return audio

def high_pass_filter(y, sr, cutoff=100):
    sos = scipy.signal.butter(10, cutoff, 'hp', fs=sr, output='sos')
    filtered = scipy.signal.sosfilt(sos, y)
    return filtered

def remove_silence(audio, sr, threshold=0.01, chunk_size=5000):
    trimmed_audio = []
    for i in range(0, len(audio), chunk_size):
        chunk = audio[i:i+chunk_size]
        if np.max(chunk) > threshold:
            trimmed_audio.extend(chunk)
    return np.array(trimmed_audio)