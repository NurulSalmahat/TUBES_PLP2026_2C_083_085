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

```/* komentar\n   dua baris */ SELECT
```

**Akar masalah.** fungsi _scan_token() sebelumnya hanya menangani komentar satu baris yang diawali --. penanganan komentar blok masih berupa TODO sehingga lexer tidak memiliki proses untuk membaca isi komentar sampai menemukan penutup */. 

**Perbaikan.** perlu adanya fungsi baru yang membaca karakter sampai menemukan */. fungsi _scan_token() mendeteksi pembuka /* kemudian memanggil _block_comment() untuk membaca karakter sampai menemukan penutup */. jika komentar tidak ditutup sampai akhir input, fungsi akan menghasilkan LexError.

**Test regresi.** test_block_comment_multiline dan test_block_comment_tidak_ditutup

**Peran AI.** AI membantu menjelaskan alur pendeteksian komentar blok dan memberikan usulan implementasi _block_comment(). kode diverifikasi dengan menjalankan pytest.

## Bug 2: menormalisasikan keyword menjadi uppercase

**Ditemukan oleh:** Nurul Salmahat · **Diperbaiki oleh:** Nurul Salmahat

**Gejala.** ketika di test pertama kali, test_keyword_huruf_kecil mengembalikan error karena keyword yang ditulis menggunakan huruf kecil seperti select, maka dikenali sebagai IDENT, bukan KEYWORD. padahal menurut SPESIFIKASI.md bagian 2.2, keyword tidak peka terhadap huruf besar dan kecil dan nilai token keyword selalu uppercase.

**Reproduksi minimal.** 

```select id from t
```

**Akar masalah.** kode lama pada fungsi _word() itu membandingkan kata secara langsung dengan KEYWORDS. Maka select di test_keyword_huruf_kecil itu tidak cocok dengan SELECT.

**Perbaikan.** Mengubah teks sementara menjadi uppercase menggunakan text.upper() untuk pemeriksaan terhadap KEYWORDS. Jika termasuk keyword, nilai token disimpan dalam uppercase. Jika bukan keyword, teks asli tetap disimpan sebagai IDENT.

**Test regresi.** test_keyword_case_insensitive dan test_identifier_yang_diawali_keyword

**Peran AI.** AI membantu menjelaskan normalisasi keyword dan pentingnya membedakan keyword dengan identifier. hasil diverifikasi melalui pengujian token.

## Bug 3: doubled quote tidak terbaca sebagai satu string

**Ditemukan oleh:** Nurul Salmahat · **Diperbaiki oleh:** Nurul Salmahat

**Gejala.** string yang mengandung dua kutip tunggal berturut-turut dipotong pada kutip pertama. Hal ini belum sesuai dengan SPESIFIKASI.md bagian 2.4 menyatakan bahwa dua kutip berturut-turut di dalam string mewakili satu karakter kutip.

**Reproduksi minimal.** 

```
'O''Brien'
```

**Akar masalah.** fungsi _string() langsung menganggap setiap kutip tunggal sebagai penutup string tanpa memeriksa apakah terdapat kutip tunggal kedua setelahnya.

**Perbaikan.** mengubah _string() agar memeriksa karakter berikutnya ketika menemukan kutip tunggal. Jika karakter berikutnya juga kutip tunggal, kedua kutip dikonsumsi dan satu karakter kutip ditambahkan ke nilai string. Jika tidak, kutip dianggap sebagai penutup string.

**Test regresi.** test_string_doubled_quote()

**Peran AI.** AI AI membantu mengidentifikasi penyebab string terpotong dan menjelaskan perbedaan kutip di dalam string dengan kutip penutup. Perbaikan diverifikasi melalui pytest.

## Bug 4: operator <> tidak dikenali sebagai satu token

**Ditemukan oleh:** Nurul Salmahat · **Diperbaiki oleh:** Nurul Salmahat

**Gejala.** operator <> ternyata dibaca menjadi dua token < dan >, padahal SPESIFIKASI.md bagian 2.5 mengharuskan <> menjadi satu token OP.

