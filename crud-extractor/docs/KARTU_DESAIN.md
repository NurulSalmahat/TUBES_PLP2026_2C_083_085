# Kartu Desain

Tuliskan lima keputusan desain penting dalam pekerjaan kalian. Untuk tiap keputusan, sebutkan
alternatif yang ditolak dan alasannya. Contoh topik (boleh memilih yang lain):

- bagaimana parser membedakan `*` sebagai "semua kolom" dan sebagai perkalian;
- di mana dan bagaimana presedensi `AND`/`OR` dinyatakan;
- mengapa error recovery berhenti di `;`, bukan di keyword `SELECT` berikutnya;
- urutan pencarian scope dan akibatnya pada shadowing serta correlated subquery;
- mengapa kolom tanpa qualifier hanya dilihat di scope terdalam, dan apa kelemahannya;
- bagaimana implementasi `INSERT ... SELECT` atau komentar blok kalian.

| No | Keputusan | Alternatif yang ditolak | Alasan |
| --- | --- | --- | --- |
| 1 | memisahkan penanganan komentar blok ke dalam fungsi khusus _block_comment() | menuliskan seluruh logika pembacaan komentar blok langsung di dalam _scan_token() | agar setiap fungsi memiliki satu tanggung jawab. jadi _scan_token() hanya fokus mengenali jenis token, sedangkan _block_comment() menangani pembacaan komentar sampai menemukan penutupnya saja. |
| 2 | melakukan normalisasi keyword menggunakan upper(), tetapi tetap mempertahankan penulisan identifier asli | mengubah seluruh teks yang ditemukan menjadi huruf besar | Keyword SQL harus dikenali tanpa membedakan huruf besar dan kecil, tetapi identifier harus tetap mempertahankan penulisan aslinya. jadi, keyword tidak mengubah nama tabel atau kolom yang sudah di deklarasikan. |
| 3 | melakukan pencarian alias mulai dari scope yg paling dalam kemudian kembali ke scope parent | melakukan pencarian dari scope paling luar (reversed) | pencarian yg paling dalam memungkinkan alias pada subquery mengesampingkan alias dengan nama yang sama pada query luar. |
| 4 | | | |
| 5 | | | |
