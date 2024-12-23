import librosa
import soundfile as sf

def pitch_shift(audio_path, shift_semitones):
    try:
        # Load the audio file
        audio, samplerate = librosa.load(audio_path, sr=None)

        # Shift pitch using librosa
        shifted_audio = librosa.effects.pitch_shift(audio, sr=samplerate, n_steps=shift_semitones)

        # Increase amplitude (volume) by a factor of 2
        shifted_audio = 5 * shifted_audio

        return shifted_audio, samplerate

    except Exception as e:
        print(f"Error processing pitch shift: {e}")
        return None, None

# Example usage
folder = "D:\\Videos\\Novelas\\"
input_file = "Final.wav"
audio_path = folder + input_file
shift_semitones = 12  # Shift up by 12 semitones (1 octave)

shifted_audio, samplerate = pitch_shift(audio_path, shift_semitones)

if shifted_audio is not None and samplerate is not None:
    # Save the transformed audio
    output_path = folder + "Remake-5x.wav"
    sf.write(output_path, shifted_audio, samplerate)
    print(f"Pitch-shifted audio saved to {output_path}")
else:
    print("Pitch shift failed.")