# Money Management Web Application
> Simple Personal Finance Management System for IPPL Course Project

## 🎯 Project Overview

A web-based money management application built with **FastAPI (Python)** backend, **SQLite** database, and **pure HTML/CSS/JavaScript** frontend. This is Week 1 implementation focusing on authentication and master data CRUD.

## ✨ Implemented Features (Week 1)

### 1. Authentication System
- Simple username/password login
- Session management with tokens
- Protected routes

**Login Credentials:**
- Username: `admin`
- Password: `admin123`

### 2. Transaction Categories CRUD
- Add, view, edit, and delete categories
- Category types: Income (`pemasukan`) or Expense (`pengeluaran`)
- Optional description field

### 3. Assets CRUD
- Add, view, edit, and delete assets
- Asset types: Cash, Bank Account (`rekening`), or Credit
- Initial balance tracking in Indonesian Rupiah (IDR)

## 🏗️ Project Structure

```
/app/
├── backend/
│   ├── server.py              # Main FastAPI application
│   ├── requirements.txt       # Python dependencies
│   └── money_management.db    # SQLite database (auto-created)
│
└── frontend/public/
    ├── login.html            # Login page
    ├── index.html            # Dashboard
    ├── kategori.html         # Categories CRUD page
    ├── aset.html             # Assets CRUD page
    ├── style.css             # Global styles
    ├── config.js             # API configuration
    ├── utils.js              # Utility functions
    ├── auth.js               # Authentication logic
    ├── kategori.js           # Categories CRUD logic
    └── aset.js               # Assets CRUD logic
```

## 🗄️ Database Schema (SQLite)

### Table: `users`
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,  -- SHA256 hashed
    nama_lengkap TEXT NOT NULL
);
```

### Table: `kategori` (Categories)
```sql
CREATE TABLE kategori (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    nama_kategori TEXT NOT NULL,
    tipe TEXT NOT NULL,  -- 'pemasukan' or 'pengeluaran'
    deskripsi TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Table: `aset` (Assets)
```sql
CREATE TABLE aset (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    nama_aset TEXT NOT NULL,
    tipe TEXT NOT NULL,  -- 'cash', 'rekening', or 'kredit'
    saldo_awal REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation & Run

1. **Install dependencies:**
```bash
cd /app/backend
pip install -r requirements.txt
```

2. **Start the server:**
```bash
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

3. **Access the application:**
```
http://localhost:8001/login.html
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/logout` - User logout

### Categories (Kategori)
- `GET /api/kategori?token={token}` - Get all categories
- `POST /api/kategori?token={token}` - Create category
- `PUT /api/kategori/{id}?token={token}` - Update category
- `DELETE /api/kategori/{id}?token={token}` - Delete category

### Assets (Aset)
- `GET /api/aset?token={token}` - Get all assets
- `POST /api/aset?token={token}` - Create asset
- `PUT /api/aset/{id}?token={token}` - Update asset
- `DELETE /api/aset/{id}?token={token}` - Delete asset

See [STRUKTUR_PROYEK.md](./STRUKTUR_PROYEK.md) for detailed API documentation in Indonesian.

## 🛠️ Tech Stack

- **Backend:** FastAPI, SQLite, aiosqlite
- **Frontend:** HTML5, CSS3, Vanilla JavaScript
- **Database:** SQLite (file-based)
- **Authentication:** Token-based (simple in-memory)

## 📝 Next Week Features

- Transaction recording (income/expense)
- Financial reports and summaries
- Dashboard with charts/graphs
- Date filtering

## 📚 Documentation

For complete documentation in Indonesian, including detailed API specs and code explanations, see:
- [STRUKTUR_PROYEK.md](./STRUKTUR_PROYEK.md) - Complete project structure and documentation (Bahasa Indonesia)

## 🎓 Learning Goals

This project demonstrates:
- RESTful API design
- CRUD operations with relational database
- Authentication & authorization basics
- Async database operations
- Frontend-backend integration
- Clean code structure and modularity

## 📄 License

Academic project for IPPL course assignment.

---

**Note:** For detailed Indonesian documentation, file explanations, and testing guide, please refer to [STRUKTUR_PROYEK.md](./STRUKTUR_PROYEK.md)
