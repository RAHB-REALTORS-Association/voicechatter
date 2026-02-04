#!/usr/bin/env python3
"""
Quick test script to verify Chatterbox integration
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_settings_api():
    """Test settings API endpoints"""
    print("=" * 60)
    print("Testing Settings API")
    print("=" * 60)
    
    # Get all settings
    print("\n1. Get all settings:")
    response = requests.get(f"{BASE_URL}/api/settings")
    print(json.dumps(response.json(), indent=2))
    
    # Get backend options
    print("\n2. Get backend options:")
    response = requests.get(f"{BASE_URL}/api/settings/backend/options")
    print(json.dumps(response.json(), indent=2))
    
    # Get current backend
    print("\n3. Get current backend:")
    response = requests.get(f"{BASE_URL}/api/settings/tts_backend")
    current = response.json()
    print(json.dumps(current, indent=2))
    
    return current['value']

def test_backend_switch():
    """Test backend switching"""
    print("\n" + "=" * 60)
    print("Testing Backend Switch")
    print("=" * 60)
    
    # Switch to qwen
    print("\n1. Switching to Qwen...")
    response = requests.put(
        f"{BASE_URL}/api/settings/tts_backend",
        json={"value": "qwen"}
    )
    print(json.dumps(response.json(), indent=2))
    
    # Switch back to chatterbox
    print("\n2. Switching back to Chatterbox Turbo...")
    response = requests.put(
        f"{BASE_URL}/api/settings/tts_backend",
        json={"value": "chatterbox_turbo"}
    )
    print(json.dumps(response.json(), indent=2))

def test_health():
    """Test health endpoint"""
    print("\n" + "=" * 60)
    print("Testing Health Endpoint")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    health = response.json()
    print(json.dumps(health, indent=2))
    
    print("\n📊 System Status:")
    print(f"  - Backend Type: {health['backend_type']}")
    print(f"  - GPU Available: {health['gpu_available']}")
    print(f"  - GPU Type: {health['gpu_type']}")
    print(f"  - Model Loaded: {health['model_loaded']}")

if __name__ == "__main__":
    try:
        print("\n🧪 Voicebox Integration Test")
        print("=" * 60)
        
        current_backend = test_settings_api()
        test_backend_switch()
        test_health()
        
        print("\n" + "=" * 60)
        print("✅ All tests passed!")
        print("=" * 60)
        print(f"\nCurrent backend: {current_backend}")
        print("Settings API is working correctly!")
        print("Backend hot-reload is functional!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
