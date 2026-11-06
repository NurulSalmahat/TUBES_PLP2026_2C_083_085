"""Test tambahan buatan kelompok.

Isi dengan:
1. Satu test regresi untuk setiap bug yang kalian perbaiki (gagal sebelum perbaikan,
   lulus sesudahnya). Beri nama yang menjelaskan bug-nya.
2. Lima test kasus tepi, masing-masing dengan komentar singkat mengapa kasus itu berisiko.
"""
from crud import ast_nodes as ast
from crud.lexer import tokenize, TokenType
from crud.parser import parse_sql
from crud.analyzer import analyze_statement
from crud.resolver import Resolver
from crud.ast_nodes import iter_nodes, ColumnRef
from crud.ast_nodes import BinaryOp
from crud.analyzer import analyze_statement

# ==========================================
# TEST REGRESI UNTUK BUG YANG DIPERBAIKI
# ==========================================

# Diperbaiki oleh: Nurul Salmahat

# 1. Menguji keyword yang tidak membedakan huruf besar dan kecil
# Alasan: keyword SQL harus tetap dikenali meskipun ditulis menggunakan huruf kecil, huruf besar, atau kombinasi keduanya.
def test_keyword_case_insensitive():
    tokens = tokenize("select Select SELECT")

    keywords = [
        token for token in tokens
        if token.type == TokenType.KEYWORD
    ]

    assert len(keywords) == 3
    assert all(token.value == "SELECT" for token in keywords)

# 2. Menguji identifier yang diawali dengan keyword
# Alasan: kata seperti selection atau fromage tidak boleh dianggap sebagai keyword hanya karena diawali dengan kata SELECT atau FROM.
# Pengujian ini memastikan lexer mengenali keseluruhan kata sebagai identifier apabila kata tersebut bukan keyword yang terdaftar.
def test_identifier_yang_diawali_keyword():
    tokens = tokenize("selection fromage")

    identifiers = [
        token for token in tokens
        if token.type == TokenType.IDENT
    ]

    assert [token.value for token in identifiers] == [
        "selection", "fromage"
    ]

# 3. Menguji komentar blok multiline
# Alasan: sebelumnya lexer belum menangani komentar blok /* ... */.
# Pengujian ini memastikan lexer dapat melewati komentar yang terdiri dari beberapa baris tanpa menganggap isinya sebagai token SQL.
def test_block_comment_multiline():
    tokens = tokenize("SELECT /* komentar\nbaris kedua */ nama FROM pelanggan")

    values = [token.value for token in tokens]

    assert "SELECT" in values
    assert "nama" in values
    assert "pelanggan" in values
    assert "komentar" not in values

# 4. Menguji komentar blok yang tidak ditutup
# Alasan: komentar blok harus memiliki penutup */.
# Pengujian ini memastikan lexer menghasilkan LexError ketika menemukan komentar blok yang tidak memiliki penutup.
def test_block_comment_tidak_ditutup():
    from crud.lexer import LexError

    try:
        tokenize("SELECT /* komentar")
        assert False, "Seharusnya menghasilkan LexError"
    except LexError:
        pass

# 5. Menguji string dengan tanda petik tunggal berulang
# Alasan: dalam SQL, tanda petik tunggal yang ditulis dua kali ('')
def test_string_doubled_quote():
    tokens = tokenize("'O''Brien'")

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "O'Brien"

# 6. Menguji operator tidak sama dengan <>
# Alasan: operator <> merupakan salah satu bentuk operator perbandingan
# yang harus dikenali lexer sebagai satu token, bukan dua token terpisah.
def test_operator_not_equal_angle_bracket():
    tokens = tokenize("<>")

    assert tokens[0].type == TokenType.OP
    assert tokens[0].value == "<>"

# 7. Menguji variasi operator yang diawali tanda <
# Alasan: lexer harus dapat membedakan operator <, <=, dan <>.
def test_operator_less_than_variants():
    tokens = tokenize("< <= <>")

    operators = [
        token.value
        for token in tokens
        if token.type == TokenType.OP
    ]

    assert operators == ["<", "<=", "<>"]

# 8. Menguji resolusi kolom tanpa qualifier pada satu tabel
# Alasan: ketika hanya terdapat satu tabel dalam scope, kolom yang
# tidak menggunakan qualifier dapat langsung dihubungkan dengan tabel tersebut.
def test_kolom_tanpa_qualifier_satu_tabel():
    sql = """
    SELECT nama
    FROM pelanggan
    WHERE aktif = 1
    """

    script = parse_sql(sql)
    assert script.errors == []

    resolver = Resolver()
    diagnostics = resolver.resolve_script(script)

    columns = [
        node for node in iter_nodes(script)
        if isinstance(node, ColumnRef)
    ]

    assert len(columns) == 2
    assert all(col.resolved == "pelanggan" for col in columns)
    assert diagnostics == []

