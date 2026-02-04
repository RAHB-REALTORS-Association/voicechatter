
import sys
import torch
from pathlib import Path

# Try to load all chatterbox variants
from huggingface_hub import scan_cache_dir

def check_variant(name, import_path, class_name):
    try:
        print(f"\n--- Checking {name} ---")
        print(f"Importing {import_path}...")
        mod = __import__(import_path, fromlist=[class_name])
        cls = getattr(mod, class_name)
        
        device = "mps" if torch.backends.mps.is_available() else "cpu"
        print(f"Loading {name} model on {device}...")
        
        # Load model
        cls.from_pretrained(device=device)
        print(f"Success! {name} loaded.")
        
    except Exception as e:
        print(f"Error loading {name}: {e}")

check_variant("Turbo", "chatterbox.tts_turbo", "ChatterboxTurboTTS")
check_variant("Standard", "chatterbox.tts", "ChatterboxTTS")
check_variant("Multilingual", "chatterbox.mtl_tts", "ChatterboxMultilingualTTS")

print("\nScanning cache for repos...")
cache_info = scan_cache_dir()
for repo in cache_info.repos:
    if "resemble" in repo.repo_id.lower() or "chatterbox" in repo.repo_id.lower():
        print(f"Found repo: {repo.repo_id}")
