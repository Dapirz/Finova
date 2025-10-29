# Struktur Proyek Money Management
## Tugas Besar IPPL - Aplikasi Manajemen Keuangan

---

## 📁 Struktur Folder

```
/app/
├── backend/                          # Backend FastAPI
│   ├── server.py                     # File utama aplikasi backend
│   ├── requirements.txt              # Dependencies Python
│   ├── .env                         # Konfigurasi environment
│   └── money_management.db          # Database SQLite (dibuat otomatis)
│
└── frontend/
    └── public/                       # Frontend HTML/CSS/JS Murni
        ├── login.html               # Halaman login
        ├── index.html               # Dashboard utama
        ├── kategori.html            # Halaman CRUD Kategori
        ├── aset.html                # Halaman CRUD Aset
        ├── style.css                # Styling global
        ├── config.js                # Konfigurasi API endpoint
        ├── utils.js                 # Fungsi utility
        ├── auth.js                  # Logika autentikasi
        ├── kategori.js              # Logika CRUD Kategori
        └── aset.js                  # Logika CRUD Aset
```

---

## 🗄️ Struktur Database (SQLite)

### Tabel: `users`
Menyimpan data user yang dapat login ke aplikasi.

| Kolom         | Tipe    | Keterangan                    |
|--------------|---------|-------------------------------|
| id           | INTEGER | Primary key (auto increment)  |
| username     | TEXT    | Username untuk login (unique) |
| password     | TEXT    | Password (hashed dengan SHA256)|
| nama_lengkap | TEXT    | Nama lengkap user             |

**Dummy Data:**
- Username: `admin`
- Password: `admin123`

### Tabel: `kategori`
Menyimpan kategori transaksi (pemasukan/pengeluaran).

| Kolom         | Tipe    | Keterangan                        |
|--------------|---------|-----------------------------------|
| id           | INTEGER | Primary key (auto increment)      |
| user_id      | INTEGER | Foreign key ke tabel users        |
| nama_kategori| TEXT    | Nama kategori (contoh: Gaji)      |
| tipe         | TEXT    | "pemasukan" atau "pengeluaran"    |
| deskripsi    | TEXT    | Deskripsi kategori (opsional)     |

### Tabel: `aset`
Menyimpan aset/dompet keuangan user.

| Kolom       | Tipe    | Keterangan                          |
|------------|---------|-------------------------------------|
| id         | INTEGER | Primary key (auto increment)        |
| user_id    | INTEGER | Foreign key ke tabel users          |
| nama_aset  | TEXT    | Nama aset (contoh: Dompet, BCA)     |
| tipe       | TEXT    | "cash", "rekening", atau "kredit"   |
| saldo_awal | REAL    | Saldo awal aset (dalam Rupiah)      |

---

## 🔧 Teknologi yang Digunakan

### Backend
- **FastAPI** - Modern Python web framework
- **SQLite** - Database relational (file-based)
- **aiosqlite** - Async SQLite untuk Python
- **Pydantic** - Validasi data
- **hashlib** - Hashing password

### Frontend
- **HTML5** - Markup
- **CSS3** - Styling (tanpa framework)
- **JavaScript (Vanilla)** - Interaktivitas (tanpa framework)

---

## 📋 API Endpoints

### 1. Autentikasi

#### POST `/api/auth/login`
Login user dengan username dan password.

**Request Body:**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Login berhasil",
  "token": "token_string_here",
  "user": {
    "id": 1,
    "username": "admin",
    "nama_lengkap": "Administrator"
  }
}
```

#### POST `/api/auth/logout`
Logout user (hapus session token).

**Query Parameter:** `token`

---

### 2. CRUD Kategori

#### GET `/api/kategori?token={token}`
Ambil semua kategori milik user yang login.

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "nama_kategori": "Gaji",
    "tipe": "pemasukan",
    "deskripsi": "Pendapatan dari gaji bulanan"
  }
]
```

#### POST `/api/kategori?token={token}`
Tambah kategori baru.

