# Laporan Bug

Salin blok di bawah untuk setiap bug. Bagian **Akar masalah** wajib ditulis dengan kata-kata
sendiri dan memakai konsep dari *Crafting Interpreters* (sebutkan bab). Bagian ini diuji lisan.

---

## Bug 0: (TEMPLATE / judul singkat)

**Ditemukan oleh:** (nama) · **Diperbaiki oleh:** (nama)

**Gejala.** Input, output yang didapat, dan output yang diharapkan menurut SPESIFIKASI.md
(sebutkan bagiannya).

**Reproduksi minimal.** SQL terpendek yang memicu bug:

```sql

```

**Akar masalah.** Mengapa kode lama salah? Konsep apa yang dilanggar?

**Perbaikan.** File dan fungsi yang diubah, serta alasannya. Sebutkan juga perbaikan
alternatif yang kalian pertimbangkan dan alasan tidak memilihnya.

**Test regresi.** Nama test di `tests/test_tambahan.py` yang gagal sebelum perbaikan dan lulus
sesudahnya.

**Peran AI.** Apakah AI membantu menemukan atau memperbaiki bug ini? Bagaimana kalian
memverifikasinya?

## Bug 1: TODO komentar blok belum didukung

**Ditemukan oleh:** Nurul Salmahat · **Diperbaiki oleh:** Nurul Salmahat

**Gejala.** ketika lexer menemukan komentar blok yang diawali /*  dan di akhiri */, program menghasilkan LexError karena fitur komentar blok belum didukung. menurut SPESIFIKASI.md bagian 2.3, lexer harus dapat melewati komentar blok dan tidak menghasilkan token dari isi komentar tersebut.

**Reproduksi minimal.** 

```
/* komentar\n   dua baris */ SELECT
```

**Akar masalah.** fungsi _scan_token() sebelumnya hanya menangani komentar satu baris yang diawali --. penanganan komentar blok masih berupa TODO sehingga lexer tidak memiliki proses untuk membaca isi komentar sampai menemukan penutup */.  Konsep ini berkaitan dengan Bab 4 Scanning pada Crafting Interpreters, yang menjelaskan bahwa scanner bertugas membaca karakter sumber program dan mengelompokkannya menjadi token. Komentar merupakan bagian dari teks sumber yang harus dikenali dan dilewati oleh scanner, bukan diteruskan sebagai token untuk tahap parsing. Dengan demikian, lexer perlu membaca seluruh isi komentar sampai menemukan penutupnya.

**Perbaikan.** perlu adanya fungsi baru yang membaca karakter sampai menemukan */. fungsi _scan_token() mendeteksi pembuka /* kemudian memanggil _block_comment() untuk membaca karakter sampai menemukan penutup */. jika komentar tidak ditutup sampai akhir input, fungsi akan menghasilkan LexError.

**Test regresi.** test_block_comment_multiline dan test_block_comment_tidak_ditutup

**Peran AI.** saya memperbaiki bug berdasarkan TODO yang terdapat pada fungsi _scan_token() dan menyesuaikan implementasinya dengan SPESIFIKASI.md.

## Bug 2: menormalisasikan keyword menjadi uppercase

**Ditemukan oleh:** Nurul Salmahat · **Diperbaiki oleh:** Nurul Salmahat

**Gejala.** ketika di test pertama kali, test_keyword_huruf_kecil mengembalikan error karena keyword yang ditulis menggunakan huruf kecil seperti select, maka dikenali sebagai IDENT, bukan KEYWORD. padahal menurut SPESIFIKASI.md bagian 2.2, keyword tidak peka terhadap huruf besar dan kecil dan nilai token keyword selalu uppercase.

**Reproduksi minimal.** 

```
select id from t
```

**Akar masalah.** kode lama pada fungsi _word() itu membandingkan kata secara langsung dengan KEYWORDS. Maka select di test_keyword_huruf_kecil itu tidak cocok dengan SELECT. Hal ini berkaitan dengan Bab 4 Scanning, khususnya proses pengenalan token berdasarkan pola karakter yang dibaca. Scanner perlu membedakan keyword dan identifier berdasarkan aturan leksikal yang telah ditentukan. Dalam implementasi ini, normalisasi huruf digunakan untuk mengenali keyword tanpa mengubah teks asli identifier.

