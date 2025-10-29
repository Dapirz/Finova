from fastapi import FastAPI, APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import logging
from pathlib import Path
from pydantic import BaseModel
from typing import List, Optional
import aiosqlite
import hashlib
import secrets

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# Database path
DB_PATH = ROOT_DIR / 'money_management.db'

# HTML files directory (serving from frontend/public)
HTML_DIR = ROOT_DIR.parent / 'frontend' / 'public'

# Create the main app
app = FastAPI()
api_router = APIRouter(prefix="/api")

# Session storage (simple in-memory untuk tugas kuliah)
sessions = {}

# ===== DATABASE SETUP =====
async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        # Tabel users
        await db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                nama_lengkap TEXT NOT NULL
            )
        ''')
        
        # Tabel kategori transaksi
        await db.execute('''
            CREATE TABLE IF NOT EXISTS kategori (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                nama_kategori TEXT NOT NULL,
                tipe TEXT NOT NULL,
                deskripsi TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        # Tabel aset
        await db.execute('''
            CREATE TABLE IF NOT EXISTS aset (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                nama_aset TEXT NOT NULL,
                tipe TEXT NOT NULL,
                saldo_awal REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        
        await db.commit()
        
        # Insert dummy user jika belum ada
        cursor = await db.execute('SELECT COUNT(*) FROM users')
        count = await cursor.fetchone()
        if count[0] == 0:
            # Password: admin123 (di-hash dengan sha256)
            hashed_pw = hashlib.sha256('admin123'.encode()).hexdigest()
            await db.execute(
                'INSERT INTO users (username, password, nama_lengkap) VALUES (?, ?, ?)',
                ('admin', hashed_pw, 'Administrator')
            )
            await db.commit()

# ===== MODELS =====
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[dict] = None

class KategoriCreate(BaseModel):
    nama_kategori: str
    tipe: str  # "pemasukan" atau "pengeluaran"
    deskripsi: Optional[str] = None

class KategoriUpdate(BaseModel):
    nama_kategori: Optional[str] = None
    tipe: Optional[str] = None
    deskripsi: Optional[str] = None

class AsetCreate(BaseModel):
    nama_aset: str
    tipe: str  # "cash", "rekening", atau "kredit"
    saldo_awal: float

class AsetUpdate(BaseModel):
    nama_aset: Optional[str] = None
    tipe: Optional[str] = None
    saldo_awal: Optional[float] = None

# ===== HELPER FUNCTIONS =====
def get_user_from_token(token: str) -> Optional[int]:
    """Ambil user_id dari token"""
    return sessions.get(token)

async def get_current_user(token: str = None):
    """Dependency untuk verifikasi user"""
    if not token:
        raise HTTPException(status_code=401, detail="Token tidak ditemukan")
    
    user_id = get_user_from_token(token)
    if not user_id:
        raise HTTPException(status_code=401, detail="Token tidak valid")
    
    return user_id

# ===== AUTH ENDPOINTS =====
@api_router.post("/auth/login", response_model=LoginResponse)
async def login(req: LoginRequest):
    async with aiosqlite.connect(DB_PATH) as db:
        # Hash password yang diinput
        hashed_pw = hashlib.sha256(req.password.encode()).hexdigest()
        
        # Cari user
        cursor = await db.execute(
            'SELECT id, username, nama_lengkap FROM users WHERE username = ? AND password = ?',
            (req.username, hashed_pw)
        )
        user = await cursor.fetchone()
        
        if not user:
            return LoginResponse(
                success=False,
                message="Username atau password salah"
            )
        
        # Generate token sederhana
        token = secrets.token_hex(32)
        sessions[token] = user[0]  # Simpan user_id
        
        return LoginResponse(
            success=True,
            message="Login berhasil",
            token=token,
            user={
                "id": user[0],
                "username": user[1],
                "nama_lengkap": user[2]
            }
        )

@api_router.post("/auth/logout")
async def logout(token: str):
    if token in sessions:
        del sessions[token]
    return {"success": True, "message": "Logout berhasil"}

# ===== KATEGORI ENDPOINTS =====
@api_router.get("/kategori")
async def get_kategori(token: str):
    user_id = await get_current_user(token)
    
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            'SELECT * FROM kategori WHERE user_id = ? ORDER BY id DESC',
            (user_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

@api_router.post("/kategori")
async def create_kategori(data: KategoriCreate, token: str):
    user_id = await get_current_user(token)
    
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            'INSERT INTO kategori (user_id, nama_kategori, tipe, deskripsi) VALUES (?, ?, ?, ?)',
            (user_id, data.nama_kategori, data.tipe, data.deskripsi)
        )
        await db.commit()
        
        return {
            "success": True,
            "message": "Kategori berhasil ditambahkan",
            "id": cursor.lastrowid
        }

@api_router.put("/kategori/{kategori_id}")
async def update_kategori(kategori_id: int, data: KategoriUpdate, token: str):
    user_id = await get_current_user(token)
    
    # Build update query
    updates = []
    values = []
    
    if data.nama_kategori is not None:
        updates.append("nama_kategori = ?")
        values.append(data.nama_kategori)
    
    if data.tipe is not None:
        updates.append("tipe = ?")
        values.append(data.tipe)
    
    if data.deskripsi is not None:
        updates.append("deskripsi = ?")
        values.append(data.deskripsi)
    
    if not updates:
        raise HTTPException(status_code=400, detail="Tidak ada data untuk diupdate")
    
    values.extend([user_id, kategori_id])
    
    async with aiosqlite.connect(DB_PATH) as db:
        query = f"UPDATE kategori SET {', '.join(updates)} WHERE user_id = ? AND id = ?"
        cursor = await db.execute(query, values)
        await db.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")
        
        return {"success": True, "message": "Kategori berhasil diupdate"}

@api_router.delete("/kategori/{kategori_id}")
async def delete_kategori(kategori_id: int, token: str):
    user_id = await get_current_user(token)
    
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            'DELETE FROM kategori WHERE user_id = ? AND id = ?',
            (user_id, kategori_id)
        )
        await db.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Kategori tidak ditemukan")
        
        return {"success": True, "message": "Kategori berhasil dihapus"}

# ===== ASET ENDPOINTS =====
@api_router.get("/aset")
async def get_aset(token: str):
    user_id = await get_current_user(token)
    
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            'SELECT * FROM aset WHERE user_id = ? ORDER BY id DESC',
            (user_id,)
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]

@api_router.post("/aset")
async def create_aset(data: AsetCreate, token: str):
    user_id = await get_current_user(token)
    
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            'INSERT INTO aset (user_id, nama_aset, tipe, saldo_awal) VALUES (?, ?, ?, ?)',
            (user_id, data.nama_aset, data.tipe, data.saldo_awal)
        )
        await db.commit()
        
        return {
            "success": True,
            "message": "Aset berhasil ditambahkan",
            "id": cursor.lastrowid
        }

@api_router.put("/aset/{aset_id}")
async def update_aset(aset_id: int, data: AsetUpdate, token: str):
    user_id = await get_current_user(token)
    
    # Build update query
    updates = []
    values = []
    
    if data.nama_aset is not None:
        updates.append("nama_aset = ?")
        values.append(data.nama_aset)
    
    if data.tipe is not None:
        updates.append("tipe = ?")
        values.append(data.tipe)
    
    if data.saldo_awal is not None:
        updates.append("saldo_awal = ?")
        values.append(data.saldo_awal)
    
    if not updates:
        raise HTTPException(status_code=400, detail="Tidak ada data untuk diupdate")
    
    values.extend([user_id, aset_id])
    
    async with aiosqlite.connect(DB_PATH) as db:
        query = f"UPDATE aset SET {', '.join(updates)} WHERE user_id = ? AND id = ?"
        cursor = await db.execute(query, values)
        await db.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Aset tidak ditemukan")
        
        return {"success": True, "message": "Aset berhasil diupdate"}

@api_router.delete("/aset/{aset_id}")
async def delete_aset(aset_id: int, token: str):
    user_id = await get_current_user(token)
    
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            'DELETE FROM aset WHERE user_id = ? AND id = ?',
            (user_id, aset_id)
        )
        await db.commit()
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Aset tidak ditemukan")
        
        return {"success": True, "message": "Aset berhasil dihapus"}

# Include router
app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("startup")
async def startup():
    await init_db()
    logger.info("Database initialized")

@app.on_event("shutdown")
async def shutdown():
    logger.info("Application shutting down")