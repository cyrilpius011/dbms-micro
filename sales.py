from customtkinter import *
import mysql.connector
from tkinter import messagebox

def call_sales():
    # Connect to the database
    m3 = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="aspire7",
        database="project",
    )
    c3 = m3.cursor()

    # Main window
    sales = CTk()
    sales.geometry("800x600")
    sales.title("Sales Page")

    set_appearance_mode("dark")
    set_default_color_theme("dark-blue")

    # Heading label
    heading_label = CTkLabel(sales, text="Our Products", font=("Arial", 24))
    heading_label.pack(padx=5, pady=10)

    # Frame for the sales form with grey border
    sales_frame = CTkFrame(sales, border_color="grey", border_width=2, corner_radius=5)
    sales_frame.pack(pady=10, padx=30, fill=BOTH, expand=True)

    # Frame for displaying product data with grey border
    data_display_frame = CTkFrame(sales_frame)
    data_display_frame.pack(padx=20, pady=10, fill=BOTH, expand=True)

    # Labels for column headers with centered alignment
    CTkLabel(data_display_frame, text="Name", font=("Arial", 15)).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
    CTkLabel(data_display_frame, text="Quantity", font=("Arial", 15)).grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    CTkLabel(data_display_frame, text="Unit Price", font=("Arial", 15)).grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    # Configure grid columns for uniform distribution
    data_display_frame.columnconfigure(0, weight=2)
    data_display_frame.columnconfigure(1, weight=2)
    data_display_frame.columnconfigure(2, weight=2)

    # Function to fetch and display data in the grid
    def display_produce_data():
        # Clear existing labels in data_display_frame (if any)
        for widget in data_display_frame.winfo_children():
            widget.grid_forget()

        # Reinsert column headers with centered alignment
        CTkLabel(data_display_frame, text="Name", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        CTkLabel(data_display_frame, text="Quantity", font=("Arial", 14)).grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        CTkLabel(data_display_frame, text="Unit Price", font=("Arial", 14)).grid(row=0, column=2, padx=5, pady=5, sticky="nsew")

        try:
            # Fetch data from the produce table
            c3.execute("SELECT type, quantity, unitprice FROM produce")
            rows = c3.fetchall()  # Fetch all rows

            # Insert data into the grid with centered alignment
            for idx, row in enumerate(rows, start=1):
                name, quantity, unitprice = row
                CTkLabel(data_display_frame, text=name).grid(row=idx, column=0, pady=5, sticky="nsew")
                CTkLabel(data_display_frame, text=str(quantity)).grid(row=idx, column=1, pady=5, sticky="nsew")
                CTkLabel(data_display_frame, text=f"${float(unitprice):.2f}").grid(row=idx, column=2, pady=5, sticky="nsew")

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch data: {err}")

    # Button to load produce data from the database with grey border
    load_data_button = CTkButton(sales_frame, text="View Our Products", command=display_produce_data,border_color="grey", border_width=1)
    load_data_button.pack(pady=20)

    # Label for product selection
    product_label = CTkLabel(sales_frame, text="Select Products and Enter Quantity", font=("Arial", 18))
    product_label.pack(pady=20)

    # Create text boxes for entering quantities
    quantity_entries = []
    product_names = []

    # Fetch product names to create entry fields
    def load_product_entries():
        try:
            c3.execute("SELECT type FROM produce")
            products = c3.fetchall()
            
            for product in products:
                product_name = product[0]
                quantity_entry = CTkEntry(sales_frame, width=250, placeholder_text=f"Enter quantity for {product_name}")
                quantity_entry.pack(padx=10, pady=5)
                quantity_entries.append(quantity_entry)
                product_names.append(product_name)

        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Failed to fetch products: {err}")

    load_product_entries()

    # Confirm button action with grey border
    def confirm_quantities():
        total_price = 0.0
        bill_details = "Bill Details:\n\n"

        sale_details = []  # To store each product's sale details temporarily

        for i, entry in enumerate(quantity_entries):
            try:
                # Get quantity, set to 0 if not entered
                quantity = int(entry.get()) if entry.get() else 0  

                # Skip this product if quantity is 0
                if quantity == 0:
                    continue

                # Fetch the unit price, ProduceID, and available stock for the corresponding product from the database
                c3.execute("SELECT unitprice, produceID, quantity FROM produce WHERE type = %s", (product_names[i],))
                result = c3.fetchone()
                
                # Verify if product data is returned
                if result is not None:
                    unit_price = float(result[0])  # Convert to float to avoid TypeError
                    produce_id = result[1]
                    available_stock = result[2]

                    # Check if the entered quantity is within available stock
                    if quantity > available_stock:
                        messagebox.showerror("Error", f"Insufficient stock for '{product_names[i]}'. Available: {available_stock}")
                        return  # Exit function if the quantity exceeds available stock

                    tp = quantity * unit_price  # Calculate total price for the product
                    total_price += tp  # Add to the overall total price

                    # Add product to the bill details
                    bill_details += f"{product_names[i]} - Quantity: {quantity}, Total: ${tp:.2f}\n"
                    
                    # Store sale details for insertion after sale ID is created
                    sale_details.append((produce_id, quantity, tp, available_stock))

                else:
                    messagebox.showerror("Error", f"Product '{product_names[i]}' not found in the database.")
                    return  # Exit function on missing product data

            except ValueError:
                messagebox.showerror("Error", f"Invalid quantity for product '{product_names[i]}'. Please enter a valid number.")
                return  # Exit function if invalid quantity is entered

        # Check if total price is zero
        if total_price == 0:
            messagebox.showinfo("Info", "No items selected or quantities entered. Please enter quantities to proceed.")
            return  # Exit the function if total price is 0

        # Insert the total sale amount into the Sales table and get the SaleID
        c3.execute("INSERT INTO Sales (SaleDate, Amount) VALUES (CURDATE(), %s)", (total_price,))
        sale_id = c3.lastrowid  # Get the last inserted SaleID for linking sale details

        # Insert sale details and update stock quantity for each product
        for produce_id, quantity, tp, available_stock in sale_details:
            c3.execute("INSERT INTO SaleDetails (SaleID, ProduceID, Count, Amount) VALUES (%s, %s, %s, %s)", 
                    (sale_id, produce_id, quantity, tp))
            new_quantity = available_stock - quantity
            c3.execute("UPDATE produce SET quantity = %s WHERE produceID = %s", (new_quantity, produce_id))

        # Show bill details in a message box
        bill_details += f"\nTotal Price: ${total_price:.2f}"
        messagebox.showinfo("Bill", bill_details)

        # Commit all changes to the database
        m3.commit()

        # Clear each entry field after confirmation
        for entry in quantity_entries:
            entry.delete(0, END)

    # Confirm button to calculate total price with grey border
    confirm_button = CTkButton(sales_frame, text="Buy Now", command=confirm_quantities,
                                border_color="grey", border_width=1)
    confirm_button.pack(pady=20)

    def logout_fun():
        sales.destroy()
        import register
        register.app.deiconify()
        messagebox.showinfo("Log Out", "You have been logged out.")
        
    # Log out button with grey border
    log_out = CTkButton(sales, text="LOG OUT", command=logout_fun, border_color="grey", border_width=1)
    log_out.pack(pady=10)

    # Start the main loop
    sales.mainloop()
    
if __name__=="__main__":
    call_sales()
