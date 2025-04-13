import os
import requests
from tqdm import tqdm

def download_file(url, filename):
    """
    Download a file with progress bar
    """
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(filename, 'wb') as file, tqdm(
        desc=filename,
        total=total_size,
        unit='iB',
        unit_scale=True,
        unit_divisor=1024,
    ) as progress_bar:
        for data in response.iter_content(chunk_size=1024):
            size = file.write(data)
            progress_bar.update(size)

def main():
    # Create models directory if it doesn't exist
    os.makedirs("models", exist_ok=True)
    
    # Model URL (Llama 2 7B Chat GGUF)
    model_url = "https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF/resolve/main/llama-2-7b-chat.Q4_K_M.gguf"
    model_path = "models/llama-2-7b-chat.gguf"
    
    # Download the model if it doesn't exist
    if not os.path.exists(model_path):
        print(f"Downloading Llama 2 model to {model_path}...")
        download_file(model_url, model_path)
        print("Download completed!")
    else:
        print("Model already exists!")

if __name__ == "__main__":
    main() 