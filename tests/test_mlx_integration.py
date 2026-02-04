import os
import sys
import asyncio
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent))

# Force MLX backend by setting TTS_MODEL_TYPE before import
os.environ["TTS_MODEL_TYPE"] = "chatterbox_turbo"

from backend.config import TTS_MODEL_TYPE
from backend.backends import get_tts_backend

async def test_mlx_backend():
    print(f"Testing TTS Model Type: {TTS_MODEL_TYPE}")
    
    try:
        backend = get_tts_backend()
        print(f"Backend loaded: {type(backend).__name__}")
        
        if hasattr(backend, "is_loaded"):
            print(f"Is loaded: {backend.is_loaded()}")
            
        # Try loading model
        print("Loading model...")
        await backend.load_model()
        print("Model loaded successfully!")
        
        # Create a simple test audio file
        print("Creating test audio file...")
        Path("backend/tests/fixtures").mkdir(parents=True, exist_ok=True)
        
        # Create a simple 1-second silence WAV file
        import wave
        import numpy as np
        
        sample_rate = 16000
        duration = 3  # 3 seconds
        
        # Generate some simple audio (sine wave for testing)
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = (np.sin(2 * np.pi * 440 * t) * 0.3).astype(np.float32)
        
        # Convert to int16 for WAV
        audio_int16 = (audio * 32767).astype(np.int16)
        
        wav_path = "backend/tests/fixtures/sample.wav"
        with wave.open(wav_path, "wb") as f:
            f.setnchannels(1)
            f.setsampwidth(2)
            f.setframerate(sample_rate)
            f.writeframes(audio_int16.tobytes())
        
        print(f"Created test audio: {wav_path}")
        
        # Create voice prompt
        print("Creating voice prompt...")
        voice_prompt, was_cached = await backend.create_voice_prompt(
            audio_path=wav_path,
            reference_text="This is a test reference audio.",
            use_cache=False
        )
        print(f"Voice prompt created (cached: {was_cached})")
        
        # Generate speech
        print("Generating speech...")
        test_text = "Hello world, this is a test of the Chatterbox MLX integration with Voicebox!"
        
        audio, sr = await backend.generate(
            text=test_text,
            voice_prompt=voice_prompt,
            language="en"
        )
        
        print(f"Generated audio shape: {audio.shape}, Sample rate: {sr}Hz")
        print(f"Audio duration: {len(audio) / sr:.2f}s")
        
        if len(audio) > 0:
            # Save the generated audio
            output_path = "test_output.wav"
            with wave.open(output_path, "wb") as f:
                f.setnchannels(1)
                f.setsampwidth(2)
                f.setframerate(sr)
                audio_int16 = (audio * 32767).astype(np.int16)
                f.writeframes(audio_int16.tobytes())
            
            print(f"\n✅ SUCCESS: Audio generated and saved to {output_path}")
            print(f"   Backend: {type(backend).__name__}")
            print(f"   Text: '{test_text}'")
            print(f"   Duration: {len(audio) / sr:.2f}s")
        else:
            print("FAILURE: Audio is empty.")
            
    except Exception as e:
        print(f"FAILURE: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_mlx_backend())
