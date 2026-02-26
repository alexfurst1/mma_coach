from backend.storage.supabase_client import supabase

def pull_metadata(video_id):
    response = (
        supabase.table('video_data')
        .select('*')
        .eq('id',video_id)
        .execute()
    )

    return response