**Perbaikan.** Mengubah teks sementara menjadi uppercase menggunakan text.upper() untuk pemeriksaan terhadap KEYWORDS. Jika termasuk keyword, nilai token disimpan dalam uppercase. Jika bukan keyword, teks asli tetap disimpan sebagai IDENT.

**Test regresi.** test_keyword_case_insensitive dan test_identifier_yang_diawali_keyword

**Peran AI.** AI memberikan saran normalisasi menggunakan upper(). Perbaikan diverifikasi melalui test.

## Bug 3: doubled quote tidak terbaca sebagai satu string

**Ditemukan oleh:** Nurul Salmahat · **Diperbaiki oleh:** Nurul Salmahat

**Gejala.** string yang mengandung dua kutip tunggal berturut-turut dipotong pada kutip pertama. Hal ini belum sesuai dengan SPESIFIKASI.md bagian 2.4 menyatakan bahwa dua kutip berturut-turut di dalam string mewakili satu karakter kutip.

**Reproduksi minimal.** 

```
'O''Brien'
```

**Akar masalah.** fungsi _string() langsung menganggap setiap kutip tunggal sebagai penutup string tanpa memeriksa apakah terdapat kutip tunggal kedua setelahnya. Konsep ini berkaitan dengan Bab 4 Scanning, yang menjelaskan proses pengenalan literal string oleh scanner. Scanner harus mengetahui batas awal dan akhir suatu string serta menangani karakter khusus yang menjadi bagian dari isi string. Oleh karena itu, tanda petik tunggal berulang perlu diperiksa terlebih dahulu agar tidak keliru dianggap sebagai penutup string.

**Perbaikan.** mengubah _string() agar memeriksa karakter berikutnya ketika menemukan kutip tunggal. Jika karakter berikutnya juga kutip tunggal, kedua kutip dikonsumsi dan satu karakter kutip ditambahkan ke nilai string. Jika tidak, kutip dianggap sebagai penutup string.

**Test regresi.** test_string_doubled_quote()

**Peran AI.** AI membantu mengidentifikasi bahwa fungsi _string() mengakhiri pembacaan string ketika menemukan tanda petik tunggal pertama. AI menyarankan pemeriksaan karakter berikutnya sebelum mengakhiri string. Perbaikan diverifikasi melalui test_string_doubled_quote dengan memastikan nilai string yang dihasilkan tetap utuh.

## Bug 4: operator <> tidak dikenali sebagai satu token

**Ditemukan oleh:** Nurul Salmahat · **Diperbaiki oleh:** Nurul Salmahat

**Gejala.** operator <> ternyata dibaca menjadi dua token < dan >, padahal SPESIFIKASI.md bagian 2.5 mengharuskan <> menjadi satu token OP.

**Reproduksi minimal.** 

```
<>
```

**Akar masalah.** pemindaian operartor < hanya memeriksa kemungkinan operator <=, jadi tidak memeriksa apakah <> memungkinkan. Konsep ini berkaitan dengan maximal munch, yaitu membaca karakter sebanyak mungkin selama masih membentuk token yang valid, sehingga <> dikenali sebagai satu token, bukan dua token terpisah.

**Perbaikan.** penambahan percabangan untuk memeriksa karakter > setelah karakter <. jika ditemukan, keduanya akan disimpan sebagai satu token OP dengan nilai <>.

**Test regresi.** test_operator_not_equal_angle_bracket dan test_operator_less_than_variants

**Peran AI.** AI membantu menganalisis penanganan operator yang diawali tanda < pada fungsi _scan_token(). Perbaikan diverifikasi melalui test_operator_not_equal_angle_bracket dan test_operator_less_than_variants.

## Bug 5: TODO kolom tanpa qualifier

**Ditemukan oleh:** Nurul Salmahat · **Diperbaiki oleh:** Nurul Salmahat

**Gejala.** kolom tanpa qualifier, seperti nama, belum memiliki nilai ColumnRef.resolved, padahal SPESIFIKASI.md bagian 4.3 mengatur resolusi kolom tanpa qualifier berdasarkan jumlah tabel pada scope terdalam.

**Reproduksi minimal.** 

```
SELECT nama
FROM pelanggan
WHERE aktif = 1
```

**Akar masalah.** fungsi _column() yang hanya menangani kolom dengan qualifier. bagian untuk kolom tanpa qualifier masih berupa TODO, jadi resolver belum menentukan tabel asal kolom. Konsep ini berkaitan dengan Bab 11 Resolving and Binding, yang membahas proses pencarian variabel berdasarkan lingkungan atau scope tempat variabel tersebut berada.