# 9. Menguji kolom tanpa qualifier pada beberapa tabel
# Alasan: ketika terdapat lebih dari satu tabel dalam scope, resolver tidak dapat memastikan asal kolom tanpa informasi skema.
def test_kolom_ambigu_tanpa_qualifier():
    sql = """
    SELECT nama
    FROM pelanggan p
    JOIN pesanan ps ON p.id = ps.id
    """

    script = parse_sql(sql)
    assert script.errors == []

    resolver = Resolver()
    diagnostics = resolver.resolve_script(script)

    columns = [
        node for node in iter_nodes(script)
        if isinstance(node, ColumnRef)
    ]

    nama = [col for col in columns if col.name == "nama"]

    assert len(nama) == 1
    assert nama[0].resolved is None
    assert any(
        d.level == "warning"
        and d.message == "kolom 'nama' ambigu tanpa skema"
        for d in diagnostics
    )

# 10. Menguji penggunaan alias yang sama pada scope berbeda
# Alasan: alias pada subquery dapat menggunakan nama yang sama dengan alias pada query luar. 
# Resolver harus mengutamakan alias pada scope terdalam sebelum mencari alias pada scope induk.
def test_shadowing_alias_di_subquery():
    sql = """
    SELECT p.nama
    FROM pelanggan p
    WHERE EXISTS (
        SELECT p.id
        FROM pesanan p
    )
    """

    script = parse_sql(sql)
    assert script.errors == []

    resolver = Resolver()
    resolver.resolve_script(script)

    columns = [
        node for node in iter_nodes(script)
        if isinstance(node, ColumnRef)
    ]

    inner_p = [
        col for col in columns
        if col.name == "id" and col.qualifier == "p"
    ]

    assert len(inner_p) == 1
    assert inner_p[0].resolved == "pesanan"

# 11. Menguji agar scope DELETE tidak bocor ke statement berikutnya
# Alasan: scope yang dibuat untuk statement DELETE harus ditutup setelah proses resolusi selesai.
def test_delete_tidak_membocorkan_scope():
    sql = """
    DELETE FROM sesi s WHERE s.id = 1;

    SELECT s.id FROM pengguna u;
    """

    script = parse_sql(sql)
    assert script.errors == []

    resolver = Resolver()
    diagnostics = resolver.resolve_script(script)

    assert any(
        d.level == "error"
        and d.message == "alias 's' tidak terdefinisi"
        for d in diagnostics
    )

# ==========================================
# TEST REGRESI UNTUK BUG YANG DIPERBAIKI
# ==========================================
# Diperbaiki oleh: Sahla Fadhilah Rahim
# 1. Menguji bug TO-DO 1 yang sebelumnya gagal di parse
def test_regresi_insert_select():
    script = parse_sql("INSERT INTO arsip_pesanan (id, total) SELECT id, total FROM pesanan WHERE tanggal < :batas;")
    assert script.errors == []
    s = script.statements[0]
    assert isinstance(s, ast.Insert)
    assert s.query is not None

# 2. Menguji Presedensi Operator AND Lebih Tinggi daripada OR
# Alasan: Operator AND harus memiliki tingkat presedensi yang lebih tinggi dibandingkan operator OR dalam ekspresi SQL 
# sesuai dengan spesifikasi.
def test_presedensi_and_or():
    sql = """
    SELECT * FROM mahasiswa
    WHERE a = 1 OR b = 2 AND c = 3;
    """

    hasil = parse_sql(sql)

    assert len(hasil.errors) == 0
    assert len(hasil.statements) == 1

    kondisi = hasil.statements[0].where

    # Bagian paling luar harus OR
    assert isinstance(kondisi, BinaryOp)
    assert kondisi.op == "OR"

    # Bagian kanan OR harus AND
    assert isinstance(kondisi.right, BinaryOp)
    assert kondisi.right.op == "AND"

# 3. Menguji Pemulihan Parser Setelah Terjadi Syntax Error
# Alasan: Ketika terjadi kesalahan sintaks pada suatu statement, parser harus mampu melakukan pemulihan dengan melewati 
# token hingga menemukan tanda titik koma (;). Hal ini bertujuan agar kesalahan pada satu statement tidak menghentikan 
# proses parsing statement berikutnya.
def test_error_recovery():
    sql = """
    SELECT FROM mahasiswa;
    SELECT * FROM dosen;
    """

    hasil = parse_sql(sql)

    # Statement pertama harus menghasilkan satu error
    assert len(hasil.errors) == 1

    # Statement kedua tetap berhasil diparse
    assert len(hasil.statements) == 1
    assert hasil.statements[0].sources[0].name == "dosen"

