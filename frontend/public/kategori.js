// Kategori CRUD functionality

checkAuth();
displayUserName();

const modal = document.getElementById('kategoriModal');
const form = document.getElementById('kategoriForm');
const tableBody = document.getElementById('kategoriTableBody');
const modalTitle = document.getElementById('modalTitle');

let editingId = null;

// Load data on page load
loadKategori();

async function loadKategori() {
    const token = getToken();
    
    try {
        const response = await fetch(`${API_BASE_URL}/kategori?token=${token}`);
        const data = await response.json();
        
        if (data.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5" class="text-center">Belum ada data kategori</td></tr>';
            return;
        }
        
        tableBody.innerHTML = data.map(item => `
            <tr data-testid="kategori-row-${item.id}">
                <td>${item.id}</td>
                <td>${item.nama_kategori}</td>
                <td>
                    <span class="badge ${item.tipe === 'pemasukan' ? 'badge-success' : 'badge-danger'}" data-testid="tipe-badge-${item.id}">
                        ${item.tipe}
                    </span>
                </td>
                <td>${item.deskripsi || '-'}</td>
                <td>
                    <button onclick="editKategori(${item.id})" class="btn btn-edit" data-testid="edit-button-${item.id}">Edit</button>
                    <button onclick="deleteKategori(${item.id})" class="btn btn-delete" data-testid="delete-button-${item.id}">Hapus</button>
                </td>
            </tr>
        `).join('');
    } catch (error) {
        console.error('Error loading kategori:', error);
        showError('Gagal memuat data kategori');
    }
}

function showAddModal() {
    editingId = null;
    modalTitle.textContent = 'Tambah Kategori';
    form.reset();
    document.getElementById('kategoriId').value = '';
    modal.classList.add('show');
}

async function editKategori(id) {
    editingId = id;
    modalTitle.textContent = 'Edit Kategori';
    document.getElementById('kategoriId').value = id;
    
    const token = getToken();
    
    try {
        const response = await fetch(`${API_BASE_URL}/kategori?token=${token}`);
        const data = await response.json();
        const item = data.find(k => k.id === id);
        
        if (item) {
            document.getElementById('namaKategori').value = item.nama_kategori;
            document.getElementById('tipe').value = item.tipe;
            document.getElementById('deskripsi').value = item.deskripsi || '';
            modal.classList.add('show');
        }
    } catch (error) {
        console.error('Error loading kategori:', error);
        showError('Gagal memuat data kategori');
    }
}

async function deleteKategori(id) {
    if (!confirm('Yakin ingin menghapus kategori ini?')) {
        return;
    }
    
    const token = getToken();
    
    try {
        const response = await fetch(`${API_BASE_URL}/kategori/${id}?token=${token}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccess(data.message);
            loadKategori();
        } else {
            showError(data.message || 'Gagal menghapus kategori');
        }
    } catch (error) {
        console.error('Error deleting kategori:', error);
        showError('Gagal menghapus kategori');
    }
}

function closeModal() {
    modal.classList.remove('show');
    form.reset();
    editingId = null;
}

// Form submit
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const token = getToken();
    const formData = {
        nama_kategori: document.getElementById('namaKategori').value,
        tipe: document.getElementById('tipe').value,
        deskripsi: document.getElementById('deskripsi').value || null
    };
    
    try {
        let url = `${API_BASE_URL}/kategori?token=${token}`;
        let method = 'POST';
        
        if (editingId) {
            url = `${API_BASE_URL}/kategori/${editingId}?token=${token}`;
            method = 'PUT';
        }
        
        const response = await fetch(url, {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccess(data.message);
            closeModal();
            loadKategori();
        } else {
            showError(data.message || 'Gagal menyimpan kategori');
        }
    } catch (error) {
        console.error('Error saving kategori:', error);
        showError('Gagal menyimpan kategori');
    }
});

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target === modal) {
        closeModal();
    }
}