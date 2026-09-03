import sqlite3
from pathlib import Path


def load_demo_products(limit: int = 24, db_path: str | None = None) -> list[dict]:
    """Load product catalogue rows for the tracked retail demo."""
    path = db_path or str(project_root() / "data" / "retailDB.sqlite")
    query = """
        SELECT
            i.product_id,
            i.modified_product_name AS product_name,
            b.modified_brand AS brand,
            f.modified_sale_price AS price,
            f.modified_discount AS discount,
            f.modified_revenue AS revenue
        FROM clean_info i
        JOIN clean_brands b ON i.product_id = b.product_id
        JOIN clean_finance f ON i.product_id = f.product_id
        WHERE i.modified_product_name IS NOT NULL
          AND b.modified_brand IS NOT NULL
          AND f.modified_sale_price IS NOT NULL
          AND f.modified_revenue IS NOT NULL
        ORDER BY f.modified_revenue DESC
        LIMIT ?
    """
    with sqlite3.connect(path) as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute(query, (limit,)).fetchall()

    products = []
    for row in rows:
        products.append({
            "item_id": row["product_id"],
            "item_name": row["product_name"],
            "item_brand": row["brand"],
            "item_category": "Footwear",
            "price": round(float(row["price"] or 0), 2),
            "discount": round(float(row["discount"] or 0), 4),
            "currency": "GBP",
            "revenue": round(float(row["revenue"] or 0), 2),
        })
    return products

def project_root() -> Path:
    return Path(__file__).resolve().parents[2]
