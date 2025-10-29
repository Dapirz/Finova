// Aset CRUD functionality

checkAuth();
displayUserName();

const modal = document.getElementById('asetModal');
const form = document.getElementById('asetForm');
const tableBody = document.getElementById('asetTableBody');
const modalTitle = document.getElementById('modalTitle');

let editingId = null;

// Load data on page load
loadAset();

async function loadAset() {
    const token = getToken();
    
    try {
        const response = await fetch(`${API_BASE_URL}/aset?token=${token}`);
        const data = await response.json();
        
        if (data.length === 0) {
            tableBody.innerHTML = '<tr><td colspan="5" class="text-center">Belum ada data aset</td></tr>';
            return;
        }
        
        tableBody.innerHTML = data.map(item => {
            let badgeClass = 'badge-primary';
            if (item.tipe === 'cash') badgeClass = 'badge-success';
            else if (item.tipe === 'kredit') badgeClass = 'badge-warning';
            
            return `
                <tr data-testid="aset-row-${item.id}">
                    <td>${item.id}</td>
                    <td>${item.nama_aset}</td>
                    <td>
                        <span class="badge ${badgeClass}" data-testid="tipe-badge-${item.id}">
                            ${item.tipe}
                        </span>
                    </td>
                    <td data-testid="saldo-${item.id}">${formatCurrency(item.saldo_awal)}</td>
                    <td>
                        <button onclick="editAset(${item.id})" class="btn btn-edit" data-testid="edit-button-${item.id}">Edit</button>
                        <button onclick="deleteAset(${item.id})" class="btn btn-delete" data-testid="delete-button-${item.id}">Hapus</button>
                    </td>
                </tr>
            `;
        }).join('');
    } catch (error) {
        console.error('Error loading aset:', error);
        showError('Gagal memuat data aset');
    }
}

function showAddModal() {
    editingId = null;
    modalTitle.textContent = 'Tambah Aset';
    form.reset();
    document.getElementById('asetId').value = '';
    modal.classList.add('show');
}

async function editAset(id) {
    editingId = id;
    modalTitle.textContent = 'Edit Aset';
    document.getElementById('asetId').value = id;
    
    const token = getToken();
    
    try {
        const response = await fetch(`${API_BASE_URL}/aset?token=${token}`);
        const data = await response.json();
        const item = data.find(a => a.id === id);
        
        if (item) {
            document.getElementById('namaAset').value = item.nama_aset;
            document.getElementById('tipe').value = item.tipe;
            document.getElementById('saldoAwal').value = item.saldo_awal;
            modal.classList.add('show');
        }
    } catch (error) {
        console.error('Error loading aset:', error);
        showError('Gagal memuat data aset');
    }
}

async function deleteAset(id) {
    if (!confirm('Yakin ingin menghapus aset ini?')) {
        return;
    }
    
    const token = getToken();
    
    try {
        const response = await fetch(`${API_BASE_URL}/aset/${id}?token=${token}`, {
            method: 'DELETE'
        });
        
        const data = await response.json();
        
        if (data.success) {
            showSuccess(data.message);
            loadAset();
        } else {
            showError(data.message || 'Gagal menghapus aset');
        }
    } catch (error) {
        console.error('Error deleting aset:', error);
        showError('Gagal menghapus aset');
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
        nama_aset: document.getElementById('namaAset').value,
        tipe: document.getElementById('tipe').value,
        saldo_awal: parseFloat(document.getElementById('saldoAwal').value)
    };
    
    try {
        let url = `${API_BASE_URL}/aset?token=${token}`;
        let method = 'POST';
        
        if (editingId) {
            url = `${API_BASE_URL}/aset/${editingId}?token=${token}`;
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
            loadAset();
        } else {
            showError(data.message || 'Gagal menyimpan aset');
        }
    } catch (error) {
        console.error('Error saving aset:', error);
        showError('Gagal menyimpan aset');
    }
});

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target === modal) {
        closeModal();
    }
}