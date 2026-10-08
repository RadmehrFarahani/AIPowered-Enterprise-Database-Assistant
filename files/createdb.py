import sqlite3
import random
from datetime import date, timedelta


# =========================================================
# Configuration
# =========================================================

DATABASE_NAME = "novatech.db"

random.seed(42)


# =========================================================
# Database Connection
# =========================================================

connection = sqlite3.connect(DATABASE_NAME)

cursor = connection.cursor()

# Enable foreign keys
cursor.execute("PRAGMA foreign_keys = ON")


# =========================================================
# Drop Existing Tables
# =========================================================

cursor.executescript("""
DROP TABLE IF EXISTS purchase_items;
DROP TABLE IF EXISTS purchases;

DROP TABLE IF EXISTS sale_items;
DROP TABLE IF EXISTS sales;

DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS categories;

DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS suppliers;

DROP TABLE IF EXISTS employees;
DROP TABLE IF EXISTS departments;
""")


# =========================================================
# Create Tables
# =========================================================

cursor.executescript("""
CREATE TABLE departments (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    location TEXT NOT NULL
);


CREATE TABLE employees (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    department_id INTEGER NOT NULL,
    position TEXT NOT NULL,
    salary REAL NOT NULL,
    hire_date TEXT NOT NULL,

    FOREIGN KEY (department_id)
        REFERENCES departments(id)
);


CREATE TABLE categories (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);


CREATE TABLE products (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category_id INTEGER NOT NULL,
    brand TEXT NOT NULL,
    price REAL NOT NULL,
    stock INTEGER NOT NULL,
    minimum_stock INTEGER NOT NULL,

    FOREIGN KEY (category_id)
        REFERENCES categories(id)
);


CREATE TABLE customers (
    id INTEGER PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    city TEXT NOT NULL,
    customer_type TEXT NOT NULL
);


CREATE TABLE suppliers (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    phone TEXT NOT NULL,
    email TEXT NOT NULL,
    city TEXT NOT NULL
);


CREATE TABLE sales (
    id INTEGER PRIMARY KEY,
    customer_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    sale_date TEXT NOT NULL,
    status TEXT NOT NULL,
    total_amount REAL NOT NULL,

    FOREIGN KEY (customer_id)
        REFERENCES customers(id),

    FOREIGN KEY (employee_id)
        REFERENCES employees(id)
);


CREATE TABLE sale_items (
    id INTEGER PRIMARY KEY,
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,
    discount REAL NOT NULL,

    FOREIGN KEY (sale_id)
        REFERENCES sales(id),

    FOREIGN KEY (product_id)
        REFERENCES products(id)
);


CREATE TABLE purchases (
    id INTEGER PRIMARY KEY,
    supplier_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    purchase_date TEXT NOT NULL,
    status TEXT NOT NULL,
    total_amount REAL NOT NULL,

    FOREIGN KEY (supplier_id)
        REFERENCES suppliers(id),

    FOREIGN KEY (employee_id)
        REFERENCES employees(id)
);


CREATE TABLE purchase_items (
    id INTEGER PRIMARY KEY,
    purchase_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price REAL NOT NULL,

    FOREIGN KEY (purchase_id)
        REFERENCES purchases(id),

    FOREIGN KEY (product_id)
        REFERENCES products(id)
);
""")


# =========================================================
# Departments
# =========================================================

departments = [
    (1, "IT", "Tehran"),
    (2, "Sales", "Tehran"),
    (3, "Human Resources", "Tehran"),
    (4, "Finance", "Tehran"),
    (5, "Procurement", "Karaj"),
    (6, "Marketing", "Tehran"),
    (7, "Logistics", "Karaj"),
    (8, "Customer Support", "Tehran"),
]

cursor.executemany("""
INSERT INTO departments
(id, name, location)
VALUES (?, ?, ?)
""", departments)


# =========================================================
# Employee Data
# =========================================================

first_names = [
    "Ali", "Sara", "Reza", "Maryam", "Amir",
    "Nima", "Zahra", "Hassan", "Mehdi", "Parisa",
    "Sina", "Mina", "Pouya", "Negar", "Arman",
    "Elham", "Milad", "Shirin", "Omid", "Nazanin"
]