**Perbaikan.** mengambil seluruh entri pada scope terdalam. jika hanya ada satu tabel, col.resolved diisi dengan tabel tersebut. jika lebih dari satu tabel, resolver memberikan warning bahwa kolom itu ambigu tanpa skema/tabel. jika tidak ada tabel acuan, resolver memberikan warning.

**Test regresi.** test_kolom_tanpa_qualifier_satu_tabel dan test_kolom_ambigu_tanpa_qualifier

**Peran AI.** AI membantu menguraikan aturan resolusi kolom tanpa qualifier berdasarkan jumlah tabel dalam scope. Perbaikan diverifikasi melalui test_kolom_tanpa_qualifier_satu_tabel dan test_kolom_ambigu_tanpa_qualifier.

## Bug 6: urutan pencarian alias dalam scope terbalik

**Ditemukan oleh:** Nurul Salmahat · **Diperbaiki oleh:** Nurul Salmahat

**Gejala.** alias pada subquery mengambil tabel dari scope luar dulu, bukan scope dalam (reversed). Hal ini tidak sesuai dengan SPESIFIKASI.md bagian 4.3 yang mengharuskan pencarian dimulai dari scope terdalam.

**Reproduksi minimal.** 

```
SELECT p.nama
FROM pelanggan p
WHERE EXISTS (
    SELECT p.id
    FROM pesanan p
);
```

**Akar masalah.** penggunaan reversed(chain) menyebabkan urutan pencarian tidak sesuai SPESIFIKASI.md. Pencarian dimulai dari lingkungan terdekat, kemudian dilanjutkan ke lingkungan luar jika nama tidak ditemukan. Prinsip tersebut diterapkan pada resolver agar alias dalam subquery diprioritaskan dibandingkan alias dengan nama yang sama pada query luar. Konsep ini juga berkaitan dengan shadowing.

**Perbaikan.** mengganti iterasi reversed(chain) menjadi chain

**Test regresi.** test_shadowing_alias_di_subquery()

**Peran AI.** AI membantu menganalisis kesalahan urutan pencarian alias pada fungsi _lookup() yang menyebabkan alias pada scope luar ditemukan lebih dahulu. Perbaikan diverifikasi menggunakan test shadowing alias pada subquery.

## Bug 7: fungsi delete pada resolver belum menyatakan keluar dari scope aktif

**Ditemukan oleh:** Nurul Salmahat · **Diperbaiki oleh:** Nurul Salmahat

**Gejala.** alias dari statement delete bisa terbawa ke statement berikutnya karena ada self.push() tapi tidak ada self.pop(). hal ini melanggar SPESIFIKASI.md bagian 4.5 yang mengharuskan setiap statement berdiri sendiri dan tidak meninggalkan scope.

**Reproduksi minimal.** 

```
DELETE FROM sesi s WHERE s.id = 1;

SELECT s.id FROM pengguna u;
```

**Akar masalah.** fungi delete memanggil push() untuk membuat scope baru, tapi tidak memanggil pop() setelah resolusi selesai. akibatnya, scope delete akan tetap aktif dan alias s akan terlihat oleh statement berikutnya. Konsep ini berkaitan dengan Bab 11 Resolving and Binding, yang menjelaskan bahwa setiap scope memiliki batas lingkungan pencarian tersendiri.

**Perbaikan.** menambahkan pemanggilan _pop() agar scope delete ditutup setelah resolusi selesai

**Test regresi.** test_delete_tidak_membocorkan_scope()

**Peran AI.** AI membantu menganalisis kemungkinan kebocoran scope pada statement DELETE dan mengarahkan pemeriksaan mekanisme _push() dan _pop(). Perbaikan diverifikasi melalui test untuk memastikan alias DELETE tidak terbawa ke statement berikutnya.

---

## Bug 8: INSERT ... SELECT belum diimplementasikan pada parser


**Ditemukan oleh:** Sahla Fadhilah Rahim · **Diperbaiki oleh:** Sahla Fadhilah Rahim

**Gejala.** 
Input: INSERT INTO arsip (id) SELECT id FROM pesanan WHERE total > 10
Output yang didapat: ParseError: Baris 1, kolom 24: INSERT ... SELECT belum didukung, ditemukan 'SELECT'
Output yang diharapkan: Statement berhasil di parse menjadi node AST Insert yang memuat klausa select_stmt sesuai dengan SPESIFIKASI.md Bagian 3 (Grammar) dan Bagian 5 (Aturan CRUD).

