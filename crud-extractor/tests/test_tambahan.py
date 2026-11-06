"""Test tambahan buatan kelompok.

Isi dengan:
1. Satu test regresi untuk setiap bug yang kalian perbaiki (gagal sebelum perbaikan,
   lulus sesudahnya). Beri nama yang menjelaskan bug-nya.
2. Lima test kasus tepi, masing-masing dengan komentar singkat mengapa kasus itu berisiko.
"""

from crud.lexer import tokenize, TokenType
from crud.parser import parse_sql
from crud.resolver import Resolver
from crud.ast_nodes import iter_nodes, ColumnRef

def test_keyword_case_insensitive():
    tokens = tokenize("select Select SELECT")

    keywords = [
        token for token in tokens
        if token.type == TokenType.KEYWORD
    ]

    assert len(keywords) == 3
    assert all(token.value == "SELECT" for token in keywords)

def test_identifier_yang_diawali_keyword():
    tokens = tokenize("selection fromage")

    identifiers = [
        token for token in tokens
        if token.type == TokenType.IDENT
    ]

    assert [token.value for token in identifiers] == [
        "selection", "fromage"
    ]

def test_block_comment_multiline():
    tokens = tokenize("SELECT /* komentar\nbaris kedua */ nama FROM pelanggan")

    values = [token.value for token in tokens]

    assert "SELECT" in values
    assert "nama" in values
    assert "pelanggan" in values
    assert "komentar" not in values

def test_block_comment_tidak_ditutup():
    from crud.lexer import LexError

    try:
        tokenize("SELECT /* komentar")
        assert False, "Seharusnya menghasilkan LexError"
    except LexError:
        pass

def test_string_doubled_quote():
    tokens = tokenize("'O''Brien'")

    assert tokens[0].type == TokenType.STRING
    assert tokens[0].value == "O'Brien"

def test_operator_not_equal_angle_bracket():
    tokens = tokenize("<>")

    assert tokens[0].type == TokenType.OP
    assert tokens[0].value == "<>"

def test_operator_less_than_variants():
    tokens = tokenize("< <= <>")

    operators = [
        token.value
        for token in tokens
        if token.type == TokenType.OP
    ]

    assert operators == ["<", "<=", "<>"]

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