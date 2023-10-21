from Libraries import os, AudioSegment, sr, wave, webrtcvad

def process_wav_file(filename):
    audio = AudioSegment.from_file(filename, format="wav")
# Increase volume (gain)
    amplified_audio = audio + 17  # Increase volume by 10 dB
# Remove background noise
    silent_audio = AudioSegment.silent(duration=len(audio), frame_rate=audio.frame_rate)
    noise_reduced_audio = amplified_audio.overlay(silent_audio, gain_during_overlay=-5)
    noise_reduced_audio.export("Database/bin/processed_audio.wav", format="wav")
    # Resample the audio
    resampled_audio = resample_wav_file("Database/bin/processed_audio.wav")
    resampled_audio.export('Database/bin/resampled_audio_file1.wav', format="wav")
    # Initialize VAD
    vad = webrtcvad.Vad(2)
    
    with wave.open("Database/bin/resampled_audio_file1.wav", 'rb') as wf:
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
        if audio_frames:
            # Convert frames to AudioData for recognition
            audio_data = sr.AudioData(b''.join(audio_frames), sample_rate, wf.getsampwidth())
            recognizer = sr.Recognizer()
            try:
                recognized_text = recognizer.recognize_google(audio_data)
                if(len(recognized_text) > 0):
                 return recognized_text
                else:
                 return False
            except sr.UnknownValueError:
                return False
            except sr.RequestError:
                return "API unavailable."
        else:
            return None


def resample_wav_file(filename, target_sample_rate=16000):
    audio = AudioSegment.from_wav(filename)
    resampled_audio = audio.set_frame_rate(target_sample_rate)
    return resampled_audio
def delete_recording(filename):
    try:
        os.remove(filename)
    except FileNotFoundError:
        print(f"File {filename} not found!")
    except Exception as e:
        print(f"Error occurred: {e}")

def save_audio_as_wav(audio_data, filename):
    with open(filename, "wb") as file:
        file.write(audio_data.get_wav_data())

