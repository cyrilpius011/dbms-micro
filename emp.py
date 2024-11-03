from customtkinter import *
from tkinter import messagebox
import mysql.connector


def call_emp():
    # Connect to database
    m2 = mysql.connector.connect(host="localhost", user="root", passwd="aspire7", database="project")
    c2 = m2.cursor()

    # Function to check animal ID in customer table    
    def animal_exists(animal_id):
        c2.execute("SELECT * FROM Animal WHERE AnimalID = %s", (animal_id,))
        return c2.fetchone() is not None

    # Function to check produce ID in customer table    
    def produce_exists(produce_id):
        c2.execute("SELECT * FROM Produce WHERE ProduceID = %s", (produce_id,))
        return c2.fetchone() is not None

    # Create the main window
    manager = CTk()
    manager.title("Manager Dashboard")
    manager.geometry("800x600")
    set_appearance_mode("dark")
    set_default_color_theme("dark-blue")
    CTkLabel(manager, text="Manager Dashboard", font=("Arial", 24, "bold")).pack(pady=10)

    main_frame = CTkFrame(manager, border_color="grey", border_width=2)
    main_frame.pack(expand=True, fill="both", padx=10, pady=10)

    # Create button frame at the top of the main frame
    button_frame = CTkFrame(main_frame, border_color="grey", border_width=2)
    button_frame.pack(side=TOP, fill="x", padx=10, pady=10)

    def create_buttons():
        CTkButton(button_frame, text="Manage Customers", command=show_customers_tab, border_color="grey").pack(side="left", padx=(7,128), pady=5)
        CTkButton(button_frame, text="Manage Employees", command=show_employee_tab, border_color="grey").pack(side="left",  padx=(0,128), pady=5)
        CTkButton(button_frame, text="Manage Animals", command=show_animals_tab, border_color="grey").pack(side="left",  padx=(0,128), pady=5)
        CTkButton(button_frame, text="Manage Products", command=show_produce_tab, border_color="grey").pack(side="left",  padx=(0,128), pady=5)
        CTkButton(button_frame, text="Manage Sales", command=show_sales_tab, border_color="grey").pack(side="left",  padx=(0,128), pady=5)
        CTkButton(button_frame, text="Log Out", command=log_out, border_color="grey").pack(side="left",  padx=(0,5), pady=5)
    def clear_frame():
        for widget in main_frame.winfo_children():
            if widget != button_frame:  # Keep the button frame
                widget.destroy()

    def clear_entries(*entries):
        for entry in entries:
            entry.delete(0, 'end')

    def show_customers_tab():
        clear_frame()
        tab = CTkFrame(main_frame, border_color="grey", border_width=2)
        tab.pack(expand=True, fill="both", padx=10, pady=10)

        CTkLabel(tab, text="Customer Management").pack(pady=10)
        CTkButton(tab, text="View Customers", command=view_customers, border_color="grey").pack(pady=5)
        
        global customer_data_label
        customer_data_label = CTkLabel(tab, text="", justify=LEFT)
        customer_data_label.pack(pady=5)

    def view_customers():
        c2.execute("SELECT * FROM Customer")
        customer = c2.fetchall()
        customer_data_label.configure(text="\n".join([f"ID: {cus[0]}, Name: {cus[1]}, Address: {cus[2]}, Phone: {cus[3]}, Email: {cus[4]}" for cus in customer]))

    def show_employee_tab():
        clear_frame()

        tab = CTkFrame(main_frame, border_color="grey", border_width=2)
        tab.pack(expand=True, fill="both", padx=10, pady=10)

        CTkLabel(tab, text="Employee Management").pack(pady=10)

        employee_id_entry = CTkEntry(tab, placeholder_text="Employee ID")
        employee_id_entry.pack(pady=5)

        employee_name_entry = CTkEntry(tab, placeholder_text="Employee Name")
        employee_name_entry.pack(pady=5)

        employee_designation_entry = CTkEntry(tab, placeholder_text="Designation")
        employee_designation_entry.pack(pady=5)

        employee_phone_entry = CTkEntry(tab, placeholder_text="Phone Number")
        employee_phone_entry.pack(pady=5)

        employee_email_entry = CTkEntry(tab, placeholder_text="Email")
        employee_email_entry.pack(pady=5)

        CTkButton(tab, text="Add Employee", command=lambda: add_employee(employee_id_entry, employee_name_entry, employee_designation_entry, employee_phone_entry, employee_email_entry), border_color="grey").pack(pady=10)
        CTkButton(tab, text="Delete Employee", command=lambda: del_employee(employee_id_entry, employee_name_entry, employee_designation_entry, employee_phone_entry, employee_email_entry), border_color="grey").pack(pady=5)
        CTkButton(tab, text="View Employees", command=view_employees, border_color="grey").pack(pady=5)
        
        global employee_data_label
        employee_data_label = CTkLabel(tab, text="", justify=LEFT)
        employee_data_label.pack(pady=5)

    def add_employee(id_entry, name_entry, designation_entry, phone_entry, email_entry):
        employee_data_label.configure(text="\n")
        id = id_entry.get()
        name = name_entry.get()
        designation = designation_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()

        if all([id, name, designation, phone, email]):
            try:
                c2.execute("INSERT INTO Employee (EmployeeID, Name, Designation, Phone, HireDate, Email) VALUES (%s, %s, %s, %s, CURDATE(), %s)",
                           (id, name, designation, phone, email))
                m2.commit()
                messagebox.showinfo("Success", "Employee added.")
                clear_entries(id_entry,name_entry, designation_entry, phone_entry, email_entry)
            except mysql.connector.IntegrityError:
                messagebox.showerror("Error", "Email already exists.")
        else:
            messagebox.showwarning("Input Error", "Enter all fields")

    def del_employee(id_entry, name_entry, designation_entry, phone_entry, email_entry):
        employee_id = id_entry.get()
        name = name_entry.get()
        designation = designation_entry.get()
        phone = phone_entry.get()
        email = email_entry.get()

        if not all([employee_id, name, designation, phone, email]):
            messagebox.showwarning("Input Error", "Please fill in all fields.")
            return
        else:
            c2.execute("SELECT Name,Designation,Phone,Email FROM Employee WHERE EmployeeID = %s", (employee_id,))
            employee = c2.fetchone()

            if employee:
                db_name, db_designation, db_phone,db_email = employee
            
            if (name == db_name and designation == db_designation and phone == db_phone and email == db_email):
                c2.execute("DELETE FROM Employee WHERE EmployeeID = %s", (employee_id,))
                m2.commit()
                messagebox.showinfo("Success", "Employee deleted successfully.")
                clear_entries(id_entry, name_entry, designation_entry, phone_entry, email_entry)
            else:
                messagebox.showwarning("Error", "Employee not found. Please check the ID.")
    
    def view_employees():
        c2.execute("SELECT * FROM Employee")
        employees = c2.fetchall()
        employee_data_label.configure(text="".join([f"ID: {emp[0]}, Name: {emp[1]}, Designation: {emp[2]}, Phone: {emp[3]}, HireDate: {emp[4]}, Email: {emp[5]}\n\n" for emp in employees]))

    def show_animals_tab():
        clear_frame()

        tab = CTkFrame(main_frame, border_color="grey", border_width=2)
        tab.pack(expand=True, fill="both", padx=10, pady=10)

        CTkLabel(tab, text="Animal Management").pack(pady=10)
        animal_id_entry = CTkEntry(tab, placeholder_text="Animal ID")
        animal_id_entry.pack(pady=5)
        
        animal_count_entry = CTkEntry(tab, placeholder_text="Count")
        animal_count_entry.pack(pady=5)

        CTkButton(tab, text="Update Animal Details", command=lambda: add_animal(animal_id_entry, animal_count_entry), border_color="grey").pack(pady=5)
        CTkButton(tab, text="View Animals", command=view_animals, border_color="grey").pack(pady=5)

        global animal_data_label
        animal_data_label = CTkLabel(tab, text="", justify=LEFT)
        animal_data_label.pack(pady=5)

    def add_animal(id_entry, count_entry):
        animal_data_label.configure(text="\n")
        animal_id = id_entry.get()
        count = count_entry.get()

        if all([animal_id, count]):
            if animal_exists(animal_id):
                try:
                    c2.execute("UPDATE Animal SET Count=%s WHERE AnimalID=%s", (count, animal_id))
                    m2.commit()
                    messagebox.showinfo("Success", "Updated")
                except mysql.connector.IntegrityError:
                    messagebox.showerror("Error", "Error")
                clear_entries(id_entry, count_entry)
            else:
                messagebox.showwarning("Error", "Check AnimalID")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def view_animals():
        c2.execute("SELECT * FROM Animal")
        animal_details = c2.fetchall()
        animal_data_label.configure(text="\n".join([f"ID: {animal[0]}, Name: {animal[1]}, Count: {animal[2]}" for animal in animal_details]))

    def show_produce_tab():
        clear_frame()

        tab = CTkFrame(main_frame, border_color="grey", border_width=2)
        tab.pack(expand=True, fill="both", padx=10, pady=10)

        CTkLabel(tab, text="Produce Management").pack(pady=10)

        id_entry = CTkEntry(tab, placeholder_text="ProduceID")
        id_entry.pack(pady=5)
        
        quantity_entry = CTkEntry(tab, placeholder_text="Quantity")
        quantity_entry.pack(pady=5)

        CTkButton(tab, text="Update Product Details", command=lambda: add_product(id_entry, quantity_entry), border_color="grey").pack(pady=5)
        CTkButton(tab, text="View Products", command=view_product, border_color="grey").pack(pady=5)

        global produce_data_label
        produce_data_label = CTkLabel(tab, text="", justify=LEFT)
        produce_data_label.pack(pady=5)
        
    def add_product(id_entry, quantity_entry):
        produce_data_label.configure(text="\n")
        produce_id = id_entry.get()
        quantity = quantity_entry.get()

        if all([produce_id, quantity]):
            if produce_exists(produce_id):
                try:
                    c2.execute("UPDATE Produce SET Quantity=%s, DateCollected=CURDATE() WHERE ProduceID=%s", (quantity, produce_id))
                    m2.commit()
                    messagebox.showinfo("Success", "Updated")
                except mysql.connector.IntegrityError:
                    messagebox.showerror("Error", "Error.")
                clear_entries(id_entry, quantity_entry)
            else:
                messagebox.showwarning("Error", "Check ProduceID")
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def view_product():
        c2.execute("SELECT * FROM Produce")
        produce_details = c2.fetchall()
        produce_data_label.configure(text="\n".join([f"ID: {produce[0]}, Type: {produce[1]}, Quantity: {produce[2]}, Date: {produce[3]}, Animal ID: {produce[4]}, Price: {produce[5]}" for produce in produce_details]))

    def show_sales_tab():
        clear_frame()
        tab = CTkFrame(main_frame, border_color="grey", border_width=2)
        tab.pack(expand=True, fill="both", padx=10, pady=10)

        CTkLabel(tab, text="Manage Sales").pack(pady=10)
        
        sale_data = CTkEntry(tab, placeholder_text="Enter SaleID")
        sale_data.pack(pady=5)
        
        CTkButton(tab, text="Sale Details", command=lambda: sale_info(sale_data), border_color="grey").pack(pady=5)
        CTkButton(tab, text="View Total Sales", command=view_sale_data, border_color="grey").pack(pady=5)
        
        global sales_data_label
        sales_data_label = CTkLabel(tab, text="", justify=LEFT)
        sales_data_label.pack(pady=5)

    def view_sale_data():
        c2.execute("SELECT * FROM Sales")
        sales_details = c2.fetchall()
        sales_data_label.configure(text="\n".join([f"ID: {sales[0]}, SaleDate: {sales[1]}, Amount: {sales[2]}" for sales in sales_details]))

    def sale_info(sale_data):
        saleid = sale_data.get()
        c2.execute("SELECT * FROM SaleDetails WHERE SaleID=%s", (saleid,))
        sale_details = c2.fetchall()
        if sale_details:
            sales_data_label.configure(text="\n".join([f"SaleID: {sales[0]}, ProduceID: {sales[1]}, Count: {sales[2]}, Amount: {sales[3]}" for sales in sale_details]))
        else:
            messagebox.showwarning("Error", "Incorrect SaleID")

    def log_out():
        manager.destroy()
        import register
        register.app.deiconify()
        messagebox.showinfo("Log Out", "You have been logged out.")

    # Create buttons at the top
    create_buttons()
    show_customers_tab()  # Show the default tab

    manager.mainloop()

if __name__=="__main__":
    call_emp()
