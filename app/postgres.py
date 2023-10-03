import psycopg2
import random
from faker import Faker

cur = None
conn = None
try:
    conn = psycopg2.connect(
        host='localhost',
        database="postgres",
        user="postgres",
        password="postgres",
        port=5432
    )

    cur = conn.cursor()

    # -------------Create Table Scripts--------------
    
    # Create the 'products' table
    create_script_product = '''
    CREATE TABLE IF NOT EXISTS products (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR(255) NOT NULL
    )'''

    # Create the 'sales' table
    create_script_sales = '''
    CREATE TABLE IF NOT EXISTS sales (
        sales_id SERIAL PRIMARY KEY,
        product_id INT REFERENCES products(product_id),
        quantity_sold INT NOT NULL,
        sale_date DATE NOT NULL,
        revenue FLOAT
    )'''

    # Create the 'inventory' table
    create_script_inventory = '''
    CREATE TABLE IF NOT EXISTS inventory (
        inventory_id SERIAL PRIMARY KEY,
        product_id INT REFERENCES products(product_id),
        quantity_available INT NOT NULL,
        last_updated TIMESTAMP NOT NULL DEFAULT now()
    )'''

    cur.execute(create_script_product)
    cur.execute(create_script_sales)
    cur.execute(create_script_inventory)

    # --------------------------Insert demo data in Table Scripts-----------------------------------------------------

    fake = Faker()

    # Populate the 'products' table with demo data
    for _ in range(10):
        product_name = fake.unique.first_name() + " Product"
        cur.execute("INSERT INTO products (product_name) VALUES (%s)", (product_name,))

    # Generate random sales data
    sales_data = []
    for product_id in range(1, 11):
        for _ in range(random.randint(1, 5)):
            sale_date = fake.date_between(start_date='-1y', end_date='today')
            quantity_sold = random.randint(1, 10)
            sales_data.append((product_id, sale_date, quantity_sold))

    # Populate the 'sales' table with demo data
    cur.executemany("INSERT INTO sales (product_id, sale_date, quantity_sold) VALUES (%s, %s, %s)", sales_data)

    # Generate random inventory data
    inventory_data = []
    for product_id in range(1, 11):
        quantity_available = random.randint(10, 100)
        inventory_data.append((product_id, quantity_available))

    # Populate the 'inventory' table with demo data
    cur.executemany("INSERT INTO inventory (product_id, quantity_available) VALUES (%s, %s)", inventory_data)

    conn.commit()

except Exception as error:
    print(error)
finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
