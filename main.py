from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
import os
from dotenv import load_dotenv
from supabase import create_client
import re

load_dotenv()

app = FastAPI()

# Security — only allow requests from getsuro.com
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://getsuro.com",
        "https://www.getsuro.com",
        "http://localhost:3000"  # for local testing
    ],
    allow_methods=["POST"],
    allow_headers=["*"],
)

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_SERVICE_KEY")
)

class WaitlistEntry(BaseModel):
    email: EmailStr  # auto validates email format

def is_valid_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

@app.post("/waitlist")
async def join_waitlist(entry: WaitlistEntry):
    email = entry.email.lower().strip()

    # Check if email already exists
    existing = supabase.table("waitlist")\
        .select("email")\
        .eq("email", email)\
        .execute()

    if existing.data:
        return {"message": "You're already on the list!"}

    # Insert safely using parameterized query
    supabase.table("waitlist").insert({"email": email}).execute()
    return {"message": "You're on the list!"}