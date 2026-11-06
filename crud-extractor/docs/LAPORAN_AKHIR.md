# Laporan Akhir

## 1. Hasil evaluasi

Tempel keluaran `python evaluate.py` setelah `data/ground_truth.csv` dilengkapi.

```
Dievaluasi: audit.sql, campuran_error.sql, laporan_penjualan.sql, pemeliharaan.sql (27 triple)

Metode   Precision  Recall     F1
parser        1.00    1.00   1.00
regex         0.65    0.81   0.72

[regex]
  salah ditemukan (FP): ('audit.sql', 16, 'sesi', 'R')
  salah ditemukan (FP): ('campuran_error.sql', 4, 'pesanan', 'R')
  salah ditemukan (FP): ('campuran_error.sql', 8, 'keranjang', 'R')
  salah ditemukan (FP): ('laporan_penjualan.sql', 2, 'pelanggan', 'D')
  salah ditemukan (FP): ('laporan_penjualan.sql', 2, 'pelanggan', 'R')
  salah ditemukan (FP): ('laporan_penjualan.sql', 2, 'pesanan', 'R')
  salah ditemukan (FP): ('laporan_penjualan.sql', 2, 'rahasia', 'R')
  salah ditemukan (FP): ('laporan_penjualan.sql', 15, 'pesanan', 'R')
  salah ditemukan (FP): ('pemeliharaan.sql', 2, 'crm.alamat', 'R')
  salah ditemukan (FP): ('pemeliharaan.sql', 2, 'crm.pelanggan', 'R')
  salah ditemukan (FP): ('pemeliharaan.sql', 2, 'pelanggan_lama', 'U')
  salah ditemukan (FP): ('pemeliharaan.sql', 15, 'crm.alamat', 'R')
  terlewat (FN):       ('audit.sql', 2, 'pesanan', 'R')
  terlewat (FN):       ('laporan_penjualan.sql', 3, 'pelanggan', 'R')
  terlewat (FN):       ('laporan_penjualan.sql', 3, 'pesanan', 'R')
  terlewat (FN):       ('pemeliharaan.sql', 3, 'crm.alamat', 'R')
  terlewat (FN):       ('pemeliharaan.sql', 3, 'crm.pelanggan', 'R')

```

## 2. Tiga kasus di mana regex salah

Untuk tiap kasus: SQL-nya, kesalahan regex, dan mengapa parser benar (kaitkan dengan konsep
lexing, parsing, atau resolusi).

1.  SQL: -- DELETE FROM pelanggan (laporan_penjualan.sql, 2)
    kesalahan regex: mendeteksi tabel pelanggan dengan operasi DELETE, padahal itu hanya berupa komentar
    mengapa parser benar: pada tahap lexing, lexer mengenali tanda -- sebagai komentar satu baris dan mengabaikan seluruh teks setelahnya hingga akhir baris. makanya, query sql ini tidak diproses lebih lanjut oleh parser 
    jenis kesalahan: False Positive (FP)
2.  SQL: pelanggan p JOIN pesanan o ON o.pelanggan_id = p.id (laporan_penjualan.sql, 4 & 5)
    kesalahan regex: regex melewatkan tabel pelanggan dan pesanan yang seharusnya dicatat sebagai opersi READ
    mengapa parser benar: parser mengenali struktur FROM dan JOIN sehingga kedua tabel dapat diidentifikasi sebagai sumber data dalam perintah SELECT 
    jenis kesalahan: False Negative (FN)
3.  SQL: SELECT id nama, FROM pesanan; (campuran_error.sql, 4)
    kesalahan regex: regex tetap mendeteksi tabel pesanan sebagai operasi READ padahal sintaksnya salah karena ada tanda koma sebelum klausa FROM. seharusnya koma diletakkan setelah id jika ingin select membaca dua kolom tabel pesanan.
    mengapa parser benar: parser memeriksa kesesuaian susunan token dengan grammar SQL. tetapi karena statementnya tidak memenuhi aturan sintaks, jadi parser tidak memasukannya ke hasil ekstraksi CRUD. 
    jenis kesalahan: False Positive (FP)

## 3. Batas pendekatan kami

Minimal tiga hal yang **tidak bisa** ditangani dengan benar oleh tool ini meskipun semua bug
sudah diperbaiki. Untuk tiap batas: contoh SQL atau situasinya, akibatnya pada CRUD matrix,
dan informasi apa yang dibutuhkan untuk mengatasinya.

1.
2.
3.

## 4. Pembagian kerja

Nurul Salmahat      : lexer dan resolver
Sahla Fadhilah Rahim: parser dan analyzer
kami juga secara remote menganalisis serta memperbaiki program yang masih mengalami kendala. untuk memastikan kami saling dapat memahami, kami sering berdiskusi dan bertukar pemahaman mengenai ruang lingkup pekerjaan masing masing agar satu presepsi yang sama dan memastikan keduanya memahami keseluruhan proses pengembangan sistem
