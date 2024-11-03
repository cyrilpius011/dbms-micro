from customtkinter import *
from tkinter import messagebox
import mysql.connector
import emp
import sales

m1 = mysql.connector.connect(host="localhost", user="root", passwd="aspire7", database="project")
c1 = m1.cursor()

# Function to clear registration fields
def clear_entries(*entries):
        for entry in entries:
            entry.delete(0, 'end')
        show_login_frame()

# Function to check email in customer table    
def email_exists(email):
    c1.execute("SELECT * FROM Customer WHERE Email = %s", (email,))
    result = c1.fetchone()
    return result is not None

# Function to fetch password from customer table 
def fetch_password(email):
    try:
        c1.execute("SELECT Password FROM Customer WHERE Email = %s", (email,))
        result = c1.fetchone()  # Fetch one record
        return result[0] if result else None
    except mysql.connector.Error:
        print("Error")
        return None

# Function to register user
def register_user():
    name = reg_username_entry.get()
    address = reg_address_entry.get()
    phone = reg_phone_entry.get()
    email = reg_email_entry.get()
    password = reg_password_entry.get()
    confirm_password = reg_cpassword_entry.get()
    
    if not all([name, address, phone, email, password, confirm_password]):
        result_label.configure(text="All fields are required.", text_color="red")
    elif password != confirm_password:
        result_label.configure(text="Passwords do not match.", text_color="red")
    elif email_exists(email):
        result_label.configure(text="Email already registered.", text_color="red")
    else:
        try:
            c1.execute("INSERT INTO Customer (Name, Address, Phone, Email, Password) VALUES (%s, %s, %s, %s, %s)",
                       (name, address, phone, email, password))
            m1.commit()
            messagebox.showinfo("Registration Successful", "You have been registered successfully!")
        except mysql.connector.Error as err:
            result_label.configure(text=f"Error: {err}", text_color="red")
        clear_entries(reg_username_entry,reg_address_entry,reg_phone_entry,reg_email_entry,reg_password_entry,reg_cpassword_entry)

# Function to log in
def login_action():
    email = login_email_entry.get() 
    password = login_password_entry.get()

    if not all([email, password]):
        error_label.configure(text="Login Failed!", text_color="red")
    else:
        if email_exists(email):
            if password == fetch_password(email):
                clear_entries(login_email_entry,login_password_entry)
                messagebox.showinfo("Logged in","Logged in!")
                app.withdraw()
                sales.call_sales()
        elif email == '1001' and password == 'password1001':
            clear_entries(login_email_entry,login_password_entry)
            messagebox.showinfo("Logged in","Manager Access!")
            app.withdraw()
            emp.call_emp()
        else:
            error_label.configure(text="Not Registered!", text_color="red")

# Initialize the main window
app = CTk()
app.geometry("800x700")
app.title("User Registration & Login")
set_appearance_mode("dark")
set_default_color_theme("dark-blue")

# Create the login frame with grey borders
login_frame = CTkFrame(app, width=500, height=600, corner_radius=10, border_width=2, border_color="grey")
login_frame.pack(pady=50, padx=30, expand=True)

login_title_label = CTkLabel(login_frame, text="LOGIN", font=("Arial", 24))
login_title_label.pack(pady=(5, 10))

login_email_entry = CTkEntry(login_frame, width=400, placeholder_text="Enter UserID")
login_email_entry.pack(pady=(20, 10), padx=10)

login_password_entry = CTkEntry(login_frame, width=400, placeholder_text="Enter Password", show="*")
login_password_entry.pack(pady=(20, 10), padx=10)

error_label = CTkLabel(login_frame, text="", font=("Arial", 14))
error_label.pack(pady=5)

login_button = CTkButton(login_frame, text="Login", command=login_action, width=150, border_width=2, border_color="grey")
login_button.pack(pady=20)

# Create the registration frame with grey borders
register_frame = CTkFrame(app, width=500, height=600, corner_radius=10, border_width=2, border_color="grey")

register_title_label = CTkLabel(register_frame, text="REGISTER", font=("Arial", 24))
register_title_label.pack(pady=(5, 10))

reg_username_entry = CTkEntry(register_frame, width=400, placeholder_text="Enter Username")
reg_username_entry.pack(pady=(20, 10), padx=10)

reg_address_entry = CTkEntry(register_frame, width=400, placeholder_text="Enter Address")
reg_address_entry.pack(pady=(20, 10), padx=10)

reg_phone_entry = CTkEntry(register_frame, width=400, placeholder_text="Enter Phone")
reg_phone_entry.pack(pady=(20, 10), padx=10)

reg_email_entry = CTkEntry(register_frame, width=400, placeholder_text="Enter Email")
reg_email_entry.pack(pady=(20, 10), padx=10)

reg_password_entry = CTkEntry(register_frame, width=400, placeholder_text="Enter Password")
reg_password_entry.pack(pady=(20, 10), padx=10)

reg_cpassword_entry = CTkEntry(register_frame, width=400, placeholder_text="Re-Enter Password")
reg_cpassword_entry.pack(pady=(20, 10), padx=10)

register_button = CTkButton(register_frame, text="Register", command=register_user, width=150, border_width=2, border_color="grey")
register_button.pack(pady=20)

result_label = CTkLabel(register_frame, text="", text_color="red")
result_label.pack(pady=(10, 0))

# Function to switch to the registration frame
def show_register_frame():
    login_frame.pack_forget()  
    register_frame.pack(pady=50, padx=30, expand=True)

# Function to switch back to the login frame
def show_login_frame():
    register_frame.pack_forget()
    login_frame.pack(pady=50, padx=30, expand=True)

# Navigation to login page
login_switch_button = CTkButton(register_frame, text="Already have an account? Login", fg_color='transparent', hover=None, command=show_login_frame)
login_switch_button.pack(pady=(20, 10))

# Register button to go to registration page
reg_button = CTkButton(login_frame, text="New User? Click Here To Register", command=show_register_frame, text_color="light blue", hover=None, fg_color="transparent")
reg_button.pack(pady=10)

# Show the login frame initially
login_frame.pack(pady=50, padx=30, expand=True)

# Start the main loop
app.mainloop()
