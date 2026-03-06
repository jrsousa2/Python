import whisper
import os
import torch

from timeit import default_timer
from datetime import datetime

print("\nCUDA is available:",torch.cuda.is_available())  # Returns True if CUDA is available, else False
print("\nDevice number:",torch.cuda.current_device())  # Prints the current CUDA device ID
print("\nGPU device name:",torch.cuda.get_device_name(torch.cuda.current_device()))  # Name of the GPU

# Verify the TORCH_HOME environment variable
torch_home = os.getenv('TORCH_HOME')

print(f"\nTORCH_HOME is set to {torch_home}")

 # Check if CUDA is available and set device to GPU if possible
if torch.cuda.is_available():
    device = "cuda" 
else:
    device = "cpu"

def load_model_to_dev():
    # Load Whisper model
    # "Large" model is required for translation
    # Move model to GPU if available
    model = whisper.load_model("large").to(device)
    return model

def generate_translated_srt(audio_path, audio_lang="en", output_srt="subtitles.srt"):

    # IF MODEL BELOW ERRORS OUT YOU NEED TO CALL THE LOAD_MODEL_TO_DEV FUNCTION  
    print("\nLoading model...")
    model = whisper.load_model("large", download_root=torch_home).to(device) #, device= device)

    print("\nWhere model is stored:",next(model.parameters()).device)
    
    # Transcribe and translate
    print("\nTranslating media...this may take a while\n")
    result = model.transcribe(audio_path, language=audio_lang, task="translate", verbose=True)
    
    subs = []
    for i, segment in enumerate(result["segments"]):
        start_time = segment["start"]
        end_time = segment["end"]
        text = segment["text"]
        
        # Convert timestamps to SRT format
        start_srt = f"{int(start_time // 3600):02}:{int((start_time % 3600) // 60):02}:{int(start_time % 60):02},{int((start_time % 1) * 1000):03}"
        end_srt = f"{int(end_time // 3600):02}:{int((end_time % 3600) // 60):02}:{int(end_time % 60):02},{int((end_time % 1) * 1000):03}"
        
        subs.append(f"{i+1}\n{start_srt} --> {end_srt}\n{text}\n\n")

    # Write to SRT file
    with open(output_srt, "w", encoding="utf-8") as f:
         f.writelines(subs)

    print(f"\nTranslated SRT file saved as {output_srt}\n")

# Example usage
# input_file = "D:\\Videos\\Arosio\\Audio.aac"
# output_file = "D:\\Videos\\Arosio\\subtitles.srt"

input_file = "D:\\Videos\\n8n\\Video_ext\\Rogue_final.mp4"

#input_file = "D:\\Videos\\n8n\\Sound\\audio1.mp3"
output_file = "D:\\Videos\\n8n\\Video_ext\\subtitles.srt"

elapsed_time = 0
start_time = default_timer()

start_time_act = datetime.now()
print("\nStart time:", start_time_act)

generate_translated_srt(input_file, audio_lang="PT", output_srt=output_file)

end_time = default_timer()
end_time_act = datetime.now()
print("\nStart time:", start_time_act)
print("\nEnd time:",end_time_act)

elapsed_time = end_time - start_time
print("\nElapsed time:",elapsed_time)