last_names = [
    "Ahmadi", "Mohammadi", "Karimi", "Hosseini",
    "Rahimi", "Ebrahimi", "Moradi", "Akbari",
    "Jafari", "Rostami", "Soleimani", "Ghasemi",
    "Nouri", "Hashemi", "Yousefi"
]

positions = {
    1: [
        "Backend Developer",
        "AI Engineer",
        "Software Engineer",
        "DevOps Engineer",
        "Data Analyst"
    ],

    2: [
        "Sales Manager",
        "Sales Specialist",
        "Account Executive"
    ],

    3: [
        "HR Specialist",
        "Recruiter",
        "HR Manager"
    ],

    4: [
        "Accountant",
        "Financial Analyst",
        "Finance Manager"
    ],

    5: [
        "Procurement Specialist",
        "Purchasing Manager",
        "Procurement Analyst"
    ],

    6: [
        "Marketing Manager",
        "Digital Marketing Specialist",
        "Marketing Specialist"
    ],

    7: [
        "Logistics Coordinator",
        "Warehouse Specialist",
        "Logistics Manager"
    ],

    8: [
        "Support Specialist",
        "Support Manager",
        "Customer Service Agent"
    ]
}


employees = []

for employee_id in range(1, 61):

    department_id = random.randint(1, 8)

    first_name = random.choice(first_names)
    last_name = random.choice(last_names)

    position = random.choice(
        positions[department_id]
    )

    salary = random.randint(25000, 90000)

    hire_date = date(
        random.randint(2019, 2025),
        random.randint(1, 12),
        random.randint(1, 28)
    )

    employees.append((
        employee_id,
        first_name,
        last_name,
        department_id,
        position,
        salary,
        hire_date.isoformat()
    ))


cursor.executemany("""
INSERT INTO employees
(id, first_name, last_name, department_id,
 position, salary, hire_date)

VALUES (?, ?, ?, ?, ?, ?, ?)
""", employees)


# =========================================================
# Categories
# =========================================================

categories = [
    (1, "Laptops"),
    (2, "Smartphones"),
    (3, "Tablets"),
    (4, "Monitors"),
    (5, "Accessories"),
    (6, "Networking"),
    (7, "Storage"),
    (8, "Printers"),
    (9, "Smart Home"),
    (10, "Wearables"),
    (11, "Audio"),
    (12, "Cameras"),
]

cursor.executemany("""
INSERT INTO categories
(id, name)
VALUES (?, ?)
""", categories)


# =========================================================
# Products
# =========================================================

brands = {
    "Laptops": [
        "Apple", "Dell", "Lenovo", "HP", "Asus"
    ],

    "Smartphones": [
        "Apple", "Samsung", "Xiaomi", "Google"
    ],

    "Tablets": [
        "Apple", "Samsung", "Lenovo"
    ],

    "Monitors": [
        "Samsung", "LG", "Dell", "BenQ"
    ],

    "Accessories": [
        "Logitech", "Anker", "UGREEN", "Baseus"
    ],

    "Networking": [
        "TP-Link", "Cisco", "D-Link", "Ubiquiti"
    ],

    "Storage": [
        "Samsung", "Kingston", "SanDisk", "Western Digital"
    ],

    "Printers": [
        "HP", "Canon", "Epson"
    ],

    "Smart Home": [
        "Xiaomi", "TP-Link", "Philips"
    ],

    "Wearables": [
        "Apple", "Samsung", "Garmin"
    ],

    "Audio": [
        "Sony", "JBL", "Anker"
    ],

    "Cameras": [
        "Canon", "Sony", "Nikon"
    ]
}


base_prices = {
    "Laptops": 900,
    "Smartphones": 450,
    "Tablets": 350,
    "Monitors": 180,
    "Accessories": 30,
    "Networking": 70,
    "Storage": 60,
    "Printers": 120,
    "Smart Home": 50,
    "Wearables": 180,
    "Audio": 70,
    "Cameras": 500
}


products = []

product_id = 1

