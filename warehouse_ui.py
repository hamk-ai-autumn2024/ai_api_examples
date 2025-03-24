from warehouse_db import *

# Constants
WEIGHT_CONVERSION = 1000  # grams to kilograms
PRICE_CONVERSION = 100    # cents to euros

# Helper function to display product information
def display_product(product):
    print(f"ID: {product[0]}, Name: {product[1]}, Amount: {product[2]}, "
          f"Weight: {product[3]/WEIGHT_CONVERSION:.2f} kg, Price: {product[4]/PRICE_CONVERSION:.2f} €")

# Add a product
def add_product_ui():
    name = input("Enter product name: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return
    try:
        amount = int(input("Enter amount: "))
        weight = int(input("Enter weight in grams: "))
        price = int(input("Enter price in cents: "))
        if amount < 0 or weight < 0 or price < 0:
            print("Error: Negative values are not allowed.")
            return
        if add_product(name, amount, weight, price):
            print("Product added successfully.")
    except ValueError:
        print("Error: Invalid input. Please enter numbers for amount, weight, and price.")

# Update a product
def update_product_ui():
    name = input("Enter product name to update: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return
    try:
        amount = int(input("Enter new amount: "))
        weight = int(input("Enter new weight in grams: "))
        price = int(input("Enter new price in cents: "))
        if amount < 0 or weight < 0 or price < 0:
            print("Error: Negative values are not allowed.")
            return
        if update_product(name, amount, weight, price):
            print("Product updated successfully.")
    except ValueError:
        print("Error: Invalid input. Please enter numbers for amount, weight, and price.")

# Delete a product
def delete_product_ui():
    name = input("Enter product name to delete: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return
    if delete_product(name):
        print("Product deleted successfully.")

# List all products in alphabetical order
def list_products_alphabetical_ui():
    products = list_products_alphabetical()
    if not products:
        print("No products found.")
    else:
        for product in products:
            display_product(product)

# List all products in ID order
def list_products_id_ui():
    products = list_products_id()
    if not products:
        print("No products found.")
    else:
        for product in products:
            display_product(product)

# Search for a product
def search_product_ui():
    name = input("Enter product name to search: ").strip()
    if not name:
        print("Error: Name cannot be empty.")
        return
    products = search_product(name)
    if not products:
        print("No products found.")
    else:
        for product in products:
            display_product(product)

# Main menu
def main():
    initialize_db()
    while True:
        print("\nWarehouse Management System")
        print("1. Add Product")
        print("2. Update Product")
        print("3. Delete Product")
        print("4. List Products (Alphabetical)")
        print("5. List Products (ID Order)")
        print("6. Search Product")
        print("7. Exit")
        choice = input("Enter your choice: ").strip()
        if choice == '1':
            add_product_ui()
        elif choice == '2':
            update_product_ui()
        elif choice == '3':
            delete_product_ui()
        elif choice == '4':
            list_products_alphabetical_ui()
        elif choice == '5':
            list_products_id_ui()
        elif choice == '6':
            search_product_ui()
        elif choice == '7':
            print("Exiting program. Goodbye!")
            break
        else:
            print("Error: Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
    