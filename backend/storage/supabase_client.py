import os
from supabase import create_client

url = os.environ.get('SUPABASE_PROJECT_URL')
key = os.environ.get('SUPABASE_API_KEY')

supabase = create_client(url,key)