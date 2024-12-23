import speech_recognition as sr
from pydub import AudioSegment
from gtts import gTTS
import librosa
import soundfile as sf

# Function to transcribe audio and get word timings
def transcribe_audio(audio_path):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    
    # Use Google's speech recognition (this requires an internet connection)
    result = recognizer.recognize_google(audio, show_all=True)
    
    # Extract words and their timings
    words = []
    if 'alternative' in result:
        for alternative in result['alternative']:
            if 'timestamps' in alternative:
                for word_info in alternative['timestamps']:
                    word, start, end = word_info['word'], word_info['start'], word_info['end']
                    words.append((word, start, end))
    
    return words

# Example usage
audio_path = "D:\\iTunes\\Baby\\Media\\Debate_crop.wav"
words = transcribe_audio(audio_path)

# Print transcribed words and timings
for word, start, end in words:
    print(f"{word}: {start}-{end}")