**Reproduksi minimal.** 

```
INSERT INTO arsip (id) SELECT id FROM pesanan WHERE total > 10;
```

**Akar masalah.** Fungsi INSERT di crud/parser.py baru mengimplementasikan klausa VALUES dan belum menangani klausa SELECT sehingga menampilkan fungsi ParseError saat mendapatkan token SELECT setelah table (kolom). Konsep ini berkaitan dengan Bab 5 dan Bab 6, yang membahas bagaimana parser mengenali dan membentuk struktur statement berdasarkan grammar. Setiap bentuk statement memiliki aturan sintaks dan struktur yang berbeda. Oleh karena itu, parser perlu mengenali INSERT ... SELECT sebagai salah satu bentuk statement INSERT yang valid, bukan hanya mendukung bentuk INSERT ... VALUES.


**Perbaikan.** 
File dan fungsi yang diubah:crud/parser.py, pada fungsi _insert().
Alasan: Menambahkan pengecekan token SELECT (if self._check_kw("SELECT"):) untuk memanggil fungsi parsing subquery (_select()) dan mengembalikan node AST ast.Insert dengan argumen select statement yang valid, menggantikan raise error bawaan awal.
Alternatif yang ditolak: Mengabaikan error atau memperlakukan select sebagai nilai values biasa, karena akan melanggar grammar dan merusak pembentukan struktur AST serta analisis aturan CRUD di tahap selanjutnya.

**Test regresi.** Nama test di `tests/test_tambahan.py` adalah test_regresi_insert_select, yang awalnya failed sebelum perbaikan dan berubah menjadi passed sesudahnya.

**Peran AI.** Tidak, saya memperbaiki bug nya sesuai dengan bug yang terlihat error pada file test.
---

## Bug 9: Kesalahan Presedensi Operator AND dan OR

**Ditemukan oleh:** Sahla Fadhilah Rahim · **Diperbaiki oleh:** Sahla Fadhilah Rahim

**Gejala.** 
Input: query SQL yang menggunakan operator AND dan OR secara bersamaan
Output yang didapat: parser menghasilkan struktur AST dengan urutan yang salah, implementasi parser lama memperlakukan kedua operator tersebut pada tingkat presedensi yang sama. Hasilnya "(a = 1 OR b = 2) AND c = 3".
Akibatnya, ekspresi yang seharusnya dikelompokkan berdasarkan prioritas operator justru diproses dari kiri ke kanan tanpa memperhatikan perbedaan presedensinya.
Output yang diharapkan: a = 1 OR (b = 2 AND c = 3), menurut SPESIFIKASI.md bagian 3.1, operator AND memiliki presedensi lebih tinggi daripada OR. 

**Reproduksi minimal.** 

```
SELECT * FROM mahasiswa WHERE a = 1 OR b = 2 AND c = 3;
```

**Akar masalah.** Berdasarkan konsep Recursive Descent Parsing pada Crafting Interpreters Bab 6, setiap tingkat presedensi operator seharusnya direpresentasikan melalui aturan parsing yang berbeda. Dengan cara ini, parser dapat menentukan operator mana yang harus diproses lebih dahulu.
Pada implementasi sebelumnya, operator AND dan OR ditempatkan dalam satu fungsi _logical(). Keduanya diproses menggunakan perulangan yang sama sehingga tidak ada pemisahan tingkat presedensi.
Hal tersebut menyebabkan parser tidak mengikuti aturan prioritas operator yang telah ditentukan dalam grammar. Seharusnya, operator OR memanggil aturan parsing AND, sedangkan operator AND memanggil aturan parsing NOT. Dengan begitu, AND akan membentuk ekspresi terlebih dahulu sebelum digabungkan dengan OR.


**Perbaikan.** 
File dan fungsi yang diubah:crud/parser.py, pada fungsi _logical() dan penambahan fungsi _and().
Perbaikan dilakukan dengan memisahkan proses parsing operator AND dan OR menjadi dua fungsi berbeda. Fungsi _logical() menangani operator OR, sedangkan fungsi _and() menangani operator AND.
Alternatif yang dipertimbangkan adalah menggunakan tanda kurung secara manual ketika memproses ekspresi. Namun, pendekatan tersebut tidak dipilih karena tidak menyelesaikan masalah presedensi secara umum dan akan membuat parser bergantung pada penulisan tanda kurung dari pengguna.

