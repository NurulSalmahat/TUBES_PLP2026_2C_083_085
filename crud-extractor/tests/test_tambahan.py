"""Test tambahan buatan kelompok.

Isi dengan:
1. Satu test regresi untuk setiap bug yang kalian perbaiki (gagal sebelum perbaikan,
   lulus sesudahnya). Beri nama yang menjelaskan bug-nya.
2. Lima test kasus tepi, masing-masing dengan komentar singkat mengapa kasus itu berisiko.
"""
from crud import ast_nodes as ast
from crud.parser import parse_sql
from crud.analyzer import analyze_statement

# ==========================================
# 1. TEST REGRESI UNTUK BUG YANG DIPERBAIKI
# ==========================================
#Menguji bug TO-DO 1 yang sebelumnya gagal di parse
"""Diperbaiki oleh:** Sahla Fadhilah Rahim"""
def test_regresi_insert_select():
    script = parse_sql("INSERT INTO arsip_pesanan (id, total) SELECT id, total FROM pesanan WHERE tanggal < :batas;")
    assert script.errors == []
    s = script.statements[0]
    assert isinstance(s, ast.Insert)
    assert s.query is not None
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