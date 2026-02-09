import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

url = os.getenv('SUPABASE_PROJECT_URL')
key = os.getenv('SUPABASE_API_KEY')

if not url or not key:
    raise Exception(
        'Missing supabase credentials.'
    )

supabase = create_client(url,key)