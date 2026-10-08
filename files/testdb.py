import sqlite3


DATABASE_NAME = "novatech.db"


connection = sqlite3.connect(DATABASE_NAME)

cursor = connection.cursor()


# ==========================================
# 1. Count records
# ==========================================

tables = [
    "departments",
    "employees",
    "categories",
    "products",
    "customers",
    "suppliers",
    "sales",
    "sale_items",
    "purchases",
    "purchase_items"
]


print("\n========== DATABASE STATISTICS ==========\n")


for table in tables:

    cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = cursor.fetchone()[0]

    print(f"{table:20} : {count}")


# ==========================================
# 2. Products
# ==========================================

print("\n========== PRODUCTS ==========\n")


cursor.execute("""
SELECT
    p.id,
    p.name,
    p.brand,
    c.name AS category,
    p.price,
    p.stock
FROM products p
JOIN categories c
    ON p.category_id = c.id
LIMIT 10
""")


products = cursor.fetchall()


for product in products:

    print(product)


# ==========================================
# 3. Employees
# ==========================================

print("\n========== EMPLOYEES ==========\n")


cursor.execute("""
SELECT
    e.id,
    e.first_name,
    e.last_name,
    d.name AS department,
    e.position
FROM employees e
JOIN departments d
    ON e.department_id = d.id
LIMIT 10
""")


employees = cursor.fetchall()


for employee in employees:

    print(employee)


# ==========================================
# 4. Top Selling Products
# ==========================================

print("\n========== TOP SELLING PRODUCTS ==========\n")


cursor.execute("""
SELECT
    p.name,
    SUM(si.quantity) AS total_sold
FROM sale_items si

JOIN products p
    ON si.product_id = p.id

JOIN sales s
    ON si.sale_id = s.id

WHERE s.status = 'Completed'

GROUP BY p.id

ORDER BY total_sold DESC

LIMIT 10
""")


top_products = cursor.fetchall()


for product in top_products:

    print(product)


# ==========================================
# 5. Top Sales Employees
# ==========================================

print("\n========== TOP SALES EMPLOYEES ==========\n")


cursor.execute("""
SELECT
    e.first_name || ' ' || e.last_name AS employee,
    SUM(s.total_amount) AS total_sales

FROM sales s

JOIN employees e
    ON s.employee_id = e.id

WHERE s.status = 'Completed'

GROUP BY e.id

ORDER BY total_sales DESC

LIMIT 10
""")


top_employees = cursor.fetchall()


for employee in top_employees:

    print(employee)


# ==========================================
# 6. Low Stock Products
# ==========================================

print("\n========== LOW STOCK PRODUCTS ==========\n")


cursor.execute("""
SELECT
    name,
    stock,
    minimum_stock
FROM products

WHERE stock < minimum_stock

ORDER BY stock ASC
""")


low_stock = cursor.fetchall()


for product in low_stock:

    print(product)


connection.close()