**Test regresi.** Nama test di `tests/test_tambahan.py` adalah test_presedensi_and_or, Test memastikan bahwa ekspresi a = 1 OR b = 2 AND c = 3 menghasilkan struktur AST yang sesuai dengan presedensi pada spesifikasi. 

**Peran AI.** memberikan alternatif perbaikan dengan memisahkan fungsi parsing berdasarkan tingkat presedensi.
Perbaikan diverifikasi dengan membandingkan struktur AST sebelum dan sesudah perubahan serta menjalankan test regresi untuk memastikan urutan operasi sudah sesuai spesifikasi.
---

## Bug 10: Error Recovery Menghentikan Parsing Seluruh File

**Ditemukan oleh:** Sahla Fadhilah Rahim · **Diperbaiki oleh:** Sahla Fadhilah Rahim

**Gejala.** 
Ketika parser menemukan syntax error pada salah satu statement, parser tidak dapat melanjutkan pemrosesan statement berikutnya. Seluruh token yang tersisa justru dibuang sampai mencapai akhir input.

Menurut SPESIFIKASI.md bagian 6, parser harus menerapkan mekanisme panic mode, yaitu membuang token sampai dan termasuk tanda titik koma (;) berikutnya, kemudian melanjutkan parsing statement setelahnya.

Hasil parser lama: statement pertama menghasilkan syntax error dan statement kedua tidak diproses karena seluruh token dibuang sampai EOF.

Hasil yang diharapkan: statement pertama menghasilkan satu syntax error dan statement kedua tetap berhasil di parse.

**Reproduksi minimal.** 

```
SELECT FROM mahasiswa;
SELECT * FROM dosen;
```
**Akar masalah.** Berdasarkan konsep Error Handling dan Panic Mode Error Recovery pada Crafting Interpreters Bab 6, parser tidak seharusnya berhenti sepenuhnya ketika menemukan kesalahan sintaks. Parser perlu menentukan titik aman atau synchronization point agar proses parsing dapat dilanjutkan.

Pada implementasi sebelumnya, fungsi _synchronize() menggunakan perulangan yang terus membuang token selama belum mencapai EOF. Tidak terdapat pemeriksaan terhadap tanda titik koma sebagai batas antar-statement.

Akibatnya, parser kehilangan kemampuan untuk mengenali awal statement berikutnya. Padahal, dalam grammar SQL yang digunakan, tanda titik koma berfungsi sebagai pemisah antar-statement sehingga dapat dijadikan titik sinkronisasi.

**Perbaikan.** 
File dan fungsi yang diubah:crud/parser.py, pada fungsi _synchronize().
Perbaikan dilakukan dengan menambahkan pemeriksaan token SEMICOLON di dalam perulangan. Ketika tanda titik koma ditemukan, parser akan membuang tanda tersebut dan menghentikan proses sinkronisasi sehingga parsing dapat dilanjutkan dari statement berikutnya.

Alternatif yang dipertimbangkan adalah menghentikan seluruh proses parsing ketika ditemukan syntax error. Namun, pendekatan tersebut tidak dipilih karena bertentangan dengan spesifikasi yang mengharuskan statement valid setelah statement yang rusak tetap diproses.

**Test regresi.** Nama test di `tests/test_tambahan.py` adalah test_error_recovery, Test memastikan bahwa ketika terdapat statement yang mengalami syntax error, statement valid setelah tanda titik koma tetap berhasil diparse.

**Peran AI.** AI membantu menemukan ketidaksesuaian antara implementasi _synchronize() dengan aturan error recovery dalam spesifikasi. Perbaikan diverifikasi dengan memberikan input yang terdiri dari statement rusak dan statement valid, kemudian memeriksa jumlah syntax error serta jumlah statement yang berhasil diparse.
---

## Bug 11: Parser Tidak Mendukung LEFT OUTER JOIN

**Ditemukan oleh:** Sahla Fadhilah Rahim · **Diperbaiki oleh:** Sahla Fadhilah Rahim

**Gejala.** 
Ketika parser menerima query SQL yang menggunakan LEFT OUTER JOIN, parser menghasilkan syntax error karena tidak mengenali keyword OUTER setelah keyword LEFT.

Menurut SPESIFIKASI.md bagian 3, aturan grammar JOIN memperbolehkan penggunaan LEFT [OUTER] JOIN. Artinya, keyword OUTER bersifat opsional setelah LEFT.

