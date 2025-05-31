import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.5/firebase-app.js'; 
import { getDatabase, ref, set, onValue } from 'https://www.gstatic.com/firebasejs/10.12.5/firebase-database.js'; 

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "slip-gaji-karyawan.firebaseapp.com",
  databaseURL: "https://slip-gaji-karyawan.firebaseio.com", 
  projectId: "slip-gaji-karyawan",
  storageBucket: "slip-gaji-karyawan.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef1234567890"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

// Save data
document.getElementById("gajiForm")?.addEventListener("submit", function(e) {
  e.preventDefault();

  const nama = document.getElementById("nama").value;
  const jabatan = document.getElementById("jabatan").value;
  const gaji = document.getElementById("gaji").value;
  const tanggal = document.getElementById("tanggal").value;

  const slipRef = ref(database, 'slips/' + Date.now());
  set(slipRef, {
    nama,
    jabatan,
    gaji,
    tanggal
  }).then(() => {
    alert("Data berhasil disimpan!");
  }).catch((error) => {
    alert("Gagal menyimpan data: " + error.message);
  });
});

// Load data
function loadSlips() {
  const slipRef = ref(database, 'slips/');
  onValue(slipRef, (snapshot) => {
    const data = snapshot.val();
    let html = "";
    for (let key in data) {
      const d = data[key];
      html += `
        <div class="slp-box">
          <p>Nama: ${d.nama}</p>
          <p>Jabatan: ${d.jabatan}</p>
          <p>Gaji: Rp${parseInt(d.gaji).toLocaleString()}</p>
          <p>Tanggal: ${d.tanggal}</p>
          <button onclick='generatePDF(${JSON.stringify(d)})'>Cetak PDF</button>
        </div>`;
    }
    document.getElementById("slipList").innerHTML = html;
  });
}
