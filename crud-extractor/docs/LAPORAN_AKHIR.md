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
Berdasarkan hasil evaluasi terhadap empat file SQL, metode parser memperoleh nilai Precision, Recall, dan F1 sebesar 1.00. Hal ini menunjukkan bahwa seluruh ekstraksi CRUD dari parser sesuai dengan data ground truth yang digunakan dalam pengujian. Sementara itu, metode regex hanya memperoleh Precision sebesar 0.65, Recall sebesar 0.81, dan F1 sebesar 0.72. Hasil tersebut menunjukkan bahwa regex masih menghasilkan beberapa deteksi yang tidak sesuai (False Positive) dan melewatkan beberapa operasi CRUD yang seharusnya terdeteksi (False Negative). Dengan demikian, pada kumpulan data pengujian ini, metode parser memberikan hasil ekstraksi yang lebih akurat dibandingkan metode regex. 

## 2. Tiga kasus di mana regex salah

Untuk tiap kasus: SQL-nya, kesalahan regex, dan mengapa parser benar (kaitkan dengan konsep
lexing, parsing, atau resolusi).

1.  SQL: -- DELETE FROM pelanggan (laporan_penjualan.sql, 2)
    kesalahan regex: mendeteksi tabel pelanggan dengan operasi DELETE, padahal itu hanya berupa komentar
    mengapa parser benar: pada tahap lexing, lexer mengenali tanda -- sebagai komentar satu baris dan mengabaikan seluruh teks setelahnya hingga akhir baris. makanya, query sql ini tidak diproses lebih lanjut oleh parser 
    jenis kesalahan: False Positive (FP)
2.  SQL: pelanggan p JOIN pesanan o ON o.pelanggan_id = p.id (laporan_penjualan.sql, 3 - 5)
    kesalahan regex: regex melewatkan tabel pelanggan dan pesanan yang seharusnya dicatat sebagai opersi READ
    mengapa parser benar: parser mengenali struktur FROM dan JOIN sehingga kedua tabel dapat diidentifikasi sebagai sumber data dalam perintah SELECT 
    jenis kesalahan: False Negative (FN)
3.  SQL: SELECT id nama, FROM pesanan; (campuran_error.sql, 4)
    kesalahan regex: regex tetap mendeteksi tabel pesanan sebagai operasi READ meskipun statement memiliki kesalahan sintaks berupa tanda koma berlebih sebelum klausa FROM.
    mengapa parser benar: parser memeriksa kesesuaian susunan token dengan grammar SQL. tetapi karena terdapat tanda koma setelah elemen terakhir pada daftar kolom, statement tidak memenuhi aturan sintaks sehingga tidak dimasukkan ke dalam hasil ekstraksi CRUD.
    jenis kesalahan: False Positive (FP)

## 3. Batas pendekatan kami

Minimal tiga hal yang **tidak bisa** ditangani dengan benar oleh tool ini meskipun semua bug
sudah diperbaiki. Untuk tiap batas: contoh SQL atau situasinya, akibatnya pada CRUD matrix,
dan informasi apa yang dibutuhkan untuk mengatasinya.

1. Validasi Schema Database
    Contoh SQL: SELECT nama_tidak_ada FROM pelanggan;
    CRUD Extractor belum bisa memastikan apakah tabel dan kolom yang digunakan dalam query benar-benar tersedia di database. Meskipun kolom tersebut belum tentu ada di database, query tetap berhasil diproses tanpa menghasilkan error. Artinya, sistem hanya bisa mengenali tabel yang digunakan dalam query, tetapi belum bisa memeriksa apakah tabel dan kolom tersebut benar-benar ada di database.
    Akibat pada CRUD Matrix: CRUD Matrix tetap mencatat tabel pelanggan sebagai tabel yang mengalami operasi Read (R).
    Informasi yang dibutuhkan untuk mengatasinya: daftar nama tabel yang ada pada database, daftar nama kolom yang ada pada setiap tabel, dan relasi antar tabel (primary key dan foreign key).
2. Column-level CRUD
    Contoh SQL: UPDATE pelanggan SET alamat = 'Bandung' WHERE id = 10;
    Query tersebut melakukan perubahan pada kolom alamat dan menggunakan kolom id sebagai kondisi. Namun, hasil analisis CRUD Extractor hanya menunjukkan bahwa tabel pelanggan mengalami operasi (U), tanpa memberikan informasi kolom yang terlibat.
    Akibat pada CRUD Matrix: CRUD Matrix belum dapat memberikan gambaran detail mengenai kolom mana yang dibaca atau diubah dalam suatu operasi.
    Informasi yang dibutuhkan untuk mengatasinya: nama tabel yang terlibat, nama kolom yang diubah, dan nama kolom yang digunakan sebagai kondisi.
3. Trigger Analysis
    Contoh SQL: CREATE TRIGGER update_stok AFTER INSERT ON pesanan
                BEGIN
                    UPDATE produk
                    SET stok = stok - 1;
                END;
    Query tersebut melakukan trigger yang secara otomatis melakukan operasi update pada tabel produk ketika terjadi insert pada tabel pesanan. Namun, berdasarkan hasil pengujian, CRUD Extractor menghasilkan syntax error karena belum mengenali CREATE TRIGGER sebagai statement yang didukung. 
    Akibat pada CRUD Matrix: operasi yang terdapat di dalam trigger tidak dapat diproses dan tidak tercatat di CRUD Matrix.
    Informasi yang dibutuhkan untuk mengatasinya: nama trigger & tabel yang menjadi pemicunya, jenis trigger (BEFORE/AFTER), jenis operasi yang memicunya (INSERT, UPDATE atau DELETE), isi perintah SQL yang dijalankan dalam trigger, serta tabel & kolom yang terdampak oleh operasi di dalam trigger.

## 4. Pembagian kerja

Nurul Salmahat      : lexer dan resolver
Sahla Fadhilah Rahim: parser dan analyzer
kami juga secara remote menganalisis serta memperbaiki program yang masih mengalami kendala. untuk memastikan kami saling dapat memahami, kami sering berdiskusi dan bertukar pemahaman mengenai ruang lingkup pekerjaan masing masing agar satu presepsi yang sama dan memastikan keduanya memahami keseluruhan proses pengembangan sistem.