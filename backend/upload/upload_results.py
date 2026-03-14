# uploads summaries to supabase
from backend.storage.supabase_client import supabase

def upload_general(video_id, ai_output): #llava outputs a string
    response = (
        supabase.table('summaries')
        .insert({'video_id':video_id,'feedback':ai_output})
        .execute()
        )
    print(response)
    return response