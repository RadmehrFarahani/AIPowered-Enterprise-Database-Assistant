from sqlalchemy import text

from connection import engine


with engine.connect() as connection:

    result = connection.execute(
        text("SELECT COUNT(*) FROM products")
    )

    count = result.scalar()

    print(
        f"Number of products: {count}"
    )