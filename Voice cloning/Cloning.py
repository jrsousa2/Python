# THIS CODE LOADS THE MODEL FROM A SPECIFIED FOLDER 
# AT THE FIRST RUN IT DOWNLOADS THE MODEL

from TTS.api import TTS
import os
import warnings

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=".*torch.load.*weights_only=False.*"
)

print("Working dir:", os.getcwd(),"\n")

# Verify the TORCH_HOME environment variable
# TTS_HOME = getenv('TTS_HOME')
# print(f"\nTTS_HOME is set to {TTS_HOME}\n")

# SET SYS VAR FOR THE MODEL CACHING
os.environ["TTS_HOME"] = r"F:\TTS"

print("Loading model...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")

# Move to GPU
#tts.to("cuda")

Sample=(
   "Would it be possible for earth to become rogue and people survive with more advanced technology (tech of say 100 years ahead)?"
   "Yes, let's unpack it step by step."
   "What does it mean for Earth to become a rogue planet?" 
)

# TTS
tts.tts_to_file(
    text= Sample,
    speaker_wav=r"F:\TTS\Jose-EN2.wav",
    language="en",
    file_path=r"F:\TTS\output.wav"
)
