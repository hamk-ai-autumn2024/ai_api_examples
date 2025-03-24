import sqlite3

# Constants
DATABASE_NAME = 'warehouse.db'
TABLE_NAME = 'products'
COLUMN_ID = 'id'
COLUMN_NAME = 'name'
COLUMN_AMOUNT = 'amount'
COLUMN_WEIGHT = 'weight'
COLUMN_PRICE = 'price'

# Database setup
def initialize_db():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                        {COLUMN_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
                        {COLUMN_NAME} TEXT UNIQUE NOT NULL,
                        {COLUMN_AMOUNT} INTEGER NOT NULL CHECK({COLUMN_AMOUNT} >= 0),
                        {COLUMN_WEIGHT} INTEGER NOT NULL CHECK({COLUMN_WEIGHT} >= 0),
                        {COLUMN_PRICE} INTEGER NOT NULL CHECK({COLUMN_PRICE} >= 0)
                    )''')
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        if conn:
            conn.close()

# Add a product
def add_product(name, amount, weight, price):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute(f'INSERT INTO {TABLE_NAME} ({COLUMN_NAME}, {COLUMN_AMOUNT}, {COLUMN_WEIGHT}, {COLUMN_PRICE}) VALUES (?, ?, ?, ?)',
                  (name, amount, weight, price))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        print("Error: Product name already exists.")
        return False
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Update a product
def update_product(name, amount, weight, price):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute(f'UPDATE {TABLE_NAME} SET {COLUMN_AMOUNT}=?, {COLUMN_WEIGHT}=?, {COLUMN_PRICE}=? WHERE {COLUMN_NAME}=?',
                  (amount, weight, price, name))
        conn.commit()
        updated = c.rowcount > 0
        if not updated:
            print("Error: Product not found.")
        return updated
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

# Delete a product
def delete_product(name):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute(f'DELETE FROM {TABLE_NAME} WHERE {COLUMN_NAME}=?', (name,))
        conn.commit()
        deleted = c.rowcount > 0
        if not deleted:
            print("Error: Product not found.")
        return deleted
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    finally:
        if conn:
            conn.close()

# List all products in alphabetical order
def list_products_alphabetical():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute(f'SELECT * FROM {TABLE_NAME} ORDER BY {COLUMN_NAME} ASC')
        products = c.fetchall()
        return products
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()

# List all products in ID order
def list_products_id():
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute(f'SELECT * FROM {TABLE_NAME} ORDER BY {COLUMN_ID} ASC')
        products = c.fetchall()
        return products
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()

# Search for a product by name (case insensitive, partial match)
def search_product(name):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        c = conn.cursor()
        c.execute(f'SELECT * FROM {TABLE_NAME} WHERE LOWER({COLUMN_NAME}) LIKE LOWER(?)', (f'%{name}%',))
        products = c.fetchall()
        return products
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        if conn:
            conn.close()
            