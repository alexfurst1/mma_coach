from backend.storage.supabase_client import supabase

def pull_metadata(cloudflare_id):
    response = (
        supabase.table('video_data')
        .select('*')
        .eq('cloudflare_key',cloudflare_id)
        .execute()
    )

    return response