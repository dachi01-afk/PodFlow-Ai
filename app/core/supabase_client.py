"""
PodFlow AI - Supabase Client
Single instance Supabase client untuk semua operasi database.
"""

from supabase import create_client, Client
from config import get_settings

settings = get_settings()
_client: Client = None


def get_supabase() -> Client:
    """Get or create Supabase client instance."""
    global _client
    if _client is None:
        _client = create_client(settings.supabase_url, settings.supabase_key)
    return _client