# 4. Menguji Parsing LEFT OUTER JOIN
# Alasan: Parser harus mampu mengenali sintaks LEFT OUTER JOIN sebagai bentuk dari LEFT JOIN. Hal ini bertujuan agar 
# penggunaan kata kunci OUTER yang bersifat opsional tidak menyebabkan kesalahan parsing pada query SQL yang valid.
def test_left_outer_join():
    sql = """
    SELECT * FROM mahasiswa
    LEFT OUTER JOIN dosen
    ON mahasiswa.id_dosen = dosen.id;
    """

    hasil = parse_sql(sql)

    assert len(hasil.errors) == 0
    assert len(hasil.statements) == 1

    statement = hasil.statements[0]

    assert len(statement.joins) == 1
    assert statement.joins[0].kind == "LEFT"

# 5. Menguji Resolusi INSERT INTO ... SELECT
# Alasan: memastikan resolver dapat menangani statement INSERT yang menggunakan SELECT sebagai sumber data
def test_insert_select_dapat_diresolusi():
    sql = """
    INSERT INTO arsip_pesanan (id, total)
    SELECT p.id, p.total
    FROM pesanan p
    WHERE p.tanggal < :batas;
    """

    script = parse_sql(sql)

    assert len(script.errors) == 0
    assert len(script.statements) == 1

    diagnostics = Resolver().resolve_script(script)

    assert not [d for d in diagnostics if d.level == "error"]

# 6. Menguji Analisis CRUD pada INSERT INTO ... SELECT
# Alasan: Pengujian ini dilakukan untuk memastikan analyzer dapat menentukan operasi CRUD dengan benar pada
# statement INSERT yang menggunakan SELECT. Tabel tujuan INSERT harus mendapatkan operasi Create (C), sedangkan 
# tabel yang menjadi sumber data pada query SELECT harus mendapatkan operasi Read (R). Pengujian ini juga 
# memastikan analyzer tidak mengalami error ketika atribut values bernilai None.
def test_insert_select_crud():
    sql = """
    INSERT INTO arsip_pesanan (id, total)
    SELECT id, total
    FROM pesanan;
    """

    script = parse_sql(sql)

    assert len(script.errors) == 0
    assert len(script.statements) == 1

    hasil = analyze_statement(script.statements[0])

    assert hasil == {
        "arsip_pesanan": {"C"},
        "pesanan": {"R"}
    }
    
# ==========================================
# 2. LIMA TEST KASUS TEPI (EDGE CASES)
# ==========================================
"""Dibuat oleh:** Sahla Fadhilah Rahim"""
# 1. Menguji klausa GROUP BY
# Alasan: rawan gagal jika struktur pengelompokan data pada kolom atau ekspresi kompleks 
# tidak dipetakan dengan benar oleh parser
def test_edge_group_by():
    script = parse_sql("SELECT status, COUNT(*) FROM pesanan GROUP BY status;")
    assert script.errors == []
    s = script.statements[0]
    assert isinstance(s, ast.Select)
    assert len(s.group_by) == 1

# 2. Menguji penggunaan DISTINCT untuk menyaring data duplikat
# Alasan: jika bendera penanda keunikan terlewat di struktur AST data kembar bisa gagal disaring
def test_edge_distinct():
    script = parse_sql("SELECT DISTINCT kategori FROM produk;")
    assert script.errors == []
    s = script.statements[0]
    assert s.distinct is True

# 3. Menguji alias tabel tanpa keyword AS (misal 'pelanggan p')
# Alasan: sangat krusial bagi resolver agar operasi CRUD pada tabel ber-alias tetap terdeteksi dengan akurat.
def test_edge_alias_tanpa_as():
    script = parse_sql("SELECT p.nama FROM pelanggan p WHERE p.id = 1;")
    assert script.errors == []
    s = script.statements[0]
    assert isinstance(s,ast.Select)

# 4. Menguji klausa WHERE IN dengan daftar nilai angka
# Alasan: rentan membuat parser bingung membedakan antara subquery dengan deretan data konstan di dalam kurung.
def test_edge_in_literal_list():
    script = parse_sql("SELECT nama FROM pelanggan WHERE id IN (1, 2, 3);")
    assert script.errors == []
    s = script.statements[0]
    assert s.where is not None

# 5. Menguji pengelompokan kondisi logika dengan tanda kurung (AND / OR)
# Alasan: berisiko tinggi pada urutan prioritas operator logika jika tanda kurung di dalam WHERE diabaikan.
def test_edge_nested_logic_brackets():
    script = parse_sql("SELECT * FROM pesanan WHERE (status = 'LUNAS' OR status = 'PROSES') AND total > 100000;")
    assert script.errors == []
    s = script.statements[0]
    assert s.where is not None