Hasil parser lama: parser menghasilkan syntax error karena setelah membaca LEFT, parser langsung mengharapkan keyword JOIN, sedangkan token yang ditemui adalah outer.

Hasil yang diharapkan: parser berhasil mengenali query tersebut sebagai statement SELECT dengan jenis JOIN LEFT.

**Reproduksi minimal.** 

```
SELECT * FROM a LEFT OUTER JOIN b ON a.id = b.id;
```
**Akar masalah.** Berdasarkan konsep Recursive Descent Parsing pada Crafting Interpreters Bab 6, setiap aturan grammar harus diterjemahkan menjadi proses parsing yang dapat mengenali seluruh bentuk sintaks yang diperbolehkan.

Pada implementasi sebelumnya, fungsi _join() sudah dapat mengenali keyword LEFT, tetapi setelah itu parser langsung memanggil _expect_kw("JOIN"). Tidak terdapat proses untuk memeriksa apakah keyword opsional OUTER muncul di antara keduanya.

Akibatnya, implementasi parser hanya mencakup bentuk LEFT JOIN, tetapi belum mencakup bentuk LEFT OUTER JOIN yang sebenarnya diperbolehkan oleh grammar.

**Perbaikan.** 
File dan fungsi yang diubah:crud/parser.py, pada fungsi _join().
Perbaikan dilakukan dengan menambahkan pemeriksaan _match_kw("OUTER") setelah parser menemukan keyword LEFT. Pemeriksaan ini bersifat opsional sehingga parser tetap dapat menerima LEFT JOIN maupun LEFT OUTER JOIN.

Alternatif yang dipertimbangkan adalah membuat percabangan terpisah untuk LEFT JOIN dan LEFT OUTER JOIN. Namun, pendekatan tersebut tidak dipilih karena kedua bentuk memiliki hasil AST yang sama, yaitu jenis JOIN LEFT. Pemeriksaan keyword opsional lebih sederhana dan sesuai dengan grammar yang digunakan.

**Test regresi.** Nama test di `tests/test_tambahan.py` adalah test_left_outer_join, Test memastikan bahwa query dengan LEFT OUTER JOIN dapat diparse tanpa menghasilkan syntax error dan menghasilkan jenis JOIN LEFT.

**Peran AI.** AI membantu menemukan ketidaksesuaian antara aturan grammar JOIN dalam spesifikasi dengan implementasi fungsi _join(). Perbaikan diverifikasi dengan menguji dua bentuk query, yaitu LEFT JOIN dan LEFT OUTER JOIN, untuk memastikan keduanya dapat diparse dan menghasilkan jenis JOIN yang sesuai.
---

## Bug 12: Resolver Mengalami Error pada INSERT INTO ... SELECT

**Ditemukan oleh:** Sahla Fadhilah Rahim · **Diperbaiki oleh:** Sahla Fadhilah Rahim

**Gejala.** 
Ketika resolver menerima statement SQL INSERT INTO ... SELECT, program menghasilkan TypeError: 'NoneType' object is not iterable.

Hal ini terjadi karena statement INSERT memiliki dua bentuk pengisian data, yaitu menggunakan VALUES atau menggunakan query SELECT. Pada bentuk INSERT INTO ... SELECT, atribut values bernilai None, sedangkan query SELECT disimpan pada atribut query.

Hasil resolver lama: resolver tetap mencoba melakukan iterasi terhadap ins.values, meskipun nilainya None. Akibatnya, proses resolusi berhenti dan menghasilkan TypeError.

Hasil yang diharapkan: resolver dapat memproses kedua bentuk INSERT, baik menggunakan VALUES maupun SELECT, tanpa menghasilkan error.

**Reproduksi minimal.** 

```
INSERT INTO arsip_pesanan (id, total)
SELECT p.id, p.total
FROM pesanan p
WHERE p.tanggal < :batas;
```
**Akar masalah.** Pada implementasi sebelumnya, fungsi _insert() di dalam resolver langsung melakukan iterasi terhadap ins.values tanpa memeriksa apakah atribut tersebut memiliki nilai. Konsep ini berkaitan dengan Bab 5 Representing Code, yang membahas representasi sintaks program dalam bentuk Abstract Syntax Tree (AST). Setiap jenis node AST dapat memiliki struktur dan atribut yang berbeda sesuai bentuk sintaksnya. Oleh karena itu, proses penelusuran AST harus memperhatikan atribut yang benar-benar tersedia pada node tersebut. Pada kasus ini, resolver perlu membedakan atribut values dan query karena keduanya merepresentasikan bentuk INSERT yang berbeda.