**Request Body:**
```json
{
  "nama_kategori": "Transport",
  "tipe": "pengeluaran",
  "deskripsi": "Biaya transportasi harian"
}
```

#### PUT `/api/kategori/{kategori_id}?token={token}`
Update kategori berdasarkan ID.

**Request Body:** (field yang ingin diupdate saja)
```json
{
  "nama_kategori": "Transportasi"
}
```

#### DELETE `/api/kategori/{kategori_id}?token={token}`
Hapus kategori berdasarkan ID.

---

### 3. CRUD Aset

#### GET `/api/aset?token={token}`
Ambil semua aset milik user yang login.

**Response:**
```json
[
  {
    "id": 1,
    "user_id": 1,
    "nama_aset": "Dompet",
    "tipe": "cash",
    "saldo_awal": 500000.0
  }
]
```

#### POST `/api/aset?token={token}`
Tambah aset baru.

**Request Body:**
```json
{
  "nama_aset": "BCA Tabungan",
  "tipe": "rekening",
  "saldo_awal": 5000000
}
```

#### PUT `/api/aset/{aset_id}?token={token}`
Update aset berdasarkan ID.

**Request Body:** (field yang ingin diupdate saja)
```json
{
  "saldo_awal": 6000000
}
```

#### DELETE `/api/aset/{aset_id}?token={token}`
Hapus aset berdasarkan ID.

---

## 🚀 Cara Menjalankan Aplikasi

### 1. Install Dependencies Backend
```bash
cd /app/backend
pip install -r requirements.txt
```

### 2. Jalankan Backend
```bash
cd /app/backend
uvicorn server:app --host 0.0.0.0 --port 8001 --reload
```

Backend akan berjalan di: `http://localhost:8001`

### 3. Akses Aplikasi
Buka browser dan akses:
```
http://localhost:8001/login.html
```

**Login dengan:**
- Username: `admin`
- Password: `admin123`

---

## 📖 Penjelasan File

### Backend Files

#### `server.py`
File utama backend yang berisi:
- Setup database SQLite dengan 3 tabel (users, kategori, aset)
- API endpoints untuk login, logout, CRUD kategori, dan CRUD aset
- Autentikasi sederhana menggunakan token (stored in-memory)
- CORS middleware untuk akses dari frontend
- Static file serving untuk HTML/CSS/JS

**Fungsi Penting:**
- `init_db()` - Inisialisasi database dan buat tabel
- `get_current_user()` - Dependency untuk verifikasi token
- `login()` - Handle autentikasi user

#### `requirements.txt`
Daftar dependencies Python yang dibutuhkan.

---

### Frontend Files

#### `login.html`
Halaman login dengan:
- Form input username dan password
- Error message display
- Info box dengan kredensial dummy

#### `index.html` (Dashboard)
Dashboard utama setelah login dengan:
- Navbar navigasi
- Card untuk navigasi ke Kategori dan Aset
- Info section tentang fitur aplikasi

#### `kategori.html`
Halaman CRUD kategori dengan:
- Tabel daftar kategori
- Button tambah kategori
- Modal form untuk tambah/edit
- Button edit dan hapus per row

#### `aset.html`
Halaman CRUD aset dengan:
- Tabel daftar aset
- Button tambah aset
- Modal form untuk tambah/edit
- Format currency untuk saldo
- Button edit dan hapus per row

