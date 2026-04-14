# uploads summaries to supabase
from backend.storage.supabase_client import supabase_client

def upload_general(video_id, ai_output): #llava outputs a string
    try:
        response = (
            supabase_client.table('summaries')
            .insert({'video_id':video_id,'feedback':ai_output})
            .execute()
            )
        return response
    except Exception as e:
        print(f'Error uploading general feedback. Error: {e}')

    return None

def upload_specific(video_id, ai_output,start_pos,end_pos):
    try:
        response = (
            supabase_client.table('timestamps')
            .insert({'video_id':video_id,'feedback':ai_output,'t_start_seconds':start_pos,'t_end_seconds':end_pos})
            .execute()
        )
        return response
    except Exception as e:
        print(f'Error uploading timestamped feedback. Error: {e}')
    
    return None