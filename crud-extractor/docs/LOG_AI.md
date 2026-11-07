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

| 8 | Nurul | bedah kode (lexer.py dan resolver.py) serta jelaskan | Diterima | agar bisa memahami cara kerja setiap kodenya serta membantu menjelaskan dan menemukan ketidaksesuaian atau bug yang tidak terdeteksi | menjalankan test dan bertanya lagi |

| 9 | Nurul Salmahat | cara menangani komentar blok /* .. */ pada lexer agar seluruh isi komentar diabaikan? serta buat juga unit testnya | Diterima | karena komentar blok dapat terdiri beberapa baris, jadi perlu ditangani sampai menemukan penutup */ agar isi komentar tidak dianggap sebagai token query SQL | Menjalankan test_block_comment_multiline dan test_block_comment_tidak_ditutup. |

| 10 | Nurul Salmahat | cara membuat keyword SQL tidak membedakan huruf besar dan kecil, tetapi tetap mempertahankan penulisan identifier | Diterima | karena keyword SQL harus dikenali meskipun ditulis menggunakan kombinasi huruf besar dan kecil, sedangkan identifier harus mempertahankan penulisan aslinya lalu AI secara otomatis memberikan unit testnya juga | Menjalankan test_keyword_case_insensitive dan test_identifier_yang_diawali_keyword. |

| 11 | Nurul Salmahat | menangani tanda petik tunggal yang berulang serta buat unit-test | Diterima | karena tanda petik tunggal berulang itu harus dianggap satu kesatuan karakter di dalam string | Menjalankan test_string_doubled_quote. |

| 12 | Nurul Salmahat | buatkan test buat ngecek operator <> dan variasi operator yang diawali tanda < | Diterima | karena untuk memastikan operator <> dikenali sebagai satu token serta dapat dibedakan dari operator <= dan < | Menjalankan test_operator_not_equal_angle_bracket dan test_operator_less_than_variants |

| 13 | Nurul Salmahat | kenapa alias pada subquery tidak terbaca dengan benar ketika menggunakan nama yang sama dengan tabel di scope luar? | Diterima | karena alias pada scope terdalam harus diprioritaskan agar tidak menyebabkan kesalahan resolusi | Menjalankan test_shadowing_alias_di_subquery. |

| 14 | Nurul Salmahat | bagaimana menentukan tabel asal untuk kolom yang tidak menggunakan qualifier atau nama tabel | Diterima | karena kolom tanpa nama tabel hanya dapat ditentukan secara pasti jika terdapat satu sumber tabel. jika sumbernya lebih dari satu, maka kolom berpotensi ambigu | Menjalankan test_kolom_tanpa_qualifier_satu_tabel dan test_kolom_ambigu_tanpa_qualifier. |

| 15 | Nurul Salmahat | buat test tambahan untuk memvalidasi bug yang sudah diperbaiki | Diterima | agar bug yang sudah diperbaiki itu mempunyai acuan kebenaran | Menjalankan test_tambahan.py |

Refleksi (3-5 kalimat)
AI paling membantu dalam menelusuri penyebab bug, terutama ketika harus memahami hubungan antara parser, resolver, dan analyzer. Selain itu, AI juga membantu dalam memahami kode Lexer dan Resolver, memberikan saran perbaikan, serta menyusun unit test untuk menguji setiap bug yang ditemukan. Namun, AI sempat memberikan saran yang kurang tepat, seperti menggunakan fungsi _collect_expr() yang ternyata tidak tersedia dalam kode dan perlu diganti dengan _collect(). Hasil analisis dan saran AI tidak langsung diterima begitu saja, tetapi diperiksa kembali dengan melihat implementasi program dan menjalankan pengujian menggunakan pytest, CLI, serta AST pada file contoh. Jadi, dapat disimpulkan bahwa AI membantu mempercepat proses pemahaman dan pencarian solusi, tetapi keputusan akhir tetap didasarkan pada pertimbangan dan verifikasi manusia.