#### `style.css`
Styling global aplikasi dengan:
- Color scheme: Purple gradient (#667eea, #764ba2)
- Responsive design
- Modal styling
- Table styling
- Form styling
- Button states dan hover effects

#### `config.js`
Konfigurasi API base URL (`/api`)

#### `utils.js`
Fungsi utility:
- `getToken()` - Ambil token dari localStorage
- `checkAuth()` - Verifikasi login status
- `logout()` - Handle logout
- `formatCurrency()` - Format angka ke Rupiah
- `displayUserName()` - Tampilkan nama user di navbar

#### `auth.js`
Logika autentikasi:
- Handle form submit login
- Call API login
- Simpan token dan user data ke localStorage
- Redirect ke dashboard

#### `kategori.js`
Logika CRUD kategori:
- `loadKategori()` - Load dan tampilkan data
- `showAddModal()` - Buka modal tambah
- `editKategori(id)` - Load data untuk edit
- `deleteKategori(id)` - Hapus kategori
- Form submit handler untuk create/update

#### `aset.js`
Logika CRUD aset:
- `loadAset()` - Load dan tampilkan data
- `showAddModal()` - Buka modal tambah
- `editAset(id)` - Load data untuk edit
- `deleteAset(id)` - Hapus aset
- Form submit handler untuk create/update

---

## 🔒 Keamanan

### Saat ini (Simple):
- Password di-hash menggunakan SHA256
- Token autentikasi disimpan in-memory (hilang saat restart server)
- Token dikirim via query parameter

### Untuk Production (Rekomendasi):
- Gunakan bcrypt untuk hashing password
- Gunakan JWT dengan expiry time
- Simpan token di database atau Redis
- Kirim token via HTTP header (Authorization: Bearer)
- Implementasi HTTPS
- Rate limiting untuk prevent brute force

---

## 📝 Fitur yang Sudah Diimplementasikan

### ✅ Minggu Ini
1. **Sistem Login**
   - Autentikasi username/password sederhana
   - Session management dengan token
   - Protected routes (redirect jika belum login)

2. **CRUD Kategori Transaksi**
   - Create: Tambah kategori baru
   - Read: Tampilkan daftar kategori
   - Update: Edit kategori
   - Delete: Hapus kategori
   - Tipe: Pemasukan atau Pengeluaran

3. **CRUD Aset**
   - Create: Tambah aset baru
   - Read: Tampilkan daftar aset
   - Update: Edit aset
   - Delete: Hapus aset
   - Tipe: Cash, Rekening, atau Kredit
   - Saldo awal dalam Rupiah

### 📅 Rencana Minggu Depan
- Fitur pencatatan transaksi (pemasukan/pengeluaran)
- Laporan keuangan (summary, filter by date)
- Dashboard dengan chart/grafik

---

## 🐛 Testing

### Manual Testing

1. **Test Login:**
```bash
curl -X POST http://localhost:8001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

2. **Test Get Kategori:**
```bash
TOKEN="your_token_here"
curl "http://localhost:8001/api/kategori?token=$TOKEN"
```

3. **Test Add Kategori:**
```bash
TOKEN="your_token_here"
curl -X POST "http://localhost:8001/api/kategori?token=$TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"nama_kategori":"Makan","tipe":"pengeluaran","deskripsi":"Biaya makan sehari-hari"}'
```

---

## 💡 Tips Development

1. **Browser DevTools**: Gunakan Console untuk debug JavaScript
2. **Network Tab**: Lihat request/response API
3. **SQLite Browser**: Gunakan tools seperti DB Browser for SQLite untuk melihat isi database
4. **Postman/Thunder Client**: Test API secara manual

---

## 🎓 Konsep Penting yang Dipelajari

### Backend (FastAPI):
- REST API design
- Database operations (CRUD)
- Authentication & Authorization
- Request/Response handling
- CORS configuration

### Frontend (Vanilla JS):
- DOM manipulation
- Fetch API untuk HTTP requests
- LocalStorage untuk client-side storage
- Event handling
- Dynamic content rendering

### Database (SQLite):
- Relational database design
- Foreign keys
- SQL queries (SELECT, INSERT, UPDATE, DELETE)
- Async database operations

---

## 📧 Catatan untuk Dosen/Asisten

Aplikasi ini dibangun dengan prinsip:
1. **Modular**: File terpisah berdasarkan fungsi
2. **Sederhana**: Tanpa framework frontend yang kompleks
3. **Dokumentasi**: Kode diberi comment yang jelas
4. **Best Practice**: Menggunakan async/await, error handling
5. **Scalable**: Mudah untuk ditambahkan fitur baru

Struktur ini memudahkan untuk pengembangan di minggu-minggu berikutnya.

---

## 📄 License
Aplikasi ini dibuat untuk keperluan akademik (Tugas Besar IPPL).
