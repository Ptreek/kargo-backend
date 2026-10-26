import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI(title="Kargo System Core API", version="1.0")

# السماح بالاتصالات الخارجية (عشان موقعك على Cloudflare يقكلمه براحته)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# بيانات الاتصال بـ Supabase
SUPABASE_URL = "https://nsvrjmnhbwrnblzwfdlk.supabase.co"
SUPABASE_KEY = "sb_publishable_MUzynqnW0_u7sRisuRpolA_XisB0xJM"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

@app.get("/")
def home():
    return {"status": "Kargo Core Engine is Running 🚀", "database": "Connected"}

@app.get("/api/merchants")
def get_merchants():
    try:
        response = supabase.table("merchants").select("*").execute()
        return {"success": True, "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/merchants")
def create_merchant(merchant: dict):
    try:
        response = supabase.table("merchants").insert(merchant).execute()
        return {"success": True, "message": "Merchant added successfully", "data": response.data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
