# Produce and Livestock Management Tool

## Overview
-This tool is designed to assist with managing customers, employees, animals, produce, and sales in a farm-related business.    It features a user-friendly interface built with `CustomTkinter` and connects to a MySQL database for persistent data storage.


## Features
### 1. Login Page
- User authentication
- Password protection
- Error handling
- User Registration

### 2. Manager Dashboard
- Manage Customers
  - View Customers

- Manage Employees
  - View Employees
  - Add Employee
  - Delete Employee

- Manage Animals
  - View Animals
  - Update Animal Details

- Manage Produce
  - View Produce
  - Update Produce Details

- Manage Sales
  - View Sales
  - View Total Sales

- Log Out

### 3. Sales Page
- View Products
- Enter Quantities
- Finalize Sale and Amount
- Log Out

## Technologies Used
- Python 3.x
- MySQL Server
- Libraries:
- ```
    - `CustomTkinter` for GUI
    - `mysql-connector-python` for database interaction

## Installation
1. Ensure you have Python 3.x installed.
2. Set up a MySQL database and create the required tables (`Customer`, `Employee`, `Animal`, `Produce`, `Sales`, `SaleDetails`).
3. Install the required Python packages:
    -pip install customtkinter
    -pip install customtkinter mysql-connector-python

## Database Schema
- Make sure your MySQL database includes the following tables (adjust types as necessary):

```sql
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY AUTO_INCREMENT,
    Name VARCHAR(255),
    Address VARCHAR(255),
    Phone VARCHAR(20),
    Email VARCHAR(100)
);

CREATE TABLE Employee (
    EmployeeID INT PRIMARY KEY,
    Name VARCHAR(255),
    Designation VARCHAR(100),
    Phone VARCHAR(20),
    HireDate DATE,
    Email VARCHAR(100) UNIQUE
);

CREATE TABLE Animal (
    AnimalID INT PRIMARY KEY,
    Name VARCHAR(100),
    Count INT
);

CREATE TABLE Produce (
    ProduceID INT PRIMARY KEY AUTO_INCREMENT,
    Type VARCHAR(100),
    Quantity INT,
    UnitPrice DECIMAL(10, 2),
    DateCollected DATE,
    AnimalID INT,
    FOREIGN KEY (AnimalID) REFERENCES Animal(AnimalID)
);

CREATE TABLE Sales (
    SaleID INT PRIMARY KEY AUTO_INCREMENT,
    SaleDate DATE,
    Amount DECIMAL(10, 2)
);

CREATE TABLE SaleDetails (
    SaleDetailID INT PRIMARY KEY AUTO_INCREMENT,
    SaleID INT,
    ProduceID INT,
    Count INT,
    Amount DECIMAL(10, 2),
    FOREIGN KEY (SaleID) REFERENCES Sales(SaleID),
    FOREIGN KEY (ProduceID) REFERENCES Produce(ProduceID)
);
```
## Usage
 1.Connect all the python files with your database
 2.Run registration.py
 3.Log in with the appropriate credentials on the Login Page.
 4.New users can register by clicking on the registration option and filling in the required details.
 6.Customers can navigate through buying option in sale page by logging in
 5.Manager can navigate through the tabs to manage customers, employees, animals, produce, and sales by logging in.

## Contact
- Cyril Pius
- cyrilpius011@gmail.com
- https://github.com/cyrilpiusch

