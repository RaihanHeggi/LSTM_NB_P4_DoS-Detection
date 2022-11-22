# Deteksi Serangan DoS Pada Jaringan SDN Berbasiskan P4 Programmable Dataplane 

## Penjelasan Mengenai Topik Tugas Akhir
Pada Tugas Akhir ini akan dibuat sebuah sistem pendeteksian dini yang cerdas yang berbasiskan Machine Learning, dalam hal ini akan menggunakan Algoritma LSTM dan Naive Bayes, 
dengan dibuatnya sistem pendeteksian ini diharapkan dapat mencegah terjadinya kerusakan lebih lanjut akibat serangan DoS pada Jaringan SDN.

## Hasil Pengujian
Dari pengujian yang dilakukan pada dataset didapatkan hasil pada CICIDS2017 didapatkan akurasi sebesar 97% dan FNR 2%, sementara pada NSL-KDD memiliki akurasi hingga 98.85% dengan FNR 1%, penggunaan dataset publik ini berkenaan dengan perbandingkan kuantitatif dengan pengujian sebelumnya dan akurasi yang dihasilkan lebih baik dari sistem selain itu nilai FNRnya cukup rendah, selain itu dilakukan pengujian terhadap dataset SDN-DL dihasilkan akurasi 89% dengan FNR 13%, hasilnya kurang baik dari penelitian sebelumnya namun memiliki effort untuk mencari fitur dan juga mengembangkan sistem dengan akurasi diatas 88% dan tidak terjadi overfitting, dan bila dibandingkan dengan algoritma pengujian lainnya hasil yang dicapai lebih baik.

### Gambar Hasil Pengujian Dataset NSL-KDD dan CICIDS2017
![CICDS2017 and NSL-KDD Evaluation](https://user-images.githubusercontent.com/58820833/177576475-3ad63178-43d9-4612-b3a2-c10598074061.png)

### Gambar Hasil Pengujian Dataset SDN-DL
![Algorithm Result SDN-DL (Training)](https://user-images.githubusercontent.com/58820833/177577372-d6aa464d-5c1e-4122-aec5-4f9b21c21371.png)

### Implementasi Website dan Realtime
#### Website
Dibangun menggunakan micro-framework flask, kemudian digunakan untuk melakukan analisis paket data yang dimasukan dalam bentuk .csv
![Desain di Rapikan Input File](https://user-images.githubusercontent.com/58820833/177577555-7d2069c5-0214-4209-b9ba-fbd47486ef88.PNG)
![Desain Sederhana](https://user-images.githubusercontent.com/58820833/177577561-f8524964-3e9a-4d46-9085-b426764ffb61.PNG)

#### Realtime 
Dibangun menggunakan Python Scapy untuk melakukan sniffing, kemudian menggunakan model yang sudah disiapkan, data yang diambil langsung dari simulasi P4-Mininet
![realtime_system](https://user-images.githubusercontent.com/58820833/177577567-3fd4bc7b-0794-48a3-ac91-7f26baa351be.PNG)


## Progress Saat Ini
1. Membuat Proposal dan Studi Literatur
2. Melakukan Pengumpulan 3 Dataset Latih Utama (NSL-KDD, CICIDS2017, dan Deep Learning SDN-DL Dataset)
3. Melakukan pre-processing (ada beberapa bagian perlu diperbaiki)
4. Membangun Modul Normalisasi (dipilih metode apa tadinya dan di putuskan menggunakan **Min Max Scalling**)
5. Membangun beberapa model pembanding untuk pengujian 
6. Menulis Publikasi (On-Review)
7. Menulis Laporan Akhir
8. Membuat Rekap Pengujian
9. Melakukan Percobaan
10. Menyimpan CSV hasil sniffing paket dari simulasi P4-Mininet
11. Menambah Topologi dan File Berkaitan dengan simulasi ke repository

## On Going 
1. Melakukan Studi Mendalam Mengenai Machine Learning Mendalam
2. Melakukan Studi Mengenai P4 Mendalam
3. Finalisasi Aplikasi Website dan Sistem Realtime

## Saran Pengembangan
1. Mengoneksikan dengan Controller Onos, saat ini masih terkendala karena bingung untuk melakukan pembuatan pipeconf onos
2. Dataset untuk pengujian P4-Mininet mungkin bisa lebih sophisticated lagi dengan tools lebih baik

## Tools Digunakan 
1. Ubuntu 18.04
2. Virtual Machine 
3. Mininet 
4. Controller Onos
5. P4 Simulation Model (Behavioral Model)
6. Openflow Switch
7. Pemrograman menggunakan Bahasa Python

## Instalasi VM-Ubuntu 18.04 untuk simulasi P4
Untuk menyiapkan VM ada baiknya langsung menuju ke guide yang ada pada kolom Rekap ada penjelasan lengkap atau dapat langsung menuju ke https://github.com/jafingerhut/p4-guide/blob/master/bin/README-install-troubleshooting.md, pada github tersebut disediakan ova dan shell script untuk menginstall kebutuhan simulasi P4, untuk tugas akhir ini saya memilih untuk menyiapkan sebuah VM kosong dengan basis ubuntu 18.04 kemudian menginstall dengan shell script yang disediakan, salah satu trouble yang dihadapi adalah adanya dua buah python, oleh karena itu pastikan untuk mengubah python yang ada dengan python3, karena shell scriptnya menginstall dengan dependencies python3, permasalahan ini pernah saya up di https://github.com/p4lang/tutorials/issues/462.


## Kontributor 
1. Sya Raihan Heggi