for category_id, category_name in categories:

    for model_number in range(1, 10):

        brand = random.choice(
            brands[category_name]
        )

        name = (
            f"{brand} "
            f"{category_name[:-1] if category_name.endswith('s') else category_name} "
            f"Model {model_number}"
        )

        base_price = base_prices[category_name]

        price = round(
            base_price * random.uniform(0.8, 4),
            2
        )

        stock = random.randint(5, 120)

        minimum_stock = random.randint(5, 20)

        products.append((
            product_id,
            name,
            category_id,
            brand,
            price,
            stock,
            minimum_stock
        ))

        product_id += 1


cursor.executemany("""
INSERT INTO products
(id, name, category_id, brand,
 price, stock, minimum_stock)

VALUES (?, ?, ?, ?, ?, ?, ?)
""", products)


# =========================================================
# Customers
# =========================================================

cities = [
    "Tehran",
    "Karaj",
    "Mashhad",
    "Isfahan",
    "Shiraz",
    "Tabriz",
    "Qom"
]

customer_types = [
    "Individual",
    "Business"
]


customers = []

for customer_id in range(1, 301):

    first_name = random.choice(first_names)

    last_name = random.choice(last_names)

    phone = (
        "09"
        + str(random.randint(100000000, 999999999))
    )

    email = (
        first_name.lower()
        + "."
        + last_name.lower()
        + str(customer_id)
        + "@example.com"
    )

    city = random.choice(cities)

    customer_type = random.choice(
        customer_types
    )

    customers.append((
        customer_id,
        first_name,
        last_name,
        phone,
        email,
        city,
        customer_type
    ))


cursor.executemany("""
INSERT INTO customers
(id, first_name, last_name,
 phone, email, city, customer_type)

VALUES (?, ?, ?, ?, ?, ?, ?)
""", customers)


# =========================================================
# Suppliers
# =========================================================

supplier_names = [
    "Pars Digital Supply",
    "Tehran Tech Distribution",
    "Arya Electronics",
    "Shahin Computer",
    "Farda Technology",
    "Novin Digital",
    "Pars Data Systems",
    "Iran Tech Supply",
    "Mehr Electronics",
    "Smart Distribution",
    "Atlas Computer",
    "Rayan Trading",
    "Shams Technology",
    "Darya Digital",
    "Kian Electronics",
    "Avand Systems",
    "Tosee Digital",
    "Arman Supply",
    "Saba Electronics",
    "Rayaneh Gostar",
    "Negin Technology",
    "Borna Digital",
    "Pardis Electronics",
    "Saman Trading",
    "Aftab Technology",
    "Shahr Computer",
    "Dana Electronics",
    "Kara Digital",
    "Mahan Technology",
    "Setareh Supply"
]


suppliers = []

for supplier_id, supplier_name in enumerate(
    supplier_names,
    start=1
):

    phone = (
        "021"
        + str(random.randint(10000000, 99999999))
    )

    email = (
        "sales"
        + str(supplier_id)
        + "@supplier.example.com"
    )

    city = random.choice([
        "Tehran",
        "Karaj",
        "Mashhad",
        "Isfahan"
    ])

    suppliers.append((
        supplier_id,
        supplier_name,
        phone,
        email,
        city
    ))


cursor.executemany("""
INSERT INTO suppliers
(id, name, phone, email, city)

VALUES (?, ?, ?, ?, ?)
""", suppliers)


# =========================================================
# Sales
# =========================================================

sales = []

start_date = date(2026, 1, 1)

statuses = [
    "Completed",
    "Completed",
    "Completed",
    "Cancelled",
    "Pending"
]


for sale_id in range(1, 801):

    customer_id = random.randint(1, 300)

    # Prefer sales department employees
    sales_employees = [
        employee[0]
        for employee in employees
        if employee[3] == 2
    ]

    employee_id = random.choice(
        sales_employees
    )

    sale_date = (
        start_date
        + timedelta(days=random.randint(0, 280))
    )

    status = random.choice(statuses)

    # temporary total
    total_amount = 0

    sales.append([
        sale_id,
        customer_id,
        employee_id,
        sale_date.isoformat(),
        status,
        total_amount
    ])


# =========================================================
# Sale Items
# =========================================================

sale_items = []

sale_item_id = 1

