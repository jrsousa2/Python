import whisper
import os
import torch

print("CUDA is available:",torch.cuda.is_available())  # Returns True if CUDA is available, else False
print("Device number:",torch.cuda.current_device())  # Prints the current CUDA device ID
print("GPU device name:",torch.cuda.get_device_name(torch.cuda.current_device()))  # Name of the GPU

# Verify the TORCH_HOME environment variable
torch_home = os.getenv('TORCH_HOME')

print(f"\nTORCH_HOME is set to {torch_home}\n")
print()

def generate_translated_srt(audio_path, audio_lang="en", output_srt="subtitles.srt"):
    # Check if CUDA is available and set device to GPU if possible
    if torch.cuda.is_available():
        device = "cuda" 
    else:
        device = "cpu"
    
    # Load Whisper model
    # "Large" model is required for translation
    # Move model to GPU if available
    model = whisper.load_model("large").to(device)  
    
    # Transcribe and translate
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
generate_translated_srt("D:\\Videos\\Arosio\\Audio.aac", audio_lang="PT", output_srt="D:\\Videos\\Arosio\\subtitles.srt")
