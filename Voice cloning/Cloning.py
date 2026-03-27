# THIS CODE LOADS THE MODEL FROM A SPECIFIED FOLDER 
# AT THE FIRST RUN IT DOWNLOADS THE MODEL

from TTS.api import TTS
import os
import warnings

from timeit import default_timer
from datetime import datetime
#from sys import exit

elapsed_time = 0
start_time = default_timer()

start_time_act = datetime.now()
print("\nStart time:", start_time_act)

print("Working dir:", os.getcwd(),"\n")

warnings.filterwarnings(
    "ignore",
    category=FutureWarning,
    message=".*torch.load.*weights_only=False.*"
)

# Verify the TORCH_HOME environment variable
# TTS_HOME = getenv('TTS_HOME')
# print(f"\nTTS_HOME is set to {TTS_HOME}\n")

# SET SYS VAR FOR THE MODEL CACHING
os.environ["TTS_HOME"] = r"F:\TTS"

print("Loading model...")
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to("cuda")

# Move to GPU
#tts.to("cuda")

EN_Sample=(
   "Would it be possible for earth to become rogue and people survive with more advanced technology (tech of say 100 years ahead)?"
   "Yes, let's unpack it step by step."
   "What does it mean for Earth to become a rogue planet?" 
)

PT_Sample=(
    "Seria possível a Terra se tornar um planeta errante e as pessoas sobreviverem com tecnologia mais avançada (tecnologia de, digamos, 100 anos à frente)?"
    "Sim, vamos analisar passo a passo."
    "O que significa a Terra se tornar um planeta errante? "
)

# TTS
tts.tts_to_file(
    text= PT_Sample,
    speaker_wav=r"F:\TTS\Jose-PT.wav",
    language="en",
    file_path=r"F:\TTS\output3.wav"
)

# TIME FINAL
end_time = default_timer()
end_time_act = datetime.now()
print("\nStart time:", start_time_act)
print("\nEnd time:",end_time_act)

elapsed_time = end_time - start_time
print("\nElapsed time:",elapsed_time,"\n")