Implementasi tersebut hanya dapat menangani INSERT yang menggunakan VALUES. Ketika menerima INSERT yang menggunakan SELECT, resolver tetap menjalankan proses iterasi terhadap atribut values yang bernilai None.

Akibatnya, resolver tidak dapat menangani seluruh bentuk statement INSERT yang didukung oleh parser.

**Perbaikan.** 
File dan fungsi yang diubah: crud/resolver.py, pada fungsi _insert().

Perbaikan dilakukan dengan menambahkan pemeriksaan if ins.values is not None sebelum melakukan iterasi terhadap nilai INSERT. Setelah itu, pemeriksaan terhadap ins.query tetap dilakukan untuk memproses query SELECT apabila tersedia.

Dengan demikian, resolver dapat membedakan proses resolusi INSERT VALUES dan INSERT SELECT.

**Test regresi.** Nama test di tests/test_tambahan.py adalah test_insert_select_dapat_diresolusi.

Test memastikan bahwa query INSERT INTO ... SELECT dapat diparse dan diresolusi tanpa menghasilkan diagnostic dengan level error.

**Peran AI.** AI membantu mengidentifikasi penyebab TypeError dengan menelusuri struktur AST hasil parsing dan proses resolusi pada fungsi _insert(). AI juga membantu menentukan bahwa atribut values perlu diperiksa sebelum dilakukan iterasi. Perbaikan diverifikasi melalui pengujian INSERT SELECT untuk memastikan proses resolusi berjalan tanpa error.
---

## Bug 13: Analyzer Mengalami Error pada INSERT INTO ... SELECT

**Ditemukan oleh:** Sahla Fadhilah Rahim · **Diperbaiki oleh:** Sahla Fadhilah Rahim

**Gejala.** 
Setelah perbaikan pada resolver, proses analisis CRUD masih menghasilkan TypeError: 'NoneType' object is not iterable ketika menerima statement INSERT INTO ... SELECT.

Hasil analyzer lama: analyzer tetap melakukan iterasi terhadap stmt.values, padahal pada bentuk INSERT SELECT atribut tersebut bernilai None. Akibatnya, proses analisis CRUD mengalami error.

Hasil yang diharapkan: analyzer dapat mengenali INSERT SELECT dengan memberikan operasi Create (C) kepada tabel tujuan INSERT dan Read (R) kepada tabel yang digunakan dalam query SELECT.

**Reproduksi minimal.** 

```
INSERT INTO arsip_pesanan (id, total)
SELECT id, total
FROM pesanan;
```
**Akar masalah.** Pada implementasi sebelumnya, fungsi analyze_statement() di dalam crud/analyzer.py hanya menangani proses analisis INSERT menggunakan atribut stmt.values. Konsep ini berkaitan dengan Bab 5 Representing Code, khususnya pola Visitor untuk mengunjungi dan memproses node-node dalam AST. Setiap node memiliki struktur yang berbeda sehingga proses penelusuran harus disesuaikan dengan jenis node yang sedang diproses. Pada kasus ini, analyzer perlu menangani atribut values dan query secara terpisah agar kedua bentuk INSERT dapat dianalisis tanpa melakukan iterasi terhadap nilai None.

Selain itu, implementasi sebelumnya menggunakan pemanggilan fungsi _collect_expr(), padahal fungsi tersebut tidak tersedia pada analyzer. Fungsi yang sudah digunakan untuk menelusuri ekspresi dan subquery adalah _collect().

Akibatnya, analyzer belum dapat menangani INSERT SELECT dengan benar.

**Perbaikan.** 
File dan fungsi yang diubah: crud/analyzer.py, pada fungsi analyze_statement().

Perbaikan dilakukan dengan menambahkan pemeriksaan stmt.values is not None sebelum melakukan iterasi terhadap nilai INSERT. Selanjutnya, ditambahkan pemeriksaan stmt.query is not None untuk memproses query SELECT menggunakan fungsi _collect_select().

Operasi CRUD yang diberikan adalah C untuk tabel tujuan INSERT dan R untuk tabel sumber yang digunakan dalam query SELECT.

