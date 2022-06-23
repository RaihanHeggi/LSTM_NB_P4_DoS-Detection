const komentar = {
    nama: "anon",
    tanggal: null,
    isiKomen: null,
    jumlahKomen: 0,
    months: ["January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
};
function submit() {
    let hari = new Date().getDate();
    let bulan = new Date().getMonth();
    let tahun = new Date().getFullYear();
    komentar.nama = document.getElementById('nama-komentar').value;
    komentar.tanggal = " • " + hari + " " + komentar.months[bulan] + " " + tahun;
    komentar.isiKomen = document.getElementById('kolom-komentar').value;
    komentar.jumlahKomen = document.querySelector('#jumkomentar').innerText;

    if (komentar.isiKomen.length == 0) {
        alert("Maaf, tolong isi komentar anda.");
    } else {
        komentar.nama = komentar.nama.length != 0 ? komentar.nama : "anon";
        document.querySelector("#jumkomentar").innerText = ++komentar.jumlahKomen;
        
        const fullData = {
            username: komentar.nama,
            date: komentar.tanggal,
            comments: komentar.isiKomen
        }
        showComments(fullData);
        renderComments();
    }
}