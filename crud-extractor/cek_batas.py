
from crud.parser import parse_sql
from crud.resolver import Resolver
from crud.analyzer import analyze_statement


pengujian = [
    {
        "nama": "1. Schema Validation",
        "sql": """
        SELECT nama_tidak_ada
        FROM pelanggan;
        """
    },
    {
        "nama": "2. Column-level CRUD",
        "sql": """
        UPDATE pelanggan
        SET alamat = 'Bandung'
        WHERE id = 10;
        """
    },
    {
        "nama": "3. Trigger Analysis",
        "sql": """
        CREATE TRIGGER update_stok
        AFTER INSERT ON pesanan
        BEGIN
            UPDATE produk SET stok = stok - 1;
        END;
        """
    }
]


for nomor, kasus in enumerate(pengujian, start=1):
    print("\n" + "=" * 55)
    print(kasus["nama"])
    print("=" * 55)

    print("\nSQL:")
    print(kasus["sql"])

    # Tahap parsing
    script = parse_sql(kasus["sql"])

    print("\n=== HASIL PARSING ===")
    print("Errors:", script.errors)
    print("Statements:", script.statements)

    # Jika parsing gagal, lanjut ke pengujian berikutnya
    if script.errors:
        print("\nParsing gagal. Resolving dan analisis CRUD dilewati.")
        continue

    # Tahap resolving
    diagnostics = Resolver().resolve_script(script)

    print("\n=== HASIL RESOLVING ===")
    print(diagnostics)

    # Tahap analisis CRUD
    print("\n=== HASIL ANALISIS CRUD ===")
    for statement in script.statements:
        print(analyze_statement(statement))