**Test regresi.** Nama test di tests/test_tambahan.py adalah test_insert_select_crud.

Test memastikan bahwa query INSERT SELECT menghasilkan pemetaan operasi CRUD yang sesuai

**Peran AI.** AI membantu menyesuaikan pemanggilan fungsi penelusuran ekspresi dengan fungsi _collect() yang sudah tersedia. Perbaikan diverifikasi melalui pengujian hasil analisis CRUD pada INSERT SELECT.
---

## Bug 14: Operasi UPDATE Merambat ke Tabel di dalam Subquery

**Ditemukan oleh:** Sahla Fadhilah Rahim · **Diperbaiki oleh:** Sahla Fadhilah Rahim

**Gejala.** 
Ketika analyzer memproses statement UPDATE yang memiliki subquery pada bagian WHERE, analyzer memberikan operasi Update (U) kepada tabel yang digunakan di dalam subquery.

Padahal, tabel tersebut hanya digunakan untuk membaca data dan seharusnya mendapatkan operasi Read (R).

Hasil analyzer lama: tabel pesanan mendapatkan operasi RUD, padahal tabel tersebut hanya digunakan dalam SELECT dan DELETE. Operasi U muncul karena analyzer ikut meneruskan operasi UPDATE ke tabel yang terdapat di dalam subquery.

Hasil yang diharapkan: tabel tujuan UPDATE mendapatkan operasi U, sedangkan tabel yang digunakan di dalam subquery hanya mendapatkan operasi R.

**Reproduksi minimal.** 

```
UPDATE pelanggan SET level = 'gold'
WHERE id IN (
    SELECT pelanggan_id
    FROM pesanan
    WHERE total > 1000000
);
```
**Akar masalah.** Pada implementasi sebelumnya, fungsi analyze_statement() di dalam crud/analyzer.py meneruskan parameter operasi "U" ketika memanggil fungsi _collect() untuk menelusuri nilai assignment dan kondisi WHERE pada statement UPDATE. Konsep ini berkaitan dengan Bab 5 Representing Code, khususnya pola Visitor dalam proses penelusuran AST. Ketika mengunjungi node, proses analisis perlu memperhatikan jenis node dan konteks penggunaannya agar informasi yang diteruskan ke node berikutnya tidak keliru. Pada kasus ini, operasi UPDATE hanya berlaku untuk tabel tujuan, sedangkan tabel yang ditemukan melalui subquery harus dianalisis sebagai operasi READ. Dengan demikian, setiap bagian AST perlu diproses berdasarkan peran dan konteksnya.

Sementara itu, fungsi _collect() bertugas menelusuri berbagai ekspresi, termasuk subquery yang terdapat di dalamnya. Ketika menemukan subquery, fungsi tersebut meneruskan parameter operasi yang diterima kepada fungsi _collect_select().

Akibatnya, operasi "U" ikut diberikan kepada tabel yang berada di dalam subquery, meskipun tabel tersebut hanya digunakan untuk membaca data.

**Perbaikan.** 
File dan fungsi yang diubah: crud/analyzer.py, pada fungsi analyze_statement().

Perbaikan dilakukan dengan mengubah parameter operasi pada pemanggilan _collect() dari "U" menjadi "R" untuk ekspresi assignment dan kondisi WHERE.

Operasi "U" tetap diberikan secara langsung kepada tabel tujuan UPDATE melalui usage[stmt.table.name].add("U").

Dengan demikian, tabel tujuan tetap mendapatkan operasi Update, sedangkan tabel yang digunakan dalam subquery hanya mendapatkan operasi Read.

**Test regresi.** Pengujian untuk kasus ini sebenarnya sudah tersedia pada tests/test_analyzer.py, yaitu test_matrix_laporan_penjualan.

Test tersebut memastikan bahwa hasil analisis CRUD dari file laporan_penjualan.sql sesuai dengan matriks yang diharapkan.

Test memastikan bahwa query INSERT SELECT menghasilkan pemetaan operasi CRUD yang sesuai

**Peran AI.** AI membantu menelusuri alur analisis CRUD dari fungsi analyze_statement() hingga fungsi _collect() dan _collect_select(). Dari proses tersebut ditemukan bahwa parameter operasi "U" diteruskan ke subquery yang seharusnya hanya dibaca. AI membantu menentukan perubahan parameter operasi menjadi "R" serta memverifikasi hasilnya menggunakan pengujian matriks CRUD yang sudah tersedia.
---


