"""
Test API Agents langsung untuk debug pipeline
"""
import httpx
import json
from config import get_settings

settings = get_settings()

print("=" * 60)
print("  TEST API AGENTS - Debug Pipeline")
print("=" * 60)

# ============================================
# TEST 1: Qwen API (Research Agent)
# ============================================
print("\n--- TEST 1: Qwen API (Research Agent) ---")
print(f"URL: {settings.qwen_api_url}")
print(f"Key: {settings.qwen_api_key[:20]}...")

try:
    response = httpx.post(
        f"{settings.qwen_api_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.qwen_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "qwen/qwen3.6-27b",
            "messages": [
                {"role": "user", "content": "Halo, ini test. Jawab dengan: OK"}
            ],
            "max_tokens": 50,
        },
        timeout=30.0,
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")
    
    if response.status_code == 200:
        print("✅ Qwen API OK!")
    else:
        print("❌ Qwen API GAGAL!")
        
except Exception as e:
    print(f"❌ Qwen API Error: {str(e)}")

# ============================================
# TEST 2: Agnes AI API (Scriptwriter Agent)
# ============================================
print("\n--- TEST 2: Agnes AI API (Scriptwriter Agent) ---")
print(f"URL: {settings.agnes_api_url}")
print(f"Key: {settings.agnes_api_key[:20]}...")

try:
    response = httpx.post(
        f"{settings.agnes_api_url}/chat/completions",
        headers={
            "Authorization": f"Bearer {settings.agnes_api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": "agnes-2.0-flash",
            "messages": [
                {"role": "user", "content": "Halo, ini test. Jawab dengan: OK"}
            ],
            "max_tokens": 50,
        },
        timeout=30.0,
    )
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text[:500]}")
    
    if response.status_code == 200:
        print("✅ Agnes AI API OK!")
    else:
        print("❌ Agnes AI API GAGAL!")
        
except Exception as e:
    print(f"❌ Agnes AI API Error: {str(e)}")

print("\n" + "=" * 60)
print("  SELESAI")
print("=" * 60)
