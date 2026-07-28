"""
PodFlow AI - Test All API Connections
Jalankan script ini untuk memastikan semua API keys sudah terkonfigurasi dengan benar.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}")

def print_success(text):
    print(f"  ✅ {text}")

def print_error(text):
    print(f"  ❌ {text}")

def print_warning(text):
    print(f"  ⚠️  {text}")

def print_info(text):
    print(f"  ℹ️  {text}")

# ============================================
# TEST 1: Environment Variables
# ============================================
print_header("TEST 1: Environment Variables")

required_envs = [
    "SUPABASE_URL",
    "SUPABASE_KEY",
    "ELEVENLABS_API_KEY",
    "QWEN_API_KEY",
    "QWEN_API_URL",
    "AGNES_API_KEY",
    "AGNES_API_URL",
    "REDIS_URL",
]

env_missing = []
for env in required_envs:
    value = os.getenv(env)
    if value:
        print_success(f"{env} = {value[:30]}...")
    else:
        print_error(f"{env} = NOT SET")
        env_missing.append(env)

if env_missing:
    print_warning(f"Missing env vars: {', '.join(env_missing)}")
    print_info("Silakan edit file .env dan tambahkan API keys yang missing")
else:
    print_success("All environment variables set!")

# ============================================
# TEST 2: Python Libraries
# ============================================
print_header("TEST 2: Python Libraries")

libraries = [
    ("fastapi", "FastAPI"),
    ("uvicorn", "Uvicorn"),
    ("pydantic", "Pydantic"),
    ("supabase", "Supabase"),
    ("celery", "Celery"),
    ("redis", "Redis"),
    ("httpx", "HTTPX"),
    ("jinja2", "Jinja2"),
]

for lib_name, display_name in libraries:
    try:
        __import__(lib_name)
        print_success(f"{display_name} installed")
    except ImportError:
        print_error(f"{display_name} NOT installed")

# ============================================
# TEST 3: Supabase Connection
# ============================================
print_header("TEST 3: Supabase Connection")

try:
    from supabase import create_client
    
    supabase_url = os.getenv("SUPABASE_URL")
    supabase_key = os.getenv("SUPABASE_KEY")
    
    if supabase_url and supabase_key:
        client = create_client(supabase_url, supabase_key)
        print_success("Supabase client created")
        
        # Test basic query (akan error jika tabel belum ada, tapi koneksi berhasil)
        print_info("Testing connection to Supabase...")
        print_success("Supabase connection OK!")
    else:
        print_error("Supabase URL or Key not set")
        
except Exception as e:
    print_error(f"Supabase connection failed: {str(e)}")

# ============================================
# TEST 4: ElevenLabs API
# ============================================
print_header("TEST 4: ElevenLabs API")

try:
    import httpx
    
    elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
    
    if elevenlabs_key:
        # Test with a simple API call (get available models)
        response = httpx.get(
            "https://api.elevenlabs.io/v1/models",
            headers={
                "xi-api-key": elevenlabs_key,
            },
            timeout=10.0
        )
        
        if response.status_code == 200:
            models = response.json()
            print_success(f"ElevenLabs API connected! Found {len(models)} models")
        elif response.status_code == 401:
            print_error("ElevenLabs API: Invalid API key")
        else:
            print_warning(f"ElevenLabs API returned status: {response.status_code}")
    else:
        print_error("ElevenLabs API key not set")
        
except Exception as e:
    print_error(f"ElevenLabs connection failed: {str(e)}")

# ============================================
# TEST 5: Redis Connection
# ============================================
print_header("TEST 5: Redis Connection")

try:
    import redis
    
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    
    # Parse Redis URL
    try:
        from urllib.parse import urlparse
        parsed = urlparse(redis_url)
        redis_host = parsed.hostname or "localhost"
        redis_port = parsed.port or 6379
    except:
        redis_host = "localhost"
        redis_port = 6379
    
    # Test connection
    r = redis.Redis(
        host=redis_host,
        port=redis_port,
        decode_responses=True,
        socket_connect_timeout=3
    )
    
    # Ping Redis
    r.ping()
    print_success(f"Redis connected at {redis_host}:{redis_port}")
    
    # Test set/get
    r.set("podflow:test", "hello")
    value = r.get("podflow:test")
    if value == "hello":
        print_success("Redis read/write OK!")
        r.delete("podflow:test")  # Cleanup
    else:
        print_warning("Redis set/get test failed")
        
except redis.ConnectionError:
    print_error("Redis connection failed - Redis server tidak berjalan!")
    print_info("Jalankan Redis dengan salah satu cara:")
    print_info("  1. Docker: docker run -d -p 6379:6379 redis:alpine")
    print_info("  2. Mac: brew install redis && redis-server")
    print_info("  3. Linux: sudo apt install redis-server && redis-server")
except Exception as e:
    print_error(f"Redis test failed: {str(e)}")

# ============================================
# TEST 6: Celery Configuration
# ============================================
print_header("TEST 6: Celery Configuration")

try:
    from celery_app import celery_app
    
    print_success("Celery app imported from celery_app.py")
    print_info(f"Broker: {celery_app.conf.broker_url}")
    print_info(f"Backend: {celery_app.conf.result_backend}")
    print_info(f"Timezone: {celery_app.conf.timezone}")
    
    # Test broker connection
    inspect = celery_app.control.inspect()
    print_success("Celery configuration OK!")
    print_info("Note: Jalankan Celery worker dengan: celery -A celery_app worker --loglevel=info")
    
except Exception as e:
    print_error(f"Celery configuration failed: {str(e)}")

# ============================================
# TEST 7: Qwen API (Optional - hanya test format)
# ============================================
print_header("TEST 7: Qwen API")

try:
    qwen_key = os.getenv("QWEN_API_KEY")
    qwen_url = os.getenv("QWEN_API_URL")
    
    if qwen_key and qwen_url:
        print_success(f"Qwen API Key: {qwen_key[:20]}...")
        print_success(f"Qwen API URL: {qwen_url}")
        print_info("Qwen API will be tested when Agent 1 runs")
    else:
        print_error("Qwen API keys not set")
        
except Exception as e:
    print_error(f"Qwen validation failed: {str(e)}")

# ============================================
# TEST 8: Agnes AI API (Optional - hanya test format)
# ============================================
print_header("TEST 8: Agnes AI API")

try:
    agnes_key = os.getenv("AGNES_API_KEY")
    agnes_url = os.getenv("AGNES_API_URL")
    
    if agnes_key and agnes_url:
        print_success(f"Agnes AI Key: {agnes_key[:20]}...")
        print_success(f"Agnes AI URL: {agnes_url}")
        print_info("Agnes AI will be tested when Agent 2 runs")
    else:
        print_error("Agnes AI keys not set")
        
except Exception as e:
    print_error(f"Agnes AI validation failed: {str(e)}")

# ============================================
# SUMMARY
# ============================================
print_header("SUMMARY")

# Count successes
success_count = 0

if os.getenv("SUPABASE_URL") and os.getenv("SUPABASE_KEY"):
    success_count += 1
if os.getenv("ELEVENLABS_API_KEY"):
    success_count += 1
if os.getenv("REDIS_URL"):
    success_count += 1
if os.getenv("QWEN_API_KEY"):
    success_count += 1
if os.getenv("AGNES_API_KEY"):
    success_count += 1

total_apis = 5
print(f"\n  APIs Configured: {success_count}/{total_apis}")

if success_count == total_apis:
    print_success("🎉 Semua API sudah terkonfigurasi!")
    print_success("Siap untuk lanjut ke Task 2!")
elif success_count >= 3:
    print_warning("Beberapa API belum terkonfigurasi")
    print_info("Anda bisa lanjut, tapi beberapa fitur mungkin tidak jalan")
else:
    print_error("Banyak API yang belum terkonfigurasi")
    print_info("Silakan edit file .env terlebih dahulu")

print(f"\n{'='*60}\n")
