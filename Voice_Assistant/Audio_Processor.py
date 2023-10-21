from Libraries import os, AudioSegment, wave, webrtcvad, librosa, sf, nr, sr, np

def process_wav_file(filename):
    if(isit_background_noise(filename)):
        return False
        
    # Load audio file
    y, samplerate = librosa.load(filename, sr=None)
    # Perform noise reduction
    reduced_noise = nr.reduce_noise(y=y, sr=samplerate)
    sf.write('Database/bin/processed_audio.wav', reduced_noise, samplerate=samplerate)
    
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
def delete_recording(filename1, filename2, filename3):
    try:
        os.remove(filename1)
        os.remove(filename2)
        os.remove(filename3)
    except FileNotFoundError:
        print(f"File not found!")
    except Exception as e:
        print(f"Error occurred: {e}")

def save_audio_as_wav(audio_data, filename):
    with open(filename, "wb") as file:
        file.write(audio_data.get_wav_data())

def isit_background_noise(filename, threshold=-50):
    # Load the audio file
    y, sr = librosa.load(filename, sr=None)
    frame_length = 512 
    # Compute short-time energy
    energy = np.array([sum(abs(y[i:i+frame_length]**2))
                       for i in range(0, len(y), frame_length)])
    
    # Convert energy to dB
    energy_db = librosa.amplitude_to_db(energy, ref=np.max)
    
    # If the average energy is below the threshold, it might be noise
    return np.mean(energy_db) < threshold