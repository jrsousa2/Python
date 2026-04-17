import librosa
import soundfile as sf

from timeit import default_timer
from datetime import datetime
#from sys import exit

def pitch_shift(audio_path, shift_semitones, vol):
    try:
        # Load the audio file
        audio, samplerate = librosa.load(audio_path, sr=None)

        # Shift pitch using librosa
        shifted_audio = librosa.effects.pitch_shift(audio, sr=samplerate, n_steps=shift_semitones)

        # Increase amplitude (volume) by a factor of 2
        shifted_audio = vol * shifted_audio

        return shifted_audio, samplerate

    except Exception as e:
        print(f"Error processing pitch shift: {e}")
        return None, None


# START OF THE CODE
elapsed_time = 0
start_time = default_timer()

start_time_act = datetime.now()
print("\nStart time:", start_time_act)

# Example usage
# folder = "D:\\Videos\\Novelas\\"
# input_file = "Final.wav"

folder = "D:\\Videos\\Tieta\\"
input_file = "Tieta.aac"
vol = 2

audio_path = folder + input_file
shift_semitones = 2  # Shift up by 12 semitones (1 octave)

# CALL FUNCTION
shifted_audio, samplerate = pitch_shift(audio_path, shift_semitones, vol)

if shifted_audio is not None and samplerate is not None:
    # Save the transformed audio
    output_path = folder + "Modified Vol"+ str(vol) + "x.wav"
    sf.write(output_path, shifted_audio, samplerate)
    print(f"Pitch-shifted audio saved to {output_path}")
else:
    print("Pitch shift failed.")

# TIME FINAL
end_time = default_timer()
end_time_act = datetime.now()
print("\nStart time:", start_time_act)
print("\nEnd time:",end_time_act)

elapsed_time = end_time - start_time
print("\nElapsed time:",elapsed_time,"\n")    