for sale in sales:

    sale_id = sale[0]

    number_of_items = random.randint(1, 5)

    selected_products = random.sample(
        products,
        number_of_items
    )

    total = 0

    for product in selected_products:

        product_id = product[0]

        product_price = product[4]

        quantity = random.randint(1, 8)

        discount = random.choice([
            0,
            0,
            0,
            5,
            10,
            15
        ])

        item_total = (
            product_price
            * quantity
            * (1 - discount / 100)
        )

        total += item_total

        sale_items.append((
            sale_item_id,
            sale_id,
            product_id,
            quantity,
            product_price,
            discount
        ))

        sale_item_id += 1

    sale[5] = round(total, 2)


cursor.executemany("""
INSERT INTO sales
(id, customer_id, employee_id,
 sale_date, status, total_amount)

VALUES (?, ?, ?, ?, ?, ?)
""", sales)


cursor.executemany("""
INSERT INTO sale_items
(id, sale_id, product_id,
 quantity, unit_price, discount)

VALUES (?, ?, ?, ?, ?, ?)
""", sale_items)


# =========================================================
# Purchases
# =========================================================

purchases = []

procurement_employees = [
    employee[0]
    for employee in employees
    if employee[3] == 5
]


for purchase_id in range(1, 301):

    supplier_id = random.randint(
        1,
        len(suppliers)
    )

    employee_id = random.choice(
        procurement_employees
    )

    purchase_date = (
        start_date
        + timedelta(days=random.randint(0, 280))
    )

    status = random.choice([
        "Completed",
        "Completed",
        "Completed",
        "Pending",
        "Cancelled"
    ])

    purchases.append([
        purchase_id,
        supplier_id,
        employee_id,
        purchase_date.isoformat(),
        status,
        0
    ])


# =========================================================
# Purchase Items
# =========================================================

purchase_items = []

purchase_item_id = 1

for purchase in purchases:

    purchase_id = purchase[0]

    number_of_items = random.randint(1, 5)

    selected_products = random.sample(
        products,
        number_of_items
    )

    total = 0

    for product in selected_products:

        product_id = product[0]

        selling_price = product[4]

        # Purchase price is lower than selling price
        purchase_price = round(
            selling_price * random.uniform(0.55, 0.85),
            2
        )

        quantity = random.randint(5, 50)

        total += (
            purchase_price
            * quantity
        )

        purchase_items.append((
            purchase_item_id,
            purchase_id,
            product_id,
            quantity,
            purchase_price
        ))

        purchase_item_id += 1

    purchase[5] = round(total, 2)


cursor.executemany("""
INSERT INTO purchases
(id, supplier_id, employee_id,
 purchase_date, status, total_amount)

VALUES (?, ?, ?, ?, ?, ?)
""", purchases)


cursor.executemany("""
INSERT INTO purchase_items
(id, purchase_id, product_id,
 quantity, unit_price)

VALUES (?, ?, ?, ?, ?)
""", purchase_items)


# =========================================================
# Commit
# =========================================================

connection.commit()


# =========================================================
# Statistics
# =========================================================

print("======================================")
print("NovaTech Database Created Successfully")
print("======================================")

print(
    "Departments:",
    cursor.execute(
        "SELECT COUNT(*) FROM departments"
    ).fetchone()[0]
)

print(
    "Employees:",
    cursor.execute(
        "SELECT COUNT(*) FROM employees"
    ).fetchone()[0]
)

print(
    "Categories:",
    cursor.execute(
        "SELECT COUNT(*) FROM categories"
    ).fetchone()[0]
)

print(
    "Products:",
    cursor.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]
)

print(
    "Customers:",
    cursor.execute(
        "SELECT COUNT(*) FROM customers"
    ).fetchone()[0]
)

print(
    "Suppliers:",
    cursor.execute(
        "SELECT COUNT(*) FROM suppliers"
    ).fetchone()[0]
)

print(
    "Sales:",
    cursor.execute(
        "SELECT COUNT(*) FROM sales"
    ).fetchone()[0]
)

print(
    "Sale Items:",
    cursor.execute(
        "SELECT COUNT(*) FROM sale_items"
    ).fetchone()[0]
)

print(
    "Purchases:",
    cursor.execute(
        "SELECT COUNT(*) FROM purchases"
    ).fetchone()[0]
)

print(
    "Purchase Items:",
    cursor.execute(
        "SELECT COUNT(*) FROM purchase_items"
    ).fetchone()[0]
)

print("======================================")


connection.close()