import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer
from supabase import create_client, Client

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
