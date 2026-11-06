# Log Penggunaan AI

Catat setiap penggunaan AI atau coding agent yang memengaruhi kode atau laporan.

| No | Siapa | Prompt / tugas (ringkas) | Hasil: diterima, diubah, atau ditolak | Alasan | Cara verifikasi |
| --- | --- | --- | --- | --- | --- |

| 1 | Sahla Fadhilah Rahim | Perbaikan mekanisme pemulihan parser setelah terjadi syntax error | Diterima | Perbaikan sesuai dengan spesifikasi yang mengharuskan parser melanjutkan pemrosesan setelah menemukan tanda titik koma | Menguji statement yang salah diikuti yang benar |

| 2 | Sahla Fadhilah Rahim | Perbaikan parsing LEFT OUTER JOIN | Diterima | Solusi sederhana dan sesuai dengan grammar karena OUTER merupakan keyword opsional setelah LEFT | Menguji LEFT JOIN dan OUTER JOIN |

| 3 | Sahla Fadhilah Rahim | Cara memperbaiki error resolver pada INSERT SELECT | Diterima | Solusi menggunakan pengecekan None sebelum iterasi sehingga dapat menangani INSERT VALUES maupun INSERT SELECT| Menjalankan test_insert_select_dapat_diresolusi|

| 4 | Sahla Fadhilah Rahim | Bagaimana cara memperbaiki error pada bagian INSERT SELECT di analyzer | Diubah | Saran awal menggunakan _collect_expr() yang tidak tersedia dalam kode, sehingga diganti dengan _collect() yang sudah ada | Menjalankan test_insert_select_crud |

| 5 | Sahla Fadhilah Rahim | Cara mengatasi operasi UPDATE yang merambat ke tabel subquery | Diterima | Karena perubahan paramater operasi sudah sesuai dengan grammar | Menjalankan test_matrix_laporan_penjualan |

| 6 | Sahla Fadhilah Rahim | Apa perbedaan hasil matriks CRUD dengan hasil yang diharapkan oleh sistem? | Diterima | Karena AI membantu menelusuri sumber operasi U tambahan pada tabel pesanan hingga ditemukan penerusan operasi yang tidak sesuai ke subquery | Membandingkan hasil res.matrix() sebelum dan sesudah perbaikan |

| 7 | Sahla Fadhilah Rahim | Tentukan pengujian regresi untuk bug INSERT SELECT | Diterima | Karena pengujian dipisahkan menjadi pengujian resolver dan analyzer, keduanya memiliki proses dan tujuan berbeda | Menjalankan kedua test secara terpisah dan seluruh test menggunakan pytest |

Refleksi (3-5 kalimat)
AI paling membantu dalam menelusuri penyebab bug, terutama ketika harus memahami hubungan antara parser, resolver, dan analyzer.  Namun, AI sempat memberikan saran yang kurang tepat, seperti menggunakan fungsi _collect_expr() yang ternyata tidak tersedia dalam kode dan perlu diganti dengan _collect(). Selain itu, hasil analisis AI tidak langsung diterima begitu saja, tetapi diperiksa kembali dengan melihat implementasi program dan menjalankan pengujian menggunakan pytest. Jadi dapat disimpulkan bahwa AI membantu mempercepat pencarian solusi, tetapi keputusan akhir tetap didasarkan pada pilihan manusia.