**Reproduksi minimal.** 

```
<>
```

**Akar masalah.** pemindaian operartor < hanya memeriksa kemungkinan operator <=, jadi tidak memeriksa apakah <> memungkinkan.

**Perbaikan.** penambahan percabangan untuk memeriksa karakter > setelah karakter <. jika ditemukan, keduanya akan disimpan sebagai satu token OP dengan nilai <>.

**Test regresi.** test_operator_not_equal_angle_bracket dan test_operator_less_than_variants

**Peran AI.** AI membantu menerangkan adanya kekurangan pemeriksaan operator dan menyusun test regresi. Perbaikan diverifikasi dengan memastikan operator <, <=, dan <> menghasilkan token yang benar.

## Bug 5: TODO kolom tanpa qualifier

**Ditemukan oleh:** Nurul Salmahat · **Diperbaiki oleh:** Nurul Salmahat

**Gejala.** kolom tanpa qualifier, seperti nama, belum memiliki nilai ColumnRef.resolved, padahal SPESIFIKASI.md bagian 4.3 mengatur resolusi kolom tanpa qualifier berdasarkan jumlah tabel pada scope terdalam.

**Reproduksi minimal.** 

```
SELECT nama
FROM pelanggan
WHERE aktif = 1
```

**Akar masalah.** fungsi _column() yang hanya menangani kolom dengan qualifier. bagian untuk kolom tanpa qualifier masih berupa TODO, jadi resolver belum menentukan tabel asal kolom.

**Perbaikan.** mengambil seluruh entri pada scope terdalam. jika hanya ada satu tabel, col.resolved diisi dengan tabel tersebut. jika lebih dari satu tabel, resolver memberikan warning bahwa kolom itu ambigu tanpa skema/tabel. jika tidak ada tabel acuan, resolver memberikan warning.

**Test regresi.** test_kolom_tanpa_qualifier_satu_tabel dan test_kolom_ambigu_tanpa_qualifier

**Peran AI.** AI membantu menjelaskan aturan resolusi kolom dan menyusun test. Perbaikan diverifikasi melalui pytest. Kondisi tanpa tabel tidak diuji melalui SQL karena sebelumnya, grammar sudah mewajibkan SELECT memiliki setidaknya 1 FROM.

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

**Akar masalah.** penggunaan reversed(chain) menyebabkan urutan pencarian tidak sesuai SPESIFIKASI.md

**Perbaikan.** mengganti iterasi reversed(chain) menjadi chain

**Test regresi.** test_shadowing_alias_di_subquery()

**Peran AI.** AI membantu menerangkan pembedahan kode dan alur kerja kode, setelah membaca kode ada reversed nya barulah perlu diganti jadi hanya chain.

## Bug 7: fungsi delete pada resolver belum menyatakan keluar dari scope aktif

**Ditemukan oleh:** Nurul Salmahat · **Diperbaiki oleh:** Nurul Salmahat

**Gejala.** alias dari statement delete bisa terbawa ke statement berikutnya karena ada self.push() tapi tidak ada self.pop(). hal ini melanggar SPESIFIKASI.md bagian 4.5 yang mengharuskan setiap statement berdiri sendiri dan tidak meninggalkan scope.

**Reproduksi minimal.** 

```
DELETE FROM sesi s WHERE s.id = 1;

SELECT s.id FROM pengguna u;
```

**Akar masalah.** fungi delete memanggil push() untuk membuat scope baru, tapi tidak memanggil pop() setelah resolusi selesai. akibatnya, scope delete akan tetap aktif dan alias s akan terlihat oleh statement berikutnya

**Perbaikan.** menambahkan pemanggilan _pop() agar scope delete ditutup setelah resolusi selesai

**Test regresi.** test_delete_tidak_membocorkan_scope()

**Peran AI.** AI membantu mengidentifikasi scope yang tidak ditutup. perbaikan diverifikasi dengan menjalankan test.

---
