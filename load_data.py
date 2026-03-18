# load_data.py
import pymysql
import pandas as pd

# Load normalized data from CSV
countries_df = pd.read_csv('countries.csv')
customer_cc_df = pd.read_csv('customer_cc.csv')
product_df = pd.read_csv('products.csv')
department_df = pd.read_csv('departments.csv')
customer_df = pd.read_csv('customers_norm.csv')
employee_df = pd.read_csv('employees_norm.csv')
payment_df = pd.read_csv('payments.csv')

# 1. Connect to MySQL
connection = pymysql.connect(
    host='localhost',
    port=3306,
    user='dss_user0',
    passwd='73841A',
    db='retail_dss0',        # ← specify your database here
    charset='utf8mb4'
)
cursor = connection.cursor()
cursor.execute('USE retail_dss0;')  # ← make sure you’re in the correct DB

# 3. Create tables
cursor.execute('DROP TABLE IF EXISTS countries;')
cursor.execute('''
CREATE TABLE countries (
    Country VARCHAR(100) NOT NULL,
    Country_Code VARCHAR(100) NOT NULL,
    country_id INT PRIMARY KEY
);
''')

cursor.execute('DROP TABLE IF EXISTS customer_cc;')
cursor.execute('''
CREATE TABLE customer_cc (
    credit_provider VARCHAR(100) NOT NULL,
    credit_provider_id INT PRIMARY KEY
);
''')

cursor.execute('DROP TABLE IF EXISTS products;')
cursor.execute('''
CREATE TABLE products (
    Product_Name VARCHAR(100) NOT NULL,
    Alcohol_Percent FLOAT NOT NULL,
    Alcohol_Amount FLOAT NOT NULL,
    Alcohol_Price FLOAT NOT NULL,
    product_id INT PRIMARY KEY NOT NULL
);
''')

cursor.execute('DROP TABLE IF EXISTS departments;')
cursor.execute('''
CREATE TABLE departments (
    department_id INT PRIMARY KEY,
    department VARCHAR(100) NOT NULL
);
''')

cursor.execute('DROP TABLE IF EXISTS customers;')
cursor.execute('''
CREATE TABLE customers (
    customer_id INT PRIMARY KEY NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    street VARCHAR(100) NOT NULL,
    four_digits INT NOT NULL,
    country_id INT NOT NULL,
    credit_provider_id INT NOT NULL,
    FOREIGN KEY (country_id) REFERENCES countries(country_id),
    FOREIGN KEY (credit_provider_id) REFERENCES customer_cc(credit_provider_id)
);
''')

cursor.execute('DROP TABLE IF EXISTS employees;')
cursor.execute('''
CREATE TABLE employees (
    employee_id INT PRIMARY KEY NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);
''')

cursor.execute('DROP TABLE IF EXISTS payments;')
cursor.execute('''
CREATE TABLE payments (
    payment_id INT PRIMARY KEY NOT NULL,
    date DATE NOT NULL,
    customer_id INT NOT NULL,
    employee_id INT NOT NULL,
    product_id INT NOT NULL,
    price FLOAT NOT NULL
);
''')

# 4. Insert data

# Countries
for _, row in countries_df.iterrows():
    cursor.execute(
        "INSERT INTO countries (Country, Country_Code, country_id) VALUES (%s, %s, %s)",
        (row.Country, row.Country_Code, int(row.country_id))
    )
connection.commit()

# Customer_cc
for _, row in customer_cc_df.iterrows():
    cursor.execute(
        "INSERT INTO customer_cc (credit_provider, credit_provider_id) VALUES (%s, %s)",
        (row.credit_provider, int(row.credit_provider_id))
    )
connection.commit()

# Products
for _, row in product_df.iterrows():
    cursor.execute(
        "INSERT INTO products (Product_Name, Alcohol_Percent, Alcohol_Amount, Alcohol_Price, product_id) VALUES (%s, %s, %s, %s, %s)",
        (row.Product_Name, float(row.Alcohol_Percent), float(row.Alcohol_Amount), float(row.Alcohol_Price), int(row.product_id))
    )
connection.commit()

# Departments
for _, row in department_df.iterrows():
    cursor.execute(
        "INSERT INTO departments (department_id, department) VALUES (%s, %s)",
        (int(row.department_id), row.department)
    )
connection.commit()

# Customers
for _, row in customer_df.iterrows():
    cursor.execute(
        "INSERT INTO customers (customer_id, first_name, last_name, full_name, email, street, four_digits, country_id, credit_provider_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
        (int(row.customer_id), row.first_name, row.last_name, row.full_name, row.email, row.street, int(row.four_digits), int(row.country_id), int(row.credit_provider_id))
    )
connection.commit()

# Employees
for _, row in employee_df.iterrows():
    cursor.execute(
        "INSERT INTO employees (employee_id, first_name, last_name, full_name, email, city, department_id) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (int(row.employee_id), row.first_name, row.last_name, row.full_name, row.email, row.city, int(row.department_id))
    )
connection.commit()

# Payments
for _, row in payment_df.iterrows():
    cursor.execute(
        "INSERT INTO payments (payment_id, date, customer_id, employee_id, product_id, price) VALUES (%s, %s, %s, %s, %s, %s)",
        (int(row.payment_id), row.date, int(row.customer_id), int(row.employee_id), int(row.product_id), float(row.price))
    )
connection.commit()

cursor.close()
connection.close()
