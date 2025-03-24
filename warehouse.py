import sqlite3

# Connect to the SQLite database with error handling
try:
    conn = sqlite3.connect('warehouse.db')
    c = conn.cursor()
except sqlite3.Error as e:
    print(f"An error occurred while connecting to the database: {e}")
    exit(1)

# Create the warehouse table if it doesn't exist with error handling
try:
    c.execute('''CREATE TABLE IF NOT EXISTS warehouse (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    amount INTEGER NOT NULL CHECK(amount >= 0),
                    weight INTEGER NOT NULL CHECK(weight >= 0),
                    price INTEGER NOT NULL CHECK(price >= 0)
                )''')
    conn.commit()
except sqlite3.Error as e:
    print(f"An error occurred while creating the table: {e}")
    conn.close()
    exit(1)

def add_product():
    """
    Adds a new product to the warehouse database.

    Prompts the user to enter the product name, amount, weight, and price.
    Validates the input and inserts the product into the database if all inputs are valid.

    Raises:
        ValueError: If the input for amount, weight, or price is not a valid integer.
        sqlite3.IntegrityError: If the product name is not unique.
        Exception: For any other exceptions that may occur during the database operation.

    Returns:
        None
    """
    try:
        name = input("Enter product name: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        amount = int(input("Enter product amount: "))
        weight = int(input("Enter product weight (in grams): "))
        price = int(input("Enter product price (in cents): "))
        c.execute("INSERT INTO warehouse (name, amount, weight, price) VALUES (?, ?, ?, ?)", (name, amount, weight, price))
        conn.commit()
        print("Product added successfully.")
    except ValueError:
        print("Invalid input. Please enter numeric values for amount, weight, and price.")
    except sqlite3.IntegrityError:
        print("Product name must be unique.")
    except Exception as e:
        print(f"An error occurred: {e}")

def update_product():
    """
    Updates the details of a product in the warehouse database.

    Prompts the user to enter the name of the product to update. If the product is found,
    it then prompts the user to enter the new product name, amount, weight, and price.
    The product details are then updated in the database.

    Raises:
        ValueError: If the user inputs non-numeric values for amount, weight, or price.
        Exception: If any other error occurs during the database operation.

    Returns:
        None
    """
    try:
        name = input("Enter the name of the product to update: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        c.execute("SELECT * FROM warehouse WHERE name LIKE ?", ('%' + name + '%',))
        product = c.fetchone()
        if product:
            new_name = input("Enter new product name: ").strip()
            if not new_name:
                print("Name cannot be empty.")
                return
            amount = int(input("Enter new product amount: "))
            weight = int(input("Enter new product weight (in grams): "))
            price = int(input("Enter new product price (in cents): "))
            c.execute("UPDATE warehouse SET name = ?, amount = ?, weight = ?, price = ? WHERE id = ?", (new_name, amount, weight, price, product[0]))
            conn.commit()
            print("Product updated successfully.")
        else:
            print("Product not found.")
    except ValueError:
        print("Invalid input. Please enter numeric values for amount, weight, and price.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_product():
    """
    Deletes a product from the warehouse database based on the name provided by the user.

    Prompts the user to enter the name of the product to delete. If the name is not empty,
    it deletes the product(s) whose name matches the input (case-insensitive) from the 
    'warehouse' table in the database. If the operation is successful, it commits the 
    changes and prints a success message. If an error occurs, it prints an error message.

    Raises:
        Exception: If an error occurs during the database operation.
    """
    try:
        name = input("Enter the name of the product to delete: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        c.execute("DELETE FROM warehouse WHERE name LIKE ?", ('%' + name + '%',))
        conn.commit()
        print("Product deleted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

def list_products_alphabetical():
    """
    Fetches and prints a list of products from the warehouse database in alphabetical order by name.

    The function executes an SQL query to select all products from the 'warehouse' table,
    orders them by the 'name' column in ascending order, and prints each product's details.
    The details include the product ID, name, amount, weight (converted to kilograms), and price (converted to euros).

    Raises:
        Exception: If an error occurs during the database query or fetching results, it prints an error message.
    """
    try:
        c.execute("SELECT * FROM warehouse ORDER BY name ASC")
        products = c.fetchall()
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Amount: {product[2]}, Weight: {product[3] / 1000} kg, Price: {product[4] / 100} €")
    except Exception as e:
        print(f"An error occurred: {e}")

def list_products_by_id():
    """
    Fetches and lists all products from the warehouse database ordered by their ID in ascending order.

    The function connects to the database, executes a query to retrieve all products, and prints each product's details.
    The details include the product ID, name, amount, weight (converted to kilograms), and price (converted to euros).

    Raises:
        Exception: If there is an error during the database query or fetching process, it prints an error message.
    """
    try:
        c.execute("SELECT * FROM warehouse ORDER BY id ASC")
        products = c.fetchall()
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Amount: {product[2]}, Weight: {product[3] / 1000} kg, Price: {product[4] / 100} €")
    except Exception as e:
        print(f"An error occurred: {e}")

def search_product():
    """
    Prompts the user to enter the name of a product to search for in the warehouse database.
    
    The function retrieves and displays products from the warehouse database that match the 
    search criteria. The product details include ID, Name, Amount, Weight (in kg), and Price (in €).
    
    If the user input is empty, an error message is displayed. If an exception occurs during 
    the database query, an error message is printed.
    
    Returns:
        None
    """
    try:
        name = input("Enter the name of the product to search: ").strip()
        if not name:
            print("Name cannot be empty.")
            return
        c.execute("SELECT * FROM warehouse WHERE name LIKE ?", ('%' + name + '%',))
        products = c.fetchall()
        for product in products:
            print(f"ID: {product[0]}, Name: {product[1]}, Amount: {product[2]}, Weight: {product[3] / 1000} kg, Price: {product[4] / 100} €")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    Main function to run the Warehouse Management System.

    This function displays a menu with options to:
    1. Add a product
    2. Update a product
    3. Delete a product
    4. List products alphabetically
    5. List products by ID
    6. Search for a product
    7. Exit the program

    The user is prompted to enter their choice, and the corresponding function is called based on the user's input.
    If the user enters an invalid choice, an error message is displayed and the menu is shown again.
    """
    while True:
        print("\nWarehouse Management System")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. List Products Alphabetically")
        print("5. List Products by ID")
        print("6. Search Product")
        print("7. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            add_product()
        elif choice == '2':
            update_product()
        elif choice == '3':
            delete_product()
        elif choice == '4':
            list_products_alphabetical()
        elif choice == '5':
            list_products_by_id()
        elif choice == '6':
            search_product()
        elif choice == '7':
            conn.close()
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()