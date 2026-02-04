
import os
import sys
import asyncio
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

from backend.config import TTS_MODEL_TYPE
from backend.backends import get_tts_backend

async def test_backend():
    print(f"Testing TTS Model Type: {TTS_MODEL_TYPE}")
    
    try:
        backend = get_tts_backend()
        print(f"Backend loaded: {type(backend).__name__}")
        
        if hasattr(backend, "is_loaded"):
            print(f"Is loaded: {backend.is_loaded()}")
            
        # Try loading model
        print("Loading model...")
        await backend.load_model()
        print("Model loaded.")
        
        # Try generation
        print("Generating audio...")
        voice_prompt, _ = await backend.create_voice_prompt(
            audio_path="backend/tests/fixtures/sample.wav", # specific sample path
            reference_text="This is a sample reference.",
            use_cache=False
        )
        
        # We might need a real audio file for the prompt if the backend validates it
        # Create a dummy file if not exists
        Path("backend/tests/fixtures").mkdir(parents=True, exist_ok=True)
        if not Path("backend/tests/fixtures/sample.wav").exists():
            # Create absolute dummy wav
            import wave
            with wave.open("backend/tests/fixtures/sample.wav", "wb") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(24000)
                f.writeframes(b'\0' * 24000) # 1 sec silence
        
        voice_prompt, _ = await backend.create_voice_prompt(
            audio_path="backend/tests/fixtures/sample.wav",
            reference_text="This is a sample reference.",
            use_cache=False
        )

        audio, sr = await backend.generate(
            text="Hello world, this is a test of the new chatterbox integration.",
            voice_prompt=voice_prompt
        )
        
        print(f"Generated audio shape: {audio.shape}, Sample rate: {sr}")
        
        if len(audio) > 0:
            print("SUCCESS: Audio generated.")
        else:
            print("FAILURE: Audio is empty.")
            
    except Exception as e:
        print(f"FAILURE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_backend())
